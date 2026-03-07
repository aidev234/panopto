"""Known-entity archive and selector matching persistence."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_known_entities_db(db_path: str = "osint_data.db") -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS known_entity_archives (
                archive_id TEXT PRIMARY KEY,
                case_id TEXT,
                case_name TEXT NOT NULL,
                archived_payload TEXT NOT NULL,
                archived_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS known_entity_selectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                archive_id TEXT NOT NULL,
                selector_type TEXT NOT NULL,
                selector_value TEXT NOT NULL,
                selector_display TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                UNIQUE(archive_id, selector_type, selector_value)
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_known_entity_selector_lookup
            ON known_entity_selectors(selector_type, selector_value)
            """
        )
        conn.commit()


def clear_known_entities(db_path: str = "osint_data.db") -> None:
    init_known_entities_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM known_entity_selectors")
        conn.execute("DELETE FROM known_entity_archives")
        conn.commit()


def _normalize_selector(selector_type: Any, selector_value: Any) -> tuple[str, str] | None:
    kind = str(selector_type or "").strip().lower()
    value = str(selector_value or "").strip()
    if not kind or not value:
        return None
    if kind == "username":
        clean = value.lstrip("@").strip().lower()
        return ("username", clean) if clean else None
    if kind == "email":
        clean = value.lower()
        return ("email", clean) if clean else None
    if kind == "phone":
        clean = re.sub(r"[^\d+]", "", value)
        if clean.startswith("00"):
            clean = f"+{clean[2:]}"
        return ("phone", clean) if clean else None
    if kind == "name":
        clean = " ".join(value.split()).lower()
        return ("name", clean) if clean else None
    if kind == "wallet":
        clean = value.lower()
        return ("wallet", clean) if clean else None
    if kind == "profile_url":
        clean = value.strip().rstrip("/").lower()
        return ("profile_url", clean) if clean else None
    if kind == "platform_username":
        raw = value.strip().lower()
        if "|" not in raw:
            return None
        platform, username = raw.split("|", 1)
        platform = platform.strip()
        username = username.strip().lstrip("@")
        if not platform or not username:
            return None
        return ("platform_username", f"{platform}|{username}")
    return None


def _extract_platform_username_from_url(raw_url: str) -> tuple[str, str] | None:
    value = str(raw_url or "").strip()
    if not value:
        return None
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    host = str(parsed.netloc or "").lower().strip()
    path_parts = [part for part in str(parsed.path or "").split("/") if part]
    if not host or not path_parts:
        return None
    host = host.removeprefix("www.")
    if host in {"x.com", "twitter.com"}:
        return ("twitter", path_parts[0].lstrip("@"))
    if host.endswith("reddit.com"):
        lowered = [part.lower() for part in path_parts]
        if lowered[0] in {"u", "user"} and len(path_parts) >= 2:
            return ("reddit", path_parts[1].lstrip("@"))
    if host.endswith("tiktok.com"):
        return ("tiktok", path_parts[0].lstrip("@"))
    if host.endswith("instagram.com"):
        return ("instagram", path_parts[0].lstrip("@"))
    if host in {"bsky.app", "bsky.social"} and path_parts[0].lower() == "profile" and len(path_parts) >= 2:
        return ("bluesky", path_parts[1].removesuffix(".bsky.social").lstrip("@"))
    if host.endswith("youtube.com"):
        first = path_parts[0]
        if first.startswith("@"):
            return ("youtube", first.lstrip("@"))
    return None


def extract_known_entity_selectors(case_row: dict[str, Any], posts: list[dict[str, Any]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    output: list[dict[str, str]] = []

    def add(selector_type: str, selector_value: str, display: str = "") -> None:
        normalized = _normalize_selector(selector_type, selector_value)
        if not normalized:
            return
        if normalized in seen:
            return
        seen.add(normalized)
        output.append(
            {
                "type": normalized[0],
                "value": normalized[1],
                "display": str(display or selector_value).strip(),
            }
        )

    case_name = str(case_row.get("case_name") or "").strip()
    if case_name:
        add("name", case_name, case_name)

    notes = case_row.get("case_notes") if isinstance(case_row.get("case_notes"), dict) else {}
    if isinstance(notes, dict):
        known_profiles = notes.get("known_profiles")
        if isinstance(known_profiles, list):
            for profile in known_profiles:
                if not isinstance(profile, dict):
                    continue
                profile_url = str(profile.get("url") or "").strip()
                if profile_url:
                    add("profile_url", profile_url, profile_url)
                    parsed = _extract_platform_username_from_url(profile_url)
                    if parsed:
                        add("platform_username", f"{parsed[0]}|{parsed[1]}", f"{parsed[0]}|{parsed[1]}")
                        add("username", parsed[1], parsed[1])
        note_text = " ".join(
            [
                str(notes.get("akas") or ""),
                str(notes.get("personal_details") or ""),
                str(notes.get("context") or ""),
            ]
        )
        for match in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", note_text):
            add("email", match, match)
        for match in re.findall(r"\+\d[\d\s().-]{6,}", note_text):
            add("phone", match, match)
        for match in re.findall(r"@([A-Za-z0-9_.-]{2,})", note_text):
            add("username", match, match)

    for post in posts:
        if not isinstance(post, dict):
            continue
        platform = str(post.get("platform") or "").strip().lower()
        username = str(post.get("username") or "").strip().lstrip("@")
        if username:
            add("username", username, username)
        if platform and username:
            add("platform_username", f"{platform}|{username}", f"{platform}|{username}")
        source_url = str(post.get("source_url") or "").strip()
        if source_url:
            add("profile_url", source_url, source_url)

    return output


def archive_case_to_known_entities(
    *,
    case_row: dict[str, Any],
    posts: list[dict[str, Any]],
    db_path: str = "osint_data.db",
) -> dict[str, Any]:
    init_known_entities_db(db_path)
    archive_id = uuid4().hex
    archived_at = _utc_now_iso()
    selectors = extract_known_entity_selectors(case_row, posts)
    payload = {
        "case": case_row if isinstance(case_row, dict) else {},
        "posts": posts if isinstance(posts, list) else [],
    }
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO known_entity_archives (archive_id, case_id, case_name, archived_payload, archived_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                archive_id,
                str(case_row.get("case_id") or "").strip(),
                str(case_row.get("case_name") or "Untitled Case").strip() or "Untitled Case",
                json.dumps(payload, ensure_ascii=True),
                archived_at,
            ),
        )
        for selector in selectors:
            conn.execute(
                """
                INSERT OR IGNORE INTO known_entity_selectors (archive_id, selector_type, selector_value, selector_display, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    archive_id,
                    selector["type"],
                    selector["value"],
                    selector["display"],
                    archived_at,
                ),
            )
        conn.commit()
    return {
        "archive_id": archive_id,
        "case_id": str(case_row.get("case_id") or "").strip(),
        "case_name": str(case_row.get("case_name") or "Untitled Case").strip() or "Untitled Case",
        "selector_count": len(selectors),
        "archived_at": archived_at,
    }


def match_known_entities(selectors: list[dict[str, Any]] | None, *, db_path: str = "osint_data.db") -> list[dict[str, Any]]:
    init_known_entities_db(db_path)
    normalized: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in selectors or []:
        if not isinstance(item, dict):
            continue
        pair = _normalize_selector(item.get("type"), item.get("value"))
        if not pair or pair in seen:
            continue
        seen.add(pair)
        normalized.append(pair)
    if not normalized:
        return []

    matches: dict[str, dict[str, Any]] = {}
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        for selector_type, selector_value in normalized:
            rows = conn.execute(
                """
                SELECT
                    a.archive_id,
                    a.case_id,
                    a.case_name,
                    a.archived_at,
                    s.selector_type,
                    s.selector_value,
                    s.selector_display
                FROM known_entity_selectors s
                JOIN known_entity_archives a ON a.archive_id = s.archive_id
                WHERE s.selector_type = ? AND s.selector_value = ?
                """,
                (selector_type, selector_value),
            ).fetchall()
            for row in rows:
                archive_id = str(row["archive_id"] or "").strip()
                if not archive_id:
                    continue
                item = matches.get(archive_id)
                if item is None:
                    item = {
                        "archive_id": archive_id,
                        "case_id": str(row["case_id"] or "").strip(),
                        "case_name": str(row["case_name"] or "Untitled Case").strip() or "Untitled Case",
                        "archived_at": str(row["archived_at"] or "").strip(),
                        "match_count": 0,
                        "matched_selectors": [],
                    }
                    matches[archive_id] = item
                item["match_count"] = int(item["match_count"]) + 1
                item["matched_selectors"].append(
                    {
                        "type": str(row["selector_type"] or "").strip(),
                        "value": str(row["selector_value"] or "").strip(),
                        "display": str(row["selector_display"] or "").strip(),
                    }
                )
    return sorted(
        list(matches.values()),
        key=lambda item: (-int(item.get("match_count") or 0), str(item.get("archived_at") or "")),
    )


def restore_archived_case(archive_id: str, *, db_path: str = "osint_data.db") -> dict[str, Any] | None:
    init_known_entities_db(db_path)
    archive_key = str(archive_id or "").strip()
    if not archive_key:
        return None
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT archive_id, case_id, case_name, archived_payload, archived_at
            FROM known_entity_archives
            WHERE archive_id = ?
            """,
            (archive_key,),
        ).fetchone()
    if not row:
        return None
    try:
        payload = json.loads(str(row[3] or "{}"))
    except json.JSONDecodeError:
        payload = {}
    case_row = payload.get("case") if isinstance(payload, dict) else {}
    posts = payload.get("posts") if isinstance(payload, dict) else []
    case_row = case_row if isinstance(case_row, dict) else {}
    posts = posts if isinstance(posts, list) else []

    from panopto.storage.posts import create_case, save_posts

    created_case = create_case(
        case_name=str(case_row.get("case_name") or "Untitled Case"),
        status=str(case_row.get("status") or "Open"),
        threat_level=str(case_row.get("threat_level") or "Low Threat"),
        data_retention_period=str(case_row.get("data_retention_period") or "3 months"),
        known_location=str(case_row.get("known_location") or ""),
        poi_image_url=str(case_row.get("poi_image_url") or ""),
        case_notes=case_row.get("case_notes") if isinstance(case_row.get("case_notes"), dict) else {},
        metadata_tags=case_row.get("metadata_tags") if isinstance(case_row.get("metadata_tags"), list) else [],
        db_path=db_path,
    )
    restored_posts = save_posts(posts, db_path=db_path, case_id=str(created_case.get("case_id") or "").strip())
    return {
        "archive_id": str(row[0] or "").strip(),
        "original_case_id": str(row[1] or "").strip(),
        "archived_at": str(row[4] or "").strip(),
        "case": created_case,
        "restored_posts": restored_posts,
    }
