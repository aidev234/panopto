"""Twitter collection helpers backed by Apify actor output."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from typing import Any, Iterable
from urllib.parse import quote, urljoin

from panopto.collectors.apify import (
    ApifyActorInputError,
    ApifyConfigurationError,
    ApifyRequestError,
    run_actor_sync_get_items,
)
from panopto.errors import SourceUnavailableError


DEFAULT_APIFY_TWITTER_ACTOR_ID = "apidojo/tweet-scraper"
APIFY_TWITTER_ACTOR_ENV = "PANOPTO_APIFY_TWITTER_ACTOR_ID"
APIFY_TWITTER_MAX_SEARCH_TERMS = 8
APIFY_TWITTER_RESULTS_LIMIT_MAX = 100


@dataclass
class TwitterPost:
    """Normalized Twitter post data."""

    post_id: str | None
    username: str
    content: str
    timestamp: datetime | None
    likes: int | None
    retweets: int | None
    replies: int | None
    source_url: str | None
    post_type: str
    referenced_username: str | None
    raw_metadata: dict[str, Any]


def _parse_collection_window(collection_window: str) -> timedelta:
    value = collection_window.strip().lower()
    patterns: list[tuple[str, str]] = [
        (r"^(\d+)\s*(w|week|weeks)$", "weeks"),
        (r"^(\d+)\s*(d|day|days)$", "days"),
        (r"^(\d+)\s*(h|hour|hours)$", "hours"),
        (r"^(\d+)\s*(m|min|minute|minutes)$", "minutes"),
    ]

    for pattern, unit in patterns:
        match = re.match(pattern, value)
        if match:
            amount = int(match.group(1))
            return timedelta(**{unit: amount})

    raise ValueError(
        "Unsupported collection_window format. "
        "Use values like '1 week', '3 days', '12 hours', or '30 minutes'."
    )


def _parse_datetime(raw_value: Any) -> datetime | None:
    if raw_value is None:
        return None

    if isinstance(raw_value, (int, float)):
        stamp = float(raw_value)
        if stamp > 10_000_000_000:
            stamp /= 1000.0
        try:
            return datetime.fromtimestamp(stamp, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None

    text = str(raw_value).strip()
    if not text:
        return None
    if text.isdigit():
        return _parse_datetime(int(text))

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%b %d, %Y %I:%M %p",
        "%b %d, %Y",
    ):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass

    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _extract_count(text: str) -> int | None:
    normalized = text.strip().lower()
    compact_match = re.search(r"([\d,.]+)\s*([km])\b", normalized)
    if compact_match:
        numeric_text = compact_match.group(1).replace(",", "").strip()
        if not re.search(r"\d", numeric_text):
            return None
        value = float(numeric_text)
        suffix = compact_match.group(2)
        multiplier = 1_000 if suffix == "k" else 1_000_000
        return int(value * multiplier)

    match = re.search(r"([\d,.]+)", normalized)
    if not match:
        return None
    digits_only = re.sub(r"\D", "", match.group(1))
    if not digits_only:
        return None
    return int(digits_only)


def _extract_metric(stats_text: str, labels: list[str]) -> int | None:
    label_group = "|".join(re.escape(label) for label in labels)
    patterns = [
        rf"(?:{label_group})\s*[:\-]\s*([\d,.]+(?:\s*[kKmM])?)",
        rf"([\d,.]+(?:\s*[kKmM])?)\s*(?:{label_group})",
    ]

    for pattern in patterns:
        match = re.search(pattern, stats_text, flags=re.IGNORECASE)
        if match:
            return _extract_count(match.group(1))

    return None


def _normalize_media_url(raw_url: str | None, *, base_url: str = "https://x.com") -> str:
    if not raw_url:
        return ""
    value = unescape(str(raw_url)).strip()
    if not value:
        return ""
    value = value.split(",", 1)[0].strip()
    if value.startswith("//"):
        value = f"https:{value}"
    elif value.startswith("/"):
        value = urljoin(base_url, value)
    if not re.match(r"^https?://", value, flags=re.IGNORECASE):
        return ""
    return value


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        output.append(normalized)
    return output


def _is_image_url(url: str) -> bool:
    lowered = url.lower()
    return (
        bool(re.search(r"\.(?:jpe?g|png|webp|gif)(?:\?|$)", lowered))
        or "pbs.twimg.com/media/" in lowered
        or "pbs.twimg.com/ext_tw_video_thumb/" in lowered
        or "preview.redd.it/" in lowered
    )


def _is_video_url(url: str) -> bool:
    lowered = url.lower()
    return bool(re.search(r"\.(?:mp4|m3u8)(?:\?|$)", lowered)) or "video.twimg.com/" in lowered


def _is_non_post_image(url: str) -> bool:
    lowered = url.lower()
    blocked_tokens = [
        "/profile_images/",
        "/profile_banners/",
        "emoji",
        "twemoji",
        "abs.twimg.com/sticky",
        "abs.twimg.com/hashflags",
        "/avatars/",
    ]
    return any(token in lowered for token in blocked_tokens)


def _get_actor_id() -> str:
    return str(os.environ.get(APIFY_TWITTER_ACTOR_ENV) or DEFAULT_APIFY_TWITTER_ACTOR_ID).strip()


def _build_apify_search_terms(
    *,
    username: str,
    cutoff: datetime,
    now_utc: datetime,
) -> list[str]:
    normalized_username = str(username or "").strip().lstrip("@").lower()
    if not normalized_username:
        return []

    ranges: list[str] = []
    start = cutoff.date()
    end = now_utc.date()
    cursor = start

    while cursor < end and len(ranges) < APIFY_TWITTER_MAX_SEARCH_TERMS:
        until = min(end, cursor + timedelta(days=180))
        ranges.append(f"from:{normalized_username} since:{cursor.isoformat()} until:{until.isoformat()}")
        cursor = until

    if not ranges:
        return [f"from:{normalized_username}"]
    return [f"from:{normalized_username}", *ranges]


def _safe_int(raw: Any) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        return int(raw)
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    text = str(raw).strip()
    if not text:
        return None
    compact = re.match(r"^([\d.]+)\s*([kKmMbB])$", text)
    if compact:
        value = float(compact.group(1))
        suffix = compact.group(2).lower()
        multiplier = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[suffix]
        return int(value * multiplier)
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def _safe_dict(raw: Any) -> dict[str, Any]:
    return raw if isinstance(raw, dict) else {}


def _safe_list(raw: Any) -> list[Any]:
    return raw if isinstance(raw, list) else []


def _extract_username(raw: Any) -> str:
    if not isinstance(raw, dict):
        return ""
    return str(
        raw.get("userName")
        or raw.get("username")
        or raw.get("screen_name")
        or raw.get("handle")
        or raw.get("name")
        or ""
    ).strip().lstrip("@").lower()


def _extract_twitter_media_metadata(item: dict[str, Any]) -> dict[str, Any]:
    image_urls: list[str] = []
    video_urls: list[str] = []
    thumbnail_url = ""

    def _add_image(raw_url: Any) -> None:
        normalized = _normalize_media_url(str(raw_url or "").strip())
        if normalized and _is_image_url(normalized) and not _is_non_post_image(normalized):
            image_urls.append(normalized)

    def _add_video(raw_url: Any) -> None:
        normalized = _normalize_media_url(str(raw_url or "").strip())
        if normalized and _is_video_url(normalized):
            video_urls.append(normalized)

    for key in ("photos", "images", "imageUrls", "image_urls"):
        for entry in _safe_list(item.get(key)):
            if isinstance(entry, str):
                _add_image(entry)
            elif isinstance(entry, dict):
                _add_image(
                    entry.get("url")
                    or entry.get("media_url")
                    or entry.get("media_url_https")
                    or entry.get("expanded_url")
                )

    for key in ("videos", "videoUrls", "video_urls"):
        for entry in _safe_list(item.get(key)):
            if isinstance(entry, str):
                _add_video(entry)
            elif isinstance(entry, dict):
                _add_video(entry.get("url") or entry.get("videoUrl") or entry.get("playbackUrl"))
                thumb = _normalize_media_url(
                    entry.get("thumbnailUrl")
                    or entry.get("thumbnail")
                    or entry.get("poster")
                )
                if thumb and not thumbnail_url:
                    thumbnail_url = thumb

    entities = _safe_dict(item.get("entities"))
    extended = _safe_dict(item.get("extendedEntities") or item.get("extended_entities"))
    for container in (entities, extended):
        for media_item in _safe_list(container.get("media")):
            media_obj = _safe_dict(media_item)
            _add_image(media_obj.get("media_url_https") or media_obj.get("media_url"))
            _add_image(media_obj.get("url") or media_obj.get("expanded_url"))
            _add_video(media_obj.get("video_url"))
            _add_video(media_obj.get("videoUrl"))
            if not thumbnail_url:
                thumb = _normalize_media_url(media_obj.get("media_url_https") or media_obj.get("media_url"))
                if thumb and _is_image_url(thumb):
                    thumbnail_url = thumb
            video_info = _safe_dict(media_obj.get("video_info"))
            for variant in _safe_list(video_info.get("variants")):
                _add_video(_safe_dict(variant).get("url"))

    _add_video(item.get("videoUrl") or item.get("video_url") or item.get("playUrl"))
    candidate_thumb = _normalize_media_url(
        item.get("thumbnail")
        or item.get("thumbnailUrl")
        or item.get("thumbnail_url")
        or item.get("previewImageUrl")
    )
    if candidate_thumb and not thumbnail_url:
        thumbnail_url = candidate_thumb

    image_urls = _dedupe_preserve_order(image_urls)
    video_urls = _dedupe_preserve_order(video_urls)
    video_url = video_urls[0] if video_urls else ""
    if not thumbnail_url and image_urls:
        thumbnail_url = image_urls[0]

    media: list[dict[str, str]] = []
    if video_url:
        video_item: dict[str, str] = {"type": "video", "url": video_url}
        if thumbnail_url:
            video_item["thumbnail_url"] = thumbnail_url
        media.append(video_item)
    media.extend({"type": "image", "url": image_url} for image_url in image_urls)

    metadata: dict[str, Any] = {}
    if media:
        metadata["media"] = media
    if image_urls:
        metadata["image_urls"] = image_urls
    if video_url:
        metadata["video_url"] = video_url
    if thumbnail_url:
        metadata["thumbnail_url"] = thumbnail_url
    return metadata


def _iter_apify_tweet_records(dataset_items: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    nested_keys = ("tweets", "posts", "results", "items", "data")
    for item in dataset_items:
        if not isinstance(item, dict):
            continue
        if item.get("noResults") is True:
            continue
        if str(item.get("error") or "").strip():
            continue

        yielded_nested = False
        for key in nested_keys:
            nested = item.get(key)
            if not isinstance(nested, list):
                continue
            for candidate in nested:
                if isinstance(candidate, dict):
                    yield candidate
            yielded_nested = True
        if not yielded_nested:
            yield item


def _apify_item_to_post(item: dict[str, Any], *, fallback_username: str) -> TwitterPost | None:
    item_type = str(item.get("type") or "").strip().lower()
    if item_type and item_type not in {"tweet", "post", "status"}:
        return None

    post_id = str(item.get("id") or item.get("tweetId") or "").strip() or None
    source_url = str(item.get("url") or item.get("twitterUrl") or item.get("tweetUrl") or "").strip() or None
    text = str(item.get("text") or item.get("fullText") or "").strip()
    if not text and not post_id and not source_url:
        return None

    author = _safe_dict(item.get("author"))
    username = str(
        author.get("userName")
        or author.get("username")
        or item.get("userName")
        or item.get("username")
        or fallback_username
    ).strip().lstrip("@").lower()
    if not username:
        username = fallback_username

    created_raw = item.get("createdAt") or item.get("created_at") or item.get("timestamp") or item.get("time")
    timestamp = _parse_datetime(created_raw)
    likes = _safe_int(item.get("likeCount"))
    retweets = _safe_int(item.get("retweetCount"))
    replies = _safe_int(item.get("replyCount"))

    quoted = _safe_dict(
        item.get("quotedTweet")
        or item.get("quotedStatus")
        or item.get("quoted_status")
        or item.get("quotedPost")
        or item.get("quoted")
        or item.get("quote")
    )
    quote_author = _safe_dict(quoted.get("author"))
    quote_username = _extract_username(quote_author) or _extract_username(quoted.get("user"))

    is_retweet = bool(item.get("isRetweet"))
    is_reply = bool(item.get("isReply"))
    is_quote = bool(item.get("isQuote") or quoted)
    post_type = "post"
    if is_retweet:
        post_type = "repost"
    elif is_reply:
        post_type = "reply"
    elif is_quote:
        post_type = "quote"

    profile_image_url = str(author.get("profilePicture") or author.get("profileImageUrl") or "").strip() or None
    media_metadata = _extract_twitter_media_metadata(item)

    quote_id = str(item.get("quoteId") or quoted.get("id") or quoted.get("tweetId") or "").strip() or None
    quote_text = str(quoted.get("text") or quoted.get("fullText") or item.get("quotedText") or "").strip() or None
    quote_url = str(
        item.get("quoteUrl")
        or quoted.get("url")
        or quoted.get("twitterUrl")
        or quoted.get("tweetUrl")
        or ""
    ).strip() or None
    if not quote_url and quote_id and quote_username:
        quote_url = f"https://x.com/{quote_username}/status/{quote_id}"

    referenced_username = None
    if is_reply:
        referenced_username = str(
            item.get("inReplyToUser")
            or item.get("inReplyToUsername")
            or item.get("inReplyToScreenName")
            or ""
        ).strip().lstrip("@").lower() or None
    elif is_quote:
        referenced_username = quote_username or None

    if not source_url and post_id:
        source_url = f"https://x.com/{username}/status/{post_id}"

    return TwitterPost(
        post_id=post_id,
        username=username,
        content=text or "(tweet)",
        timestamp=timestamp,
        likes=likes,
        retweets=retweets,
        replies=replies,
        source_url=source_url,
        post_type=post_type,
        referenced_username=referenced_username,
        raw_metadata={
            "raw_timestamp": str(created_raw or "").strip() or None,
            "profile_image_url": profile_image_url,
            "quote_id": quote_id,
            "quote_text": quote_text,
            "quote_url": quote_url,
            "quote_username": quote_username or None,
            "quote_count": _safe_int(item.get("quoteCount")),
            "bookmark_count": _safe_int(item.get("bookmarkCount")),
            "lang": str(item.get("lang") or "").strip() or None,
            "author": author,
            "source": str(item.get("source:") or item.get("source") or "").strip() or None,
            **media_metadata,
            "raw": item,
        },
    )


def _collect_from_apify(
    *,
    normalized_username: str,
    cutoff: datetime,
    now_utc: datetime,
    timeout: int,
    max_pages: int,
) -> list[TwitterPost]:
    actor_id = _get_actor_id()
    search_terms = _build_apify_search_terms(
        username=normalized_username,
        cutoff=cutoff,
        now_utc=now_utc,
    )
    if not search_terms:
        return []

    max_items = min(APIFY_TWITTER_RESULTS_LIMIT_MAX, max(20, max_pages * 35))
    actor_input_candidates = [
        {"searchTerms": [f"from:{normalized_username}"], "sort": "Latest", "maxItems": max_items},
        {"searchTerms": search_terms, "sort": "Latest", "maxItems": max_items},
        {"searchTerms": [f"from:{normalized_username}"], "sort": "Latest"},
        {"searchTerms": search_terms, "sort": "Latest"},
    ]

    dataset_items: list[dict[str, Any]] = []
    last_input_error = ""
    for actor_input in actor_input_candidates:
        try:
            dataset_items = run_actor_sync_get_items(
                actor_id=actor_id,
                actor_input=actor_input,
                timeout_seconds=max(timeout, 60),
            )
            if dataset_items:
                break
        except ApifyActorInputError as exc:
            last_input_error = str(exc)
            continue

    if not dataset_items and last_input_error:
        raise ApifyActorInputError(last_input_error)

    posts: list[TwitterPost] = []
    for item in _iter_apify_tweet_records(dataset_items):
        normalized = _apify_item_to_post(item, fallback_username=normalized_username)
        if normalized is None:
            continue
        if normalized.timestamp and normalized.timestamp < cutoff:
            continue
        posts.append(normalized)
    return posts


def collect_twitter_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 3,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
    now_utc: datetime | None = None,
) -> list[dict[str, Any]]:
    """Collect posts from Apify actor output for a user."""

    _ = request_delay_seconds
    _ = proxies

    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = username.strip().lstrip("@").lower()
    window = _parse_collection_window(collection_window)
    if now_utc is None:
        now = datetime.now(timezone.utc)
    elif now_utc.tzinfo is None:
        now = now_utc.replace(tzinfo=timezone.utc)
    else:
        now = now_utc.astimezone(timezone.utc)
    cutoff = now - window

    try:
        collected = _collect_from_apify(
            normalized_username=normalized_username,
            cutoff=cutoff,
            now_utc=now,
            timeout=timeout,
            max_pages=max_pages,
        )
    except ApifyConfigurationError as exc:
        raise SourceUnavailableError(
            platform="twitter",
            username=normalized_username,
            reason=str(exc),
        ) from exc
    except (ApifyActorInputError, ApifyRequestError) as exc:
        raise SourceUnavailableError(
            platform="twitter",
            username=normalized_username,
            reason=str(exc),
        ) from exc

    profile_image_url = ""
    for post in collected:
        if not profile_image_url:
            profile_image_url = str((post.raw_metadata or {}).get("profile_image_url") or "").strip()

    filtered: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str, str | None]] = set()
    best_by_post_id: dict[str, TwitterPost] = {}
    posts_without_id: list[TwitterPost] = []

    for post in collected:
        if post.post_id:
            existing = best_by_post_id.get(post.post_id)
            if existing is None or len(post.content) > len(existing.content):
                best_by_post_id[post.post_id] = post
        else:
            posts_without_id.append(post)

    normalized_posts = list(best_by_post_id.values()) + posts_without_id

    for post in normalized_posts:
        if post.post_type == "repost":
            continue

        iso_ts = post.timestamp.isoformat() if post.timestamp else None
        dedupe_key = ("id" if post.post_id else "body", post.post_id or post.content, iso_ts)
        if dedupe_key in seen_keys:
            continue
        seen_keys.add(dedupe_key)

        if post.timestamp and post.timestamp < cutoff:
            continue

        filtered.append(
            {
                "post_id": post.post_id,
                "username": post.username,
                "content": post.content,
                "timestamp": iso_ts,
                "likes": post.likes,
                "retweets": post.retweets,
                "replies": post.replies,
                "source_url": post.source_url,
                "post_type": post.post_type,
                "referenced_username": post.referenced_username,
                "metadata": {
                    **(post.raw_metadata or {}),
                    "profile_image_url": str(
                        (post.raw_metadata or {}).get("profile_image_url") or profile_image_url or ""
                    ).strip()
                    or None,
                },
            }
        )

    filtered.sort(key=lambda post: post["timestamp"] or "", reverse=True)
    return filtered
