"""TikTok collection helpers for local OSINT workflows via tikvib.com."""

from __future__ import annotations

import random
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Iterable
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

from panopto.errors import UsernameNotFoundError

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


@dataclass
class TikTokPost:
    post_id: str | None
    username: str
    content: str
    timestamp: datetime | None
    likes: int | None
    comments: int | None
    views: int | None
    source_url: str | None
    video_url: str | None
    thumbnail_url: str | None
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
            return timedelta(**{unit: int(match.group(1))})

    raise ValueError(
        "Unsupported collection_window format. "
        "Use values like '1 week', '3 days', '12 hours', or '30 minutes'."
    )


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


def _parse_datetime(raw_value: str | None, now_utc: datetime) -> datetime | None:
    if not raw_value:
        return None

    text = raw_value.strip()
    lower = text.lower()

    ago_match = re.match(r"^(\d+)\s*(s|sec|secs|second|seconds|m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days|w|week|weeks)\s*ago?$", lower)
    if ago_match:
        amount = int(ago_match.group(1))
        unit = ago_match.group(2)
        if unit.startswith(("s", "sec")):
            return now_utc - timedelta(seconds=amount)
        if unit.startswith(("m", "min")):
            return now_utc - timedelta(minutes=amount)
        if unit.startswith(("h", "hr")):
            return now_utc - timedelta(hours=amount)
        if unit.startswith("d"):
            return now_utc - timedelta(days=amount)
        if unit.startswith("w"):
            return now_utc - timedelta(weeks=amount)

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


def _page_indicates_missing_user(html: str) -> bool:
    lower = html.lower()
    signals = [
        "user not found",
        "profile not found",
        "this account does not exist",
        "404",
    ]
    return any(signal in lower for signal in signals)


def _iter_pages(
    session: requests.Session,
    username: str,
    max_pages: int,
    request_delay_seconds: float,
    timeout: int,
) -> Iterable[str]:
    safe_username = quote(username, safe="")
    for page in range(1, max_pages + 1):
        url = f"https://www.tikvib.com/profile/{safe_username}"
        if page > 1:
            url = f"{url}?page={page}"
        response = session.get(url, timeout=timeout)
        if response.status_code == 404:
            raise UsernameNotFoundError(platform="tiktok", username=username)
        response.raise_for_status()
        html = response.text
        if not html.strip():
            break
        yield html
        if request_delay_seconds > 0 and page < max_pages:
            time.sleep(request_delay_seconds + random.uniform(0.0, 0.35))


def _extract_posts_from_html(username: str, html: str, *, now_utc: datetime) -> list[TikTokPost]:
    soup = BeautifulSoup(html, "html.parser")
    posts: list[TikTokPost] = []

    candidates = soup.select("article, .video-item, .post-item, [data-video-id], [data-post-id]")
    if not candidates:
        candidates = [link.parent for link in soup.select("a[href*='/video/']") if link.parent]

    for item in candidates:
        stats_text = item.get_text(" ", strip=True)
        content_node = item.select_one(
            ".desc, .caption, .video-desc, .post-desc, .title, .video-title, p"
        )
        content = content_node.get_text(" ", strip=True) if content_node else ""

        timestamp_node = (
            item.select_one("time")
            or item.find(attrs={"datetime": True})
            or item.select_one(".time, .create-time, .date")
        )
        raw_time = None
        if timestamp_node:
            raw_time = timestamp_node.get("datetime") or timestamp_node.get("data-time") or timestamp_node.get_text(strip=True)
        timestamp = _parse_datetime(raw_time, now_utc=now_utc)

        video_tag = item.select_one("video")
        source_tag = video_tag.select_one("source") if video_tag else None
        video_url = None
        if source_tag and source_tag.get("src"):
            video_url = source_tag.get("src")
        elif video_tag and video_tag.get("src"):
            video_url = video_tag.get("src")
        if not video_url:
            for attr in ("data-video", "data-video-url", "data-src", "data-play"):
                maybe = item.get(attr)
                if maybe and ".mp4" in maybe:
                    video_url = maybe
                    break
        if not video_url:
            mp4_link = item.select_one("a[href$='.mp4'], a[href*='.mp4?']")
            if mp4_link:
                video_url = mp4_link.get("href")

        thumbnail_url = None
        if video_tag and video_tag.get("poster"):
            thumbnail_url = video_tag.get("poster")
        if not thumbnail_url:
            image = item.select_one("img")
            if image:
                thumbnail_url = image.get("src") or image.get("data-src")

        source_link = item.select_one("a[href*='/video/']")
        source_href = source_link.get("href") if source_link else ""

        post_id = item.get("data-video-id") or item.get("data-post-id")
        if not post_id and source_href:
            id_match = re.search(r"/video/(\d+)", source_href)
            if id_match:
                post_id = id_match.group(1)

        source_url = None
        if source_href:
            source_url = urljoin("https://www.tikvib.com", source_href)
        elif post_id:
            source_url = f"https://www.tikvib.com/profile/{username}/video/{post_id}"

        likes = _extract_metric(stats_text, ["like", "likes", "heart"])
        comments = _extract_metric(stats_text, ["comment", "comments"])
        views = _extract_metric(stats_text, ["view", "views", "plays"])

        if not content and not video_url:
            continue
        if not post_id and not source_url and not video_url:
            continue

        posts.append(
            TikTokPost(
                post_id=post_id,
                username=username,
                content=content or "(video)",
                timestamp=timestamp,
                likes=likes,
                comments=comments,
                views=views,
                source_url=source_url,
                video_url=urljoin("https://www.tikvib.com", video_url) if video_url else None,
                thumbnail_url=urljoin("https://www.tikvib.com", thumbnail_url) if thumbnail_url else None,
                raw_metadata={
                    "raw_timestamp": raw_time,
                },
            )
        )

    return posts


def collect_tiktok_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 4,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Collect TikTok profile posts from tikvib.com."""
    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = username.strip().lstrip("@")
    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    now_utc = datetime.now(timezone.utc)
    collected: list[TikTokPost] = []
    user_missing_signal = False

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        for html in _iter_pages(
            session,
            normalized_username,
            max_pages=max_pages,
            request_delay_seconds=request_delay_seconds,
            timeout=timeout,
        ):
            page_posts = _extract_posts_from_html(normalized_username, html, now_utc=now_utc)
            if not page_posts and _page_indicates_missing_user(html):
                user_missing_signal = True
            if not page_posts:
                continue
            collected.extend(page_posts)

    if not collected and user_missing_signal:
        raise UsernameNotFoundError(platform="tiktok", username=normalized_username)

    best_by_post_id: dict[str, TikTokPost] = {}
    posts_without_id: list[TikTokPost] = []

    for post in collected:
        if post.post_id:
            existing = best_by_post_id.get(post.post_id)
            if existing is None or len(post.content) > len(existing.content):
                best_by_post_id[post.post_id] = post
        else:
            posts_without_id.append(post)

    normalized_posts = list(best_by_post_id.values()) + posts_without_id
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str | None]] = set()

    for post in normalized_posts:
        if post.timestamp and post.timestamp < cutoff:
            continue

        iso_ts = post.timestamp.isoformat() if post.timestamp else None
        dedupe_key = ("id" if post.post_id else "body", post.post_id or post.content, iso_ts)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        metadata = {
            **(post.raw_metadata or {}),
            "video_url": post.video_url,
            "thumbnail_url": post.thumbnail_url,
            "views": post.views,
        }
        rows.append(
            {
                "post_id": post.post_id,
                "platform": "TikTok",
                "username": normalized_username,
                "content": post.content,
                "timestamp": iso_ts,
                "likes": post.likes,
                "retweets": None,
                "replies": post.comments,
                "source_url": post.source_url,
                "post_type": "post",
                "referenced_username": None,
                "metadata": metadata,
            }
        )

    rows.sort(key=lambda post: post["timestamp"] or "", reverse=True)
    return rows
