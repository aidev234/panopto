"""Twitter collection helpers for local OSINT workflows.

This module collects posts from twitterwebviewer.com for a given username and
filters results to a configurable collection window.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from os import getenv
from typing import Any, Iterable
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

from panopto.collectors.apify import (
    ApifyActorInputError,
    ApifyConfigurationError,
    ApifyRequestError,
    run_actor_sync_get_items,
)
from panopto.errors import SourceUnavailableError


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

DEFAULT_APIFY_TWITTER_ACTOR_ID = "apidojo/tweet-scraper"
APIFY_TWITTER_ACTOR_ENV = "PANOPTO_APIFY_TWITTER_ACTOR_ID"
APIFY_TWITTER_MAX_SEARCH_TERMS = 8
APIFY_TWITTER_RESULTS_LIMIT_MAX = 100


@dataclass
class TwitterPost:
    """Represents a collected post from twitterwebviewer."""

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
    """Parse strings like '1 week', '2 days', '12h' into a timedelta."""

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
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass

    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
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


def _classify_post_type(
    stats_text: str,
    content: str,
    username: str,
    referenced_username: str | None,
    has_external_reference: bool,
) -> str:
    text = f"{stats_text} {content}".lower()
    if "replying to" in text:
        return "reply"
    if " reposted" in text or text.startswith("reposted") or " retweeted" in text:
        return "repost"
    if has_external_reference:
        return "quote"
    if referenced_username and referenced_username.lower().lstrip("@") != username.lower().lstrip("@"):
        return "quote"
    return "post"


def _normalize_media_url(raw_url: str | None, *, base_url: str = "https://twitterwebviewer.com") -> str:
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


def _extract_media_from_item(item: Any) -> dict[str, Any]:
    image_candidates: list[str] = []
    video_candidates: list[str] = []
    thumbnail = ""

    for video in item.select("video"):
        src = _normalize_media_url(video.get("src"))
        if src:
            video_candidates.append(src)
        poster = _normalize_media_url(video.get("poster"))
        if poster and not thumbnail:
            thumbnail = poster
        for source in video.select("source[src]"):
            source_url = _normalize_media_url(source.get("src"))
            if source_url:
                video_candidates.append(source_url)

    for img in item.select("img"):
        raw_image = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-image-url")
            or img.get("data-original")
            or ""
        )
        image_url = _normalize_media_url(raw_image)
        if image_url:
            image_candidates.append(image_url)
        srcset = img.get("srcset") or ""
        if srcset:
            for chunk in srcset.split(","):
                part = chunk.strip().split(" ")[0].strip()
                source_url = _normalize_media_url(part)
                if source_url:
                    image_candidates.append(source_url)

    for source in item.select("source[srcset]"):
        srcset = source.get("srcset") or ""
        for chunk in srcset.split(","):
            part = chunk.strip().split(" ")[0].strip()
            source_url = _normalize_media_url(part)
            if source_url:
                image_candidates.append(source_url)

    for link in item.select("a[href]"):
        href = _normalize_media_url(link.get("href"))
        if not href:
            continue
        if _is_video_url(href):
            video_candidates.append(href)
        elif _is_image_url(href):
            image_candidates.append(href)

    image_urls = [
        url for url in _dedupe_preserve_order(image_candidates) if _is_image_url(url) and not _is_non_post_image(url)
    ]
    video_urls = [url for url in _dedupe_preserve_order(video_candidates) if _is_video_url(url)]
    video_url = video_urls[0] if video_urls else ""
    if not thumbnail and image_urls:
        thumbnail = image_urls[0]

    media: list[dict[str, str]] = []
    if video_url:
        media_item = {"type": "video", "url": video_url}
        if thumbnail:
            media_item["thumbnail_url"] = thumbnail
        media.append(media_item)
    media.extend({"type": "image", "url": image_url} for image_url in image_urls)

    metadata: dict[str, Any] = {}
    if media:
        metadata["media"] = media
    if image_urls:
        metadata["image_urls"] = image_urls
    if video_url:
        metadata["video_url"] = video_url
    if thumbnail:
        metadata["thumbnail_url"] = thumbnail
    return metadata


def _extract_posts_from_html(username: str, html: str) -> list[TwitterPost]:
    soup = BeautifulSoup(html, "html.parser")
    posts: list[TwitterPost] = []

    candidates = soup.select("article, .tweet, .timeline-item, [data-testid='tweet']")
    if not candidates:
        candidates = [link.parent for link in soup.select("a[href*='/status/']") if link.parent]

    for item in candidates:
        content_node = item.select_one(
            ".tweet-text, .content, .post-content, [data-testid='tweetText']"
        )
        content = content_node.get_text(" ", strip=True) if content_node else ""

        timestamp_node = item.select_one("time") or item.find(attrs={"datetime": True})
        raw_time = None
        if timestamp_node:
            raw_time = timestamp_node.get("datetime") or timestamp_node.get_text(strip=True)
        timestamp = _parse_datetime(raw_time)

        stats_text = item.get_text(" ", strip=True)
        if not content:
            compact_text = stats_text
            if raw_time:
                compact_text = compact_text.replace(raw_time, " ")
            compact_text = re.sub(
                r"\b[\d,.]+(?:\s*[kKmM])?\s*(?:likes?|retweets?|reposts?|replies?|comments?)\b",
                " ",
                compact_text,
                flags=re.IGNORECASE,
            )
            compact_text = re.sub(r"\s+", " ", compact_text).strip()
            content = compact_text

        likes = _extract_metric(stats_text, ["like", "likes", "❤️"])
        retweets = _extract_metric(stats_text, ["retweet", "retweets", "repost", "reposts"])
        replies = _extract_metric(stats_text, ["reply", "replies", "comment", "comments"])

        status_links = item.select("a[href*='/status/']")
        status_link = status_links[0] if status_links else None
        post_id = item.get("data-tweet-id") or item.get("id")
        selected_href = ""
        selected_author = None
        link_authors: list[str] = []
        quote_href = ""
        quote_author = None

        for link in status_links:
            href = link.get("href") or ""
            author_match = re.search(
                r"(?:x|twitter)\.com/([^/]+)/status/\d+",
                href,
                flags=re.IGNORECASE,
            )
            if author_match:
                link_authors.append(author_match.group(1).lower().lstrip("@"))

        if not post_id and status_links:
            target_href = None
            fallback_href = None

            for link in status_links:
                href = link.get("href") or ""
                if "/status/" not in href:
                    continue
                if not fallback_href:
                    fallback_href = href
                user_match = re.search(
                    r"(?:x|twitter)\.com/([^/]+)/status/\d+",
                    href,
                    flags=re.IGNORECASE,
                )
                if user_match and user_match.group(1).lower().lstrip("@") == username.lower().lstrip("@"):
                    target_href = href
                    break

            selected_href = target_href or fallback_href or ""
            selected_author_match = re.search(
                r"(?:x|twitter)\.com/([^/]+)/status/\d+",
                selected_href,
                flags=re.IGNORECASE,
            )
            if selected_author_match:
                selected_author = selected_author_match.group(1).lower().lstrip("@")
            status_match = re.search(r"/status/(\d+)", selected_href)
            if status_match:
                post_id = status_match.group(1)
        elif status_link:
            selected_href = status_link.get("href") or ""
            selected_author_match = re.search(
                r"(?:x|twitter)\.com/([^/]+)/status/\d+",
                selected_href,
                flags=re.IGNORECASE,
            )
            if selected_author_match:
                selected_author = selected_author_match.group(1).lower().lstrip("@")

        for link in status_links:
            href = link.get("href") or ""
            author_match = re.search(
                r"(?:x|twitter)\.com/([^/]+)/status/\d+",
                href,
                flags=re.IGNORECASE,
            )
            if not author_match:
                continue
            candidate_author = author_match.group(1).lower().lstrip("@")
            if candidate_author == username.lower().lstrip("@"):
                continue
            quote_href = href
            quote_author = candidate_author
            break

        post_type = _classify_post_type(
            stats_text,
            content,
            username=username,
            referenced_username=selected_author,
            has_external_reference=any(
                author.lower().lstrip("@") != username.lower().lstrip("@") for author in link_authors
            ),
        )
        source_url = urljoin("https://x.com", selected_href) if selected_href else None
        if not source_url and post_id:
            source_url = f"https://x.com/{username}/status/{post_id}"

        if content and (post_id or status_link):
            media_metadata = _extract_media_from_item(item)
            quote_node = item.select_one(
                ".quote-text, .quoted-text, .quoted-tweet-text, blockquote, [data-testid='tweetText'] + div"
            )
            quote_text = ""
            if quote_node:
                quote_text = quote_node.get_text(" ", strip=True)
            posts.append(
                TwitterPost(
                    post_id=post_id,
                    username=username,
                    content=content,
                    timestamp=timestamp,
                    likes=likes,
                    retweets=retweets,
                    replies=replies,
                    source_url=source_url,
                    post_type=post_type,
                    referenced_username=selected_author,
                    raw_metadata={
                        "raw_timestamp": raw_time,
                        "quote_text": quote_text or None,
                        "quote_url": urljoin("https://x.com", quote_href) if quote_href else None,
                        "quote_username": quote_author,
                        **media_metadata,
                    },
                )
            )

    if not posts:
        posts = _extract_posts_from_embedded_data(username=username, html=html)

    return posts


def _extract_posts_from_embedded_data(username: str, html: str) -> list[TwitterPost]:
    """Fallback parser for JS-rendered pages with tweet payloads embedded in scripts."""

    posts: list[TwitterPost] = []

    normalized = re.sub(r'\\+"', '"', html).replace("\\/", "/")
    search_blobs = [html, normalized]

    text_pattern = re.compile(r'"(?:full_text|text)"\s*:\s*"((?:\\.|[^"\\])*)"')
    ts_pattern = re.compile(r'"(?:created_at|timestamp)"\s*:\s*"((?:\\.|[^"\\])*)"')
    id_pattern = re.compile(r'"(?:id_str|rest_id)"\s*:\s*"((?:\\.|[^"\\])*)"')

    text_matches: list[str] = []
    ts_matches: list[str] = []
    id_matches: list[str] = []
    for blob in search_blobs:
        text_matches = text_pattern.findall(blob)
        ts_matches = ts_pattern.findall(blob)
        id_matches = id_pattern.findall(blob)
        if text_matches:
            break

    for index, raw_text in enumerate(text_matches):
        cleaned_text = (
            raw_text.replace('\\"', '"')
            .replace("\\n", "\n")
            .replace("\\/", "/")
            .strip()
        )
        if not cleaned_text:
            continue

        raw_ts = ts_matches[index] if index < len(ts_matches) else None
        raw_id = id_matches[index] if index < len(id_matches) else None
        timestamp = _parse_datetime(raw_ts.replace('\\"', '"') if raw_ts else None)

        posts.append(
            TwitterPost(
                post_id=raw_id.replace('\\"', '"') if raw_id else None,
                username=username,
                content=cleaned_text,
                timestamp=timestamp,
                likes=None,
                retweets=None,
                replies=None,
                source_url=None,
                post_type="post",
                referenced_username=None,
                raw_metadata={"raw_timestamp": raw_ts},
            )
        )

    return posts


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

    quote_id = str(
        item.get("quoteId")
        or quoted.get("id")
        or quoted.get("tweetId")
        or ""
    ).strip() or None
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


def _source_hosts() -> list[str]:
    env_raw = str(getenv("TWITTER_SOURCE_HOSTS", "")).strip()
    if env_raw:
        hosts = [
            host.strip().lower().lstrip("https://").lstrip("http://").strip("/")
            for host in env_raw.split(",")
            if host.strip()
        ]
        if hosts:
            return hosts
    return ["twitterwebviewer.com", "xcancel.com", "nitter.net"]


def _candidate_page_urls(username: str, page: int, *, host: str) -> list[str]:
    safe_username = quote(username, safe="")
    safe_query_username = quote(f"@{username}", safe="")
    if "twitterwebviewer.com" in host:
        return [
            f"https://{host}/?user={safe_username}&page={page}",
            f"https://{host}/?q={safe_query_username}&page={page}",
            f"https://{host}/?q={safe_query_username}",
            f"https://{host}/{safe_username}",
            f"https://{host}/@{safe_username}",
        ]
    return [
        f"https://{host}/{safe_username}",
        f"https://{host}/{safe_username}/with_replies",
        f"https://{host}/search?f=tweets&q=from%3A{safe_username}",
    ]


def _page_signal_score(html: str, username: str) -> int:
    lower = html.lower()
    user_token = username.lower()

    score = 0
    signal_patterns = [
        r"data-tweet-id",
        r"/status/\d+",
        r'"full_text"',
        r'\\"full_text\\"',
        r'"created_at"',
        r'\\"created_at\\"',
        r'tweettext',
        r'data-testid=["\']tweet',
        r'"tweet_results"',
    ]

    for pattern in signal_patterns:
        if re.search(pattern, lower):
            score += 3

    if f"@{user_token}" in lower:
        score += 1
    if f"/{user_token}" in lower:
        score += 1

    if "twitter viewer - view twitter without account" in lower and score < 4:
        score -= 4

    return score


def _iter_pages(
    username: str,
    session: requests.Session,
    max_pages: int,
    delay_seconds: float,
    timeout: int,
    render_proxy_template: str | None = None,
    request_retries: int = 1,
    max_workers: int = 6,
) -> Iterable[str]:
    had_any_successful_response = False
    request_failures = 0
    attempted_urls: set[str] = set()
    low_signal_pages = 0

    for page in range(1, max_pages + 1):
        responses: list[str] = []
        candidate_urls: list[str] = []
        seen_urls: set[str] = set()
        for host in _source_hosts():
            for target_url in _candidate_page_urls(username=username, page=page, host=host):
                attempted_urls.add(target_url)
                if target_url in seen_urls:
                    continue
                seen_urls.add(target_url)
                candidate_urls.append(target_url)

        def _fetch_candidate(target_url: str) -> tuple[bool, bool, str]:
            request_url = target_url
            if render_proxy_template:
                request_url = render_proxy_template.format(url=quote(target_url, safe=""))

            base_get = getattr(session, "get", None)
            if not callable(base_get):
                return False, True, ""

            base_headers = getattr(session, "headers", None)
            base_proxies = getattr(session, "proxies", None)
            base_cookies = getattr(session, "cookies", None)

            # For non-requests Session objects (e.g. tests), use the provided getter directly.
            if base_headers is None and base_proxies is None and base_cookies is None:
                for attempt in range(request_retries + 1):
                    try:
                        response = base_get(request_url, timeout=timeout)
                    except requests.RequestException:
                        if attempt < request_retries:
                            continue
                        return False, True, ""

                    if response.status_code != 200:
                        return True, False, ""

                    html = response.text.strip()
                    if html:
                        return True, False, html
                    return True, False, ""
                return False, True, ""

            worker_session = requests.Session()
            if base_headers is not None:
                worker_session.headers.update(dict(base_headers))
            if base_proxies is not None:
                worker_session.proxies.update(dict(base_proxies))
            if base_cookies is not None:
                worker_session.cookies.update(base_cookies)
            try:
                for attempt in range(request_retries + 1):
                    try:
                        response = worker_session.get(request_url, timeout=timeout)
                    except requests.RequestException:
                        if attempt < request_retries:
                            continue
                        return False, True, ""

                    if response.status_code != 200:
                        return True, False, ""

                    html = response.text.strip()
                    if html:
                        return True, False, html
                    return True, False, ""
            finally:
                worker_session.close()

            return False, True, ""

        worker_count = max(1, min(max_workers, len(candidate_urls)))
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = [executor.submit(_fetch_candidate, target_url) for target_url in candidate_urls]
            for future in as_completed(futures):
                got_response, failed_request, html = future.result()
                if got_response:
                    had_any_successful_response = True
                if failed_request:
                    request_failures += 1
                if html:
                    responses.append(html)

        if not responses:
            if page == 1 and request_failures > 0 and not had_any_successful_response and attempted_urls:
                raise SourceUnavailableError(
                    platform="twitter",
                    username=username,
                    reason=f"all_source_requests_failed ({len(attempted_urls)} urls)",
                )
            break

        scored_responses = [(body, _page_signal_score(body, username)) for body in responses]
        best_html, best_score = max(scored_responses, key=lambda item: item[1])
        if best_score <= 0:
            low_signal_pages += 1
            if page > 1 and low_signal_pages >= 2:
                break
            continue
        low_signal_pages = 0

        yield best_html

        if delay_seconds > 0:
            time.sleep(delay_seconds)


def _extract_post_id_from_url(url: str | None) -> str | None:
    value = str(url or "").strip()
    if not value:
        return None
    match = re.search(r"/status/(\d+)", value)
    return match.group(1) if match else None


def _iter_rss_posts(
    username: str,
    session: requests.Session,
    *,
    timeout: int,
) -> list[TwitterPost]:
    """Fallback parser for Nitter/Xcancel RSS feeds."""
    posts: list[TwitterPost] = []
    seen_links: set[str] = set()
    for host in _source_hosts():
        if "twitterwebviewer.com" in host:
            continue
        rss_urls = [
            f"https://{host}/{quote(username, safe='')}/rss",
            f"https://{host}/rss/{quote(username, safe='')}",
        ]
        for rss_url in rss_urls:
            try:
                response = session.get(rss_url, timeout=timeout)
            except requests.RequestException:
                continue
            if response.status_code != 200:
                continue
            body = str(response.text or "").strip()
            if not body or "<rss" not in body.lower():
                continue
            soup = BeautifulSoup(body, "xml")
            items = soup.find_all("item")
            if not items:
                continue
            for item in items:
                link_text = str((item.find("link").text if item.find("link") else "") or "").strip()
                if not link_text or link_text in seen_links:
                    continue
                seen_links.add(link_text)
                title_text = str((item.find("title").text if item.find("title") else "") or "").strip()
                content_text = ""
                if item.find("description"):
                    content_text = str(item.find("description").text or "").strip()
                if not content_text and title_text:
                    # Nitter titles are commonly "username: tweet text".
                    content_text = re.sub(r"^[^:]{1,80}:\s*", "", title_text).strip()
                if not content_text:
                    continue
                raw_time = str((item.find("pubDate").text if item.find("pubDate") else "") or "").strip()
                timestamp = _parse_datetime(raw_time)
                post_id = _extract_post_id_from_url(link_text)
                posts.append(
                    TwitterPost(
                        post_id=post_id,
                        username=username,
                        content=BeautifulSoup(content_text, "html.parser").get_text(" ", strip=True),
                        timestamp=timestamp,
                        likes=None,
                        retweets=None,
                        replies=None,
                        source_url=link_text,
                        post_type="post",
                        referenced_username=None,
                        raw_metadata={"raw_timestamp": raw_time},
                    )
                )
    return posts


def _page_indicates_missing_user(html: str) -> bool:
    lowered = html.lower()
    patterns = [
        "user not found",
        "username not found",
        "this account doesn",
        "this account does not exist",
        "account does not exist",
        "no tweets found",
        "cannot find user",
    ]
    return any(pattern in lowered for pattern in patterns)


def _extract_profile_image_from_html(html: str) -> str:
    def _is_profile_image_url(url: str) -> bool:
        lowered = str(url or "").lower()
        if not lowered:
            return False
        include_tokens = (
            "/profile_images/",
            "profile_images",
            "avatar",
            "profile_image",
            "pfp",
        )
        exclude_tokens = (
            "/profile_banners/",
            "/media/",
            "ext_tw_video_thumb",
            "hashflags",
            "twemoji",
            "sticky/default_profile_images",
            "abs.twimg.com",
            "/emoji/",
        )
        if any(token in lowered for token in exclude_tokens):
            return False
        return any(token in lowered for token in include_tokens)

    # Prefer explicit profile-image JSON fields when available.
    json_patterns = [
        r'"profile_image_url_https"\s*:\s*"([^"]+)"',
        r'"profile_image_url"\s*:\s*"([^"]+)"',
    ]
    for pattern in json_patterns:
        for match in re.findall(pattern, html or ""):
            raw_url = str(match).replace("\\/", "/")
            url = _normalize_media_url(raw_url)
            if url and _is_profile_image_url(url):
                return url

    soup = BeautifulSoup(html, "html.parser")
    selectors = [
        "img[src*='/profile_images/']",
        "img[data-src*='/profile_images/']",
        "img[src*='profile_image']",
        "img[data-src*='profile_image']",
        "img[src*='avatar']",
        "img[data-src*='avatar']",
    ]
    for selector in selectors:
        for node in soup.select(selector):
            raw = node.get("src") or node.get("data-src")
            url = _normalize_media_url(raw)
            if url and _is_profile_image_url(url):
                return url
    return ""


def _iter_rendered_pages(
    username: str,
    max_pages: int,
    timeout: int,
    *,
    browser_proxy: str | None,
) -> Iterable[str]:
    """Optional browser-rendered fallback for JS-heavy pages."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return []

    with sync_playwright() as playwright:
        launch_options: dict[str, Any] = {"headless": True}
        if browser_proxy:
            launch_options["proxy"] = {"server": browser_proxy}

        browser = playwright.chromium.launch(**launch_options)
        page = browser.new_page()

        try:
            page.goto(
                f"https://twitterwebviewer.com/?q={quote(f'@{username}', safe='')}",
                wait_until="networkidle",
                timeout=timeout * 1000,
            )

            search_box = page.query_selector(
                "input#home-search-input, input[name='q'], input[type='search']"
            )
            if search_box:
                search_box.fill(f"@{username}")
                search_box.press("Enter")
                page.wait_for_timeout(1500)

            def _click_load_more() -> bool:
                selectors = [
                    "button:has-text('Load more tweets')",
                    "a:has-text('Load more tweets')",
                    "button:has-text('Load more')",
                    "a:has-text('Load more')",
                ]
                for selector in selectors:
                    locator = page.locator(selector)
                    if locator.count() == 0:
                        continue
                    try:
                        locator.first.scroll_into_view_if_needed(timeout=1500)
                    except Exception:
                        pass
                    try:
                        locator.first.click(timeout=2500)
                        return True
                    except Exception:
                        continue
                return False

            pages: list[str] = []
            previous_size = 0
            stagnant_rounds = 0
            for _ in range(max_pages):
                html = page.content()
                pages.append(html)
                current_size = len(html)
                if current_size <= previous_size:
                    stagnant_rounds += 1
                else:
                    stagnant_rounds = 0
                previous_size = current_size

                clicked = _click_load_more()
                if clicked:
                    try:
                        page.wait_for_load_state("networkidle", timeout=max(1500, timeout * 300))
                    except Exception:
                        pass
                    page.wait_for_timeout(1000)
                    continue

                page.mouse.wheel(0, 2600)
                page.wait_for_timeout(1200)
                if stagnant_rounds >= 2:
                    break

            return pages
        finally:
            browser.close()


def collect_twitter_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 3,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
    render_proxy_template: str | None = None,
    browser_proxy: str | None = None,
    browser_fallback: bool = True,
    browser_enrich_existing: bool = False,
) -> list[dict[str, Any]]:
    """Collect posts from Apify actor output for a user.

    Args:
        username: Twitter username (without @).
        collection_window: Relative window e.g. "1 week", "3 days".
        max_pages: Maximum pages to request for pagination.
        request_delay_seconds: Delay between requests to reduce blocking risk.
        timeout: Per-request timeout in seconds.
        proxies: Optional requests proxies mapping.
        render_proxy_template: Optional URL template for JS-rendering proxy providers.
            Use `{url}` placeholder for the encoded target URL.
        browser_proxy: Optional proxy URL for browser-rendered fallback.
        browser_fallback: Whether to use browser-rendered fallback when requests
            pages do not contain extractable posts.
        browser_enrich_existing: Whether to run browser-rendered pagination even
            when request-based pages already produced posts. Useful when
            additional history requires clicking "Load more tweets".

    Returns:
        List of post dictionaries with content, timestamp, and engagement metadata.
    """

    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = username.strip().lstrip("@").lower()
    window = _parse_collection_window(collection_window)
    now = datetime.now(timezone.utc)
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
                    "profile_image_url": str((post.raw_metadata or {}).get("profile_image_url") or profile_image_url or "").strip() or None,
                },
            }
        )

    filtered.sort(key=lambda p: p["timestamp"] or "", reverse=True)
    return filtered
