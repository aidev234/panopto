"""Twitter collection helpers for local OSINT workflows.

This module collects posts from twitterwebviewer.com for a given username and
filters results to a configurable collection window.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Iterable

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - handled at runtime
    requests = None

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:  # pragma: no cover - handled at runtime
    BeautifulSoup = None


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


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
    raw_metadata: dict[str, Any]




def _ensure_dependencies() -> None:
    if requests is None or BeautifulSoup is None:
        raise RuntimeError(
            "Missing dependencies. Install with: pip install requests beautifulsoup4"
        )

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


def _parse_datetime(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None

    text = raw_value.strip()

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
    match = re.search(r"([\d,.]+)", text)
    if not match:
        return None
    return int(match.group(1).replace(",", "").replace(".", ""))


def _extract_metric(stats_text: str, labels: list[str]) -> int | None:
    label_group = "|".join(re.escape(label) for label in labels)
    patterns = [
        rf"(?:{label_group})\s*[:\-]?\s*([\d,.]+)",
        rf"([\d,.]+)\s*(?:{label_group})",
    ]

    for pattern in patterns:
        match = re.search(pattern, stats_text, flags=re.IGNORECASE)
        if match:
            return _extract_count(match.group(1))

    return None


def _extract_posts_from_html(username: str, html: str) -> list[TwitterPost]:
    _ensure_dependencies()
    soup = BeautifulSoup(html, "html.parser")
    posts: list[TwitterPost] = []

    candidates = soup.select("article, .tweet, .post, .timeline-item")
    if not candidates:
        candidates = [soup]

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
        likes = _extract_metric(stats_text, ["like", "likes", "❤️"])
        retweets = _extract_metric(stats_text, ["retweet", "retweets", "repost", "reposts"])
        replies = _extract_metric(stats_text, ["reply", "replies", "comment", "comments"])

        post_id = item.get("data-tweet-id") or item.get("id")

        if content or timestamp:
            posts.append(
                TwitterPost(
                    post_id=post_id,
                    username=username,
                    content=content,
                    timestamp=timestamp,
                    likes=likes,
                    retweets=retweets,
                    replies=replies,
                    raw_metadata={
                        "raw_timestamp": raw_time,
                    },
                )
            )

    return posts


def _iter_pages(
    username: str,
    session: requests.Session,
    max_pages: int,
    delay_seconds: float,
    timeout: int,
) -> Iterable[str]:
    _ensure_dependencies()
    base_url = "https://twitterwebviewer.com/"

    for page in range(1, max_pages + 1):
        params = {"user": username, "page": page}
        response = session.get(base_url, params=params, timeout=timeout)

        if response.status_code != 200:
            raise requests.HTTPError(
                f"twitterwebviewer returned status {response.status_code} for page {page}",
                response=response,
            )

        if not response.text.strip():
            break

        yield response.text

        if delay_seconds > 0:
            time.sleep(delay_seconds)


def collect_twitter_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 3,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Collect posts from `twitterwebviewer.com` for a user.

    Args:
        username: Twitter username (without @).
        collection_window: Relative window e.g. "1 week", "3 days".
        max_pages: Maximum pages to request for pagination.
        request_delay_seconds: Delay between requests to reduce blocking risk.
        timeout: Per-request timeout in seconds.
        proxies: Optional requests proxies mapping.

    Returns:
        List of post dictionaries with content, timestamp, and engagement metadata.
    """

    _ensure_dependencies()

    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = username.strip().lstrip("@")
    window = _parse_collection_window(collection_window)
    now = datetime.now(timezone.utc)
    cutoff = now - window

    collected: list[TwitterPost] = []

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        for html in _iter_pages(
            username=normalized_username,
            session=session,
            max_pages=max_pages,
            delay_seconds=request_delay_seconds,
            timeout=timeout,
        ):
            page_posts = _extract_posts_from_html(username=normalized_username, html=html)
            if not page_posts:
                break
            collected.extend(page_posts)

    filtered: list[dict[str, Any]] = []
    seen_keys: set[tuple[str | None, str, str | None]] = set()

    for post in collected:
        iso_ts = post.timestamp.isoformat() if post.timestamp else None
        dedupe_key = (post.post_id, post.content, iso_ts)
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
                "metadata": post.raw_metadata,
            }
        )

    filtered.sort(key=lambda p: p["timestamp"] or "", reverse=True)
    return filtered
