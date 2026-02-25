"""SQLite persistence for locally collected Twitter OSINT data."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
from panopto.analysis.llm_warning_assessor import build_demo_posts


def init_db(db_path: str = "osint_data.db") -> None:
    """Create required database tables if they do not already exist."""

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                case_name TEXT NOT NULL,
                status TEXT NOT NULL,
                threat_level TEXT NOT NULL,
                known_location TEXT,
                poi_image_url TEXT,
                case_notes TEXT NOT NULL DEFAULT '{}',
                metadata_tags TEXT NOT NULL DEFAULT '[]',
                opened_at TEXT NOT NULL,
                last_edited_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS twitter_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_post_id TEXT,
                case_id TEXT,
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
        if "case_id" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN case_id TEXT")
        if "source_url" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN source_url TEXT")
        if "referenced_username" not in existing_columns:
            conn.execute("ALTER TABLE twitter_posts ADD COLUMN referenced_username TEXT")
        case_columns = {row[1] for row in conn.execute("PRAGMA table_info(cases)").fetchall()}
        if "metadata_tags" not in case_columns:
            conn.execute("ALTER TABLE cases ADD COLUMN metadata_tags TEXT NOT NULL DEFAULT '[]'")
        if "poi_image_url" not in case_columns:
            conn.execute("ALTER TABLE cases ADD COLUMN poi_image_url TEXT")
        if "case_notes" not in case_columns:
            conn.execute("ALTER TABLE cases ADD COLUMN case_notes TEXT NOT NULL DEFAULT '{}'")
        conn.commit()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _valid_status(value: str) -> str:
    allowed = {
        "Open": "Open",
        "Under Investigation": "Under Investigation",
        "Closed": "Closed",
        "Watchlist": "Watchlist",
        "UnderInvestigation": "Under Investigation",
        "under investigation": "Under Investigation",
        "underinvestigation": "Under Investigation",
    }
    raw = str(value or "").strip()
    return allowed.get(raw, allowed.get(raw.lower(), "Open"))


def _valid_threat_level(value: str) -> str:
    allowed = {
        "Low Threat": "Low Threat",
        "Moderate Threat": "Moderate Threat",
        "Substantial Threat": "Substantial Threat",
        "High Threat": "High Threat",
        "Very High Threat": "Very High Threat",
        "low threat": "Low Threat",
        "moderate threat": "Moderate Threat",
        "substantial threat": "Substantial Threat",
        "high threat": "High Threat",
        "very high threat": "Very High Threat",
    }
    raw = str(value or "").strip()
    return allowed.get(raw, allowed.get(raw.lower(), "Low Threat"))


def _normalize_metadata_tags(raw: Any) -> list[str]:
    if isinstance(raw, str):
        values = [item.strip() for item in raw.split(",")]
    elif isinstance(raw, list):
        values = [str(item).strip() for item in raw]
    else:
        values = []
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        if not item:
            continue
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:24]


def _normalize_poi_image_url(raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""
    if value.lower().startswith(("http://", "https://", "data:image/")):
        return value
    return ""


def _normalize_case_notes(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    return raw


def create_case(
    *,
    case_name: str,
    status: str = "Open",
    threat_level: str = "Low Threat",
    known_location: str = "",
    poi_image_url: str = "",
    case_notes: dict[str, Any] | None = None,
    metadata_tags: list[str] | str | None = None,
    db_path: str = "osint_data.db",
) -> dict[str, Any]:
    init_db(db_path)
    now = _utc_now_iso()
    row = {
        "case_id": uuid4().hex,
        "case_name": str(case_name or "").strip() or "Untitled Case",
        "status": _valid_status(status),
        "threat_level": _valid_threat_level(threat_level),
        "known_location": str(known_location or "").strip(),
        "poi_image_url": _normalize_poi_image_url(poi_image_url),
        "case_notes": _normalize_case_notes(case_notes or {}),
        "metadata_tags": _normalize_metadata_tags(metadata_tags or []),
        "opened_at": now,
        "last_edited_at": now,
    }
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO cases (case_id, case_name, status, threat_level, known_location, poi_image_url, case_notes, metadata_tags, opened_at, last_edited_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["case_id"],
                row["case_name"],
                row["status"],
                row["threat_level"],
                row["known_location"],
                row["poi_image_url"],
                json.dumps(row["case_notes"], ensure_ascii=True),
                json.dumps(row["metadata_tags"], ensure_ascii=True),
                row["opened_at"],
                row["last_edited_at"],
            ),
        )
        conn.commit()
    return row


def list_cases(db_path: str = "osint_data.db") -> list[dict[str, Any]]:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT
                c.case_id,
                c.case_name,
                c.status,
                c.threat_level,
                c.known_location,
                c.poi_image_url,
                c.case_notes,
                c.metadata_tags,
                c.opened_at,
                c.last_edited_at,
                COUNT(p.id) AS post_count
            FROM cases c
            LEFT JOIN twitter_posts p ON p.case_id = c.case_id
            GROUP BY c.case_id, c.case_name, c.status, c.threat_level, c.known_location, c.poi_image_url, c.case_notes, c.metadata_tags, c.opened_at, c.last_edited_at
            ORDER BY c.last_edited_at DESC
            """
        ).fetchall()
    output: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        try:
            parsed = json.loads(str(item.get("metadata_tags") or "[]"))
            item["metadata_tags"] = [str(tag) for tag in parsed if str(tag).strip()] if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            item["metadata_tags"] = []
        try:
            parsed_notes = json.loads(str(item.get("case_notes") or "{}"))
            item["case_notes"] = _normalize_case_notes(parsed_notes)
        except json.JSONDecodeError:
            item["case_notes"] = {}
        output.append(item)
    return output


def update_case(
    case_id: str,
    *,
    case_name: str | None = None,
    status: str | None = None,
    threat_level: str | None = None,
    known_location: str | None = None,
    poi_image_url: str | None = None,
    case_notes: dict[str, Any] | None = None,
    metadata_tags: list[str] | str | None = None,
    db_path: str = "osint_data.db",
) -> dict[str, Any] | None:
    init_db(db_path)
    updates: list[str] = []
    params: list[Any] = []
    if case_name is not None:
        updates.append("case_name = ?")
        params.append(str(case_name).strip() or "Untitled Case")
    if status is not None:
        updates.append("status = ?")
        params.append(_valid_status(status))
    if threat_level is not None:
        updates.append("threat_level = ?")
        params.append(_valid_threat_level(threat_level))
    if known_location is not None:
        updates.append("known_location = ?")
        params.append(str(known_location).strip())
    if poi_image_url is not None:
        updates.append("poi_image_url = ?")
        params.append(_normalize_poi_image_url(poi_image_url))
    if case_notes is not None:
        updates.append("case_notes = ?")
        params.append(json.dumps(_normalize_case_notes(case_notes), ensure_ascii=True))
    if metadata_tags is not None:
        updates.append("metadata_tags = ?")
        params.append(json.dumps(_normalize_metadata_tags(metadata_tags), ensure_ascii=True))
    updates.append("last_edited_at = ?")
    params.append(_utc_now_iso())
    params.append(case_id)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            f"UPDATE cases SET {', '.join(updates)} WHERE case_id = ?",
            tuple(params),
        )
        conn.commit()
        if cursor.rowcount < 1:
            return None
        row = conn.execute(
            """
            SELECT case_id, case_name, status, threat_level, known_location, poi_image_url, case_notes, metadata_tags, opened_at, last_edited_at
            FROM cases
            WHERE case_id = ?
            """,
            (case_id,),
        ).fetchone()
        if not row:
            return None
    parsed_tags: list[str] = []
    try:
        decoded = json.loads(str(row[7] or "[]"))
        if isinstance(decoded, list):
            parsed_tags = [str(tag) for tag in decoded if str(tag).strip()]
    except json.JSONDecodeError:
        parsed_tags = []
    parsed_notes: dict[str, Any] = {}
    try:
        decoded_notes = json.loads(str(row[6] or "{}"))
        parsed_notes = _normalize_case_notes(decoded_notes)
    except json.JSONDecodeError:
        parsed_notes = {}
    return {
        "case_id": row[0],
        "case_name": row[1],
        "status": row[2],
        "threat_level": row[3],
        "known_location": row[4],
        "poi_image_url": str(row[5] or "").strip(),
        "case_notes": parsed_notes,
        "metadata_tags": parsed_tags,
        "opened_at": row[8],
        "last_edited_at": row[9],
    }


def touch_case(case_id: str | None, *, db_path: str = "osint_data.db") -> None:
    if not case_id:
        return
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE cases SET last_edited_at = ? WHERE case_id = ?",
            (_utc_now_iso(), case_id),
        )
        conn.commit()


def delete_case(case_id: str, *, db_path: str = "osint_data.db", delete_posts: bool = True) -> bool:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        if delete_posts:
            conn.execute("DELETE FROM twitter_posts WHERE case_id = ?", (case_id,))
        cursor = conn.execute("DELETE FROM cases WHERE case_id = ?", (case_id,))
        conn.commit()
        return cursor.rowcount > 0


def create_demo_case(db_path: str = "osint_data.db") -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    demo_avatar = "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=256&q=80"
    case = create_case(
        case_name="POI SMITH, John",
        status="Under Investigation",
        threat_level="High Threat",
        known_location="New York",
        poi_image_url=demo_avatar,
        case_notes={
            "name": "SMITH, John",
            "location": "New York, NY",
            "age": "34",
            "akas": "Johnny Smith, J. Smith, @demo_subject",
            "subject_image_url": demo_avatar,
            "context": (
                "Subject appears highly active across multiple platforms with frequent travel references "
                "and intermittent expressions of grievance. Activity indicates a growing operational pattern."
            ),
            "threat_risk_assessment": (
                "Elevated concern due to explicit firearm/ammunition language and escalating hostile rhetoric. "
                "Current posture assessed as high risk pending corroboration of intent and capability."
            ),
            "personal_details": (
                "Likely resides in the NYC metro area. Mentions spouse and repeated short-notice travel. "
                "Uses encrypted email and multiple social aliases."
            ),
            "known_profiles": [
                {
                    "site": "Twitter/X",
                    "url": "https://x.com/demo_subject",
                    "image_url": demo_avatar,
                    "screenshot_url": "/recon_shots/twitter-cbd0039562da9a05.png?v=1",
                },
                {
                    "site": "Reddit",
                    "url": "https://www.reddit.com/user/demo_subject",
                    "image_url": demo_avatar,
                    "screenshot_url": "/recon_shots/reddit-1bbd6bf419da4867.png?v=1",
                },
                {
                    "site": "Bluesky",
                    "url": "https://bsky.app/profile/demo_subject.bsky.social",
                    "image_url": demo_avatar,
                    "screenshot_url": "/recon_shots/bluesky-e669742696b86463.png?v=1",
                },
            ],
        },
        metadata_tags=[],
        db_path=db_path,
    )
    posts = build_demo_posts(username="demo_subject", now=now)
    if not posts:
        posts = [
            {
                "post_id": "demo-fallback-1",
                "platform": "Twitter",
                "username": "demo_subject",
                "content": "I am going to buy a gun and ammo this weekend. Enough talking.",
                "timestamp": now.isoformat(),
                "source_url": "https://x.com/demo_subject/status/demo-fallback-1",
                "post_type": "post",
                "metadata": {"profile_image_url": demo_avatar},
            }
        ]
    inserted = save_posts(posts, db_path=db_path, case_id=case["case_id"])
    return {
        "case": case,
        "inserted_posts": inserted,
    }


def save_posts(posts: list[dict[str, Any]], db_path: str = "osint_data.db", *, case_id: str | None = None) -> int:
    """Insert posts into SQLite, ignoring duplicates. Returns inserted row count."""

    init_db(db_path)
    collected_at = _utc_now_iso()

    inserted = 0
    with sqlite3.connect(db_path) as conn:
        for post in posts:
            metadata_json = json.dumps(post.get("metadata") or {}, ensure_ascii=True)
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO twitter_posts (
                    source_post_id,
                    case_id,
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
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post.get("post_id"),
                    case_id,
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
                        case_id = COALESCE(case_id, ?),
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
                        case_id,
                        metadata_json,
                        post.get("username"),
                        post.get("platform") or "Twitter",
                        post.get("content") or "",
                        post.get("timestamp"),
                        post.get("post_id"),
                    ),
                )

        conn.commit()

    touch_case(case_id, db_path=db_path)
    return inserted


def clear_posts(db_path: str = "osint_data.db", *, clear_cases: bool = False) -> None:
    """Delete all collected rows while preserving schema."""

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM twitter_posts")
        if clear_cases:
            conn.execute("DELETE FROM cases")
        conn.commit()
