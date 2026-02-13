"""SQLite persistence for locally collected Twitter OSINT data."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def init_db(db_path: str = "osint_data.db") -> None:
    """Create required database tables if they do not already exist."""

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT,
                likes INTEGER,
                retweets INTEGER,
                replies INTEGER,
                raw_metadata TEXT,
                collected_at TEXT NOT NULL,
                UNIQUE(source_post_id, username, timestamp, content)
            )
            """
        )
        conn.commit()


def save_posts(posts: list[dict[str, Any]], db_path: str = "osint_data.db") -> int:
    """Insert posts into SQLite, ignoring duplicates. Returns inserted row count."""

    init_db(db_path)
    collected_at = datetime.now(timezone.utc).isoformat()

    inserted = 0
    with sqlite3.connect(db_path) as conn:
        for post in posts:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO twitter_posts (
                    source_post_id,
                    username,
                    content,
                    timestamp,
                    likes,
                    retweets,
                    replies,
                    raw_metadata,
                    collected_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post.get("post_id"),
                    post.get("username"),
                    post.get("content") or "",
                    post.get("timestamp"),
                    post.get("likes"),
                    post.get("retweets"),
                    post.get("replies"),
                    str(post.get("metadata")),
                    collected_at,
                ),
            )
            if cursor.rowcount == 1:
                inserted += 1

        conn.commit()

    return inserted
