from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import panopto.collectors.tiktok as tiktok_collection


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
