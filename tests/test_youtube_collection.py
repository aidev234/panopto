from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from panopto.collectors.youtube import (
    _extract_count,
    _parse_relative_timestamp,
    collect_youtube_posts,
    normalize_youtube_username,
    youtube_videos_url,
)


class _FakeResponse:
    def __init__(self, text: str = "", status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")


class _FakeSession:
    def __init__(self, html: str, status_code: int = 200):
        self._html = html
        self._status_code = status_code
        self.headers = {}
        self.proxies = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, url, timeout=20):
        return _FakeResponse(text=self._html, status_code=self._status_code)


def test_youtube_videos_url_formats_handle_to_uppercase_videos_path():
    assert youtube_videos_url("aoc") == "https://www.youtube.com/@AOC/videos"


def test_youtube_videos_url_strips_at_prefix():
    assert youtube_videos_url("@aoc") == "https://www.youtube.com/@AOC/videos"


def test_youtube_videos_url_accepts_full_profile_url():
    assert (
        youtube_videos_url("https://www.youtube.com/@AOC/videos")
        == "https://www.youtube.com/@AOC/videos"
    )


def test_youtube_videos_url_requires_username():
    with pytest.raises(ValueError, match="username is required"):
        youtube_videos_url("  ")


def test_normalize_youtube_username_accepts_profile_url():
    assert normalize_youtube_username("https://www.youtube.com/@AOC/videos") == "AOC"


def test_collect_youtube_posts_parses_initial_data_and_filters_window():
    now = datetime.now(timezone.utc)
    recent = "1 day ago"
    old = "2 years ago"

    html = f"""
    <script>
      var ytInitialData = {{
        "contents": {{
          "twoColumnBrowseResultsRenderer": {{
            "tabs": [
              {{
                "tabRenderer": {{
                  "content": {{
                    "richGridRenderer": {{
                      "contents": [
                        {{
                          "richItemRenderer": {{
                            "content": {{
                              "videoRenderer": {{
                                "videoId": "vid1",
                                "title": {{"runs": [{{"text": "Recent upload"}}]}},
                                "publishedTimeText": {{"simpleText": "{recent}"}},
                                "viewCountText": {{"simpleText": "12K views"}},
                                "thumbnail": {{"thumbnails": [{{"url": "https://i.ytimg.com/vi/vid1/hqdefault.jpg"}}]}}
                              }}
                            }}
                          }}
                        }},
                        {{
                          "richItemRenderer": {{
                            "content": {{
                              "videoRenderer": {{
                                "videoId": "old1",
                                "title": {{"runs": [{{"text": "Old upload"}}]}},
                                "publishedTimeText": {{"simpleText": "{old}"}},
                                "viewCountText": {{"simpleText": "200 views"}},
                                "thumbnail": {{"thumbnails": [{{"url": "https://i.ytimg.com/vi/old1/hqdefault.jpg"}}]}}
                              }}
                            }}
                          }}
                        }}
                      ]
                    }}
                  }}
                }}
              }}
            ]
          }}
        }}
      }};
    </script>
    """

    fake_session = _FakeSession(html=html, status_code=200)
    with patch("panopto.collectors.youtube.requests.Session", return_value=fake_session):
        rows = collect_youtube_posts(
            "https://www.youtube.com/@AOC/videos",
            "30 days",
            max_pages=1,
        )

    assert len(rows) == 1
    row = rows[0]
    assert row["post_id"] == "vid1"
    assert row["platform"] == "YouTube"
    assert row["source_url"] == "https://www.youtube.com/watch?v=vid1"
    assert row["metadata"]["embed_url"] == "https://www.youtube.com/embed/vid1"
    assert row["metadata"]["views"] == 12000


def test_extract_count_supports_billions_suffix():
    assert _extract_count("1.2B views") == 1_200_000_000


def test_parse_relative_timestamp_supports_common_abbreviations():
    now = datetime.now(timezone.utc)
    assert _parse_relative_timestamp("3 hr ago", now_utc=now) is not None
    assert _parse_relative_timestamp("2 hrs ago", now_utc=now) is not None
    assert _parse_relative_timestamp("4 mos ago", now_utc=now) is not None


def test_collect_youtube_posts_rejects_unsupported_max_pages():
    with pytest.raises(ValueError, match="max_pages=1"):
        collect_youtube_posts("AOC", "30 days", max_pages=2)
