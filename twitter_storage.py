"""SQLite persistence for locally collected Twitter OSINT data."""

from __future__ import annotations

import json
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
                platform TEXT NOT NULL DEFAULT 'Twitter',
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
                collected_at TEXT NOT NULL,
                UNIQUE(source_post_id, username, timestamp, content)
            )
            """
        )
        existing_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(twitter_posts)").fetchall()
        }
        if "post_type" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN post_type TEXT NOT NULL DEFAULT 'post'")
        if "platform" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN platform TEXT NOT NULL DEFAULT 'Twitter'")
        if "source_url" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN source_url TEXT")
        if "referenced_username" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN referenced_username TEXT")
        if "topic_id" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN topic_id INTEGER")
        if "theme_label" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN theme_label TEXT")
        if "theme_keywords" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN theme_keywords TEXT")
        if "theme_tag" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN theme_tag TEXT")
        conn.commit()


def save_posts(posts: list[dict[str, Any]], db_path: str = "osint_data.db") -> int:
    """Insert posts into SQLite, ignoring duplicates. Returns inserted row count."""

    init_db(db_path)
    collected_at = datetime.now(timezone.utc).isoformat()

    inserted = 0
    with sqlite3.connect(db_path) as conn:
        for post in posts:
            metadata_json = json.dumps(post.get("metadata") or {}, ensure_ascii=True)
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO twitter_posts (
                    source_post_id,
                    platform,
                    username,
                    content,
                    timestamp,
                    likes,
                    retweets,
                    replies,
                    post_type,
                    source_url,
                    referenced_username,
                    raw_metadata,
                    collected_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post.get("post_id"),
                    post.get("platform") or "Twitter",
                    post.get("username"),
                    post.get("content") or "",
                    post.get("timestamp"),
                    post.get("likes"),
                    post.get("retweets"),
                    post.get("replies"),
                    post.get("post_type") or "post",
                    post.get("source_url"),
                    post.get("referenced_username"),
                    metadata_json,
                    collected_at,
                ),
            )
            if cursor.rowcount == 1:
                inserted += 1
            else:
                conn.execute(
                    """
                    UPDATE twitter_posts
                    SET post_type = CASE
                            WHEN post_type IS NULL OR post_type = 'post' THEN ?
                            ELSE post_type
                        END,
                        source_url = COALESCE(source_url, ?),
                        referenced_username = COALESCE(referenced_username, ?),
                        raw_metadata = CASE
                            WHEN raw_metadata IS NULL OR raw_metadata = '' OR raw_metadata = '{}'
                            THEN ?
                            ELSE raw_metadata
                        END
                    WHERE username = ?
                      AND platform = ?
                      AND content = ?
                      AND IFNULL(timestamp, '') = IFNULL(?, '')
                      AND IFNULL(source_post_id, '') = IFNULL(?, '')
                    """,
                    (
                        post.get("post_type") or "post",
                        post.get("source_url"),
                        post.get("referenced_username"),
                        metadata_json,
                        post.get("username"),
                        post.get("platform") or "Twitter",
                        post.get("content") or "",
                        post.get("timestamp"),
                        post.get("post_id"),
                    ),
                )

        conn.commit()

    return inserted


def clear_posts(db_path: str = "osint_data.db") -> None:
    """Delete all collected rows while preserving schema."""

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM twitter_posts")
        conn.commit()
