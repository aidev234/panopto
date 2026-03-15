from __future__ import annotations

import json
import re
import sqlite3
import sys
import types
from io import BytesIO
from unittest.mock import patch

from frontend.server import (
    PostExplorerHandler,
    _build_case_notes_pdf_fallback,
    _build_case_notes_pdf_stylized,
    _extract_mermaid_block,
    _image_source_to_data_uri,
    _load_architecture_markdown,
    _render_architecture_page_html,
    query_posts,
)
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
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO twitter_posts (username, content, timestamp, post_type, source_url, collected_at) VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("alice", "I live in New York", "2024-01-10T00:00:00", "post", "https://x.com/alice/status/1", "2024-01-10T00:00:00"),
                ("bob", "Moving to Boston", "2024-01-01T00:00:00", "reply", "https://x.com/bob/status/2", "2024-01-01T00:00:00"),
                ("carol", "New York trip", "2024-01-05T00:00:00", "repost", "https://x.com/carol/status/3", "2024-01-05T00:00:00"),
            ],
        )
        conn.commit()


def test_posts_sorted_and_filterable(tmp_path):
    db_path = tmp_path / "osint_data.db"
    _seed_db(db_path)

    payload = query_posts(sort_order="oldest", db_path=db_path)

    assert payload["count"] == 3
    assert payload["posts"][0]["username"] == "bob"


def test_query_posts_does_not_dedupe_across_platforms(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                case_id TEXT,
                platform TEXT NOT NULL DEFAULT 'Twitter',
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                post_type TEXT NOT NULL DEFAULT 'post',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO twitter_posts (source_post_id, platform, username, content, timestamp, collected_at) VALUES (?, ?, ?, ?, ?, ?)",
            [
                ("tw-1", "Twitter", "shared_user", "same text", "2026-02-12T18:15:54+00:00", "2026-02-12T18:16:00+00:00"),
                ("rd-1", "Reddit", "shared_user", "same text", "2026-02-12T18:15:54+00:00", "2026-02-12T18:16:00+00:00"),
            ],
        )
        conn.commit()

    payload = query_posts(db_path=db_path)

    assert payload["count"] == 2
    assert sorted(post["platform"] for post in payload["posts"]) == ["Reddit", "Twitter"]


def test_query_posts_keeps_unparseable_timestamps_when_date_filter_set(tmp_path):
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
                post_type TEXT NOT NULL DEFAULT 'post',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, collected_at) VALUES (?, ?, ?, ?, ?)",
            ("bad-ts", "alice", "undated post", "not-a-date", "2026-02-12T18:16:00+00:00"),
        )
        conn.commit()

    payload = query_posts(db_path=db_path, start_date="2026-02-01", end_date="2026-02-28")
    assert payload["count"] == 1
    assert payload["posts"][0]["post_id"] == "bad-ts"


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


def test_query_posts_prioritizes_direct_search_matches_before_weaker_metadata_matches(tmp_path):
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
                post_type TEXT NOT NULL DEFAULT 'post',
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, raw_metadata, collected_at) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    "newer-entity",
                    "alice",
                    "Heading home after work",
                    "2026-02-12T18:15:54+00:00",
                    json.dumps({"llm_assessment": {"underlying_theme": "Boston travel planning", "tagged_primary": ["planning"]}}),
                    "2026-02-12T18:16:00+00:00",
                ),
                (
                    "older-content",
                    "bob",
                    "Boston deployment moved up again",
                    "2026-02-01T08:00:00+00:00",
                    json.dumps({}),
                    "2026-02-01T08:01:00+00:00",
                ),
            ],
        )
        conn.commit()

    payload = query_posts(query="boston", sort_order="newest", db_path=db_path)

    assert payload["count"] == 2
    assert [post["post_id"] for post in payload["posts"]] == ["older-content", "newer-entity"]


def test_architecture_markdown_includes_mermaid_diagram():
    markdown_text = _load_architecture_markdown()
    mermaid = _extract_mermaid_block(markdown_text)

    assert "# PANOPTO Architecture Diagram" in markdown_text
    assert "flowchart TB" in mermaid
    assert "frontend/server.py" in mermaid


def test_architecture_page_embeds_svg_and_mermaid_source():
    html = _render_architecture_page_html().decode("utf-8")

    assert "<title>PANOPTO Architecture</title>" in html
    assert 'src="/architecture-diagram.svg"' in html
    assert "/docs/architecture-diagram.md" in html
    assert "flowchart TB" in html


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


def test_query_posts_supports_instagram_platform_tag(tmp_path):
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
                "ig1",
                "aoc",
                "Instagram post",
                "2026-02-12T18:15:54+00:00",
                "post",
                "https://www.instagram.com/p/ig1/",
                "Instagram",
                json.dumps({"image_urls": ["https://cdn.example.com/ig1.jpg"]}),
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path, include_tags={"instagram"})

    assert payload["count"] == 1
    assert payload["posts"][0]["platform"] == "Instagram"
    assert payload["posts"][0]["metadata"]["image_urls"] == ["https://cdn.example.com/ig1.jpg"]


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


def test_query_posts_extracts_washington_dc_location_tag(tmp_path):
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
                "dc1",
                "alice",
                "Heading to Washington, DC for meetings near the National Mall.",
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
    assert "ner:location" in post["tags"]
    assert "loc:washington-dc" in post["tags"]
    assert "loc:washington" not in post["tags"]
    assert any(entity.get("type") == "location" and entity.get("text") == "Washington DC" for entity in post["entities"])
    assert not any(entity.get("type") == "location" and entity.get("text") == "Washington" for entity in post["entities"])


def test_query_posts_extracts_ottawa_location_tag(tmp_path):
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
                "ott1",
                "alice",
                "Primary location: Ottawa, Canada.",
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
    assert "ner:location" in post["tags"]
    assert "loc:ottawa" in post["tags"]
    assert any(entity.get("type") == "location" and entity.get("text") == "Ottawa" for entity in post["entities"])


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
    assert "Possible Indicators of Capability" in post["threat_signal_categories"]
    assert post["threat_categories"] == []
    assert "analyst@example.com" in [item.lower() for item in post["selector_matches"]]
    assert "selector:email" in post["tags"]
    assert "threat:indicator" in post["tags"]


def test_query_posts_exposes_llm_assessment_fields(tmp_path):
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
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, platform, raw_metadata, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "llm1",
                "demo",
                "I am forced to act, it is carved into me",
                "2026-02-12T18:15:54+00:00",
                "post",
                "Twitter",
                json.dumps(
                    {
                        "llm_assessment": {
                            "tagged_primary": ["Last Resort"],
                            "tagged_secondary": ["Negative Emotional State", "Violent Ideation"],
                            "underlying_theme": "Perceived compulsion/destiny to act violently",
                            "rationale": "Author states a compelled pathway toward violence.",
                        }
                    }
                ),
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path)
    assert payload["count"] == 1
    post = payload["posts"][0]
    assert post["llm_primary_warning_behaviours"] == ["Last Resort"]
    assert "Negative Emotional State" in post["llm_secondary_risk_factors"]
    assert post["llm_underlying_theme"] == "Perceived compulsion/destiny to act violently"
    assert post["llm_rationale"] == "Author states a compelled pathway toward violence."
    assert "llm:primary-warning" in post["tags"]
    assert "llm:secondary-risk" in post["tags"]


def test_query_posts_clears_underlying_theme_without_warning_behaviours(tmp_path):
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
            "INSERT INTO twitter_posts (source_post_id, username, content, timestamp, post_type, platform, raw_metadata, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "llm-theme-only",
                "demo",
                "Just routine life updates.",
                "2026-02-12T18:15:54+00:00",
                "post",
                "Twitter",
                json.dumps(
                    {
                        "llm_assessment": {
                            "tagged_primary": [],
                            "tagged_secondary": [],
                            "underlying_theme": "Routine commentary",
                            "rationale": "none",
                        }
                    }
                ),
                "2026-02-12T18:16:00+00:00",
            ),
        )
        conn.commit()

    payload = query_posts(db_path=db_path)
    assert payload["count"] == 1
    post = payload["posts"][0]
    assert post["llm_primary_warning_behaviours"] == []
    assert post["llm_secondary_risk_factors"] == []
    assert post["llm_underlying_theme"] == ""


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


def test_collect_endpoint_rejects_non_object_json_body():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(["not", "an", "object"]).encode("utf-8")
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert errors
    assert errors[0][0] == 400


def test_collect_endpoint_rejects_non_utf8_json_body():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = b"\xff\xfe\x00\x00"
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert errors
    assert errors[0][0] == 400
    assert errors[0][1] == "invalid json body"


def test_collect_endpoint_rejects_invalid_content_length_header():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": "abc"}
    handler.rfile = BytesIO(b"{}")
    handler.wfile = BytesIO()

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert errors
    assert errors[0][0] == 400
    assert errors[0][1] == "invalid content-length header"


def test_collect_endpoint_rejects_oversized_json_body():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str((2 * 1024 * 1024) + 1)}
    handler.rfile = BytesIO(b"{}")
    handler.wfile = BytesIO()

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert errors
    assert errors[0][0] == 413
    assert errors[0][1] == "json body too large"


def test_collect_endpoint_rejects_incomplete_body():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = b"{}"
    handler.path = "/api/collect"
    handler.headers = {"Content-Length": str(len(body) + 4)}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert errors
    assert errors[0][0] == 400
    assert errors[0][1] == "incomplete request body"


def test_session_end_rejects_invalid_optional_json_body():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/session/end"
    handler.headers = {"Content-Length": "abc"}
    handler.rfile = BytesIO(b"{}")
    handler.wfile = BytesIO()
    handler.server = types.SimpleNamespace(shutdown=lambda: None)

    errors = []

    def _send_error(code, message=None):
        errors.append((code, message))

    handler.send_error = _send_error
    handler.send_response = lambda code: None
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with (
        patch("frontend.server.clear_posts") as clear_posts,
        patch("frontend.server.save_config") as save_config,
    ):
        handler.do_POST()

    assert errors
    assert errors[0] == (400, "invalid content-length header")
    clear_posts.assert_not_called()
    save_config.assert_not_called()


def test_case_notes_pdf_fallback_ignores_invalid_profile_rows():
    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "known_profiles": ["not-a-dict", {"site": "Twitter/X", "url": "https://x.com/sama"}],
        },
    }

    pdf_bytes = _build_case_notes_pdf_fallback(case_row, posts=[])

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert re.search(rb"Pg 1 of \d+", pdf_bytes)


def test_case_notes_pdf_fallback_only_includes_major_profiles():
    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "known_profiles": [
                {"site": "Twitter/X", "url": "https://x.com/alpha"},
                {"site": "Instagram", "url": "https://www.instagram.com/alpha/"},
                {"site": "TikTok", "url": "https://www.tiktok.com/@alpha"},
            ],
        },
    }

    pdf_bytes = _build_case_notes_pdf_fallback(case_row, posts=[])

    assert b"Major Profiles" in pdf_bytes
    assert b"https://x.com/alpha" not in pdf_bytes
    assert b"https://www.instagram.com/alpha/" in pdf_bytes
    assert b"https://www.tiktok.com/@alpha" in pdf_bytes


def test_case_notes_pdf_fallback_appends_digital_footprint_section():
    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "recon_snapshot": {
                "payload": {
                    "results": [
                        {
                            "selector_type": "email",
                            "selector": "alpha@example.com",
                            "site": "twitter",
                            "status": "present",
                            "profile_url": "https://x.com/alpha",
                            "source": "scanner",
                        },
                        {
                            "selector_type": "username",
                            "selector": "alpha",
                            "site": "reddit",
                            "status": "present",
                            "profile_url": "https://reddit.com/user/alpha",
                            "source": "scanner",
                        },
                    ],
                    "person_data_profiles": [
                        {
                            "query_type": "profile",
                            "query_value": "https://www.linkedin.com/in/alpha/",
                            "full_name": "Alpha Person",
                            "location_name": "Boston",
                        }
                    ],
                }
            }
        },
    }

    pdf_bytes = _build_case_notes_pdf_fallback(case_row, posts=[])

    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"Digital Footprint Evidence" in pdf_bytes
    assert b"APPENDIX A" in pdf_bytes
    assert b"Results" in pdf_bytes
    assert b"High Confidence" not in pdf_bytes
    assert b"Medium Confidence" not in pdf_bytes
    assert b"Low Confidence" not in pdf_bytes
    assert b"alpha@example.com" in pdf_bytes
    assert b"username: alpha" in pdf_bytes
    assert b"profile: https://www.linkedin.com/in/alpha/" in pdf_bytes


def test_case_notes_pdf_fallback_respects_report_only_exclusions():
    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "threat_risk_assessment": "This section should be hidden in report output.",
            "report_preferences": {
                "excluded_sections": ["threat_risk_assessment"],
                "excluded_footprint_result_keys": [
                    "recon (scanner)|email|alpha@example.com|status: present | site: twitter | url: https://x.com/alpha"
                ],
            },
            "recon_snapshot": {
                "payload": {
                    "results": [
                        {
                            "selector_type": "email",
                            "selector": "alpha@example.com",
                            "site": "twitter",
                            "status": "present",
                            "profile_url": "https://x.com/alpha",
                            "source": "scanner",
                        },
                        {
                            "selector_type": "username",
                            "selector": "alpha",
                            "site": "reddit",
                            "status": "present",
                            "profile_url": "https://reddit.com/user/alpha",
                            "source": "scanner",
                        },
                    ]
                }
            },
        },
    }

    pdf_bytes = _build_case_notes_pdf_fallback(case_row, posts=[])

    assert b"Threat / Risk Assessment" not in pdf_bytes
    assert b"Low Confidence" not in pdf_bytes
    assert b"High Confidence" not in pdf_bytes
    assert b"alpha@example.com" not in pdf_bytes
    assert b"Digital Footprint Evidence" in pdf_bytes
    assert b"Results" in pdf_bytes


def test_case_notes_pdf_fallback_includes_selectors_section():
    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "personal_details": "Details",
            "selector_emails": "alpha@example.com, beta@example.com",
            "selector_phone_numbers": "+12025550199",
            "selector_usernames": "alpha_handle, beta_handle",
        },
    }

    pdf_bytes = _build_case_notes_pdf_fallback(case_row, posts=[])

    assert b"Selectors" in pdf_bytes
    assert b"Emails: alpha@example.com, beta@example.com" in pdf_bytes
    assert b"Phone Numbers: +12025550199" in pdf_bytes
    assert b"User Names: alpha_handle, beta_handle" in pdf_bytes


def test_case_notes_pdf_stylized_interpolates_dynamic_sections():
    captured: dict[str, str] = {}

    class _FakePage:
        def set_content(self, html, wait_until=None):
            captured["html"] = html

        def pdf(self, format="A4", print_background=True):
            return b"%PDF-1.4\n%fake\n"

    class _FakeContext:
        def new_page(self):
            return _FakePage()

        def close(self):
            return None

    class _FakeBrowser:
        def new_context(self, viewport=None):
            return _FakeContext()

        def close(self):
            return None

    class _FakePlaywright:
        chromium = types.SimpleNamespace(launch=lambda headless=True: _FakeBrowser())

    class _FakeSyncPlaywright:
        def __enter__(self):
            return _FakePlaywright()

        def __exit__(self, exc_type, exc, tb):
            return False

    fake_sync_api = types.ModuleType("playwright.sync_api")
    fake_sync_api.sync_playwright = lambda: _FakeSyncPlaywright()
    fake_playwright = types.ModuleType("playwright")
    fake_playwright.sync_api = fake_sync_api

    case_row = {
        "case_name": "Case Alpha",
        "case_notes": {
            "context": "Operational context for interpolation test.",
            "threat_risk_assessment": "Threat summary.",
            "personal_details": "Personal details summary.",
            "known_profiles": [{"site": "Twitter/X", "url": "https://x.com/alpha"}],
            "recon_snapshot": {
                "payload": {
                    "results": [
                        {
                            "selector_type": "email",
                            "selector": "alpha@example.com",
                            "site": "twitter",
                            "status": "present",
                            "profile_url": "https://x.com/alpha",
                            "source": "scanner",
                        }
                    ]
                }
            },
        },
    }

    with patch.dict(sys.modules, {"playwright": fake_playwright, "playwright.sync_api": fake_sync_api}):
        pdf_bytes = _build_case_notes_pdf_stylized(case_row, posts=[])

    assert pdf_bytes.startswith(b"%PDF-1.4")
    html = captured["html"]
    assert "Operational context for interpolation test." in html
    assert "Threat summary." in html
    assert "Personal details summary." in html
    assert "https://x.com/alpha" in html
    assert "alpha@example.com" in html
    assert "Digital Footprint Evidence" in html
    assert "Appendix A" in html
    assert "{_html_escape(context)}" not in html


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
        return_value={"count": 0, "posts": [], "collected": 0, "inserted": 0},
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


def test_session_end_requires_loopback_client():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"shutdown": True}).encode("utf-8")
    handler.path = "/api/session/end"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()
    handler.client_address = ("10.0.0.25", 44444)

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.clear_posts") as clear_mock:
        handler.do_POST()

    clear_mock.assert_not_called()
    assert responses and responses[0] == 403
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "forbidden"


def test_session_end_can_shutdown_without_clearing_data():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"shutdown": False, "clear_data": False}).encode("utf-8")
    handler.path = "/api/session/end"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()
    handler.client_address = ("127.0.0.1", 44444)

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.clear_posts") as clear_mock:
        handler.do_POST()

    clear_mock.assert_not_called()
    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["status"] == "ok"
    assert payload["cleared"] is False
    assert payload["config_cleared"] is False
    assert payload["shutdown"] is False


def test_session_end_wipe_clears_data_and_config():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"shutdown": False, "clear_data": True, "clear_config": True}).encode("utf-8")
    handler.path = "/api/session/end"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()
    handler.client_address = ("127.0.0.1", 44444)

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with (
        patch("frontend.server.clear_posts") as clear_mock,
        patch("frontend.server.save_config") as save_config_mock,
    ):
        handler.do_POST()

    clear_mock.assert_called_once()
    clear_args = clear_mock.call_args.args
    clear_kwargs = clear_mock.call_args.kwargs
    assert clear_args
    assert str(clear_args[0]).endswith("osint_data.db")
    assert clear_kwargs == {"clear_cases": True}
    save_config_mock.assert_called_once()
    kwargs = save_config_mock.call_args.kwargs
    assert kwargs["custom_keyword_list"] == []
    assert kwargs["clear_pdl_api_key"] is True
    assert kwargs["clear_osint_industries_api_key"] is True
    assert kwargs["clear_numverify_api_key"] is True
    assert kwargs["clear_openai_api_key"] is True
    assert kwargs["clear_apify_api_token"] is True

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["status"] == "ok"
    assert payload["cleared"] is True
    assert payload["config_cleared"] is True
    assert payload["shutdown"] is False


def test_recon_endpoint_requires_loopback_client():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"selectors": [{"type": "username", "value": "sama"}]}).encode("utf-8")
    handler.path = "/api/recon"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()
    handler.client_address = ("10.0.0.99", 54321)

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_POST()

    assert responses and responses[0] == 403
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "forbidden"


def test_image_source_to_data_uri_rejects_traversal_and_non_image_files():
    assert _image_source_to_data_uri("/../../panopto.py") == ""
    assert _image_source_to_data_uri("/app.js") == ""


def test_image_source_to_data_uri_allows_static_images():
    uri = _image_source_to_data_uri("/favicon.svg")
    assert uri.startswith("data:image/")


def test_posts_endpoint_rejects_db_path_outside_allowed_roots():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/posts?db_path=/etc/passwd"
    handler.headers = {}
    handler.rfile = BytesIO()
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    handler.do_GET()

    assert responses and responses[0] == 400
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "invalid_request"


def test_posts_endpoint_includes_face_recognition_fields():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/posts"
    handler.headers = {}
    handler.rfile = BytesIO()
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    base_payload = {
        "count": 1,
        "posts": [
            {
                "username": "alice",
                "content": "sample",
                "timestamp": "2026-02-12T18:15:54+00:00",
                "metadata": {},
            }
        ],
    }
    face_payload = {
        "posts": [
            {
                "username": "alice",
                "content": "sample",
                "timestamp": "2026-02-12T18:15:54+00:00",
                "metadata": {
                    "face_recognition": [
                        {
                            "media_url": "https://cdn.example.com/pic.jpg",
                            "analysis_url": "https://cdn.example.com/pic.jpg",
                            "faces": [
                                {
                                    "person_id": "person_1",
                                    "label": "Person 1",
                                    "color": "#22c55e",
                                    "bbox": {"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4},
                                }
                            ],
                        }
                    ]
                },
                "face_person_ids": ["person_1"],
            }
        ],
        "face_clusters": [{"person_id": "person_1", "label": "Person 1", "count": 1, "color": "#22c55e"}],
        "face_recognition": {"available": True, "reason": "ok", "images_analyzed": 1, "faces_detected": 1},
    }
    with patch("frontend.server.query_posts", return_value=base_payload), patch(
        "frontend.server._FACE_RECOGNITION_ENGINE.annotate_posts", return_value=face_payload
    ) as face_mock:
        handler.do_GET()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["face_clusters"][0]["person_id"] == "person_1"
    assert payload["face_recognition"]["available"] is True
    assert payload["posts"][0]["face_person_ids"] == ["person_1"]
    assert payload["posts"][0]["metadata"]["face_recognition"][0]["faces"][0]["label"] == "Person 1"
    face_mock.assert_called_once()


def test_posts_endpoint_face_refresh_forces_reanalysis():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/posts?face_refresh=1"
    handler.headers = {}
    handler.rfile = BytesIO()
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.query_posts", return_value={"count": 0, "posts": []}), patch(
        "frontend.server._FACE_RECOGNITION_ENGINE.annotate_posts",
        return_value={"posts": [], "face_clusters": [], "face_recognition": {"available": True, "reason": "ok"}},
    ) as face_mock:
        handler.do_GET()

    assert responses and responses[0] == 200
    face_mock.assert_called_once_with([], force_refresh=True)


def test_query_posts_filters_by_case_id(tmp_path):
    db_path = tmp_path / "osint_data.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                case_id TEXT,
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
        conn.executemany(
            "INSERT INTO twitter_posts (source_post_id, case_id, username, content, timestamp, platform, collected_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                ("c1", "case_alpha", "alice", "Alpha case post", "2026-02-10T00:00:00+00:00", "Twitter", "2026-02-10T00:00:00+00:00"),
                ("c2", "case_bravo", "bob", "Bravo case post", "2026-02-10T00:00:00+00:00", "Twitter", "2026-02-10T00:00:00+00:00"),
            ],
        )
        conn.commit()

    payload = query_posts(db_path=db_path, case_id="case_alpha")

    assert payload["count"] == 1
    assert payload["posts"][0]["content"] == "Alpha case post"


def test_cases_api_create_list_delete(tmp_path):
    db_path = tmp_path / "osint_data.db"

    with patch("frontend.server.DEFAULT_DB_PATH", db_path):
        create_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        create_body = json.dumps(
            {
                "case_name": "POI Alpha",
                "status": "Open",
                "threat_level": "Moderate Threat",
                "known_location": "Boston",
                "metadata_tags": ["travel", "financial stress"],
                "case_notes": {"name": "POI Alpha", "context": "initial context"},
            }
        ).encode("utf-8")
        create_handler.path = "/api/cases"
        create_handler.headers = {"Content-Length": str(len(create_body))}
        create_handler.rfile = BytesIO(create_body)
        create_handler.wfile = BytesIO()
        create_codes = []
        create_handler.send_response = lambda code: create_codes.append(code)
        create_handler.send_header = lambda *args, **kwargs: None
        create_handler.end_headers = lambda *args, **kwargs: None
        create_handler.do_POST()
        assert create_codes and create_codes[0] == 201
        created = json.loads(create_handler.wfile.getvalue().decode("utf-8"))
        assert created["case_name"] == "POI Alpha"
        case_id = created["case_id"]

        list_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        list_handler.path = "/api/cases"
        list_handler.headers = {}
        list_handler.wfile = BytesIO()
        list_codes = []
        list_handler.send_response = lambda code: list_codes.append(code)
        list_handler.send_header = lambda *args, **kwargs: None
        list_handler.end_headers = lambda *args, **kwargs: None
        list_handler.do_GET()
        assert list_codes and list_codes[0] == 200
        payload = json.loads(list_handler.wfile.getvalue().decode("utf-8"))
        assert payload["cases"]
        assert payload["cases"][0]["case_id"] == case_id
        assert payload["cases"][0]["threat_level"] == "Moderate Threat"
        assert "travel" in payload["cases"][0]["metadata_tags"]
        assert payload["cases"][0]["case_notes"]["context"] == "initial context"

        patch_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        patch_body = json.dumps({"metadata_tags": ["family", "work"], "case_notes": {"context": "updated context"}}).encode("utf-8")
        patch_handler.path = f"/api/cases/{case_id}"
        patch_handler.headers = {"Content-Length": str(len(patch_body))}
        patch_handler.rfile = BytesIO(patch_body)
        patch_handler.wfile = BytesIO()
        patch_codes = []
        patch_handler.send_response = lambda code: patch_codes.append(code)
        patch_handler.send_header = lambda *args, **kwargs: None
        patch_handler.end_headers = lambda *args, **kwargs: None
        patch_handler.do_PATCH()
        assert patch_codes and patch_codes[0] == 200
        patched = json.loads(patch_handler.wfile.getvalue().decode("utf-8"))
        assert patched["metadata_tags"] == ["family", "work"]
        assert patched["case_notes"]["context"] == "updated context"

        delete_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        delete_handler.path = f"/api/cases/{case_id}"
        delete_handler.headers = {}
        delete_handler.wfile = BytesIO()
        delete_codes = []
        delete_handler.send_response = lambda code: delete_codes.append(code)
        delete_handler.send_header = lambda *args, **kwargs: None
        delete_handler.end_headers = lambda *args, **kwargs: None
        delete_handler.do_DELETE()
        assert delete_codes and delete_codes[0] == 200


def test_cases_demo_endpoint_creates_case_and_posts(tmp_path):
    db_path = tmp_path / "osint_data.db"

    with patch("frontend.server.DEFAULT_DB_PATH", db_path):
        handler = PostExplorerHandler.__new__(PostExplorerHandler)
        body = b"{}"
        handler.path = "/api/cases/demo"
        handler.headers = {"Content-Length": str(len(body))}
        handler.rfile = BytesIO(body)
        handler.wfile = BytesIO()
        responses = []
        handler.send_response = lambda code: responses.append(code)
        handler.send_header = lambda *args, **kwargs: None
        handler.end_headers = lambda *args, **kwargs: None

        handler.do_POST()

        assert responses and responses[0] == 201
        payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
        assert payload["case"]["case_id"]
        assert payload["case"]["case_notes"]["name"] == "SMITH, John"
        assert payload["case"]["case_notes"]["known_profiles"]
        assert len(payload["case"]["case_notes"]["known_profiles"]) >= 8
        sites = [str(item.get("site", "")).lower() for item in payload["case"]["case_notes"]["known_profiles"]]
        assert any("twitter" in site for site in sites)
        assert any("github" in site for site in sites)
        assert any("threads" in site for site in sites)
        assert all(str(item.get("screenshot_url", "")).strip() for item in payload["case"]["case_notes"]["known_profiles"])
        assert payload["inserted_posts"] >= 1
        posts_payload = query_posts(db_path=db_path, case_id=payload["case"]["case_id"])
        assert posts_payload["count"] >= 1
        assert any(
            (post.get("llm_primary_warning_behaviours") or post.get("llm_secondary_risk_factors"))
            for post in posts_payload["posts"]
        )
        assert not any(
            (
                isinstance(post.get("metadata"), dict)
                and (
                    post["metadata"].get("media")
                    or post["metadata"].get("image_urls")
                    or post["metadata"].get("embed_url")
                    or post["metadata"].get("media_urls")
                    or post["metadata"].get("video_url")
                )
            )
            for post in posts_payload["posts"]
        )


def test_case_notes_pdf_export_endpoint_downloads_pdf(tmp_path):
    db_path = tmp_path / "osint_data.db"

    with patch("frontend.server.DEFAULT_DB_PATH", db_path):
        create_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        create_body = json.dumps(
            {
                "case_name": "POI Delta",
                "status": "Open",
                "threat_level": "Low Threat",
                "known_location": "Boston",
                "case_notes": {
                    "name": "Delta Subject",
                    "location": "Boston",
                    "age": "29",
                    "akas": "Delta",
                    "context": "Context section",
                    "threat_risk_assessment": "Low risk",
                    "personal_details": "Personal details",
                    "known_profiles": [{"site": "Twitter/X / @delta", "url": "https://x.com/delta", "screenshot_url": ""}],
                },
            }
        ).encode("utf-8")
        create_handler.path = "/api/cases"
        create_handler.headers = {"Content-Length": str(len(create_body))}
        create_handler.rfile = BytesIO(create_body)
        create_handler.wfile = BytesIO()
        create_handler.send_response = lambda code: None
        create_handler.send_header = lambda *args, **kwargs: None
        create_handler.end_headers = lambda *args, **kwargs: None
        create_handler.do_POST()
        created = json.loads(create_handler.wfile.getvalue().decode("utf-8"))
        case_id = created["case_id"]

        get_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        get_handler.path = f"/api/cases/{case_id}/notes.pdf"
        get_handler.headers = {}
        get_handler.wfile = BytesIO()
        response_codes = []
        response_headers = {}
        get_handler.send_response = lambda code: response_codes.append(code)
        get_handler.send_header = lambda key, value: response_headers.__setitem__(key, value)
        get_handler.end_headers = lambda *args, **kwargs: None
        get_handler.do_GET()

        assert response_codes and response_codes[0] == 200
        assert response_headers.get("Content-Type") == "application/pdf"
        assert "attachment" in str(response_headers.get("Content-Disposition", "")).lower()
        payload = get_handler.wfile.getvalue()
        assert payload.startswith(b"%PDF-1.4")


def test_case_notes_pdf_export_post_uses_live_draft_payload(tmp_path):
    db_path = tmp_path / "osint_data.db"

    with patch("frontend.server.DEFAULT_DB_PATH", db_path):
        create_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        create_body = json.dumps(
            {
                "case_name": "POI Delta",
                "status": "Open",
                "threat_level": "Low Threat",
                "known_location": "Boston",
                "case_notes": {
                    "name": "Stored Subject",
                    "context": "Stored context",
                },
            }
        ).encode("utf-8")
        create_handler.path = "/api/cases"
        create_handler.headers = {"Content-Length": str(len(create_body))}
        create_handler.rfile = BytesIO(create_body)
        create_handler.wfile = BytesIO()
        create_handler.send_response = lambda code: None
        create_handler.send_header = lambda *args, **kwargs: None
        create_handler.end_headers = lambda *args, **kwargs: None
        create_handler.do_POST()
        created = json.loads(create_handler.wfile.getvalue().decode("utf-8"))
        case_id = created["case_id"]

        export_handler = PostExplorerHandler.__new__(PostExplorerHandler)
        export_body = json.dumps(
            {
                "case_name": "Draft Export Name",
                "known_location": "Seattle",
                "case_notes": {
                    "name": "Draft Subject",
                    "location": "Seattle",
                    "context": "Draft context for export only",
                },
            }
        ).encode("utf-8")
        export_handler.path = f"/api/cases/{case_id}/notes.pdf"
        export_handler.headers = {"Content-Length": str(len(export_body))}
        export_handler.rfile = BytesIO(export_body)
        export_handler.wfile = BytesIO()
        response_codes = []
        response_headers = {}
        export_handler.send_response = lambda code: response_codes.append(code)
        export_handler.send_header = lambda key, value: response_headers.__setitem__(key, value)
        export_handler.end_headers = lambda *args, **kwargs: None
        export_handler.do_POST()

        assert response_codes and response_codes[0] == 200
        assert response_headers.get("Content-Type") == "application/pdf"
        assert "draft-export-name-report.pdf" in str(response_headers.get("Content-Disposition", "")).lower()
        payload = export_handler.wfile.getvalue()
        assert payload.startswith(b"%PDF-1.4")
        assert b"Draft Subject" in payload
        assert b"Draft context for export only" in payload
        assert b"Stored context" not in payload


def test_collect_start_endpoint_returns_job_id():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "targets": [{"platform": "twitter", "username": "AKayWyatt"}],
            "start_date": "2026-01-08",
            "end_date": "2026-02-15",
        }
    ).encode("utf-8")
    handler.path = "/api/collect/start"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.load_config", return_value={"apify_api_token": "test-token"}), patch(
        "frontend.server.start_collection_job",
        return_value={
            "job_id": "job123",
            "status": "queued",
            "phase": "queued",
            "current_stage": 0,
            "total_stages": 2,
            "progress": 0.0,
            "targets": [{"platform": "twitter", "username": "akaywyatt"}],
            "start_date": "2026-01-08",
            "end_date": "2026-02-15",
            "created_at": "2026-02-17T00:00:00+00:00",
            "updated_at": "2026-02-17T00:00:00+00:00",
        },
    ):
        handler.do_POST()

    assert responses and responses[0] == 202
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["job_id"] == "job123"
    assert payload["status"] == "queued"


def test_collect_start_requires_apify_token_for_apify_platforms():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "targets": [{"platform": "twitter", "username": "aoc"}],
            "start_date": "2026-01-08",
            "end_date": "2026-02-15",
        }
    ).encode("utf-8")
    handler.path = "/api/collect/start"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.load_config", return_value={"apify_api_token": ""}):
        handler.do_POST()

    assert responses and responses[0] == 400
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "apify_token_required"
    assert "twitter" in payload["error"]["platforms"]


def test_collect_status_endpoint_returns_not_found():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/collect/status?job_id=missing"
    handler.headers = {}
    handler.rfile = BytesIO()
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.get_collection_job_status", return_value=None):
        handler.do_GET()

    assert responses and responses[0] == 404
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["error"]["code"] == "not_found"


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


def test_recon_endpoint_rejects_missing_selectors():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({}).encode("utf-8")
    handler.path = "/api/recon"
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


def test_recon_endpoint_returns_targets_and_leads():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"selectors": [{"type": "username", "value": "@sama"}]}).encode("utf-8")
    handler.path = "/api/recon"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.run_recon",
        return_value={
            "selectors": [{"type": "username", "value": "sama"}],
            "results": [],
            "collection_targets": [{"platform": "twitter", "username": "sama"}],
            "leads": [{"site": "github", "profile_url": "https://github.com/sama"}],
            "checked": 10,
            "present_count": 2,
        },
    ):
        handler.do_POST()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["collection_targets"] == [{"platform": "twitter", "username": "sama"}]
    assert payload["leads"] == [{"site": "github", "profile_url": "https://github.com/sama"}]


def test_config_endpoint_get_returns_config():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    handler.path = "/api/config"
    handler.headers = {}
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.load_public_config",
        return_value={
            "pdl_api_key_configured": True,
            "osint_industries_api_key_configured": True,
            "numverify_api_key_configured": True,
            "openai_api_key_configured": True,
            "secret_storage_mode": "encrypted_file",
        },
    ):
        handler.do_GET()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["pdl_api_key_configured"] is True
    assert payload["osint_industries_api_key_configured"] is True
    assert payload["numverify_api_key_configured"] is True
    assert payload["openai_api_key_configured"] is True
    assert payload["secret_storage_mode"] == "encrypted_file"


def test_config_endpoint_post_saves_config():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "pdl_api_key": "pdl_live_key",
            "osint_industries_api_key": "oi_live_key",
            "numverify_api_key": "numverify_live_key",
            "openai_api_key": "sk-test-live-key",
        }
    ).encode("utf-8")
    handler.path = "/api/config"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.save_config",
        return_value={},
    ) as save_mock:
        with patch(
            "frontend.server.load_public_config",
            return_value={
                "pdl_api_key_configured": True,
                "osint_industries_api_key_configured": True,
                "numverify_api_key_configured": True,
                "openai_api_key_configured": True,
                "secret_storage_mode": "encrypted_file",
            },
        ):
            handler.do_POST()

    save_mock.assert_called_once()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["pdl_api_key_configured"] is True
    assert payload["osint_industries_api_key_configured"] is True
    assert payload["numverify_api_key_configured"] is True
    assert payload["openai_api_key_configured"] is True


def test_llm_estimate_endpoint_returns_estimate_payload():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps({"posts": [{"row_id": 1, "content": "sample post", "metadata": {}}]}).encode("utf-8")
    handler.path = "/api/llm/estimate"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.estimate_warning_assessment_cost",
        return_value={"candidate_posts": 1, "estimated_total_cost_usd": 0.0012},
    ):
        handler.do_POST()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["estimate"]["candidate_posts"] == 1


def test_llm_sandbox_endpoint_returns_assessed_post():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "text": "I know exactly when they leave the building.",
            "username": "tester",
            "platform": "Sandbox",
            "source_url": "https://example.test/post/1",
        }
    ).encode("utf-8")
    handler.path = "/api/llm/sandbox"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.analyze_post_sandbox",
        return_value={
            "row_id": 0,
            "post_id": "sandbox-123",
            "platform": "Sandbox",
            "username": "tester",
            "content": "I know exactly when they leave the building.",
            "timestamp": "2026-03-11T00:00:00+00:00",
            "source_url": "https://example.test/post/1",
            "post_type": "post",
            "metadata": {
                "sandbox": True,
                "llm_assessment": {
                    "tagged_primary": ["Pathway"],
                    "tagged_secondary": ["Capability (access)"],
                    "underlying_theme": "Target-focused planning",
                },
                "identity_intel_assessment": {
                    "tags": [
                        {"label": "location: Washington DC", "intel": "inferred"},
                        {"label": "handle: tester", "intel": "stated"},
                    ],
                    "theme": "User possibly based in Washington DC",
                },
                "sandbox_debug": {
                    "request_text": "I know exactly when they leave the building.",
                    "combined_messages": [{"role": "system", "content": "combined"}, {"role": "user", "content": "text"}],
                    "threat_messages": [{"role": "system", "content": "threat"}, {"role": "user", "content": "text"}],
                    "identity_messages": [{"role": "system", "content": "identity"}, {"role": "user", "content": "text"}],
                    "threat_error": "",
                    "identity_error": "",
                    "threat_raw": {"tagged_primary": ["Pathway"]},
                    "threat_normalized": {
                        "tagged_primary": ["Pathway"],
                        "tagged_secondary": ["Capability (access)"],
                        "underlying_theme": "Target-focused planning",
                        "rationale": "",
                    },
                    "identity_raw": {
                        "tags": [{"label": "location: Washington DC", "intel": "inferred"}],
                        "theme": "User possibly based in Washington DC",
                    },
                    "identity_normalized": {
                        "tags": [
                            {"label": "location: Washington DC", "intel": "inferred"},
                            {"label": "handle: tester", "intel": "stated"},
                        ],
                        "theme": "User possibly based in Washington DC",
                    },
                },
                "sandbox_analysis": {
                    "threat_checked": True,
                    "identity_checked": True,
                    "threat_present": True,
                    "identity_present": True,
                },
            },
        },
    ):
        handler.do_POST()

    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["status"] == "ok"
    assert payload["post"]["metadata"]["llm_assessment"]["underlying_theme"] == "Target-focused planning"
    assert payload["post"]["metadata"]["identity_intel_assessment"]["theme"] == "User possibly based in Washington DC"
    assert payload["analysis_status"]["threat_checked"] is True
    assert payload["analysis_status"]["identity_checked"] is True


def test_llm_run_endpoint_persists_assessment_updates():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "case_id": "case_1",
            "posts": [{"row_id": 7, "content": "sample post", "metadata": {}}],
        }
    ).encode("utf-8")
    handler.path = "/api/llm/run"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch(
        "frontend.server.apply_warning_assessments",
        return_value=[
            {
                "row_id": 7,
                "metadata": {
                    "llm_assessment": {
                        "primary_warning_behaviours": ["Fixation"],
                        "risk_level": "Moderate",
                    }
                },
            }
        ],
    ):
        with patch("frontend.server.update_post_llm_assessments", return_value=1) as persist_mock:
            handler.do_POST()

    persist_mock.assert_called_once()
    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["assessed"] == 1
    assert payload["persisted"] == 1


def test_post_assessment_endpoint_persists_manual_edits():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "row_id": 19,
            "case_id": "case_1",
            "metadata": {
                "llm_assessment": {
                    "tagged_primary": ["Fixation", "Fixation"],
                    "tagged_secondary": ["Stressor"],
                    "underlying_theme": "Escalating grievance",
                    "rationale": "analyst override",
                }
            },
        }
    ).encode("utf-8")
    handler.path = "/api/posts/assessment"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.update_post_llm_assessments", return_value=1) as persist_mock:
        handler.do_POST()

    persist_mock.assert_called_once()
    called_updates = persist_mock.call_args.kwargs["updates"]
    assert called_updates and called_updates[0]["row_id"] == 19
    llm = called_updates[0]["metadata"]["llm_assessment"]
    assert llm["tagged_primary"] == ["Fixation"]
    assert llm["primary_warning_behaviours"] == ["Fixation"]
    assert llm["tagged_secondary"] == ["Stressor"]
    assert llm["secondary_risk_factors"] == ["Stressor"]
    assert llm["underlying_theme"] == "Escalating grievance"
    assert responses and responses[0] == 200
    payload = json.loads(handler.wfile.getvalue().decode("utf-8"))
    assert payload["persisted"] == 1


def test_post_assessment_endpoint_clears_theme_without_behaviours():
    handler = PostExplorerHandler.__new__(PostExplorerHandler)
    body = json.dumps(
        {
            "row_id": 21,
            "case_id": "case_1",
            "metadata": {
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": [],
                    "underlying_theme": "Should be removed",
                    "rationale": "analyst override",
                }
            },
        }
    ).encode("utf-8")
    handler.path = "/api/posts/assessment"
    handler.headers = {"Content-Length": str(len(body))}
    handler.rfile = BytesIO(body)
    handler.wfile = BytesIO()

    responses = []
    handler.send_response = lambda code: responses.append(code)
    handler.send_header = lambda *args, **kwargs: None
    handler.end_headers = lambda *args, **kwargs: None

    with patch("frontend.server.update_post_llm_assessments", return_value=1) as persist_mock:
        handler.do_POST()

    persist_mock.assert_called_once()
    called_updates = persist_mock.call_args.kwargs["updates"]
    llm = called_updates[0]["metadata"]["llm_assessment"]
    assert llm["tagged_primary"] == []
    assert llm["tagged_secondary"] == []
    assert llm["underlying_theme"] == ""
    assert responses and responses[0] == 200
