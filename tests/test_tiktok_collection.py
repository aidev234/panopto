from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import panopto.collectors.tiktok as tiktok_collection
from panopto.collectors.apify import ApifyRequestError
from panopto.errors import SourceUnavailableError


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
    dataset = [
        {"id": "same", "text": "Short", "createTimeISO": recent_iso, "webVideoUrl": "https://www.tiktok.com/@aoc/video/same"},
        {"id": "same", "text": "Longer canonical caption", "createTimeISO": recent_iso, "webVideoUrl": "https://www.tiktok.com/@aoc/video/same"},
        {"id": "old", "text": "Old clip", "createTimeISO": old_iso, "webVideoUrl": "https://www.tiktok.com/@aoc/video/old"},
    ]

    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "1 week", max_pages=2, request_delay_seconds=0)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "same"
    assert rows[0]["content"] == "Longer canonical caption"
    assert rows[0]["source_url"] == "https://www.tiktok.com/@aoc/video/same"


def test_parse_collection_window_rejects_invalid_format():
    try:
        tiktok_collection.collect_tiktok_posts("aoc", "yesterday")
    except ValueError as exc:
        assert "Unsupported collection_window format" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_collect_tiktok_posts_returns_rows_from_apify_dataset():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "id": "fallback123",
            "text": "Recovered from actor output",
            "createTimeISO": (now - timedelta(days=1)).isoformat(),
            "webVideoUrl": "https://www.tiktok.com/@aoc/video/fallback123",
        }
    ]
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "1 week", max_pages=1, request_delay_seconds=0, browser_fallback=True)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "fallback123"
    assert rows[0]["content"] == "Recovered from actor output"


def test_collect_tiktok_posts_surfaces_apify_request_errors():
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", side_effect=ApifyRequestError("blocked")):
        try:
            tiktok_collection.collect_tiktok_posts("aoc", "1 week", max_pages=1, request_delay_seconds=0, browser_fallback=True)
        except SourceUnavailableError as exc:
            assert exc.platform == "tiktok"
            assert "blocked" in str(exc)
        else:
            raise AssertionError("Expected SourceUnavailableError")


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
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=[]):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "1 week", max_pages=1, request_delay_seconds=0, browser_fallback=False)
    assert rows == []


def test_collect_tiktok_posts_maps_direct_video_urls_from_apify():
    dataset = [
        {
            "id": "123456",
            "text": "(video)",
            "createTimeISO": "2026-02-10T00:00:00+00:00",
            "webVideoUrl": "https://www.tiktok.com/@aoc/video/123456",
        }
    ]
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts(
            "aoc",
            "30 days",
            max_pages=1,
            request_delay_seconds=0,
            browser_fallback=True,
            now_utc=datetime(2026, 3, 12, tzinfo=timezone.utc),
        )
    assert len(rows) == 1
    assert rows[0]["post_id"] == "123456"


def test_inclusive_cutoff_keeps_boundary_day():
    now = datetime(2026, 3, 12, 18, 30, tzinfo=timezone.utc)
    cutoff = tiktok_collection._inclusive_cutoff(now, "30 days")

    assert cutoff.isoformat() == "2026-02-10T00:00:00+00:00"


def test_collect_tiktok_posts_raises_unavailable_when_apify_not_configured():
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", side_effect=tiktok_collection.ApifyConfigurationError("missing token")):
        try:
            tiktok_collection.collect_tiktok_posts("aoc", "30 days", max_pages=1, request_delay_seconds=0, browser_fallback=False)
        except SourceUnavailableError as exc:
            assert exc.platform == "tiktok"
            assert exc.username == "aoc"
        else:
            raise AssertionError("Expected SourceUnavailableError when Apify is not configured")


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


def test_collect_tiktok_posts_uses_apify_actor_and_maps_rich_video_fields():
    dataset = [
        {
            "id": "7361111111111111111",
            "text": "Clip caption",
            "createTimeISO": "2026-02-20T12:10:00+00:00",
            "webVideoUrl": "https://www.tiktok.com/@aoc/video/7361111111111111111",
            "diggCount": 77,
            "commentCount": 12,
            "playCount": 987,
            "shareCount": 15,
            "collectCount": 4,
            "locationCreated": "US",
            "isAd": True,
            "musicMeta": {"musicName": "Track 1", "musicAuthor": "Artist 1"},
            "videoMeta": {"height": 1920, "width": 1080, "duration": 19},
            "video": {"downloadAddr": "https://v16.tiktokcdn.com/clip.mp4", "cover": "https://p16.tiktokcdn.com/cover.jpg"},
            "authorMeta.name": "aoc",
            "authorMeta.nickName": "AOC",
            "authorMeta.verified": True,
            "authorMeta.bioLink.link": "https://example.org",
            "authorMeta.fans": 1010,
            "authorMeta.heart": 2020,
            "authorMeta.video": 303,
            "authorMeta.digg": 4040,
        }
    ]
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "30 days", browser_fallback=False)

    assert len(rows) == 1
    row = rows[0]
    assert row["post_id"] == "7361111111111111111"
    assert row["content"] == "Clip caption"
    assert row["likes"] == 77
    assert row["replies"] == 12
    assert row["source_url"] == "https://www.tiktok.com/@aoc/video/7361111111111111111"
    assert row["metadata"]["country_of_creation"] == "US"
    assert row["metadata"]["is_ad"] is True
    assert row["metadata"]["plays"] == 987
    assert row["metadata"]["shares"] == 15
    assert row["metadata"]["saves"] == 4
    assert row["metadata"]["video_url"] == "https://v16.tiktokcdn.com/clip.mp4"
    assert row["metadata"]["media"][0]["type"] == "video"
    assert row["metadata"]["media"][0]["url"] == "https://v16.tiktokcdn.com/clip.mp4"
    assert row["metadata"]["media"][0]["thumbnail_url"] == "https://p16.tiktokcdn.com/cover.jpg"
    assert row["metadata"]["image_urls"] == ["https://p16.tiktokcdn.com/cover.jpg"]
    assert row["metadata"]["video_format"]["duration"] == 19
    assert row["metadata"]["music"]["musicName"] == "Track 1"
    assert row["metadata"]["author_name"] == "aoc"
    assert row["metadata"]["author_nickname"] == "AOC"
    assert row["metadata"]["author_verified"] is True
    assert row["metadata"]["link_in_bio"] == "https://example.org"
    assert row["metadata"]["author_fans"] == 1010
    assert row["metadata"]["author_hearts"] == 2020
    assert row["metadata"]["author_videos"] == 303
    assert row["metadata"]["author_likes"] == 4040


def test_collect_tiktok_posts_raises_unavailable_when_apify_fails():
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", side_effect=ApifyRequestError("boom")):
        try:
            tiktok_collection.collect_tiktok_posts("aoc", "30 days", request_delay_seconds=0, browser_fallback=False)
        except SourceUnavailableError as exc:
            assert exc.platform == "tiktok"
            assert "boom" in str(exc)
        else:
            raise AssertionError("Expected SourceUnavailableError")


def test_collect_tiktok_posts_maps_apify_profile_with_nested_videos():
    dataset = [
        {
            "authorMeta.name": "aoc",
            "authorMeta.nickName": "AOC",
            "authorMeta.verified": True,
            "authorMeta.bioLink.link": "https://example.org",
            "authorMeta.fans": 1010,
            "authorMeta.heart": 2020,
            "authorMeta.video": 303,
            "authorMeta.digg": 4040,
            "videos": [
                {
                    "id": "7362222222222222222",
                    "text": "Nested clip",
                    "createTimeISO": "2026-02-22T02:10:00+00:00",
                    "webVideoUrl": "https://www.tiktok.com/@aoc/video/7362222222222222222",
                    "playCount": 200,
                    "diggCount": 20,
                    "commentCount": 2,
                }
            ],
        }
    ]
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "30 days", browser_fallback=False)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "7362222222222222222"
    assert rows[0]["content"] == "Nested clip"
    assert rows[0]["metadata"]["author_name"] == "aoc"


def test_collect_tiktok_posts_maps_apify_item_list_shape():
    dataset = [
        {
            "authorMeta.name": "aoc",
            "itemList": [
                {
                    "id": "7363333333333333333",
                    "text": "ItemList clip",
                    "createTime": 1769451494,
                    "webVideoUrl": "https://www.tiktok.com/@aoc/video/7363333333333333333",
                }
            ],
        }
    ]
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=dataset):
        rows = tiktok_collection.collect_tiktok_posts("aoc", "365 days", browser_fallback=False)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "7363333333333333333"
    assert rows[0]["content"] == "ItemList clip"


def test_collect_tiktok_posts_does_not_fallback_when_apify_configured_and_empty():
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", return_value=[]):
        with patch("panopto.collectors.tiktok._iter_pages") as iter_pages_mock:
            rows = tiktok_collection.collect_tiktok_posts("aoc", "30 days", browser_fallback=True)

    assert rows == []
    iter_pages_mock.assert_not_called()


def test_collect_tiktok_posts_surfaces_apify_errors_when_configured():
    with patch("panopto.collectors.tiktok.run_actor_sync_get_items", side_effect=ApifyRequestError("boom")):
        try:
            tiktok_collection.collect_tiktok_posts("aoc", "30 days", browser_fallback=True)
        except SourceUnavailableError as exc:
            assert exc.platform == "tiktok"
            assert "boom" in str(exc)
        else:
            raise AssertionError("expected SourceUnavailableError")
