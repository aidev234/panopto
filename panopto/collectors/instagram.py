"""Instagram collection via Apify actor."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import os
import re
from typing import Any, Iterable
from urllib.parse import quote

from panopto.collectors.apify import (
    ApifyActorInputError,
    ApifyConfigurationError,
    ApifyRequestError,
    run_actor_sync_get_items,
)
from panopto.errors import SourceUnavailableError

DEFAULT_APIFY_INSTAGRAM_ACTOR_ID = "apify/instagram-scraper"
APIFY_INSTAGRAM_ACTOR_ENV = "PANOPTO_APIFY_INSTAGRAM_ACTOR_ID"
APIFY_INSTAGRAM_RESULTS_LIMIT_MAX = 100


def normalize_instagram_username(raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""
    value = re.sub(r"^https?://(?:www\.)?instagram\.com/", "", value, flags=re.IGNORECASE)
    value = value.split("/", 1)[0]
    value = re.sub(r"^@+", "", value)
    return value.strip()


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
            return timedelta(**{unit: int(match.group(1))})
    raise ValueError(
        "Unsupported collection_window format. "
        "Use values like '1 week', '3 days', '12 hours', or '30 minutes'."
    )


def _get_actor_id() -> str:
    return str(os.environ.get(APIFY_INSTAGRAM_ACTOR_ENV) or DEFAULT_APIFY_INSTAGRAM_ACTOR_ID).strip()


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
        "%B %d, %Y",
    ):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


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
    compact = re.match(r"^([\d.]+)\s*([kKmM])$", text)
    if compact:
        value = float(compact.group(1))
        suffix = compact.group(2).lower()
        return int(value * (1_000 if suffix == "k" else 1_000_000))
    digits = re.sub(r"\D", "", text)
    return int(digits) if digits else None


def _first_non_empty(mapping: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(mapping.get(key) or "").strip()
        if value:
            return value
    return ""


def _first_http_url(mapping: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = str(mapping.get(key) or "").strip()
        if value.lower().startswith(("http://", "https://")):
            return value
    return ""


def _extract_text_field(raw: Any) -> str:
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, dict):
        for key in ("text", "caption", "value"):
            value = str(raw.get(key) or "").strip()
            if value:
                return value
    if isinstance(raw, list):
        parts = [_extract_text_field(item) for item in raw]
        joined = "\n".join(part for part in parts if part)
        return joined.strip()
    return str(raw or "").strip()


def _iter_post_records(dataset_items: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for item in dataset_items:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("latestPosts"), list):
            owner = item if isinstance(item, dict) else {}
            for post in item.get("latestPosts") or []:
                if isinstance(post, dict):
                    merged = dict(post)
                    merged.setdefault("ownerUsername", _first_non_empty(owner, "username", "userName", "ownerUsername"))
                    yield merged
            continue
        if isinstance(item.get("posts"), list):
            for post in item.get("posts") or []:
                if isinstance(post, dict):
                    yield post
            continue
        for list_key in ("items", "results", "datasetItems", "data"):
            nested = item.get(list_key)
            if not isinstance(nested, list):
                continue
            for post in nested:
                if isinstance(post, dict):
                    yield post
            break
        else:
            yield item


def _extract_actor_error_message(dataset_items: list[dict[str, Any]]) -> str:
    for item in dataset_items:
        if not isinstance(item, dict):
            continue
        error = str(item.get("error") or "").strip()
        description = str(item.get("errorDescription") or item.get("message") or "").strip()
        if error and description:
            return f"{error}: {description}"
        if error:
            return error
        if description:
            return description
        if item.get("noResults") is True:
            return "apify actor returned no results"
    return ""


def _looks_like_post_record(record: dict[str, Any]) -> bool:
    if not isinstance(record, dict):
        return False

    if _first_non_empty(record, "shortCode", "shortcode", "code"):
        return True

    url = _first_http_url(record, "url", "postUrl", "link", "permalink")
    if re.search(r"/(?:p|reel)/[A-Za-z0-9_-]+/?", url):
        return True

    if _extract_text_field(record.get("caption")):
        return True

    if (
        record.get("timestamp")
        or record.get("takenAtTimestamp")
        or record.get("taken_at_timestamp")
        or record.get("createdAt")
        or record.get("created_time")
        or record.get("time")
    ):
        return True

    if _first_http_url(record, "displayUrl", "imageUrl", "thumbnailSrc", "thumbnail_url", "videoUrl", "video_url"):
        return True

    if isinstance(record.get("images"), list) and len(record.get("images") or []) > 0:
        return True
    if isinstance(record.get("childPosts"), list) and len(record.get("childPosts") or []) > 0:
        return True

    return False


def _extract_shortcode(record: dict[str, Any]) -> str:
    direct = _first_non_empty(record, "shortCode", "shortcode", "code")
    if direct and re.match(r"^[A-Za-z0-9_-]{5,}$", direct):
        return direct
    url = _first_non_empty(record, "url", "postUrl", "link")
    match = re.search(r"/(?:p|reel)/([A-Za-z0-9_-]+)/?", url)
    return match.group(1) if match else ""


def _extract_source_url(record: dict[str, Any], username: str, shortcode: str) -> str:
    direct = _first_http_url(record, "url", "postUrl", "link", "permalink")
    if direct:
        return direct
    if shortcode:
        return f"https://www.instagram.com/p/{shortcode}/"
    return f"https://www.instagram.com/{quote(username, safe='')}/"


def _extract_media(record: dict[str, Any]) -> tuple[list[dict[str, str]], list[str], str, str]:
    image_urls: list[str] = []
    video_url = ""
    thumbnail_url = ""
    seen_images: set[str] = set()

    def _add_image(url: str) -> None:
        clean = str(url or "").strip()
        if not clean.lower().startswith(("http://", "https://")):
            return
        if clean in seen_images:
            return
        seen_images.add(clean)
        image_urls.append(clean)

    for key in ("displayUrl", "imageUrl", "thumbnailSrc", "thumbnail_url"):
        value = str(record.get(key) or "").strip()
        if value and value.lower().startswith(("http://", "https://")):
            _add_image(value)
            if not thumbnail_url:
                thumbnail_url = value
    if isinstance(record.get("images"), list):
        for image in record.get("images") or []:
            if isinstance(image, str):
                _add_image(image)
            elif isinstance(image, dict):
                _add_image(_first_http_url(image, "url", "displayUrl", "imageUrl"))

    if isinstance(record.get("childPosts"), list):
        for child in record.get("childPosts") or []:
            if not isinstance(child, dict):
                continue
            _add_image(_first_http_url(child, "displayUrl", "imageUrl", "thumbnailSrc"))
            if not video_url:
                child_video = _first_http_url(child, "videoUrl", "video_url")
                if child_video:
                    video_url = child_video

    candidate_video = _first_http_url(record, "videoUrl", "video_url")
    if candidate_video:
        video_url = candidate_video

    # Keep only the primary image to avoid noisy carousel expansion in post cards.
    if len(image_urls) > 1:
        image_urls = image_urls[:1]

    media: list[dict[str, str]] = []
    if video_url:
        entry: dict[str, str] = {"type": "video", "url": video_url}
        if thumbnail_url:
            entry["thumbnail_url"] = thumbnail_url
        media.append(entry)
    for image_url in image_urls:
        media.append({"type": "image", "url": image_url})

    return media, image_urls, video_url, thumbnail_url


def _extract_profile_image_url(record: dict[str, Any], normalized_username: str) -> str:
    direct = _first_http_url(
        record,
        "ownerProfilePicUrl",
        "ownerProfilePicURL",
        "owner_profile_pic_url",
        "profilePicUrl",
        "profile_pic_url",
    )
    if direct:
        return direct
    owner = record.get("owner")
    if isinstance(owner, dict):
        owner_direct = _first_http_url(
            owner,
            "profile_pic_url",
            "profilePicUrl",
            "profile_pic_url_hd",
            "avatar_url",
            "avatar",
            "image_url",
        )
        if owner_direct:
            return owner_direct
    user = record.get("user")
    if isinstance(user, dict):
        user_direct = _first_http_url(
            user,
            "profile_pic_url",
            "profilePicUrl",
            "profile_pic_url_hd",
            "avatar_url",
            "avatar",
            "image_url",
        )
        if user_direct:
            return user_direct
    return ""


def _extract_owner_username(record: dict[str, Any]) -> str:
    owner = record.get("owner")
    if isinstance(owner, dict):
        nested = _first_non_empty(owner, "username", "userName", "ownerUsername")
        if nested:
            return nested.strip().lstrip("@").lower()
    user = record.get("user")
    if isinstance(user, dict):
        nested = _first_non_empty(user, "username", "userName", "ownerUsername")
        if nested:
            return nested.strip().lstrip("@").lower()
    direct = _first_non_empty(record, "ownerUsername", "username", "userName")
    return direct.strip().lstrip("@").lower() if direct else ""


def _belongs_to_target_owner(record: dict[str, Any], normalized_username: str) -> bool:
    target = normalized_username.strip().lstrip("@").lower()
    if not target:
        return False
    owner_username = _extract_owner_username(record)
    if owner_username:
        return owner_username == target
    return True


def _build_actor_input_candidates(username: str, max_items: int) -> list[dict[str, Any]]:
    profile_url = f"https://www.instagram.com/{quote(username, safe='')}/"
    return [
        {
            "username": [username],
            "resultsLimit": max_items,
        },
        {
            "directUrls": [profile_url],
            "resultsType": "posts",
            "resultsLimit": max_items,
            "searchType": "user",
            "searchLimit": 1,
            "addParentData": False,
        },
    ]


def collect_instagram_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 4,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
    browser_fallback: bool = True,
) -> list[dict[str, Any]]:
    """Collect Instagram posts for a user via Apify actor output."""
    _ = request_delay_seconds
    _ = proxies
    _ = browser_fallback

    normalized_username = normalize_instagram_username(username)
    if not normalized_username:
        raise ValueError("username must be a non-empty string")

    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    actor_id = _get_actor_id()
    max_items = min(APIFY_INSTAGRAM_RESULTS_LIMIT_MAX, max(10, max_pages * 35))

    last_input_error: str = ""
    last_actor_error: str = ""
    dataset_items: list[dict[str, Any]] = []
    for actor_input in _build_actor_input_candidates(normalized_username, max_items):
        try:
            candidate_items = run_actor_sync_get_items(
                actor_id=actor_id,
                actor_input=actor_input,
                timeout_seconds=max(timeout, 180),
            )
            if candidate_items:
                post_like_items: list[dict[str, Any]] = []
                for record in _iter_post_records(candidate_items):
                    if _looks_like_post_record(record):
                        post_like_items.append(record)
                if post_like_items:
                    dataset_items = post_like_items
                    break
                actor_error = _extract_actor_error_message(candidate_items)
                if actor_error:
                    last_actor_error = actor_error
            # Try alternate input variants when a run is accepted but returns no items.
            continue
        except ApifyActorInputError as exc:
            last_input_error = str(exc)
            continue
        except ApifyConfigurationError as exc:
            raise SourceUnavailableError(
                platform="instagram",
                username=normalized_username,
                reason=str(exc),
            ) from exc
        except ApifyRequestError as exc:
            raise SourceUnavailableError(
                platform="instagram",
                username=normalized_username,
                reason=str(exc),
            ) from exc

    if not dataset_items and last_input_error:
        raise SourceUnavailableError(
            platform="instagram",
            username=normalized_username,
            reason=f"apify actor input rejected: {last_input_error[:160]}",
        )
    if not dataset_items and last_actor_error:
        raise SourceUnavailableError(
            platform="instagram",
            username=normalized_username,
            reason=last_actor_error[:200],
        )

    rows: list[dict[str, Any]] = []
    for record in _iter_post_records(dataset_items):
        if not isinstance(record, dict):
            continue
        if not _belongs_to_target_owner(record, normalized_username):
            continue

        row_username = _extract_owner_username(record) or normalized_username
        shortcode = _extract_shortcode(record)
        source_url = _extract_source_url(record, row_username, shortcode)
        timestamp_dt = _parse_datetime(
            record.get("timestamp")
            or record.get("takenAtTimestamp")
            or record.get("taken_at_timestamp")
            or record.get("createdAt")
            or record.get("created_time")
            or record.get("time")
        )
        if timestamp_dt and timestamp_dt < cutoff:
            continue

        media, image_urls, video_url, thumbnail_url = _extract_media(record)
        content = (
            _extract_text_field(record.get("caption"))
            or _extract_text_field(record.get("captionText"))
            or _extract_text_field(record.get("text"))
            or _extract_text_field(record.get("description"))
            or "(no text content)"
        )
        likes = _safe_int(record.get("likesCount") or record.get("likes"))
        comments = _safe_int(record.get("commentsCount") or record.get("comments") or record.get("commentCount"))
        profile_image_url = _extract_profile_image_url(record, normalized_username)

        rows.append(
            {
                "post_id": shortcode or None,
                "platform": "Instagram",
                "username": row_username,
                "content": content,
                "timestamp": timestamp_dt.isoformat() if timestamp_dt else None,
                "likes": likes,
                "retweets": None,
                "replies": comments,
                "source_url": source_url,
                "post_type": "post",
                "referenced_username": None,
                "metadata": {
                    "media": media,
                    "image_urls": image_urls,
                    "video_url": video_url,
                    "thumbnail_url": thumbnail_url,
                    "profile_image_url": profile_image_url,
                    "apify_actor_id": actor_id,
                },
            }
        )

    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row.get("post_id") or f"{row.get('timestamp') or ''}|{row.get('content') or ''}")
        existing = deduped.get(key)
        if existing is None or len(str(row.get("content") or "")) > len(str(existing.get("content") or "")):
            deduped[key] = row

    filtered = sorted(deduped.values(), key=lambda item: str(item.get("timestamp") or ""), reverse=True)
    return filtered
