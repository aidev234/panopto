from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from panopto.errors import SourceAccessBlockedError
from panopto.collectors.instagram import (
    _dismiss_browser_overlays,
    _extract_posts_from_html,
    _iter_pages,
    _safe_scroll_height,
    _safe_scroll_to_bottom,
    _safe_page_content,
    collect_instagram_posts,
    normalize_instagram_username,
)


def test_normalize_instagram_username():
    assert normalize_instagram_username("@aoc") == "aoc"
    assert normalize_instagram_username("https://www.instagram.com/AOC/") == "AOC"


def test_extract_posts_from_html_parses_post_link_and_caption():
    html = """
    <article data-shortcode="abc123">
      <a href="https://www.instagram.com/p/abc123/">open</a>
      <p class="caption">Hello Instagram</p>
      <time datetime="2026-02-10T12:00:00Z"></time>
      <img src="https://cdn.example.com/ig.jpg" />
    </article>
    """
    posts = _extract_posts_from_html("aoc", html, now_utc=datetime(2026, 2, 12, tzinfo=timezone.utc))
    assert len(posts) == 1
    assert posts[0]["post_id"] == "abc123"
    assert posts[0]["content"] == "Hello Instagram"
    assert posts[0]["source_url"] == "https://www.instagram.com/p/abc123/"
    assert posts[0]["platform"] == "Instagram"


def test_collect_instagram_posts_filters_window_and_dedupes():
    now = datetime.now(timezone.utc)
    recent_iso = (now - timedelta(days=1)).isoformat()
    old_iso = (now - timedelta(days=50)).isoformat()
    html = f"""
    <article data-shortcode="r1">
      <a href="https://www.instagram.com/p/r1/">open</a>
      <p>Recent IG</p>
      <time datetime="{recent_iso}"></time>
    </article>
    <article data-shortcode="r1">
      <a href="https://www.instagram.com/p/r1/">open</a>
      <p>Recent IG with more detail</p>
      <time datetime="{recent_iso}"></time>
    </article>
    <article data-shortcode="o1">
      <a href="https://www.instagram.com/p/o1/">open</a>
      <p>Old IG</p>
      <time datetime="{old_iso}"></time>
    </article>
    """
    with patch("panopto.collectors.instagram._iter_pages", return_value=[html]):
        rows = collect_instagram_posts("aoc", "14 days", request_delay_seconds=0, browser_fallback=False)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "r1"
    assert rows[0]["content"] == "Recent IG with more detail"


def test_collect_instagram_browser_fallback_when_request_path_empty():
    browser_html = """
    <article data-shortcode="b1">
      <a href="https://www.instagram.com/p/b1/">open</a>
      <p>Loaded after scroll</p>
      <time datetime="2026-02-10T12:00:00Z"></time>
    </article>
    """
    with (
        patch("panopto.collectors.instagram._iter_pages", return_value=["<html></html>"]),
        patch("panopto.collectors.instagram._iter_rendered_pages", return_value=[browser_html]),
    ):
        rows = collect_instagram_posts("aoc", "30 days", request_delay_seconds=0, browser_fallback=True)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "b1"


def test_collect_instagram_browser_backfill_when_static_only_old_posts():
    now = datetime.now(timezone.utc)
    old_iso = (now - timedelta(days=180)).isoformat()
    recent_iso = (now - timedelta(days=1)).isoformat()
    static_html = f"""
    <article data-shortcode="old1">
      <a href="https://www.instagram.com/p/old1/">open</a>
      <p>Pinned old post</p>
      <time datetime="{old_iso}"></time>
    </article>
    """
    browser_html = f"""
    <article data-shortcode="new1">
      <a href="https://www.instagram.com/p/new1/">open</a>
      <p>Recent post from rendered path</p>
      <time datetime="{recent_iso}"></time>
    </article>
    """
    with (
        patch("panopto.collectors.instagram._iter_pages", return_value=[static_html]),
        patch("panopto.collectors.instagram._iter_rendered_pages", return_value=[browser_html]),
    ):
        rows = collect_instagram_posts("aoc", "14 days", request_delay_seconds=0, browser_fallback=True)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "new1"


def test_collect_instagram_uses_official_fallback_when_aggregator_paths_empty():
    html = """
    <article>
      <a href="/p/newer1/">open</a>
      <img src="https://cdn.example.com/newer.jpg" />
    </article>
    """
    with (
        patch("panopto.collectors.instagram._iter_pages", return_value=[]),
        patch("panopto.collectors.instagram._iter_rendered_pages", return_value=[]),
        patch("panopto.collectors.instagram._iter_official_rendered_pages", return_value=[html]),
    ):
        rows = collect_instagram_posts("aoc", "30 days", request_delay_seconds=0, browser_fallback=True)

    assert len(rows) == 1
    assert rows[0]["source_url"] == "https://www.instagram.com/p/newer1/"


def test_collect_instagram_raises_blocked_error_on_challenge_pages():
    blocked_html = "<html><body>Just a moment... /cdn-cgi/challenge-platform/ cloudflare</body></html>"
    with (
        patch("panopto.collectors.instagram._iter_pages", return_value=[blocked_html]),
        patch("panopto.collectors.instagram.requests.Session.get") as mock_get,
    ):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = blocked_html
        try:
            collect_instagram_posts("aoc", "30 days", request_delay_seconds=0, browser_fallback=False)
        except SourceAccessBlockedError as exc:
            assert exc.platform == "instagram"
            assert exc.username == "aoc"
        else:
            raise AssertionError("Expected SourceAccessBlockedError on challenge page")


def test_extract_posts_from_html_fallback_reads_links_from_script_payload():
    html = """
    <html><body>
      <script>
        window.__DATA__ = {"items":[{"url":"https://www.instagram.com/reel/xyz123/"}]};
      </script>
    </body></html>
    """
    posts = _extract_posts_from_html("aoc", html, now_utc=datetime(2026, 2, 12, tzinfo=timezone.utc))
    assert len(posts) == 1
    assert posts[0]["post_id"] == "xyz123"
    assert posts[0]["source_url"] == "https://www.instagram.com/reel/xyz123/"


def test_extract_posts_from_html_fallback_reads_shortcode_payload_without_links():
    html = """
    <html><body>
      <script>
        window.__DATA__ = {"edge_media_to_caption":{"shortcode":"zzTop999"}};
      </script>
    </body></html>
    """
    posts = _extract_posts_from_html("aoc", html, now_utc=datetime(2026, 2, 12, tzinfo=timezone.utc))
    assert len(posts) == 1
    assert posts[0]["post_id"] == "zzTop999"
    assert posts[0]["source_url"] == "https://www.instagram.com/p/zzTop999/"


def test_iter_pages_tries_detail_url_variants():
    class _Response:
        def __init__(self, status_code: int, text: str):
            self.status_code = status_code
            self.text = text

    class _Session:
        def __init__(self):
            self.calls = []

        def get(self, url, timeout=20):
            self.calls.append(url)
            if "detail/?username" in url:
                return _Response(200, "<html>ok</html>")
            return _Response(404, "")

    session = _Session()
    pages = list(_iter_pages(session, "aoc", max_pages=1, request_delay_seconds=0, timeout=20))

    assert pages == ["<html>ok</html>"]
    assert any("detail/?username=aoc" in call for call in session.calls)


def test_dismiss_browser_overlays_executes_js_and_escape():
    class _Keyboard:
        def __init__(self):
            self.keys = []

        def press(self, key):
            self.keys.append(key)

    class _Page:
        def __init__(self):
            self.scripts = []
            self.keyboard = _Keyboard()

        def evaluate(self, script):
            self.scripts.append(script)
            return None

    page = _Page()
    _dismiss_browser_overlays(page)

    assert page.scripts
    assert "closeTokens" in page.scripts[0]
    assert page.keyboard.keys == ["Escape"]


def test_safe_page_content_retries_transient_errors():
    class _Page:
        def __init__(self):
            self.calls = 0

        def content(self):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("navigating")
            return "<html>ok</html>"

        def wait_for_timeout(self, _ms):
            return None

    page = _Page()
    assert _safe_page_content(page) == "<html>ok</html>"


def test_safe_scroll_helpers_retry_transient_navigation_errors():
    class _Page:
        def __init__(self):
            self.eval_calls = 0
            self.scrolled = False

        def evaluate(self, expression):
            self.eval_calls += 1
            if self.eval_calls == 1:
                raise RuntimeError("context destroyed")
            if "scrollHeight" in expression and "window.scrollTo" not in expression:
                return 900
            if "window.scrollTo" in expression:
                self.scrolled = True
                return None
            return None

        def wait_for_timeout(self, _ms):
            return None

    page = _Page()
    assert _safe_scroll_height(page) == 900
    _safe_scroll_to_bottom(page)
    assert page.scrolled is True
