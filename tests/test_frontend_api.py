from __future__ import annotations

import json
import sqlite3
from io import BytesIO
from unittest.mock import patch

from frontend.server import PostExplorerHandler, query_posts
from panopto.errors import UsernameNotFoundError
from panopto.post_query import parse_day


def _seed_db(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                topic_id INTEGER,
                theme_label TEXT,
                theme_keywords TEXT,
                theme_tag TEXT,
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO twitter_posts (username, content, timestamp, post_type, source_url, theme_label, theme_tag, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("alice", "I live in New York", "2024-01-10T00:00:00", "post", "https://x.com/alice/status/1", "city / home", "theme:city-home", "2024-01-10T00:00:00"),
                ("bob", "Moving to Boston", "2024-01-01T00:00:00", "reply", "https://x.com/bob/status/2", "relocation", "theme:relocation", "2024-01-01T00:00:00"),
                ("carol", "New York trip", "2024-01-05T00:00:00", "repost", "https://x.com/carol/status/3", "city / travel", "theme:city-travel", "2024-01-05T00:00:00"),
            ],
        )
        conn.commit()


def test_posts_sorted_and_filterable(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    payload = query_posts(sort_order="oldest", db_path=db_path)

    assert payload["count"] == 3
    assert payload["posts"][0]["username"] == "bob"


def test_boolean_nested_search(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    query = '"New York" AND ("live in" OR "moving to")'
    payload = query_posts(query=query, db_path=db_path)

    assert payload["count"] == 1
    assert payload["posts"][0]["username"] == "alice"


def test_username_query_with_at_prefix(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    payload = query_posts(query="@alice", db_path=db_path)

    assert payload["count"] == 1
    assert payload["posts"][0]["username"] == "alice"


def test_content_cleaning_and_display_name(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (username, content, timestamp, collected_at) VALUES (?, ?, ?, ?)",
            (
                "sama",
                "Sam Altman @sama · 1d We shipped an update today. 2.1K 343 8.9K 1.8M Screenshot Share",
                "2026-02-12T18:15:54+00:00",
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(query="update", db_path=db_path)

    assert payload["count"] == 1
    assert payload["posts"][0]["display_name"] == "Sam Altman"
    assert payload["posts"][0]["content"] == "We shipped an update today"


def test_content_cleaning_strips_view_profile_fragment(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (username, content, timestamp, collected_at) VALUES (?, ?, ?, ?)",
            (
                "elonmusk",
                "Elon Musk @elonmusk · 9h View Profile Starlink now at 10 million users",
                "2026-02-12T18:15:54+00:00",
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(query="starlink", db_path=db_path)
    assert payload["count"] == 1
    assert payload["posts"][0]["content"] == "Starlink now at 10 million users"


def test_include_exclude_tag_filters(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    include_reply = query_posts(db_path=db_path, include_tags={"reply"})
    exclude_repost = query_posts(db_path=db_path, exclude_tags={"repost"})

    assert include_reply["count"] == 1
    assert include_reply["posts"][0]["post_type"] == "reply"
    assert exclude_repost["count"] == 2


def test_query_posts_date_range_filter(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    payload = query_posts(db_path=db_path, start_date="2024-01-06", end_date="2024-01-10")

    assert payload["count"] == 1
    assert payload["posts"][0]["username"] == "alice"


def test_theme_aggregates_and_theme_tag_filter(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    payload = query_posts(db_path=db_path)
    theme_filtered = query_posts(db_path=db_path, include_tags={"theme:city-home", "theme:relocation"})

    assert payload["themes"]
    assert payload["themes"][0]["count"] >= 1
    assert theme_filtered["count"] == 2


def test_theme_aggregates_exclude_temporal_only_labels(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO twitter_posts (username, content, timestamp, post_type, source_url, theme_label, theme_tag, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "dave",
                "Temporal label test",
                "2024-01-06T00:00:00",
                "post",
                "https://x.com/dave/status/4",
                "7d / 3d",
                "theme:7d-3d",
                "2024-01-06T00:00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path)
    theme_tags = {theme["tag"] for theme in payload["themes"]}

    assert payload["count"] == 4
    assert "theme:7d-3d" not in theme_tags


def test_query_posts_supports_tiktok_platform_and_video_metadata(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, source_url, platform, raw_metadata, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "123",
                "aoc",
                "Clip caption",
                "2026-02-12T18:15:54+00:00",
                "post",
                "https://www.tikvib.com/profile/aoc/video/123",
                "TikTok",
                json.dumps({"video_url": "https://cdn.example.com/clip.mp4"}),
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path, include_tags={"tiktok"})

    assert payload["count"] == 1
    assert payload["posts"][0]["platform"] == "TikTok"
    assert payload["posts"][0]["metadata"]["video_url"] == "https://cdn.example.com/clip.mp4"


def test_query_posts_supports_bluesky_platform_tag(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, source_url, platform, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "b1",
                "aoc",
                "Bluesky post",
                "2026-02-12T18:15:54+00:00",
                "post",
                "https://bsky.app/profile/aoc.bsky.social/post/b1",
                "Bluesky",
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path, include_tags={"bluesky"})

    assert payload["count"] == 1
    assert payload["posts"][0]["platform"] == "Bluesky"


def test_query_posts_supports_youtube_platform_tag(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, source_url, platform, raw_metadata, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "y1",
                "AOC",
                "Recent upload",
                "2026-02-12T18:15:54+00:00",
                "post",
                "https://www.youtube.com/watch?v=y1",
                "YouTube",
                json.dumps({"embed_url": "https://www.youtube.com/embed/y1"}),
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path, include_tags={"youtube"})

    assert payload["count"] == 1
    assert payload["posts"][0]["platform"] == "YouTube"
    assert payload["posts"][0]["metadata"]["embed_url"] == "https://www.youtube.com/embed/y1"


def test_query_posts_extracts_ner_entities_and_location_tags(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, platform, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "n1",
                "alice",
                "Alexandria Ocasio-Cortez visited New York with Sam Altman",
                "2026-02-12T18:15:54+00:00",
                "post",
                "Twitter",
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path)

    assert payload["count"] == 1
    post = payload["posts"][0]
    assert any(entity.get("type") == "location" and entity.get("text") == "New York" for entity in post["entities"])
    assert "ner:location" in post["tags"]
    assert "loc:new-york" in post["tags"]


def test_query_posts_extracts_threat_and_selector_signals(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                post_type TEXT NOT NULL DEFAULT 'post',
                source_url TEXT,
                referenced_username TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, platform, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "sig1",
                "demo",
                "I am going to buy a gun and my email is analyst@example.com call 415-555-1212",
                "2026-02-12T18:15:54+00:00",
                "post",
                "Twitter",
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path)
    post = payload["posts"][0]

    threat_terms = [item.lower() for item in post["threat_matches"]]
    assert "buy" in threat_terms or "going to" in threat_terms
    assert "gun" in threat_terms
    assert "Possible Indicators of Capability" in post["threat_categories"]
    assert "analyst@example.com" in [item.lower() for item in post["selector_matches"]]
    assert "selector:email" in post["tags"]
    assert "threat:indicator" in post["tags"]


def test_collect_endpoint_rejects_invalid_dates():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"username": "sama", "start_date": "2026-02-20", "end_date": "2026-02-10"}).encode(
        "utf-8"
    )
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert responses and responses[0] == 400
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "invalid_request"


def test_collect_endpoint_handles_blank_content_length_header():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": ""}
    handler.rfile = BytesIO(b"")
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert responses and responses[0] == 400
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "invalid_request"


def test_parse_day_accepts_common_formats():
    assert str(parse_day("2026-02-15")) == "2026-02-15"
    assert str(parse_day("02/15/2026")) == "2026-02-15"
    assert str(parse_day("02-15-2026")) == "2026-02-15"


def test_collect_endpoint_accepts_date_range_in_start_field():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "targets": [{"platform": "twitter", "username": "AKayWyatt"}],
            "start_date": "01/08/2026-02/15/2026",
            "end_date": "",
        }
    ).encode("utf-8")
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    errors = []
    responses = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.collect_for_targets",
        return_value={"count": 0, "posts": [], "themes": [], "collected": 0, "inserted": 0},
    ):
        handler.do_POST()

    assert not errors
    assert responses and responses[0] == 200


def test_collect_endpoint_internal_value_error_returns_500():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "targets": [{"platform": "twitter", "username": "AKayWyatt"}],
            "start_date": "2026-01-08",
            "end_date": "2026-02-15",
        }
    ).encode("utf-8")
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.collect_for_targets", side_effect=ValueError("int parse failure")):
        handler.do_POST()

    assert responses and responses[0] == 500
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "internal_error"


def test_collect_endpoint_username_not_found_returns_404():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "targets": [{"platform": "twitter", "username": "missing_user"}],
            "start_date": "2026-01-08",
            "end_date": "2026-02-15",
        }
    ).encode("utf-8")
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.collect_for_targets",
        side_effect=UsernameNotFoundError(platform="twitter", username="missing_user"),
    ):
        handler.do_POST()

    assert responses and responses[0] == 404
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "username_not_found"
