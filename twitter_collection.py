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
from html import unescape
from os import getenv
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


def _candidate_page_urls(username: str, page: int) -> list[str]:
    safe_username = quote(username, safe="")
    safe_query_username = quote(f"@{username}", safe="")
    return [
        f"https://twitterwebviewer.com/?user={safe_username}&page={page}",
        f"https://twitterwebviewer.com/?q={safe_query_username}&page={page}",
        f"https://twitterwebviewer.com/?q={safe_query_username}",
        f"https://twitterwebviewer.com/{safe_username}",
        f"https://twitterwebviewer.com/@{safe_username}",
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
) -> Iterable[str]:
    for page in range(1, max_pages + 1):
        responses: list[str] = []
        for target_url in _candidate_page_urls(username=username, page=page):
            request_url = target_url
            params = None
            if render_proxy_template:
                request_url = render_proxy_template.format(url=quote(target_url, safe=""))

            response = session.get(request_url, params=params, timeout=timeout)

            if response.status_code != 200:
                continue

            html = response.text.strip()
            if html:
                responses.append(html)

        if not responses:
            break

        best_html = max(responses, key=lambda body: _page_signal_score(body, username))
        if _page_signal_score(best_html, username) <= 0 and page > 1:
            break

        yield best_html

        if delay_seconds > 0:
            time.sleep(delay_seconds)


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
    """Collect posts from `twitterwebviewer.com` for a user.

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

    normalized_username = username.strip().lstrip("@")
    window = _parse_collection_window(collection_window)
    now = datetime.now(timezone.utc)
    cutoff = now - window

    collected: list[TwitterPost] = []
    user_missing_signal = False

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        effective_render_proxy = render_proxy_template or getenv("TWITTER_RENDER_PROXY_TEMPLATE")

        for html in _iter_pages(
            username=normalized_username,
            session=session,
            max_pages=max_pages,
            delay_seconds=request_delay_seconds,
            timeout=timeout,
            render_proxy_template=effective_render_proxy,
        ):
            page_posts = _extract_posts_from_html(username=normalized_username, html=html)
            if not page_posts and _page_indicates_missing_user(html):
                user_missing_signal = True
            if not page_posts:
                break
            collected.extend(page_posts)

    should_use_browser = browser_fallback and (not collected or browser_enrich_existing)
    if should_use_browser:
        effective_browser_proxy = browser_proxy or getenv("TWITTER_BROWSER_PROXY")
        for rendered_html in _iter_rendered_pages(
            username=normalized_username,
            max_pages=max_pages,
            timeout=timeout,
            browser_proxy=effective_browser_proxy,
        ):
            page_posts = _extract_posts_from_html(username=normalized_username, html=rendered_html)
            if not page_posts and _page_indicates_missing_user(rendered_html):
                user_missing_signal = True
            if not page_posts:
                continue
            collected.extend(page_posts)

    if not collected and user_missing_signal:
        raise UsernameNotFoundError(platform="twitter", username=normalized_username)

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
                "metadata": post.raw_metadata,
            }
        )

    filtered.sort(key=lambda p: p["timestamp"] or "", reverse=True)
    return filtered
