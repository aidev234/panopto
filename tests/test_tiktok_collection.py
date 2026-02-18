from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import panopto.collectors.tiktok as tiktok_collection
from panopto.errors import SourceAccessBlockedError
from requests import RequestException


def test_extract_posts_from_html_includes_video_urls_and_stats():
    html = """
    <article data-video-id="12345">
      <div class="caption">First clip</div>
      <time datetime="2026-02-10T10:00:00Z"></time>
      <a href="/profile/aoc/video/12345">Open</a>
      <video poster="/thumb.jpg"><source src="/videos/12345.mp4" type="video/mp4" /></video>
      <div>1.2K likes 34 comments 8.9K views</div>
    </article>
    """

    posts = tiktok_collection._extract_posts_from_html(
        "aoc", html, now_utc=datetime(2026, 2, 15, tzinfo=timezone.utc)
    )

    assert len(posts) == 1
    post = posts[0]
    assert post.post_id == "12345"
    assert post.content == "First clip"
    assert post.likes == 1200
    assert post.comments == 34
    assert post.views == 8900
    assert post.source_url == "https://www.tikvib.com/profile/aoc/video/12345"
    assert post.video_url == "https://www.tikvib.com/videos/12345.mp4"
    assert post.thumbnail_url == "https://www.tikvib.com/thumb.jpg"


def test_collect_tiktok_posts_filters_by_window_and_dedupes():
    now = datetime.now(timezone.utc)
    recent_iso = (now - timedelta(days=1)).isoformat()
    old_iso = (now - timedelta(days=20)).isoformat()

    html = f"""
    <article data-video-id="same">
      <div class="caption">Short</div>
      <time datetime="{recent_iso}"></time>
      <a href="/profile/aoc/video/same"></a>
      <video><source src="/v/same.mp4" /></video>
    </article>
    <article data-video-id="same">
      <div class="caption">Longer canonical caption</div>
      <time datetime="{recent_iso}"></time>
      <a href="/profile/aoc/video/same"></a>
      <video><source src="/v/same.mp4" /></video>
    </article>
    <article data-video-id="old">
      <div class="caption">Old clip</div>
      <time datetime="{old_iso}"></time>
      <a href="/profile/aoc/video/old"></a>
      <video><source src="/v/old.mp4" /></video>
    </article>
    """

    with patch("panopto.collectors.tiktok._iter_pages", return_value=[html]):
        rows = tiktok_collection.collect_tiktok_posts(
            "aoc", "1 week", max_pages=2, request_delay_seconds=0
        )

    assert len(rows) == 1
    assert rows[0]["post_id"] == "same"
    assert rows[0]["content"] == "Longer canonical caption"
    assert rows[0]["metadata"]["video_url"] == "https://www.tikvib.com/v/same.mp4"


def test_parse_collection_window_rejects_invalid_format():
    try:
        tiktok_collection.collect_tiktok_posts("aoc", "yesterday")
    except ValueError as exc:
        assert "Unsupported collection_window format" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_collect_tiktok_posts_uses_rendered_fallback_when_request_pages_empty():
    now = datetime.now(timezone.utc)
    recent_iso = (now - timedelta(days=1)).isoformat()
    rendered_html = f"""
    <article data-video-id="fallback123">
      <div class="caption">Recovered from rendered page</div>
      <time datetime="{recent_iso}"></time>
      <a href="/profile/aoc/video/fallback123"></a>
      <video><source src="/v/fallback123.mp4" /></video>
    </article>
    """

    with patch("panopto.collectors.tiktok._iter_pages", return_value=["<html><body>no static posts</body></html>"]):
        with patch("panopto.collectors.tiktok._iter_rendered_pages", return_value=[rendered_html]):
            rows = tiktok_collection.collect_tiktok_posts(
                "aoc",
                "1 week",
                max_pages=1,
                request_delay_seconds=0,
                browser_fallback=True,
            )

    assert len(rows) == 1
    assert rows[0]["post_id"] == "fallback123"
    assert rows[0]["content"] == "Recovered from rendered page"


def test_collect_tiktok_posts_uses_rendered_fallback_when_static_fetch_raises():
    now = datetime.now(timezone.utc)
    recent_iso = (now - timedelta(days=1)).isoformat()
    rendered_html = f"""
    <article data-video-id="fallback999">
      <div class="caption">Recovered after static fetch error</div>
      <time datetime="{recent_iso}"></time>
      <a href="/profile/aoc/video/fallback999"></a>
      <video><source src="/v/fallback999.mp4" /></video>
    </article>
    """

    with patch("panopto.collectors.tiktok._iter_pages", side_effect=RequestException("blocked")):
        with patch("panopto.collectors.tiktok._iter_rendered_pages", return_value=[rendered_html]):
            rows = tiktok_collection.collect_tiktok_posts(
                "aoc",
                "1 week",
                max_pages=1,
                request_delay_seconds=0,
                browser_fallback=True,
            )

    assert len(rows) == 1
    assert rows[0]["post_id"] == "fallback999"


def test_extract_posts_from_html_accepts_absolute_tiktok_links_and_link_only_posts():
    html = """
    <article>
      <a href="https://www.tiktok.com/@aoc/video/7654321">Open</a>
      <img src="https://cdn.example.com/thumb.jpg" />
    </article>
    """
    posts = tiktok_collection._extract_posts_from_html(
        "aoc",
        html,
        now_utc=datetime(2026, 2, 15, tzinfo=timezone.utc),
    )

    assert len(posts) == 1
    assert posts[0].post_id == "7654321"
    assert posts[0].source_url == "https://www.tiktok.com/@aoc/video/7654321"


def test_collect_tiktok_posts_does_not_raise_not_found_from_html_marker_only():
    html = "<html><body>user not found</body></html>"
    with patch("panopto.collectors.tiktok._iter_pages", return_value=[html]):
        rows = tiktok_collection.collect_tiktok_posts(
            "aoc",
            "1 week",
            max_pages=1,
            request_delay_seconds=0,
            browser_fallback=False,
        )
    assert rows == []


def test_collect_tiktok_posts_uses_official_fallback_when_aggregator_paths_empty():
    html = """
    <article>
      <a href="https://www.tiktok.com/@aoc/video/123456">Open</a>
      <img src="https://cdn.example.com/thumb.jpg" />
    </article>
    """
    with patch("panopto.collectors.tiktok._iter_pages", return_value=[]):
        with patch("panopto.collectors.tiktok._iter_rendered_pages", return_value=[]):
            with patch("panopto.collectors.tiktok._iter_official_rendered_pages", return_value=[html]):
                rows = tiktok_collection.collect_tiktok_posts(
                    "aoc",
                    "30 days",
                    max_pages=1,
                    request_delay_seconds=0,
                    browser_fallback=True,
                )
    assert len(rows) == 1
    assert rows[0]["post_id"] == "123456"


def test_collect_tiktok_posts_raises_blocked_error_on_challenge_pages():
    blocked_html = "<html><body>Just a moment... captcha cloudflare</body></html>"
    with patch("panopto.collectors.tiktok._iter_pages", return_value=[blocked_html]):
        try:
            tiktok_collection.collect_tiktok_posts(
                "aoc",
                "30 days",
                max_pages=1,
                request_delay_seconds=0,
                browser_fallback=False,
            )
        except SourceAccessBlockedError as exc:
            assert exc.platform == "tiktok"
            assert exc.username == "aoc"
        else:
            raise AssertionError("Expected SourceAccessBlockedError on challenge page")


def test_extract_posts_from_html_fallback_reads_links_from_script_payload():
    html = """
    <html><body>
      <script>
        window.__DATA__ = {"items":[{"url":"https://www.tiktok.com/@aoc/video/999001"}]};
      </script>
    </body></html>
    """
    posts = tiktok_collection._extract_posts_from_html(
        "aoc",
        html,
        now_utc=datetime(2026, 2, 15, tzinfo=timezone.utc),
    )
    assert len(posts) == 1
    assert posts[0].post_id == "999001"


def test_extract_posts_from_html_fallback_reads_video_id_payload_without_links():
    html = """
    <html><body>
      <script>
        window.__DATA__ = {"itemList":[{"videoId":"999777"}]};
      </script>
    </body></html>
    """
    posts = tiktok_collection._extract_posts_from_html(
        "aoc",
        html,
        now_utc=datetime(2026, 2, 15, tzinfo=timezone.utc),
    )
    assert len(posts) == 1
    assert posts[0].post_id == "999777"
    assert posts[0].source_url == "https://www.tiktok.com/@aoc/video/999777"


def test_iter_pages_tries_profile_url_variants():
    class _Response:
        def __init__(self, status_code: int, text: str):
            self.status_code = status_code
            self.text = text

        def raise_for_status(self):
            if self.status_code >= 400:
                raise RuntimeError(f"status {self.status_code}")

    class _Session:
        def __init__(self):
            self.calls = []

        def get(self, url, timeout=20):
            self.calls.append(url)
            if "/profile/@aoc" in url:
                return _Response(200, "<html>ok</html>")
            return _Response(404, "")

    session = _Session()
    pages = list(tiktok_collection._iter_pages(session, "aoc", max_pages=1, request_delay_seconds=0, timeout=20))

    assert pages == ["<html>ok</html>"]
    assert any("/profile/@aoc" in call for call in session.calls)
