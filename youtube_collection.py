"""YouTube collection helpers for local OSINT workflows."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable
from urllib.parse import quote

import requests

from panopto.errors import UsernameNotFoundError

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

_YOUTUBE_PROFILE_URL_RE = re.compile(
    r"^https?://(?:www\.)?youtube\.com/@([^/?#]+)",
    re.IGNORECASE,
)


def normalize_youtube_username(raw: Any) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    match = _YOUTUBE_PROFILE_URL_RE.match(text)
    if match:
        text = match.group(1)
    text = re.sub(r"^@+", "", text).strip()
    return text


def youtube_videos_url(username: str) -> str:
    """Build a YouTube channel videos URL from a handle-like username."""

    normalized = normalize_youtube_username(username)
    if not normalized:
        raise ValueError("username is required")

    handle = quote(normalized.upper(), safe="")
    return f"https://www.youtube.com/@{handle}/videos"


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


def _extract_count(text: str | None) -> int | None:
    if not text:
        return None
    normalized = str(text).strip().lower()
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


def _text_from_runs(raw: Any) -> str:
    if isinstance(raw, dict):
        simple = raw.get("simpleText")
        if isinstance(simple, str):
            return simple
        runs = raw.get("runs")
        if isinstance(runs, list):
            parts = [str(part.get("text") or "") for part in runs if isinstance(part, dict)]
            return "".join(parts).strip()
    if isinstance(raw, str):
        return raw
    return ""


def _parse_relative_timestamp(text: str, now_utc: datetime) -> datetime | None:
    value = text.strip().lower()
    value = value.replace("streamed", "").replace("premiered", "").strip()

    relative = re.search(
        r"(\d+)\s+(minute|hour|day|week|month|year)s?\s+ago",
        value,
        flags=re.IGNORECASE,
    )
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2).lower()
        if unit == "minute":
            return now_utc - timedelta(minutes=amount)
        if unit == "hour":
            return now_utc - timedelta(hours=amount)
        if unit == "day":
            return now_utc - timedelta(days=amount)
        if unit == "week":
            return now_utc - timedelta(weeks=amount)
        if unit == "month":
            return now_utc - timedelta(days=amount * 30)
        if unit == "year":
            return now_utc - timedelta(days=amount * 365)

    absolute = text.replace("Streamed", "").replace("Premiered", "").strip()
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(absolute, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    return None


def _extract_initial_data(html: str) -> dict[str, Any]:
    match = re.search(r"var\s+ytInitialData\s*=\s*(\{.*?\})\s*;\s*</script>", html, flags=re.DOTALL)
    if not match:
        return {}
    blob = match.group(1).strip()
    try:
        parsed = json.loads(blob)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _iter_video_renderers(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        video_renderer = node.get("videoRenderer")
        if isinstance(video_renderer, dict):
            yield video_renderer
        for value in node.values():
            yield from _iter_video_renderers(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_video_renderers(item)


def _page_indicates_missing_user(html: str) -> bool:
    lower = html.lower()
    signals = [
        "this channel does not exist",
        "404 not found",
        "channel unavailable",
        "the channel does not exist",
    ]
    return any(signal in lower for signal in signals)


def _iter_pages(
    session: requests.Session,
    username: str,
    max_pages: int,
    timeout: int,
) -> Iterable[str]:
    # YouTube videos tab is delivered as an initial payload; pagination needs continuations
    # and is not required for the initial collector implementation.
    _ = max_pages
    url = youtube_videos_url(username)
    response = session.get(url, timeout=timeout)
    if response.status_code in {400, 404}:
        raise UsernameNotFoundError(platform="youtube", username=normalize_youtube_username(username))
    response.raise_for_status()
    yield response.text


def collect_youtube_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 1,
    request_delay_seconds: float = 0.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Collect YouTube channel videos from the /videos tab."""
    _ = request_delay_seconds
    normalized_username = normalize_youtube_username(username)
    if not normalized_username:
        raise ValueError("username must be a non-empty string")

    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    now_utc = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    user_missing_signal = False

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        for html in _iter_pages(session, normalized_username, max_pages=max_pages, timeout=timeout):
            payload = _extract_initial_data(html)
            if not payload and _page_indicates_missing_user(html):
                user_missing_signal = True
            for renderer in _iter_video_renderers(payload):
                video_id = str(renderer.get("videoId") or "").strip()
                if not video_id:
                    continue

                title = _text_from_runs(renderer.get("title"))
                published_text = _text_from_runs(renderer.get("publishedTimeText"))
                timestamp = _parse_relative_timestamp(published_text, now_utc=now_utc)
                if timestamp and timestamp < cutoff:
                    continue

                view_text = _text_from_runs(renderer.get("viewCountText")) or _text_from_runs(
                    renderer.get("shortViewCountText")
                )
                views = _extract_count(view_text)

                thumbnails = renderer.get("thumbnail", {}).get("thumbnails", [])
                thumbnail_url = ""
                if isinstance(thumbnails, list) and thumbnails:
                    last_thumb = thumbnails[-1]
                    if isinstance(last_thumb, dict):
                        thumbnail_url = str(last_thumb.get("url") or "").strip()

                source_url = f"https://www.youtube.com/watch?v={video_id}"
                rows.append(
                    {
                        "post_id": video_id,
                        "platform": "YouTube",
                        "username": normalized_username,
                        "content": title or "(video)",
                        "timestamp": timestamp.isoformat() if timestamp else None,
                        "likes": None,
                        "retweets": None,
                        "replies": None,
                        "source_url": source_url,
                        "post_type": "post",
                        "referenced_username": None,
                        "metadata": {
                            "video_url": source_url,
                            "embed_url": f"https://www.youtube.com/embed/{video_id}",
                            "thumbnail_url": thumbnail_url,
                            "views": views,
                            "published_text": published_text or None,
                        },
                    }
                )

    if not rows and user_missing_signal:
        raise UsernameNotFoundError(platform="youtube", username=normalized_username)

    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row.get("post_id") or "")
        if not key:
            continue
        existing = deduped.get(key)
        if existing is None or len(str(row.get("content") or "")) > len(str(existing.get("content") or "")):
            deduped[key] = row

    results = list(deduped.values())
    results.sort(key=lambda post: post.get("timestamp") or "", reverse=True)
    return results
