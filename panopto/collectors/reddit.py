"""Reddit collection helpers for local OSINT workflows."""

from __future__ import annotations

import random
import re
import time
from datetime import datetime, timedelta, timezone
from html import unescape
from typing import Any
from urllib.parse import quote

import requests

from panopto.errors import UsernameNotFoundError

DEFAULT_HEADERS = {
    "User-Agent": "panopto-osint-collector/1.0 (+local; respectful-rate-limit)",
    "Accept": "application/json",
}


def _parse_collection_window(collection_window: str) -> timedelta:
    value = collection_window.strip().lower()
    units = {
        "week": 7,
        "weeks": 7,
        "w": 7,
        "day": 1,
        "days": 1,
        "d": 1,
        "hour": 1 / 24,
        "hours": 1 / 24,
        "h": 1 / 24,
    }
    amount = int(value.split()[0]) if value and value.split()[0].isdigit() else None
    unit = value.split()[1] if len(value.split()) > 1 else value[-1:] if amount is not None else ""
    if amount is None or unit not in units:
        raise ValueError("Unsupported collection_window format. Use e.g. '1 week' or '7 days'.")
    return timedelta(days=amount * units[unit])


def _retrying_get(
    session: requests.Session,
    url: str,
    params: dict[str, Any],
    timeout: int,
    *,
    username: str,
) -> requests.Response:
    backoff = 1.0
    for attempt in range(4):
        response = session.get(url, params=params, timeout=timeout)
        if response.status_code < 400:
            return response
        if response.status_code == 404:
            raise UsernameNotFoundError(platform="reddit", username=username)
        if response.status_code not in {429, 500, 502, 503, 504}:
            response.raise_for_status()
        if attempt < 3:
            time.sleep(backoff + random.uniform(0.0, 0.5))
            backoff *= 2
    response.raise_for_status()
    return response


def _iter_listing(
    session: requests.Session,
    username: str,
    listing: str,
    max_pages: int,
    request_delay_seconds: float,
    timeout: int,
) -> list[dict[str, Any]]:
    endpoint = f"https://www.reddit.com/user/{quote(username, safe='')}/{listing}/.json"
    after = None
    items: list[dict[str, Any]] = []

    for _ in range(max_pages):
        params: dict[str, Any] = {"limit": 100, "raw_json": 1}
        if after:
            params["after"] = after

        response = _retrying_get(
            session,
            endpoint,
            params=params,
            timeout=timeout,
            username=username,
        )
        payload = response.json()
        children = payload.get("data", {}).get("children", [])
        if not children:
            break

        items.extend(children)
        after = payload.get("data", {}).get("after")
        if not after:
            break

        if request_delay_seconds > 0:
            time.sleep(request_delay_seconds + random.uniform(0.0, 0.35))

    return items


def _normalize_media_url(raw_url: Any) -> str:
    if raw_url is None:
        return ""
    value = unescape(str(raw_url)).strip()
    if not value:
        return ""
    if value.startswith("//"):
        value = f"https:{value}"
    if not value.lower().startswith(("http://", "https://")):
        return ""
    return value


def _is_image_url(url: str) -> bool:
    return bool(url) and any(token in url.lower() for token in [".jpg", ".jpeg", ".png", ".webp", ".gif", "preview.redd.it/"])


def _is_video_url(url: str) -> bool:
    return bool(url) and any(token in url.lower() for token in [".mp4", ".m3u8", "v.redd.it/"])


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        output.append(normalized)
    return output


def _extract_reddit_media(data: dict[str, Any], *, is_comment: bool) -> dict[str, Any]:
    if is_comment:
        return {}

    image_candidates: list[str] = []
    video_candidates: list[str] = []
    thumbnail = ""

    preview = data.get("preview")
    if isinstance(preview, dict):
        images = preview.get("images") or []
        if isinstance(images, list):
            for image in images:
                if not isinstance(image, dict):
                    continue
                source = image.get("source")
                if isinstance(source, dict):
                    source_url = _normalize_media_url(source.get("url"))
                    if source_url:
                        image_candidates.append(source_url)
                        if not thumbnail:
                            thumbnail = source_url
                resolutions = image.get("resolutions") or []
                if isinstance(resolutions, list):
                    for resolution in resolutions:
                        if not isinstance(resolution, dict):
                            continue
                        resolution_url = _normalize_media_url(resolution.get("url"))
                        if resolution_url:
                            image_candidates.append(resolution_url)

    media_metadata = data.get("media_metadata")
    if isinstance(media_metadata, dict):
        for media_entry in media_metadata.values():
            if not isinstance(media_entry, dict):
                continue
            source = media_entry.get("s")
            if not isinstance(source, dict):
                continue
            gallery_url = _normalize_media_url(source.get("u") or source.get("gif") or source.get("mp4"))
            if gallery_url:
                if _is_video_url(gallery_url):
                    video_candidates.append(gallery_url)
                else:
                    image_candidates.append(gallery_url)

    candidate_image = _normalize_media_url(data.get("url_overridden_by_dest") or data.get("url"))
    if candidate_image and _is_image_url(candidate_image):
        image_candidates.append(candidate_image)

    secure_media = data.get("secure_media") if isinstance(data.get("secure_media"), dict) else {}
    media = data.get("media") if isinstance(data.get("media"), dict) else {}
    reddit_video = secure_media.get("reddit_video") if isinstance(secure_media.get("reddit_video"), dict) else {}
    if not reddit_video and isinstance(media.get("reddit_video"), dict):
        reddit_video = media.get("reddit_video")

    if isinstance(reddit_video, dict):
        for key in ("fallback_url", "dash_url", "hls_url", "scrubber_media_url"):
            candidate_video = _normalize_media_url(reddit_video.get(key))
            if candidate_video:
                video_candidates.append(candidate_video)

    candidate_thumbnail = _normalize_media_url(data.get("thumbnail"))
    if candidate_thumbnail and _is_image_url(candidate_thumbnail) and not thumbnail:
        thumbnail = candidate_thumbnail

    image_urls = [url for url in _dedupe_preserve_order(image_candidates) if _is_image_url(url)]
    video_urls = [url for url in _dedupe_preserve_order(video_candidates) if _is_video_url(url)]
    video_url = video_urls[0] if video_urls else ""
    if not thumbnail and image_urls:
        thumbnail = image_urls[0]

    media_items: list[dict[str, str]] = []
    if video_url:
        item: dict[str, str] = {"type": "video", "url": video_url}
        if thumbnail:
            item["thumbnail_url"] = thumbnail
        media_items.append(item)
    media_items.extend({"type": "image", "url": image_url} for image_url in image_urls)

    metadata: dict[str, Any] = {}
    if media_items:
        metadata["media"] = media_items
    if image_urls:
        metadata["image_urls"] = image_urls
    if video_url:
        metadata["video_url"] = video_url
    if thumbnail:
        metadata["thumbnail_url"] = thumbnail
    return metadata


def collect_reddit_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 4,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Collect Reddit submitted posts and comments for a user."""
    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = re.sub(r"^u/", "", username.strip().strip("/"), flags=re.IGNORECASE).strip()
    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    collected: list[dict[str, Any]] = []
    seen: set[str] = set()

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        submitted = _iter_listing(
            session,
            normalized_username,
            "submitted",
            max_pages=max_pages,
            request_delay_seconds=request_delay_seconds,
            timeout=timeout,
        )
        comments = _iter_listing(
            session,
            normalized_username,
            "comments",
            max_pages=max_pages,
            request_delay_seconds=request_delay_seconds,
            timeout=timeout,
        )

    for item in [*submitted, *comments]:
        data = item.get("data", {})
        post_id = data.get("name") or data.get("id")
        if not post_id or post_id in seen:
            continue
        seen.add(post_id)

        created = data.get("created_utc")
        if created is None:
            continue
        timestamp = datetime.fromtimestamp(float(created), tz=timezone.utc)
        if timestamp < cutoff:
            continue

        is_comment = str(data.get("name", "")).startswith("t1_")
        if is_comment:
            content = (data.get("body") or "").strip()
            post_type = "comment"
            replies = None
            referenced_username = data.get("link_author")
        else:
            title = (data.get("title") or "").strip()
            selftext = (data.get("selftext") or "").strip()
            content = f"{title}\n{selftext}".strip() if selftext else title
            post_type = "post"
            replies = data.get("num_comments")
            referenced_username = None

        if not content:
            continue

        permalink = data.get("permalink") or ""
        source_url = f"https://www.reddit.com{permalink}" if permalink else data.get("url")
        media_metadata = _extract_reddit_media(data, is_comment=is_comment)
        profile_image_url = _normalize_media_url(
            data.get("icon_img")
            or data.get("snoovatar_img")
            or data.get("author_icon_img")
        )

        collected.append(
            {
                "post_id": post_id,
                "platform": "Reddit",
                "username": normalized_username,
                "content": content,
                "timestamp": timestamp.isoformat(),
                "likes": data.get("score"),
                "retweets": None,
                "replies": replies,
                "source_url": source_url,
                "post_type": post_type,
                "referenced_username": referenced_username,
                "metadata": {
                    "subreddit": data.get("subreddit"),
                    "kind": item.get("kind"),
                    "profile_image_url": profile_image_url or None,
                    **media_metadata,
                },
            }
        )

    collected.sort(key=lambda post: post["timestamp"] or "", reverse=True)
    return collected
