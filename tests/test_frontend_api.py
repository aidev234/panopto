from __future__ import annotations

import sqlite3

from frontend.server import query_posts


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
                raw_metadata TEXT,
                collected_at TEXT NOT NULL
            )
            """
        )
        conn.executemany(
            "INSERT INTO twitter_posts (username, content, timestamp, collected_at) VALUES (?, ?, ?, ?)",
            [
                ("alice", "I live in New York", "2024-01-10T00:00:00", "2024-01-10T00:00:00"),
                ("bob", "Moving to Boston", "2024-01-01T00:00:00", "2024-01-01T00:00:00"),
                ("carol", "New York trip", "2024-01-05T00:00:00", "2024-01-05T00:00:00"),
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
