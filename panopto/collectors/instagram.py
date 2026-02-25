"""Instagram collection helpers for local OSINT workflows via byviewer.com."""

from __future__ import annotations

import re
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

from panopto.errors import SourceAccessBlockedError, UsernameNotFoundError

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


def _parse_datetime(raw_value: str | None, *, now_utc: datetime) -> datetime | None:
    if not raw_value:
        return None
    text = str(raw_value).strip()
    if not text:
        return None
    relative = re.match(
        r"^(\d+)\s*(s|sec|secs|second|seconds|m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days|w|week|weeks)\s*ago?$",
        text.lower(),
    )
    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)
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


def _page_indicates_missing_user(html: str) -> bool:
    lowered = html.lower()
    signals = [
        "user not found",
        "profile not found",
        "this account doesn't exist",
        "this account does not exist",
        "no user found",
        "not available",
    ]
    return any(signal in lowered for signal in signals)


def _extract_posts_from_html(username: str, html: str, *, now_utc: datetime) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    posts: list[dict[str, Any]] = []
    candidates = soup.select("article, .post, .item, .card, [data-post-id], [data-shortcode]")
    if not candidates:
        candidates = [
            link.parent
            for link in soup.select("a[href*='instagram.com/p/'], a[href*='instagram.com/reel/'], a[href^='/p/'], a[href^='/reel/']")
            if link.parent
        ]

    for item in candidates:
        post_link = item.select_one("a[href*='instagram.com/p/'], a[href*='instagram.com/reel/'], a[href^='/p/'], a[href^='/reel/']")
        href = str(post_link.get("href") or "").strip() if post_link else ""
        if href and href.startswith("/"):
            href = urljoin("https://www.instagram.com", href)
        if href and "instagram.com/" not in href.lower():
            href = ""

        shortcode = item.get("data-shortcode") or ""
        if not shortcode and href:
            match = re.search(r"/(?:p|reel)/([^/?#]+)/?", href)
            if match:
                shortcode = match.group(1).strip()

        text_node = item.select_one(".caption, .desc, .content, p")
        content = text_node.get_text(" ", strip=True) if text_node else ""
        if not content:
            content = item.get_text(" ", strip=True)
        content = re.sub(r"\s+", " ", content).strip()

        time_node = item.select_one("time") or item.find(attrs={"datetime": True}) or item.select_one(".time, .date")
        raw_time = None
        if time_node:
            raw_time = time_node.get("datetime") or time_node.get("data-time") or time_node.get_text(strip=True)
        timestamp = _parse_datetime(raw_time, now_utc=now_utc)

        image_candidates: list[str] = []
        video_candidates: list[str] = []
        thumbnail = ""
        for img in item.select("img"):
            src = str(img.get("src") or img.get("data-src") or "").strip()
            if src.startswith("//"):
                src = f"https:{src}"
            if src.lower().startswith(("http://", "https://")):
                image_candidates.append(src)
                if not thumbnail:
                    thumbnail = src
        for video in item.select("video"):
            src = str(video.get("src") or "").strip()
            if src.lower().startswith(("http://", "https://")):
                video_candidates.append(src)
            poster = str(video.get("poster") or "").strip()
            if poster.lower().startswith(("http://", "https://")) and not thumbnail:
                thumbnail = poster
        media: list[dict[str, str]] = []
        if video_candidates:
            first_video = video_candidates[0]
            entry: dict[str, str] = {"type": "video", "url": first_video}
            if thumbnail:
                entry["thumbnail_url"] = thumbnail
            media.append(entry)
        for image_url in image_candidates:
            media.append({"type": "image", "url": image_url})

        if not shortcode and not href and not content:
            continue
        posts.append(
            {
                "post_id": shortcode or None,
                "platform": "Instagram",
                "username": username,
                "content": content or "(no text content)",
                "timestamp": timestamp.isoformat() if timestamp else None,
                "likes": None,
                "retweets": None,
                "replies": None,
                "source_url": href or (f"https://www.instagram.com/{username}/" if username else None),
                "post_type": "post",
                "referenced_username": None,
                "metadata": {
                    "media": media,
                    "image_urls": image_candidates,
                    "video_url": video_candidates[0] if video_candidates else "",
                    "thumbnail_url": thumbnail,
                    "raw_timestamp": raw_time,
                },
            }
        )
    if posts:
        return posts

    # Fallback for script-heavy pages where post links are embedded in JSON blobs.
    normalized_html = html.replace("\\/", "/").replace("\\u002F", "/")
    link_pattern = re.compile(
        r"(https?://(?:www\.)?instagram\.com/(?:p|reel)/[A-Za-z0-9_-]+/?|/(?:p|reel)/[A-Za-z0-9_-]+/?)"
    )
    for match in link_pattern.findall(normalized_html):
        href = str(match).strip()
        source_url = href if href.startswith("http") else urljoin("https://www.instagram.com", href)
        shortcode_match = re.search(r"/(?:p|reel)/([A-Za-z0-9_-]+)/?", source_url)
        shortcode = shortcode_match.group(1) if shortcode_match else None
        posts.append(
            {
                "post_id": shortcode,
                "platform": "Instagram",
                "username": username,
                "content": "(no text content)",
                "timestamp": None,
                "likes": None,
                "retweets": None,
                "replies": None,
                "source_url": source_url,
                "post_type": "post",
                "referenced_username": None,
                "metadata": {
                    "media": [],
                    "image_urls": [],
                    "video_url": "",
                    "thumbnail_url": "",
                    "raw_timestamp": None,
                    "fallback_source": "regex_link",
                },
            }
        )
    if posts:
        return posts

    # Final fallback for payloads that only expose shortcodes without direct links.
    shortcode_pattern = re.compile(r'"shortcode"\s*:\s*"([A-Za-z0-9_-]+)"')
    for shortcode in shortcode_pattern.findall(normalized_html):
        posts.append(
            {
                "post_id": shortcode,
                "platform": "Instagram",
                "username": username,
                "content": "(no text content)",
                "timestamp": None,
                "likes": None,
                "retweets": None,
                "replies": None,
                "source_url": f"https://www.instagram.com/p/{shortcode}/",
                "post_type": "post",
                "referenced_username": None,
                "metadata": {
                    "media": [],
                    "image_urls": [],
                    "video_url": "",
                    "thumbnail_url": "",
                    "raw_timestamp": None,
                    "fallback_source": "shortcode_payload",
                },
            }
        )
    return posts


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
            f"https://www.byviewer.com/detail/?username={safe_username}",
            f"https://www.byviewer.com/detail?username={safe_username}",
        ]
        if page > 1:
            url_variants = [f"{url}&page={page}" for url in url_variants]
        page_html = ""
        for url in url_variants:
            try:
                response = session.get(url, timeout=timeout)
            except requests.RequestException:
                continue
            if response.status_code == 404:
                continue
            if response.status_code >= 400:
                continue
            html = response.text.strip()
            if html:
                page_html = html
                break
        if not page_html:
            break
        yield page_html
        if request_delay_seconds > 0 and page < max_pages:
            time.sleep(request_delay_seconds)


def _looks_like_block_page(html: str) -> bool:
    lower = str(html or "").lower()
    return any(marker in lower for marker in BLOCK_PAGE_MARKERS)


def _extract_profile_image_from_html(html: str) -> str:
    soup = BeautifulSoup(str(html or ""), "html.parser")
    selectors = [
        "meta[property='og:image']",
        "meta[name='twitter:image']",
        "img[src*='profile']",
        "img[data-src*='profile']",
        "img[src*='avatar']",
        "img[data-src*='avatar']",
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
                value = urljoin("https://www.instagram.com", value)
            if not re.match(r"^https?://", value, flags=re.IGNORECASE):
                continue
            lowered = value.lower()
            if "profile" in lowered or "avatar" in lowered:
                return value
            fallback.append(value)
    return fallback[0] if fallback else ""


def _attach_profile_image(rows: list[dict[str, Any]], profile_image_url: str) -> None:
    if not profile_image_url:
        return
    for row in rows:
        metadata = row.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
            row["metadata"] = metadata
        if not str(metadata.get("profile_image_url") or "").strip():
            metadata["profile_image_url"] = profile_image_url


def _dismiss_browser_overlays(page: Any) -> None:
    try:
        page.evaluate(
            """
            () => {
              const closeTokens = [
                'close', 'dismiss', 'cancel', 'not now', 'not now.', 'later', 'skip',
                'accept', 'allow', 'agree', 'ok', 'x', 'log in', 'login'
              ];
              const nodes = Array.from(
                document.querySelectorAll(
                  "button, [role='button'], a[role='button'], .close, .modal-close, [aria-label]"
                )
              );
              for (const node of nodes) {
                const text = ((node.textContent || '') + ' ' + (node.getAttribute('aria-label') || '')).toLowerCase();
                const cls = String(node.className || '').toLowerCase();
                if (!text.trim() && !cls.trim()) continue;
                if (closeTokens.some((token) => text.includes(token) || cls.includes(token))) {
                  node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                }
              }

              // Remove simple full-screen overlays that block scroll/click.
              const blockers = Array.from(document.querySelectorAll("div, section, aside"));
              for (const el of blockers) {
                const style = window.getComputedStyle(el);
                if (style.position === 'fixed' && (style.zIndex || '0') !== 'auto') {
                  const z = Number(style.zIndex || 0);
                  const rect = el.getBoundingClientRect();
                  if (z >= 100 && rect.width >= window.innerWidth * 0.9 && rect.height >= window.innerHeight * 0.4) {
                    el.style.display = 'none';
                  }
                }
              }
              if (document.body) document.body.style.overflow = 'auto';
              if (document.documentElement) document.documentElement.style.overflow = 'auto';
            }
            """
        )
    except Exception:
        pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def _safe_page_content(page: Any, *, attempts: int = 3, wait_ms: int = 250) -> str:
    for _ in range(max(1, attempts)):
        try:
            return str(page.content() or "")
        except Exception:
            try:
                page.wait_for_timeout(wait_ms)
            except Exception:
                pass
    return ""


def _safe_scroll_height(page: Any, *, attempts: int = 2, wait_ms: int = 200) -> int:
    for _ in range(max(1, attempts)):
        try:
            return int(page.evaluate("() => document.body ? document.body.scrollHeight : 0"))
        except Exception:
            try:
                page.wait_for_timeout(wait_ms)
            except Exception:
                pass
    return 0


def _safe_scroll_to_bottom(page: Any, *, attempts: int = 2, wait_ms: int = 200) -> None:
    for _ in range(max(1, attempts)):
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            return
        except Exception:
            try:
                page.wait_for_timeout(wait_ms)
            except Exception:
                pass


def _iter_rendered_pages(
    username: str,
    max_pages: int,
    timeout: int,
) -> Iterable[str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return []

    url = f"https://www.byviewer.com/detail?username={quote(username, safe='')}"
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
            page.wait_for_timeout(1500)
            html_snapshots: list[str] = []
            previous_height = 0
            stagnant_rounds = 0
            for _ in range(max(4, max_pages * 4)):
                _dismiss_browser_overlays(page)

                html = _safe_page_content(page)
                if html:
                    html_snapshots.append(html)
                current_height = _safe_scroll_height(page)
                if current_height <= previous_height:
                    stagnant_rounds += 1
                else:
                    stagnant_rounds = 0
                previous_height = current_height
                if stagnant_rounds >= 2:
                    try:
                        clicked = bool(
                            page.evaluate(
                                """
                                () => {
                                  const labels = ['load more', 'show more', 'more'];
                                  const nodes = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                                  for (const node of nodes) {
                                    const text = (node.textContent || '').toLowerCase().trim();
                                    if (!text) continue;
                                    if (labels.some((label) => text.includes(label))) {
                                      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                      return true;
                                    }
                                  }
                                  return false;
                                }
                                """
                            )
                        )
                    except Exception:
                        clicked = False
                    if not clicked:
                        break
                    stagnant_rounds = 0
                    page.wait_for_timeout(1300)
                    continue
                _safe_scroll_to_bottom(page)
                page.wait_for_timeout(1300)
            return html_snapshots
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

    url = f"https://www.instagram.com/{quote(username, safe='')}/"
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
            page.wait_for_timeout(1800)
            snapshots: list[str] = []
            previous_height = 0
            stagnant_rounds = 0
            for _ in range(max(3, max_pages * 3)):
                _dismiss_browser_overlays(page)
                html = _safe_page_content(page)
                if html:
                    snapshots.append(html)
                current_height = _safe_scroll_height(page)
                if current_height <= previous_height:
                    stagnant_rounds += 1
                else:
                    stagnant_rounds = 0
                previous_height = current_height
                if stagnant_rounds >= 2:
                    try:
                        clicked = bool(
                            page.evaluate(
                                """
                                () => {
                                  const labels = ['more posts', 'load more', 'show more', 'more'];
                                  const nodes = Array.from(document.querySelectorAll('button, a, [role="button"]'));
                                  for (const node of nodes) {
                                    const text = (node.textContent || '').toLowerCase().trim();
                                    if (!text) continue;
                                    if (labels.some((label) => text.includes(label))) {
                                      node.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                      return true;
                                    }
                                  }
                                  return false;
                                }
                                """
                            )
                        )
                    except Exception:
                        clicked = False
                    if not clicked:
                        break
                    stagnant_rounds = 0
                    page.wait_for_timeout(1200)
                    continue
                _safe_scroll_to_bottom(page)
                page.wait_for_timeout(1300)
            return snapshots
        finally:
            context.close()
            browser.close()


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
    """Collect Instagram posts for a user via byviewer detail page."""
    normalized_username = normalize_instagram_username(username)
    if not normalized_username:
        raise ValueError("username must be a non-empty string")

    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    now_utc = datetime.now(timezone.utc)
    rows: list[dict[str, Any]] = []
    browser_rows: list[dict[str, Any]] = []
    blocked_detected = False
    profile_image_url = ""

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)
        probe_url = f"https://www.byviewer.com/detail?username={quote(normalized_username, safe='')}"
        try:
            probe_response = session.get(probe_url, timeout=timeout)
            if probe_response.status_code in {403, 429}:
                blocked_detected = True
            if _looks_like_block_page(probe_response.text):
                blocked_detected = True
        except requests.RequestException:
            pass
        for html in _iter_pages(
            session=session,
            username=normalized_username,
            max_pages=max_pages,
            request_delay_seconds=request_delay_seconds,
            timeout=timeout,
        ):
            if not profile_image_url:
                profile_image_url = _extract_profile_image_from_html(html)
            if _looks_like_block_page(html):
                blocked_detected = True
                continue
            page_rows = _extract_posts_from_html(normalized_username, html, now_utc=now_utc)
            _attach_profile_image(page_rows, profile_image_url)
            rows.extend(page_rows)

    needs_browser_backfill = False
    if rows:
        has_recent = False
        for row in rows:
            raw_ts = row.get("timestamp")
            if not raw_ts:
                continue
            parsed = _parse_datetime(str(raw_ts), now_utc=now_utc)
            if parsed and parsed >= cutoff:
                has_recent = True
                break
        needs_browser_backfill = not has_recent

    if browser_fallback and (not rows or needs_browser_backfill):
        for html in _iter_rendered_pages(
            username=normalized_username,
            max_pages=max_pages,
            timeout=max(timeout, 40),
        ):
            if not profile_image_url:
                profile_image_url = _extract_profile_image_from_html(html)
            if _looks_like_block_page(html):
                blocked_detected = True
                continue
            page_rows = _extract_posts_from_html(normalized_username, html, now_utc=now_utc)
            _attach_profile_image(page_rows, profile_image_url)
            browser_rows.extend(page_rows)
    if browser_rows:
        rows.extend(browser_rows)

    if browser_fallback and not rows:
        for html in _iter_official_rendered_pages(
            username=normalized_username,
            max_pages=max_pages,
            timeout=max(timeout, 45),
        ):
            if not profile_image_url:
                profile_image_url = _extract_profile_image_from_html(html)
            if _looks_like_block_page(html):
                blocked_detected = True
                continue
            page_rows = _extract_posts_from_html(normalized_username, html, now_utc=now_utc)
            _attach_profile_image(page_rows, profile_image_url)
            rows.extend(page_rows)

    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(row.get("post_id") or f"{row.get('timestamp') or ''}|{row.get('content') or ''}")
        existing = deduped.get(key)
        if existing is None or len(str(row.get("content") or "")) > len(str(existing.get("content") or "")):
            deduped[key] = row

    filtered: list[dict[str, Any]] = []
    for row in deduped.values():
        raw_ts = row.get("timestamp")
        post_ts = _parse_datetime(str(raw_ts), now_utc=now_utc) if raw_ts else None
        if post_ts and post_ts < cutoff:
            continue
        filtered.append(row)
    if not filtered and blocked_detected:
        raise SourceAccessBlockedError(platform="instagram", username=normalized_username)
    filtered.sort(key=lambda item: str(item.get("timestamp") or ""), reverse=True)
    return filtered
