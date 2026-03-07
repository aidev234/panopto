"""TikTok collection helpers for local OSINT workflows."""

from __future__ import annotations

import random
import re
import time
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
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

BLOCK_PAGE_MARKERS = (
    "just a moment",
    "verify you are human",
    "attention required",
    "cloudflare",
    "captcha",
)

DEFAULT_APIFY_TIKTOK_ACTOR_ID = "clockworks/tiktok-scraper"
APIFY_TIKTOK_ACTOR_ENV = "PANOPTO_APIFY_TIKTOK_ACTOR_ID"
APIFY_TIKTOK_RESULTS_LIMIT_MAX = 100


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


def _get_actor_id() -> str:
    return str(os.environ.get(APIFY_TIKTOK_ACTOR_ENV) or DEFAULT_APIFY_TIKTOK_ACTOR_ID).strip()


def _deep_get(mapping: dict[str, Any], *paths: str) -> Any:
    for path in paths:
        if path in mapping:
            value = mapping.get(path)
            if value not in (None, "", []):
                return value
        current: Any = mapping
        ok = True
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current.get(part)
            else:
                ok = False
                break
        if ok and current not in (None, "", []):
            return current
    return None


def _safe_bool(raw: Any) -> bool | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        return raw
    text = str(raw).strip().lower()
    if not text:
        return None
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return None


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


def _first_non_empty_str(mapping: dict[str, Any], *paths: str) -> str:
    value = _deep_get(mapping, *paths)
    text = str(value or "").strip()
    return text


def _coerce_http_url(raw: Any) -> str:
    value = str(raw or "").strip()
    return value if re.match(r"^https?://", value, flags=re.IGNORECASE) else ""


def _parse_datetime_apify(raw_value: Any, now_utc: datetime) -> datetime | None:
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
    if text.isdigit():
        return _parse_datetime_apify(int(text), now_utc=now_utc)
    return _parse_datetime(text, now_utc=now_utc)


def _normalize_apify_video_item(record: dict[str, Any], *, normalized_username: str, actor_id: str, now_utc: datetime) -> TikTokPost | None:
    post_id = _first_non_empty_str(record, "id", "aweme_id", "itemId", "video.id", "videoId")

    source_url = _coerce_http_url(
        _deep_get(
            record,
            "webVideoUrl",
            "videoUrl",
            "url",
            "video.url",
            "shareUrl",
        )
    )
    if not source_url and post_id:
        source_url = f"https://www.tiktok.com/@{quote(normalized_username, safe='')}/video/{post_id}"

    caption = _first_non_empty_str(record, "text", "desc", "caption")
    content = caption or "(video)"

    timestamp = _parse_datetime_apify(
        _deep_get(record, "createTimeISO", "createTime", "timestamp", "createdAt", "create_time"),
        now_utc=now_utc,
    )

    likes = _safe_int(_deep_get(record, "diggCount", "likes", "stats.diggCount", "statistics.likes"))
    comments = _safe_int(_deep_get(record, "commentCount", "comments", "stats.commentCount", "statistics.comments"))
    plays = _safe_int(_deep_get(record, "playCount", "views", "stats.playCount", "statistics.views"))
    shares = _safe_int(_deep_get(record, "shareCount", "stats.shareCount", "statistics.shares"))
    saves = _safe_int(_deep_get(record, "collectCount", "saveCount", "stats.collectCount", "statistics.saves"))

    video_url = _coerce_http_url(_deep_get(record, "video.downloadAddr", "video.playAddr", "video_url", "downloadAddr"))
    thumbnail_url = _coerce_http_url(
        _deep_get(
            record,
            "video.cover",
            "video.dynamicCover",
            "video.originCover",
            "thumbnail",
            "thumbnail_url",
        )
    )

    if not post_id and not source_url and not video_url and not thumbnail_url:
        return None

    author_username = _first_non_empty_str(
        record,
        "authorMeta.name",
        "author.uniqueId",
        "author.nickname",
        "author.username",
        "authorName",
    )
    author_nickname = _first_non_empty_str(record, "authorMeta.nickName", "author.nickname", "author.nickName")
    author_verified = _safe_bool(_deep_get(record, "authorMeta.verified", "author.verified"))
    author_signature = _first_non_empty_str(record, "authorMeta.signature", "author.signature", "author.bio")
    author_avatar = _coerce_http_url(
        _deep_get(record, "authorMeta.avatar", "author.avatarLarger", "author.avatarMedium", "author.avatarThumb")
    )
    link_in_bio = _first_non_empty_str(
        record,
        "authorMeta.bioLink.link",
        "author.bioLink.link",
        "author.link",
        "author.website",
    )
    fans = _safe_int(_deep_get(record, "authorMeta.fans", "authorStats.followerCount", "author.followerCount"))
    hearts = _safe_int(_deep_get(record, "authorMeta.heart", "authorStats.heartCount", "author.heartCount"))
    videos = _safe_int(_deep_get(record, "authorMeta.video", "authorStats.videoCount", "author.videoCount"))
    author_likes = _safe_int(_deep_get(record, "authorMeta.digg", "authorStats.diggCount", "author.diggCount"))

    music = _deep_get(record, "musicMeta", "music")
    if not isinstance(music, dict):
        music = {}
    video_format = _deep_get(record, "videoMeta", "video")
    if not isinstance(video_format, dict):
        video_format = {}

    metadata = {
        "apify_actor_id": actor_id,
        "caption": caption,
        "country_of_creation": _first_non_empty_str(record, "locationCreated", "region", "country"),
        "is_ad": _safe_bool(_deep_get(record, "isAd", "isSponsored")),
        "music": music,
        "video_format": video_format,
        "video_url": video_url or None,
        "thumbnail_url": thumbnail_url or None,
        "media": (
            [
                {
                    "type": "video",
                    "url": video_url,
                    **({"thumbnail_url": thumbnail_url} if thumbnail_url else {}),
                }
            ]
            if video_url
            else ([{"type": "image", "url": thumbnail_url}] if thumbnail_url else [])
        ),
        "image_urls": [thumbnail_url] if thumbnail_url else [],
        "plays": plays,
        "shares": shares,
        "saves": saves,
        "likes": likes,
        "comments": comments,
        "author_name": author_username or None,
        "author_nickname": author_nickname or None,
        "author_verified": author_verified,
        "author_signature": author_signature or None,
        "author_avatar_url": author_avatar or None,
        "profile_image_url": author_avatar or None,
        "link_in_bio": link_in_bio or None,
        "author_fans": fans,
        "author_hearts": hearts,
        "author_videos": videos,
        "author_likes": author_likes,
        "author": {
            "name": author_username or None,
            "nickname": author_nickname or None,
            "verified": author_verified,
            "signature": author_signature or None,
            "avatar_url": author_avatar or None,
            "link_in_bio": link_in_bio or None,
            "fans": fans,
            "hearts": hearts,
            "videos": videos,
            "likes": author_likes,
        },
        "raw": record,
    }

    return TikTokPost(
        post_id=post_id or None,
        username=normalized_username,
        content=content,
        timestamp=timestamp,
        likes=likes,
        comments=comments,
        views=plays,
        source_url=source_url or None,
        video_url=video_url or None,
        thumbnail_url=thumbnail_url or None,
        raw_metadata=metadata,
    )


def _iter_apify_video_records(dataset_items: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for item in dataset_items:
        if not isinstance(item, dict):
            continue
        if item.get("noResults") is True:
            continue
        if str(item.get("error") or "").strip():
            continue

        yielded_nested = False
        for list_key in ("videos", "posts", "items", "latestPosts", "itemList", "aweme_list"):
            nested = item.get(list_key)
            if not isinstance(nested, list):
                continue
            for candidate in nested:
                if not isinstance(candidate, dict):
                    continue
                merged = dict(item)
                merged.update(candidate)
                yield merged
            yielded_nested = True

        if not yielded_nested:
            yield item


def _collect_from_apify(
    *,
    normalized_username: str,
    cutoff: datetime,
    max_pages: int,
    timeout: int,
    now_utc: datetime,
) -> list[dict[str, Any]]:
    actor_id = _get_actor_id()
    max_items = min(APIFY_TIKTOK_RESULTS_LIMIT_MAX, max(12, max_pages * 30))
    actor_input = {
        "profiles": [normalized_username],
        "profileScrapeSections": ["videos"],
        "resultsPerPage": max_items,
        "excludePinnedPosts": False,
        "profileSorting": "latest",
    }
    dataset_items = run_actor_sync_get_items(
        actor_id=actor_id,
        actor_input=actor_input,
        timeout_seconds=max(timeout, 180),
    )

    posts: list[TikTokPost] = []
    for item in _iter_apify_video_records(dataset_items):
        normalized = _normalize_apify_video_item(
            item,
            normalized_username=normalized_username,
            actor_id=actor_id,
            now_utc=now_utc,
        )
        if normalized is None:
            continue
        if normalized.timestamp and normalized.timestamp < cutoff:
            continue
        posts.append(normalized)

    best_by_post_id: dict[str, TikTokPost] = {}
    posts_without_id: list[TikTokPost] = []
    for post in posts:
        if post.post_id:
            existing = best_by_post_id.get(post.post_id)
            if existing is None or len(post.content) > len(existing.content):
                best_by_post_id[post.post_id] = post
        else:
            posts_without_id.append(post)
    normalized_posts = list(best_by_post_id.values()) + posts_without_id
    normalized_posts.sort(key=lambda post: post.timestamp.isoformat() if post.timestamp else "", reverse=True)

    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str | None]] = set()
    for post in normalized_posts:
        iso_ts = post.timestamp.isoformat() if post.timestamp else None
        dedupe_key = ("id" if post.post_id else "body", post.post_id or post.content, iso_ts)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
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
                "metadata": post.raw_metadata,
            }
        )
    return rows


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
        url_variants = [
            f"https://www.tikvib.com/profile/{safe_username}",
            f"https://www.tikvib.com/profile/@{safe_username}",
        ]
        if page > 1:
            url_variants = [f"{url}?page={page}" for url in url_variants]
        page_html = ""
        saw_non_404 = False
        for url in url_variants:
            response = session.get(url, timeout=timeout)
            if response.status_code == 404:
                continue
            saw_non_404 = True
            response.raise_for_status()
            html = response.text
            if html.strip():
                page_html = html
                break
        if not page_html:
            break
        yield page_html
        if request_delay_seconds > 0 and page < max_pages:
            time.sleep(request_delay_seconds + random.uniform(0.0, 0.35))


def _looks_like_block_page(html: str) -> bool:
    lower = str(html or "").lower()
    return any(marker in lower for marker in BLOCK_PAGE_MARKERS)


def _extract_profile_image_from_html(html: str) -> str:
    soup = BeautifulSoup(str(html or ""), "html.parser")
    selectors = [
        "meta[property='og:image']",
        "meta[name='twitter:image']",
        "img[src*='avatar']",
        "img[data-src*='avatar']",
        "img[src*='profile']",
        "img[data-src*='profile']",
    ]
    fallback: list[str] = []
    for selector in selectors:
        for node in soup.select(selector):
            raw = node.get("content") or node.get("src") or node.get("data-src")
            value = str(raw or "").strip()
            if not value:
                continue
            if value.startswith("//"):
                value = f"https:{value}"
            if value.startswith("/"):
                value = urljoin("https://www.tikvib.com", value)
            if not re.match(r"^https?://", value, flags=re.IGNORECASE):
                continue
            lowered = value.lower()
            if "avatar" in lowered or "profile" in lowered:
                return value
            fallback.append(value)
    return fallback[0] if fallback else ""


def _iter_rendered_pages(
    username: str,
    max_pages: int,
    timeout: int,
) -> Iterable[str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return []

    url = f"https://www.tikvib.com/profile/{quote(username, safe='')}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=DEFAULT_HEADERS["User-Agent"],
            locale="en-US",
            timezone_id="UTC",
            viewport={"width": 1360, "height": 900},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            page.wait_for_timeout(1400)
            snapshots: list[str] = []
            previous_height = 0
            stagnant_rounds = 0

            for _ in range(max(2, max_pages * 2)):
                try:
                    page.evaluate(
                        """
                        () => {
                          const closeTokens = ['close', 'dismiss', 'cancel', 'not now', 'skip', 'accept', 'allow', 'agree', 'ok', 'x'];
                          const nodes = Array.from(document.querySelectorAll('button, [role="button"], .close, .modal-close'));
                          for (const node of nodes) {
                            const text = ((node.textContent || '') + ' ' + (node.getAttribute('aria-label') || '')).toLowerCase();
                            const cls = String(node.className || '').toLowerCase();
                            if (!text.trim() && !cls.trim()) continue;
                            if (closeTokens.some((token) => text.includes(token) || cls.includes(token))) {
                              node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                            }
                          }
                        }
                        """
                    )
                except Exception:
                    pass

                snapshots.append(page.content())
                current_height = int(page.evaluate("() => document.body ? document.body.scrollHeight : 0"))
                if current_height <= previous_height:
                    stagnant_rounds += 1
                else:
                    stagnant_rounds = 0
                previous_height = current_height
                if stagnant_rounds >= 2:
                    break

                page.mouse.wheel(0, 2600)
                page.wait_for_timeout(1200)

            return snapshots
        finally:
            context.close()
            browser.close()


def _iter_official_rendered_pages(
    username: str,
    max_pages: int,
    timeout: int,
) -> Iterable[str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return []

    url = f"https://www.tiktok.com/@{quote(username, safe='')}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=DEFAULT_HEADERS["User-Agent"],
            locale="en-US",
            timezone_id="UTC",
            viewport={"width": 1360, "height": 900},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            page.wait_for_timeout(1700)
            snapshots: list[str] = []
            previous_height = 0
            stagnant_rounds = 0
            for _ in range(max(3, max_pages * 3)):
                snapshots.append(page.content())
                current_height = int(page.evaluate("() => document.body ? document.body.scrollHeight : 0"))
                if current_height <= previous_height:
                    stagnant_rounds += 1
                else:
                    stagnant_rounds = 0
                previous_height = current_height
                if stagnant_rounds >= 2:
                    break
                page.mouse.wheel(0, 2800)
                page.wait_for_timeout(1300)
            return snapshots
        finally:
            context.close()
            browser.close()


def _extract_posts_from_html(username: str, html: str, *, now_utc: datetime) -> list[TikTokPost]:
    soup = BeautifulSoup(html, "html.parser")
    posts: list[TikTokPost] = []

    candidates = soup.select("article, .video-item, .post-item, [data-video-id], [data-post-id], [data-e2e='user-post-item']")
    if not candidates:
        candidates = [
            link.parent
            for link in soup.select("a[href*='/video/'], a[href*='tiktok.com/@'], a[href^='/@']")
            if link.parent
        ]

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

        source_link = item.select_one("a[href*='/video/'], a[href*='tiktok.com/@'], a[href^='/@']")
        source_href = source_link.get("href") if source_link else ""

        post_id = item.get("data-video-id") or item.get("data-post-id")
        if not post_id and source_href:
            id_match = re.search(r"/video/(\d+)", source_href)
            if id_match:
                post_id = id_match.group(1)

        source_url = None
        if source_href:
            if re.match(r"^https?://", source_href, flags=re.IGNORECASE):
                source_url = source_href
            elif source_href.startswith("/@"):
                source_url = urljoin("https://www.tiktok.com", source_href)
            else:
                source_url = urljoin("https://www.tikvib.com", source_href)
        elif post_id:
            source_url = f"https://www.tikvib.com/profile/{username}/video/{post_id}"

        likes = _extract_metric(stats_text, ["like", "likes", "heart"])
        comments = _extract_metric(stats_text, ["comment", "comments"])
        views = _extract_metric(stats_text, ["view", "views", "plays"])

        if not post_id and not source_url and not video_url and not thumbnail_url:
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

    if posts:
        return posts

    # Fallback for script-heavy pages where anchors are embedded in JSON payloads.
    normalized_html = html.replace("\\/", "/").replace("\\u002F", "/")
    link_pattern = re.compile(
        r"(https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9._-]+/video/\d+/?|/@[A-Za-z0-9._-]+/video/\d+/?)"
    )
    for match in link_pattern.findall(normalized_html):
        href = str(match).strip()
        source_url = href if href.startswith("http") else urljoin("https://www.tiktok.com", href)
        id_match = re.search(r"/video/(\d+)", source_url)
        post_id = id_match.group(1) if id_match else None
        posts.append(
            TikTokPost(
                post_id=post_id,
                username=username,
                content="(video)",
                timestamp=None,
                likes=None,
                comments=None,
                views=None,
                source_url=source_url,
                video_url=None,
                thumbnail_url=None,
                raw_metadata={"fallback_source": "regex_link"},
            )
        )
    if posts:
        return posts

    # Final fallback for payloads that only expose video ids.
    id_pattern = re.compile(r'"(?:videoId|aweme_id|itemId|id)"\s*:\s*"(\d{6,})"')
    for video_id in id_pattern.findall(normalized_html):
        posts.append(
            TikTokPost(
                post_id=video_id,
                username=username,
                content="(video)",
                timestamp=None,
                likes=None,
                comments=None,
                views=None,
                source_url=f"https://www.tiktok.com/@{username}/video/{video_id}",
                video_url=None,
                thumbnail_url=None,
                raw_metadata={"fallback_source": "id_payload"},
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
    browser_fallback: bool = True,
) -> list[dict[str, Any]]:
    """Collect TikTok profile posts, preferring Apify actor output."""
    if not username or not username.strip():
        raise ValueError("username must be a non-empty string")

    normalized_username = username.strip().lstrip("@").lower()
    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    now_utc = datetime.now(timezone.utc)
    _ = request_delay_seconds
    _ = proxies
    _ = browser_fallback

    try:
        return _collect_from_apify(
            normalized_username=normalized_username,
            cutoff=cutoff,
            max_pages=max_pages,
            timeout=timeout,
            now_utc=now_utc,
        )
    except ApifyConfigurationError as exc:
        raise SourceUnavailableError(
            platform="tiktok",
            username=normalized_username,
            reason=str(exc),
        ) from exc
    except (ApifyActorInputError, ApifyRequestError) as exc:
        raise SourceUnavailableError(
            platform="tiktok",
            username=normalized_username,
            reason=str(exc),
        ) from exc
