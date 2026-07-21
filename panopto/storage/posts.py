"""SQLite persistence for locally collected Twitter OSINT data."""

from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
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
                data_retention_period TEXT NOT NULL DEFAULT '3 months',
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
        if "data_retention_period" not in case_columns:
            conn.execute("ALTER TABLE cases ADD COLUMN data_retention_period TEXT NOT NULL DEFAULT '3 months'")
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


def _valid_data_retention_period(value: str) -> str:
    allowed = {
        "24h": "24h",
        "24 hours": "24h",
        "1 week": "1 week",
        "3 week": "3 week",
        "3 weeks": "3 week",
        "6 weeks": "6 weeks",
        "3 months": "3 months",
        "1 year": "1 year",
    }
    raw = str(value or "").strip()
    return allowed.get(raw, allowed.get(raw.lower(), "3 months"))


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
    if value.lower().startswith(("http://", "https://", "data:image/")) or value.startswith("/"):
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
    data_retention_period: str = "3 months",
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
        "data_retention_period": _valid_data_retention_period(data_retention_period),
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
            INSERT INTO cases (case_id, case_name, status, threat_level, data_retention_period, known_location, poi_image_url, case_notes, metadata_tags, opened_at, last_edited_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["case_id"],
                row["case_name"],
                row["status"],
                row["threat_level"],
                row["data_retention_period"],
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
                c.data_retention_period,
                c.known_location,
                c.poi_image_url,
                c.case_notes,
                c.metadata_tags,
                c.opened_at,
                c.last_edited_at,
                COUNT(p.id) AS post_count
            FROM cases c
            LEFT JOIN twitter_posts p ON p.case_id = c.case_id
            GROUP BY c.case_id, c.case_name, c.status, c.threat_level, c.data_retention_period, c.known_location, c.poi_image_url, c.case_notes, c.metadata_tags, c.opened_at, c.last_edited_at
            ORDER BY c.last_edited_at DESC
            """
        ).fetchall()
    output: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["data_retention_period"] = _valid_data_retention_period(item.get("data_retention_period"))
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
    data_retention_period: str | None = None,
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
    if data_retention_period is not None:
        updates.append("data_retention_period = ?")
        params.append(_valid_data_retention_period(data_retention_period))
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
            SELECT case_id, case_name, status, threat_level, data_retention_period, known_location, poi_image_url, case_notes, metadata_tags, opened_at, last_edited_at
            FROM cases
            WHERE case_id = ?
            """,
            (case_id,),
        ).fetchone()
        if not row:
            return None
    parsed_tags: list[str] = []
    try:
        decoded = json.loads(str(row[8] or "[]"))
        if isinstance(decoded, list):
            parsed_tags = [str(tag) for tag in decoded if str(tag).strip()]
    except json.JSONDecodeError:
        parsed_tags = []
    parsed_notes: dict[str, Any] = {}
    try:
        decoded_notes = json.loads(str(row[7] or "{}"))
        parsed_notes = _normalize_case_notes(decoded_notes)
    except json.JSONDecodeError:
        parsed_notes = {}
    return {
        "case_id": row[0],
        "case_name": row[1],
        "status": row[2],
        "threat_level": row[3],
        "data_retention_period": _valid_data_retention_period(row[4]),
        "known_location": row[5],
        "poi_image_url": str(row[6] or "").strip(),
        "case_notes": parsed_notes,
        "metadata_tags": parsed_tags,
        "opened_at": row[9],
        "last_edited_at": row[10],
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


def _demo_profile(
    *,
    site: str,
    url: str,
    image_url: str,
    screenshot_url: str,
    collection_ready: bool = False,
    **extra: Any,
) -> dict[str, Any]:
    row = {
        "site": site,
        "url": url,
        "image_url": image_url,
        "screenshot_url": screenshot_url,
        "collection_ready": collection_ready,
    }
    row.update({key: value for key, value in extra.items() if value not in (None, "")})
    return row


def _demo_recon_row(
    *,
    selector_type: str,
    selector: str,
    site: str,
    profile_url: str,
    source: str = "scanner",
    screenshot_url: str = "",
    supported_for_collection: bool = False,
    reason: str = "profile_confirmed",
    picture_url: str = "",
    **extra: Any,
) -> dict[str, Any]:
    site_key = site.lower().replace("twitter/x", "twitter").replace(" ", "_")
    row = {
        "selector_type": selector_type,
        "selector": selector,
        "site": site,
        "site_key": site_key,
        "status": "present",
        "profile_url": profile_url,
        "reason": reason,
        "source": source,
        "supported_for_collection": supported_for_collection,
        "screenshot_url": screenshot_url,
        "picture_url": picture_url,
    }
    row.update({key: value for key, value in extra.items() if value not in (None, "")})
    return row


def _build_demo_recon_snapshot(*, avatar: str, alias_avatar: str) -> dict[str, Any]:
    selectors = [
        {"type": "username", "value": "demo_subject"},
        {"type": "username", "value": "graymarketmaps"},
        {"type": "email", "value": "demo.subject@proton.me"},
        {"type": "email", "value": "ops.demo@pm.me"},
        {"type": "phone", "value": "+1 202 555 0199"},
        {"type": "name", "value": "John R. Smith"},
        {"type": "location", "value": "Washington, DC"},
    ]
    results = [
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="Twitter/X",
            profile_url="https://x.com/demo_subject",
            screenshot_url="/recon_shots/twitter-cbd0039562da9a05.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="Reddit",
            profile_url="https://www.reddit.com/user/demo_subject",
            screenshot_url="/recon_shots/reddit-1bbd6bf419da4867.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="Bluesky",
            profile_url="https://bsky.app/profile/demo_subject.bsky.social",
            screenshot_url="/recon_shots/bluesky-e669742696b86463.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="Instagram",
            profile_url="https://www.instagram.com/demo_subject/",
            screenshot_url="/recon_shots/instagram-d9f5b517be1d2384.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="TikTok",
            profile_url="https://www.tiktok.com/@demo_subject",
            screenshot_url="/recon_shots/tiktok-d9f524822ecc46f5.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="demo_subject",
            site="YouTube",
            profile_url="https://www.youtube.com/@demo_subject",
            screenshot_url="/recon_shots/youtube-f37afb94a246ea31.png?v=1",
            supported_for_collection=True,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="demo.subject@proton.me",
            site="GitHub",
            profile_url="https://github.com/demo-subject-labs",
            source="osint_industries",
            screenshot_url="/recon_shots/github-58fa2a45fb9f6f78.png?v=1",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="demo.subject@proton.me",
            site="LinkedIn",
            profile_url="https://www.linkedin.com/in/demo-subject",
            source="pdl",
            screenshot_url="/recon_shots/linkedin-d5d654847d55de7c.png?v=1",
        ),
        _demo_recon_row(
            selector_type="username",
            selector="graymarketmaps",
            site="Threads",
            profile_url="https://www.threads.net/@graymarketmaps",
            source="osint_industries",
            screenshot_url="/recon_shots/threads-a4c0302526055f53.png?v=1",
        ),
        _demo_recon_row(
            selector_type="username",
            selector="graymarketmaps",
            site="GitLab",
            profile_url="https://gitlab.com/graymarketmaps",
            source="scanner",
            screenshot_url="/recon_shots/gitlab-9cdb60fea3bb25d9.png?v=1",
        ),
        {
            "selector_type": "email",
            "selector": "ops.demo@pm.me",
            "site": "protonmail",
            "site_key": "protonmail",
            "status": "present",
            "profile_url": "",
            "reason": "account_registration_signal",
            "source": "osint_industries",
            "supported_for_collection": False,
        },
    ]
    collection_targets = [
        {"platform": "twitter", "username": "demo_subject"},
        {"platform": "reddit", "username": "demo_subject"},
        {"platform": "bluesky", "username": "demo_subject.bsky.social"},
        {"platform": "instagram", "username": "demo_subject"},
        {"platform": "tiktok", "username": "demo_subject"},
        {"platform": "youtube", "username": "demo_subject"},
    ]
    osint_profiles = [
        {
            "module": "github",
            "query_type": "email",
            "query_value": "demo.subject@proton.me",
            "username": "demo-subject-labs",
            "name": "J. Smith",
            "profile_url": "https://github.com/demo-subject-labs",
            "website": "https://github.com",
            "bio": "Mapping scripts, transit notes, and private planning tools.",
            "registered": "True",
            "creation_date": "2021-02-14T12:40:00",
            "last_seen": "2026-05-29T22:14:00",
            "followers": "14",
            "following": "3",
            "picture_url": alias_avatar,
            "screenshot_url": "/recon_shots/github-58fa2a45fb9f6f78.png?v=1",
        },
        {
            "module": "strava",
            "query_type": "email",
            "query_value": "demo.subject@proton.me",
            "username": "graymarketmaps",
            "name": "John S.",
            "profile_url": "https://www.strava.com/athletes/demo-subject",
            "website": "https://www.strava.com",
            "location": "Washington, DC",
            "creation_date": "2019-09-18T09:20:00",
            "last_seen": "2026-05-31T13:05:00",
            "picture_url": avatar,
        },
        {
            "module": "chess",
            "query_type": "username",
            "query_value": "graymarketmaps",
            "username": "graymarketmaps",
            "name": "graymarketmaps",
            "profile_url": "https://www.chess.com/member/graymarketmaps",
            "website": "https://www.chess.com",
            "registered": "True",
            "creation_date": "2020-06-02T16:11:00",
            "last_seen": "2026-05-27T23:41:00",
        },
    ]
    person_data_profile = {
        "id": "pdl_demo_subject_001",
        "query_type": "email",
        "query_value": "demo.subject@proton.me",
        "full_name": "John Robert Smith",
        "first_name": "John",
        "last_name": "Smith",
        "sex": "male",
        "birth_year": "1991",
        "location_name": "Washington, District of Columbia, United States",
        "location_locality": "Washington",
        "location_region": "District of Columbia",
        "location_country": "United States",
        "job_title": "Contract Logistics Coordinator",
        "job_company_name": "Capitol Route Services",
        "job_company_website": "https://example.org/capitol-route-services",
        "linkedin_url": "https://www.linkedin.com/in/demo-subject",
        "twitter_url": "https://x.com/demo_subject",
        "github_url": "https://github.com/demo-subject-labs",
        "facebook_url": "https://www.facebook.com/demo.subject.synthetic",
        "professional_email": "john.smith@example.org",
        "work_email": "john.smith@example.org",
        "personal_emails": ["demo.subject@proton.me", "ops.demo@pm.me"],
        "mobile_phone": "+1 202 555 0199",
        "personal_phones": ["+1 202 555 0199"],
        "interests": ["urban exploration", "private mapping", "amateur radio", "logistics"],
        "skills": ["route planning", "Python", "open-source mapping", "radio scanning"],
        "picture_url": avatar,
        "profiles": [
            "https://x.com/demo_subject",
            "https://github.com/demo-subject-labs",
            "https://www.linkedin.com/in/demo-subject",
            "https://www.reddit.com/user/demo_subject",
        ],
    }
    numverify_profiles = [
        {
            "query_type": "phone",
            "query_value": "+1 202 555 0199",
            "valid": True,
            "number": "+12025550199",
            "local_format": "(202) 555-0199",
            "international_format": "+1 202-555-0199",
            "country_prefix": "+1",
            "country_code": "US",
            "country_name": "United States of America",
            "location": "Washington DC",
            "carrier": "Demo Wireless",
            "line_type": "mobile",
        }
    ]
    leads = [
        {"site": "Twitter/X", "profile_url": "https://x.com/demo_subject", "screenshot_url": "/recon_shots/twitter-cbd0039562da9a05.png?v=1"},
        {"site": "GitHub", "profile_url": "https://github.com/demo-subject-labs", "source": "osint_industries", "screenshot_url": "/recon_shots/github-58fa2a45fb9f6f78.png?v=1"},
        {"site": "LinkedIn", "profile_url": "https://www.linkedin.com/in/demo-subject", "source": "pdl", "screenshot_url": "/recon_shots/linkedin-d5d654847d55de7c.png?v=1"},
        {"site": "email", "lead_type": "attribute", "attribute": "Personal email", "value": "ops.demo@pm.me", "source": "pdl", "profile_name": "John Robert Smith"},
        {"site": "phone", "lead_type": "attribute", "attribute": "Mobile phone", "value": "+1 202 555 0199", "source": "pdl", "profile_name": "John Robert Smith"},
    ]
    breach_records = [
        {
            "breachName": "MetroForum Leak",
            "source": "Breach intelligence",
            "selectorType": "email",
            "selectorValue": "demo.subject@proton.me",
            "severity": "High",
            "fields": [["Email", "demo.subject@proton.me"], ["Username", "graymarketmaps"], ["Last IP City", "Washington, DC"]],
        },
        {
            "breachName": "HobbyRadio Paste",
            "source": "Breach intelligence",
            "selectorType": "username",
            "selectorValue": "graymarketmaps",
            "severity": "Medium",
            "fields": [["Recovery Email", "ops.demo@pm.me"], ["Phone", "+1 202 555 0199"]],
        },
    ]
    return {
        "generated_at": _utc_now_iso(),
        "source": "canned_conference_demo",
        "payload": {
            "selectors": selectors,
            "results": results,
            "collection_targets": collection_targets,
            "leads": leads,
            "osint_profiles": osint_profiles,
            "osint_spec_results": [
                {"module": "github", "query_type": "email", "query_value": "demo.subject@proton.me", "title": "Repository activity", "fields": {"repos": "7", "last_push": "2026-05-29"}},
                {"module": "strava", "query_type": "email", "query_value": "demo.subject@proton.me", "title": "Route traces", "fields": {"city": "Washington, DC", "activities": "42"}},
            ],
            "numverify_profiles": numverify_profiles,
            "person_data_profile": person_data_profile,
            "person_data_profiles": [person_data_profile],
            "breach_records": breach_records,
            "api_modules_queried": [
                {"module": "person_data_labs", "label": "People Data Labs"},
                {"module": "osint_industries", "label": "OSINT Industries"},
                {"module": "numverify", "label": "Numverify"},
                {"module": "breach_demo", "label": "Breach intelligence"},
            ],
            "collection_ready_profiles": [row for row in results if row.get("supported_for_collection")],
            "unsupported_profiles_with_url": [
                row for row in results if row.get("status") == "present" and row.get("profile_url") and not row.get("supported_for_collection")
            ],
            "known_present_without_url": [
                row for row in results if row.get("status") == "present" and not row.get("profile_url")
            ],
            "checked": len(results),
            "present_count": len([row for row in results if row.get("status") == "present"]),
        },
    }


def _build_demo_extra_posts(*, username: str, now: datetime, avatar: str, alias_avatar: str) -> list[dict[str, Any]]:
    return [
        {
            "post_id": "demo-conf-twitter-1",
            "platform": "Twitter",
            "username": username,
            "content": "Pinned the conference-center loading dock map, badge desk shift change, and Union Station walking route into the private notes folder.",
            "timestamp": now.replace(hour=7, minute=42, second=0, microsecond=0).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-conf-twitter-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "identity_intel_assessment": {
                    "theme": "Route planning near a public venue",
                    "selectors": {"locations": ["Union Station", "conference-center loading dock"]},
                    "rationale": "Mentions specific venue-adjacent locations and operational timing.",
                },
                "llm_assessment": {
                    "tagged_primary": ["Pathway Warning Behavior"],
                    "tagged_secondary": ["Leakage"],
                    "underlying_theme": "Operational venue mapping",
                    "rationale": "Specific route and access point language suggests planning behavior in the synthetic scenario.",
                },
            },
        },
        {
            "post_id": "demo-conf-reddit-1",
            "platform": "Reddit",
            "username": username,
            "content": "Burner inbox is ops.demo@pm.me. Do not use my work email. Phone stays off until after the 8:30 meetup.",
            "timestamp": now.replace(hour=9, minute=18, second=0, microsecond=0).isoformat(),
            "source_url": f"https://www.reddit.com/user/{username}/comments/demo-conf-reddit-1",
            "post_type": "comment",
            "metadata": {
                "profile_image_url": avatar,
                "identity_intel_assessment": {
                    "theme": "Selector disclosure",
                    "selectors": {"emails": ["ops.demo@pm.me"], "times": ["8:30"]},
                    "rationale": "Post exposes an alternate email and timing reference.",
                },
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": ["Personal grievance and concealment"],
                    "underlying_theme": "Covert communications",
                    "rationale": "References a burner inbox and communication discipline.",
                },
            },
        },
        {
            "post_id": "demo-conf-instagram-1",
            "platform": "Instagram",
            "username": "graymarketmaps",
            "content": "Carousel: hotel roof sightlines, badge pickup queue, and a clean view of the service alley from the skywalk.",
            "timestamp": now.replace(hour=12, minute=6, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.instagram.com/p/demo-conf-instagram-1/",
            "post_type": "post",
            "metadata": {
                "profile_image_url": alias_avatar,
                "image_urls": [],
                "llm_assessment": {
                    "tagged_primary": ["Pathway Warning Behavior"],
                    "tagged_secondary": ["Preoccupation"],
                    "underlying_theme": "Surveillance-style location posting",
                    "rationale": "Describes sightlines and access views in the synthetic conference scenario.",
                },
            },
        },
        {
            "post_id": "demo-conf-youtube-1",
            "platform": "YouTube",
            "username": username,
            "content": "Uploaded unlisted clip: scanner audio test, radio check, and downtown walk-through notes.",
            "timestamp": now.replace(hour=17, minute=24, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.youtube.com/watch?v=demo-conf-youtube-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": alias_avatar,
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": ["Capability interest"],
                    "underlying_theme": "Communications capability interest",
                    "rationale": "Radio/scanner testing is treated as a capability-relevant demo signal.",
                },
            },
        },
        {
            "post_id": "demo-conf-bluesky-1",
            "platform": "Bluesky",
            "username": "demo_subject.bsky.social",
            "content": "If the main account disappears, graymarketmaps has the route notes and the GitHub repo has the geofence script.",
            "timestamp": now.replace(hour=20, minute=33, second=0, microsecond=0).isoformat(),
            "source_url": "https://bsky.app/profile/demo_subject.bsky.social/post/demo-conf-bluesky-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Leakage"],
                    "underlying_theme": "Cross-platform alias linkage",
                    "rationale": "Links backup alias and code repository to the subject in the synthetic data.",
                },
            },
        },
    ]


def _build_demo_case_playbook() -> dict[str, Any]:
    return {
        "title": "Synthetic webinar pivot: selector to closure",
        "opening_prompt": (
            "Start with the known username @demo_subject, pivot to linked selectors, collect supported profiles, "
            "triage warning behaviours, and close the case with a concise risk disposition."
        ),
        "completion_criteria": [
            "Confirm cross-platform identity linkage between @demo_subject, graymarketmaps, and demo-subject-labs.",
            "Identify at least two selector pivots: demo.subject@proton.me, ops.demo@pm.me, and +1 202 555 0199.",
            "Surface venue logistics, fallback communications, route planning, and capability-interest signals.",
            "Use LLM warning tags to separate high-signal posts from routine Washington, DC activity.",
            "Export a case report or save the case as Watchlist after documenting recommended next actions.",
        ],
        "ai_pivot_steps": [
            {
                "stage": "Seed selector",
                "query": "@demo_subject OR demo.subject@proton.me",
                "expected_result": "Finds the primary account plus the Reddit selector disclosure post.",
                "talk_track": "Show how one username quickly expands into email, phone, and profile leads.",
            },
            {
                "stage": "Alias linkage",
                "query": "graymarketmaps OR demo-subject-labs",
                "expected_result": "Returns the Bluesky alias-linkage post and enrichment records tying the alias to GitHub.",
                "talk_track": "Use the entity graph and footprint views to explain identity resolution.",
            },
            {
                "stage": "Venue logistics",
                "query": "route OR loading dock OR service alley",
                "expected_result": "Highlights venue-adjacent posts about access points, sightlines, and route notes.",
                "talk_track": "Pivot from broad social collection into specific operational context.",
            },
            {
                "stage": "Fallback communications",
                "query": "ops.demo@pm.me OR burner OR fallback channel",
                "expected_result": "Finds communication discipline posts and the alternate inbox.",
                "talk_track": "Show selector extraction and explain why alternate channels change triage priority.",
            },
            {
                "stage": "Assessment",
                "query": "\"Pathway Warning Behavior\" OR \"Capability interest\"",
                "expected_result": "Uses stored LLM labels to isolate posts worth analyst review.",
                "talk_track": "Demonstrate AI-assisted prioritization without claiming the demo data is real.",
            },
        ],
        "analyst_closeout": {
            "recommended_status": "Watchlist",
            "watchlist_cadence": "Daily",
            "summary": (
                "The synthetic record supports a high-concern demo disposition because independent fake sources "
                "connect identity selectors, venue logistics, fallback communications, and capability interest. "
                "Recommended webinar closeout is Watchlist with daily review cadence and exported PDF notes."
            ),
        },
    }


def create_demo_case(db_path: str = "osint_data.db") -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    demo_avatar = "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=256&q=80"
    demo_alias_avatar = "https://images.unsplash.com/photo-1542204625-de293a8e5b9c?auto=format&fit=crop&w=256&q=80"
    known_profiles = [
        _demo_profile(site="Twitter/X / @demo_subject", url="https://x.com/demo_subject", image_url=demo_avatar, screenshot_url="/recon_shots/twitter-cbd0039562da9a05.png?v=1", collection_ready=True),
        _demo_profile(site="Reddit / u/demo_subject", url="https://www.reddit.com/user/demo_subject", image_url=demo_avatar, screenshot_url="/recon_shots/reddit-1bbd6bf419da4867.png?v=1", collection_ready=True),
        _demo_profile(site="Bluesky / @demo_subject.bsky.social", url="https://bsky.app/profile/demo_subject.bsky.social", image_url=demo_avatar, screenshot_url="/recon_shots/bluesky-e669742696b86463.png?v=1", collection_ready=True),
        _demo_profile(site="Instagram / @demo_subject", url="https://www.instagram.com/demo_subject/", image_url=demo_alias_avatar, screenshot_url="/recon_shots/instagram-d9f5b517be1d2384.png?v=1", collection_ready=True),
        _demo_profile(site="TikTok / @demo_subject", url="https://www.tiktok.com/@demo_subject", image_url=demo_alias_avatar, screenshot_url="/recon_shots/tiktok-d9f524822ecc46f5.png?v=1", collection_ready=True),
        _demo_profile(site="YouTube / @demo_subject", url="https://www.youtube.com/@demo_subject", image_url=demo_alias_avatar, screenshot_url="/recon_shots/youtube-f37afb94a246ea31.png?v=1", collection_ready=True),
        _demo_profile(site="GitHub / @demo-subject-labs", url="https://github.com/demo-subject-labs", image_url=demo_alias_avatar, screenshot_url="/recon_shots/github-58fa2a45fb9f6f78.png?v=1"),
        _demo_profile(site="LinkedIn / demo-subject", url="https://www.linkedin.com/in/demo-subject", image_url=demo_alias_avatar, screenshot_url="/recon_shots/linkedin-d5d654847d55de7c.png?v=1"),
        _demo_profile(site="Threads / @graymarketmaps", url="https://www.threads.net/@graymarketmaps", image_url=demo_alias_avatar, screenshot_url="/recon_shots/threads-a4c0302526055f53.png?v=1"),
        _demo_profile(site="GitLab / @graymarketmaps", url="https://gitlab.com/graymarketmaps", image_url=demo_alias_avatar, screenshot_url="/recon_shots/gitlab-9cdb60fea3bb25d9.png?v=1"),
    ]
    case = create_case(
        case_name="DEMO CASE - POI SMITH, John R.",
        status="Under Investigation",
        threat_level="High Threat",
        data_retention_period="1 week",
        known_location="Washington, DC",
        poi_image_url=demo_avatar,
        case_notes={
            "name": "SMITH, John",
            "location": "Washington, DC",
            "age": "34",
            "akas": "Johnny Smith, J. Smith, @demo_subject, graymarketmaps, demo-subject-labs",
            "subject_image_url": demo_avatar,
            "context": (
                "Synthetic conference walkthrough case. The subject has a fully fake digital footprint across "
                "social, developer, enrichment, phone, and breach-style demo sources. Recent posts cluster around "
                "venue logistics, route planning, alternate communications, and cross-platform alias linkage."
            ),
            "threat_risk_assessment": (
                "High concern in the canned scenario because pathway-style planning, communications discipline, "
                "capability interest, and grievance language appear across independent synthetic sources. "
                "The case is intentionally fictional and designed to exercise the full Orion workflow."
            ),
            "personal_details": (
                "Probable Washington, DC metro presence. Reported contract logistics role at a fictional company. "
                "Selector set includes demo.subject@proton.me, ops.demo@pm.me, john.smith@example.org, "
                "+1 202 555 0199, @demo_subject, graymarketmaps, and GitHub alias demo-subject-labs."
            ),
            "demo_playbook": _build_demo_case_playbook(),
            "selector_emails": "demo.subject@proton.me, ops.demo@pm.me, john.smith@example.org",
            "selector_phone_numbers": "+1 202 555 0199",
            "selector_usernames": "@demo_subject, graymarketmaps, demo-subject-labs",
            "known_profiles": known_profiles,
            "recon_snapshot": _build_demo_recon_snapshot(avatar=demo_avatar, alias_avatar=demo_alias_avatar),
            "report_preferences": {
                "excluded_sections": [],
                "excluded_footprint_result_keys": [],
            },
        },
        metadata_tags=["conference-demo", "synthetic", "full-walkthrough", "digital-footprint"],
        db_path=db_path,
    )
    posts = build_demo_posts(username="demo_subject", now=now)
    posts.extend(_build_demo_extra_posts(username="demo_subject", now=now, avatar=demo_avatar, alias_avatar=demo_alias_avatar))
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


def _build_vip_threat_recon_snapshot(*, avatar: str, alias_avatar: str) -> dict[str, Any]:
    social_avatar = "/demo_avatars/stephen-brooks-social.png"
    professional_avatar = "/demo_avatars/stephen-brooks-professional.png"
    running_avatar = "/demo_avatars/stephen-brooks-running.png"
    twitter_avatar = "/demo_avatars/vaporwave-punisher-x.svg"
    reddit_avatar = "/demo_avatars/vaporwave-punisher-reddit.svg"
    controller_avatar = "/demo_avatars/gamer-controller.svg"
    vaporwave_avatar = "/demo_avatars/meme-vaporwave.svg"
    forum_avatar = "/demo_avatars/retro-forum-face.svg"
    selectors = [
        {"type": "username", "value": "voidpill3d"},
        {"type": "username", "value": "silverhandsteve"},
        {"type": "username", "value": "stevebrooks98"},
        {"type": "username", "value": "SBrooksBoston"},
        {"type": "email", "value": "silverhandsteve@protonmail.com"},
        {"type": "email", "value": "stephenbrooks@gmail.com"},
        {"type": "name", "value": "Stephen Brooks"},
        {"type": "name", "value": "Steve Brooks"},
        {"type": "name", "value": "S. Brooks"},
        {"type": "date_of_birth", "value": "1998-06-03"},
        {"type": "location", "value": "Jamaica Plain / Roxbury Crossing, Boston, MA"},
        {"type": "location", "value": "Boston, MA"},
    ]
    results = [
        _demo_recon_row(
            selector_type="username",
            selector="voidpill3d",
            site="Twitter/X",
            profile_url="https://x.com/voidpill3d",
            supported_for_collection=True,
            picture_url=twitter_avatar,
        ),
        _demo_recon_row(
            selector_type="username",
            selector="voidpill3d",
            site="Reddit",
            profile_url="https://www.reddit.com/user/voidpill3d",
            supported_for_collection=True,
            picture_url=reddit_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Instagram",
            profile_url="https://www.instagram.com/stevebrooks98/",
            source="osint_industries",
            supported_for_collection=True,
            picture_url=vaporwave_avatar,
            username="stevebrooks98",
            name="Steve Brooks",
            bio="Private account with public highlights for desk builds, concerts, and city walks.",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="TikTok",
            profile_url="https://www.tiktok.com/@stephenbrooks.tech",
            source="osint_industries",
            supported_for_collection=True,
            picture_url=controller_avatar,
            username="stephenbrooks.tech",
            name="Stephen Brooks",
            bio="Short clips about controller repair, budget tools, and 3D-print cleanup.",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="YouTube",
            profile_url="https://www.youtube.com/@StephenBrooksMA",
            source="osint_industries",
            supported_for_collection=True,
            picture_url=professional_avatar,
            username="StephenBrooksMA",
            name="Stephen Brooks",
            bio="Unpolished tutorial uploads for home lab notes, slicer settings, and scanner audio cleanup.",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="GitHub",
            profile_url="https://github.com/voidpill3d",
            source="osint_industries",
            picture_url=forum_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Twitch",
            profile_url="https://www.twitch.tv/voidpill3d",
            source="osint_industries",
            picture_url=controller_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Steam",
            profile_url="https://steamcommunity.com/id/voidpill3d",
            source="osint_industries",
            picture_url=controller_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Chess.com",
            profile_url="https://www.chess.com/member/voidpill3d",
            source="osint_industries",
            picture_url=vaporwave_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Bluesky",
            profile_url="https://bsky.app/profile/stevebrooks.bsky.social",
            source="osint_industries",
            supported_for_collection=True,
            picture_url=running_avatar,
            username="stevebrooks.bsky.social",
            name="Steve Brooks",
            bio="Running notes, MBTA complaints, and low-volume replies to local tech accounts.",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="LinkedIn",
            profile_url="https://www.linkedin.com/in/stephen-brooks-demo",
            source="pdl",
            picture_url=professional_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="stephenbrooks@gmail.com",
            site="Facebook",
            profile_url="https://www.facebook.com/stephen.brooks.demo",
            source="scanner",
            picture_url=professional_avatar,
            supported_for_collection=True,
            collection_status="Private/Locked",
            collection_note="Collects public group activity only.",
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Strava",
            profile_url="https://www.strava.com/athletes/voidpill3d-demo",
            source="osint_industries",
            picture_url=running_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="Etsy",
            profile_url="https://www.etsy.com/people/silverhandsteve-demo",
            source="breach_demo",
            picture_url=professional_avatar,
        ),
        _demo_recon_row(
            selector_type="email",
            selector="silverhandsteve@protonmail.com",
            site="PlayStation Network",
            profile_url="https://psnprofiles.com/voidpill3d-demo",
            source="breach_demo",
            picture_url=controller_avatar,
        ),
    ]
    collection_targets = [
        {"platform": "twitter", "username": "voidpill3d"},
        {"platform": "reddit", "username": "voidpill3d"},
        {"platform": "instagram", "username": "stevebrooks98"},
        {"platform": "tiktok", "username": "stephenbrooks.tech"},
        {"platform": "youtube", "username": "StephenBrooksMA"},
        {"platform": "bluesky", "username": "stevebrooks.bsky.social"},
        {"platform": "facebook", "username": "stephen.brooks.demo"},
    ]
    strava_route = [
        {"lat": 42.31491, "lon": -71.11161},
        {"lat": 42.31735, "lon": -71.10541},
        {"lat": 42.32187, "lon": -71.10108},
        {"lat": 42.32844, "lon": -71.09522},
        {"lat": 42.33321, "lon": -71.10004},
    ]
    osint_profiles = [
        {
            "module": "strava",
            "query_type": "email",
            "query_value": "silverhandsteve@protonmail.com",
            "username": "voidpill3d",
            "name": "Steve B.",
            "profile_url": "https://www.strava.com/athletes/voidpill3d-demo",
            "website": "https://www.strava.com",
            "location": "Boston, MA",
            "biolocation": "Jamaica Plain, Boston, MA",
            "bio": "Runs before work, tracks shoe mileage, and keeps public notes on neighborhood routes.",
            "last_seen": "2026-06-12T11:42:00",
            "picture_url": avatar,
            "avatar_url": running_avatar,
            "geo_signals": [
                {"kind": "polyline", "label": "Morning run route", "coordinates": strava_route},
                {"kind": "point", "label": "Frequent start point", "lat": 42.31491, "lon": -71.11161},
            ],
        },
        {
            "module": "google_reviews",
            "query_type": "email",
            "query_value": "stephenbrooks@gmail.com",
            "username": "Stephen Brooks",
            "name": "Stephen Brooks",
            "profile_url": "https://maps.google.com/localguides/demo-stephen-brooks",
            "picture_url": professional_avatar,
            "website": "https://maps.google.com",
            "bio": "Occasional local guide reviews for coffee shops, repair counters, and gyms near transit stops.",
            "review_text": "Reliable late pickup near Centre Street; easy walk from the Orange Line after work.",
            "location": "Jamaica Plain / Roxbury Crossing, Boston, MA",
            "biolocation": "Centre Street corridor, Boston, MA",
            "geo_signals": [
                {"kind": "point", "label": "Cafe review", "lat": 42.30982, "lon": -71.11514},
                {"kind": "point", "label": "Gym review", "lat": 42.33206, "lon": -71.09679},
            ],
        },
        {
            "module": "airbnb",
            "query_type": "email",
            "query_value": "silverhandsteve@protonmail.com",
            "username": "silverhandsteve",
            "name": "Steve B.",
            "profile_url": "https://www.airbnb.com/users/show/demo-silverhandsteve",
            "picture_url": running_avatar,
            "website": "https://www.airbnb.com",
            "bio": "Short-stay travel account with sparse reviews and no public contact details.",
            "review_text": "Guest mentioned wanting to be close to the Orange Line and Jamaica Pond.",
            "location": "Boston, MA",
            "biolocation": "Orange Line / Jamaica Pond, Boston, MA",
            "geo_signals": [
                {"kind": "point", "label": "Guest review area", "lat": 42.31652, "lon": -71.10364},
            ],
        },
        {
            "module": "steam",
            "query_type": "email",
            "query_value": "silverhandsteve@protonmail.com",
            "username": "voidpill3d",
            "name": "silverhandsteve",
            "profile_url": "https://steamcommunity.com/id/voidpill3d",
            "picture_url": controller_avatar,
            "website": "https://steamcommunity.com",
            "bio": "Mostly single-player backlog, co-op weekends, and controller repair notes.",
            "location": "Boston, MA",
        },
        {
            "module": "forum",
            "query_type": "email",
            "query_value": "stephenbrooks@gmail.com",
            "username": "SBrooksBoston",
            "name": "S. Brooks",
            "profile_url": "https://forums.example.invalid/u/SBrooksBoston",
            "picture_url": forum_avatar,
            "website": "https://forums.example.invalid",
            "bio": "Low-volume maker forum account discussing slicer settings and desktop support fixes.",
            "location": "Roxbury Crossing, Boston, MA",
            "biolocation": "Roxbury Crossing, Boston, MA",
        },
    ]
    person_data_profile = {
        "id": "pdl_stephen_brooks_demo_001",
        "query_type": "email",
        "query_value": "silverhandsteve@protonmail.com",
        "full_name": "Stephen Brooks",
        "first_name": "Stephen",
        "middle_initial": "A",
        "last_name": "Brooks",
        "aliases": ["Steve Brooks", "Stephen A. Brooks", "S. Brooks", "SBrooksBoston", "silverhandsteve", "voidpill3d"],
        "sex": "male",
        "birth_date": "1998-06-03",
        "birth_year": "1998",
        "location_name": "Boston, Massachusetts, United States",
        "location_locality": "Boston",
        "location_region": "Massachusetts",
        "location_country": "United States",
        "biolocations": ["Jamaica Plain, Boston, MA", "Roxbury Crossing, Boston, MA", "Centre Street corridor, Boston, MA"],
        "job_title": "Help Desk Technician",
        "job_company_name": "Fictional Harbor IT Services",
        "linkedin_url": "https://www.linkedin.com/in/stephen-brooks-demo",
        "facebook_url": "https://www.facebook.com/stephen.brooks.demo",
        "twitter_url": "https://x.com/voidpill3d",
        "professional_email": "stephenbrooks@gmail.com",
        "personal_emails": ["silverhandsteve@protonmail.com", "stephenbrooks@gmail.com"],
        "interests": ["running", "gaming", "3D printing", "anti-corporate grievance forums", "Boston nightlife"],
        "skills": ["desktop support", "Python scripting", "CAD printing", "route mapping"],
        "picture_url": professional_avatar,
        "profiles": [
            "https://x.com/voidpill3d",
            "https://www.linkedin.com/in/stephen-brooks-demo",
            "https://www.facebook.com/stephen.brooks.demo",
            "https://www.strava.com/athletes/voidpill3d-demo",
            "https://steamcommunity.com/id/voidpill3d",
            "https://psnprofiles.com/voidpill3d-demo",
        ],
    }
    breach_records = [
        {
            "breachName": "Twitter/X Breach",
            "source": "Breach intelligence",
            "selectorType": "username",
            "selectorValue": "voidpill3d",
            "severity": "High",
            "fields": [["Username", "voidpill3d"], ["Email", "silverhandsteve@protonmail.com"], ["Created", "2017-09-21"]],
        },
        {
            "breachName": "Etsy Order Export",
            "source": "Breach intelligence",
            "selectorType": "email",
            "selectorValue": "silverhandsteve@protonmail.com",
            "severity": "High",
            "fields": [
                ["Email", "silverhandsteve@protonmail.com"],
                ["Name", "Stephen Brooks"],
                ["Alias", "Steve Brooks"],
                ["Shipping Area", "Jamaica Plain / Roxbury Crossing, Boston, MA"],
                ["Residential Address", "142 Arborway Apt 3B, Boston, MA 02130"],
            ],
        },
        {
            "breachName": "PlayStation Network Breach",
            "source": "Breach intelligence",
            "selectorType": "email",
            "selectorValue": "silverhandsteve@protonmail.com",
            "severity": "High",
            "fields": [["Online ID", "CALLofVOID"], ["Name", "Stephen Brooks"], ["DOB", "1998-06-03"]],
        },
        {
            "breachName": "RetroGameForum Leak",
            "source": "Breach intelligence",
            "selectorType": "username",
            "selectorValue": "SBrooksBoston",
            "severity": "Medium",
            "fields": [["Username", "SBrooksBoston"], ["Email", "stephenbrooks@gmail.com"], ["Location", "Roxbury Crossing, Boston, MA"]],
        },
    ]
    leads = [
        {"site": "Twitter/X", "profile_url": "https://x.com/voidpill3d"},
        {"site": "LinkedIn", "profile_url": "https://www.linkedin.com/in/stephen-brooks-demo", "source": "pdl"},
        {"site": "email", "lead_type": "attribute", "attribute": "Breach email", "value": "silverhandsteve@protonmail.com", "source": "breach_demo", "profile_name": "Stephen Brooks"},
        {"site": "email", "lead_type": "attribute", "attribute": "Pivot email", "value": "silverhandsteve@protonmail.com", "source": "breach_demo", "profile_name": "Stephen Brooks"},
        {"site": "dob", "lead_type": "attribute", "attribute": "Date of birth", "value": "1998-06-03", "source": "breach_demo", "profile_name": "Stephen Brooks"},
    ]
    return {
        "generated_at": _utc_now_iso(),
        "source": "canned_vip_threat_demo",
        "payload": {
            "selectors": selectors,
            "results": results,
            "collection_targets": collection_targets,
            "leads": leads,
            "osint_profiles": osint_profiles,
            "osint_spec_results": [
                {"module": "strava", "query_type": "email", "query_value": "silverhandsteve@protonmail.com", "title": "Route traces", "fields": {"city": "Boston, MA", "activities": "58"}},
                {"module": "google_reviews", "query_type": "email", "query_value": "stephenbrooks@gmail.com", "title": "Review locations", "fields": {"neighborhood": "Jamaica Plain / Roxbury Crossing"}},
                {"module": "airbnb", "query_type": "email", "query_value": "silverhandsteve@protonmail.com", "title": "Guest review", "fields": {"area": "Orange Line / Jamaica Pond"}},
            ],
            "person_data_profile": person_data_profile,
            "person_data_profiles": [person_data_profile],
            "numverify_profiles": [],
            "breach_records": breach_records,
            "api_modules_queried": [
                {"module": "person_data_labs", "label": "People Data Labs"},
                {"module": "osint_industries", "label": "OSINT Industries"},
                {"module": "breach_demo", "label": "Breach intelligence"},
            ],
            "collection_ready_profiles": [row for row in results if row.get("supported_for_collection")],
            "unsupported_profiles_with_url": [
                row for row in results if row.get("status") == "present" and row.get("profile_url") and not row.get("supported_for_collection")
            ],
            "known_present_without_url": [],
            "checked": len(results),
            "present_count": len([row for row in results if row.get("status") == "present"]),
        },
    }


def build_vip_threat_demo_recon(selectors: list[dict[str, str]] | None = None) -> dict[str, Any] | None:
    normalized = [
        {
            "type": str(item.get("type") or "").strip().lower(),
            "value": str(item.get("value") or "").strip().lower().removeprefix("@"),
        }
        for item in (selectors if isinstance(selectors, list) else [])
        if isinstance(item, dict)
    ]
    demo_values = {
        ("username", "voidpill3d"),
        ("username", "silverhandsteve"),
        ("username", "stevebrooks.bsky.social"),
        ("username", "stevebrooks98"),
        ("username", "stephenbrooks.tech"),
        ("username", "stephenbrooksma"),
        ("email", "silverhandsteve@protonmail.com"),
        ("email", "stephenbrooks@gmail.com"),
        ("name", "stephen brooks"),
    }
    if not any((item["type"], item["value"]) in demo_values for item in normalized):
        return None

    demo_avatar = "/demo_avatars/stephen-brooks-social.png"
    demo_alias_avatar = "/demo_avatars/stephen-brooks-professional.png"
    snapshot = _build_vip_threat_recon_snapshot(avatar=demo_avatar, alias_avatar=demo_alias_avatar)
    payload = deepcopy(snapshot.get("payload") or {})
    if normalized:
        payload["selectors"] = [{"type": item["type"], "value": item["value"]} for item in normalized]
    payload["demo"] = True
    payload["demo_label"] = "VIP threat walkthrough"
    username_only = any(item["type"] == "username" and item["value"] == "voidpill3d" for item in normalized) and not any(
        item["type"] in {"email", "name"} for item in normalized
    )
    if username_only:
        results = [
            row for row in payload.get("results", [])
            if str(row.get("selector_type") or "").lower() == "username"
            and str(row.get("selector") or "").lower() == "voidpill3d"
        ]
        breach_records = [
            row for row in payload.get("breach_records", [])
            if str(row.get("breachName") or "") == "Twitter/X Breach"
        ]
        payload.update(
            {
                "results": results,
                "collection_targets": [
                    {"platform": "twitter", "username": "voidpill3d"},
                    {"platform": "reddit", "username": "voidpill3d"},
                ],
                "leads": [
                    {
                        "site": "email",
                        "lead_type": "attribute",
                        "attribute": "Breach email",
                        "value": "silverhandsteve@protonmail.com",
                        "source": "breach_demo",
                    }
                ],
                "osint_profiles": [],
                "osint_spec_results": [],
                "person_data_profile": {},
                "person_data_profiles": [],
                "numverify_profiles": [],
                "breach_records": breach_records,
                "api_modules_queried": [
                    {"module": "scanner", "label": "Profile scanner"},
                    {"module": "breach_demo", "label": "Breach intelligence"},
                ],
                "collection_ready_profiles": [row for row in results if row.get("supported_for_collection")],
                "unsupported_profiles_with_url": [
                    row for row in results if row.get("status") == "present" and row.get("profile_url") and not row.get("supported_for_collection")
                ],
                "known_present_without_url": [],
                "checked": len(results),
                "present_count": len([row for row in results if row.get("status") == "present"]),
            }
        )
    return payload


def _build_vip_threat_extra_posts(*, now: datetime, avatar: str, alias_avatar: str) -> list[dict[str, Any]]:
    running_avatar = "/demo_avatars/stephen-brooks-running.png"
    controller_avatar = "/demo_avatars/gamer-controller.svg"
    vaporwave_avatar = "/demo_avatars/meme-vaporwave.svg"
    forum_avatar = "/demo_avatars/retro-forum-face.svg"
    base = build_demo_posts(username="voidpill3d", now=now)
    posts = [row for row in base if str(row.get("post_id", "")).startswith("demo-llm-")]
    base_avatars = [avatar, alias_avatar, controller_avatar, vaporwave_avatar, forum_avatar, running_avatar]
    for index, row in enumerate(posts):
        row["post_id"] = str(row.get("post_id", "")).replace("demo-llm-", "vip-threat-llm-")
        row["source_url"] = str(row.get("source_url", "")).replace("/status/demo-llm-", "/status/vip-threat-llm-")
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        metadata = dict(metadata)
        metadata["profile_image_url"] = base_avatars[index % len(base_avatars)]
        row["metadata"] = metadata
    scenario_posts = [
        {
            "post_id": "vip-threat-x-1",
            "platform": "Twitter",
            "username": "voidpill3d",
            "content": "Saw ISB has John Browning speaking again. Same polished conference talk, same people pretending the system is working fine.",
            "timestamp": now.replace(hour=7, minute=45, second=0, microsecond=0).isoformat(),
            "source_url": "https://x.com/voidpill3d/status/vip-threat-x-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "llm_assessment": {
                    "tagged_primary": ["Pathway Warning Behavior", "Identification Warning Behavior"],
                    "tagged_secondary": ["Leakage", "Fixation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "ISB conference and CEO target fixation",
                    "rationale": "Directly names the fictional ISB regional finance conference and CEO John Browning while framing violence as grievance-driven redress.",
                },
            },
        },
        {
            "post_id": "vip-threat-x-2",
            "platform": "Twitter",
            "username": "voidpill3d",
            "content": "If you need me, use silverhandsteve@protonmail.com. I barely check the old inbox anymore.",
            "timestamp": now.replace(hour=8, minute=20, second=0, microsecond=0).isoformat(),
            "source_url": "https://x.com/voidpill3d/status/vip-threat-x-2",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "identity_intel_assessment": {
                    "theme": "Email pivot disclosure",
                    "selectors": {"emails": ["silverhandsteve@protonmail.com"]},
                    "rationale": "Links the breach email to the pivot email used in the demo.",
                },
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": ["Personal grievance and concealment"],
                    "underlying_theme": "Fallback communications",
                    "rationale": "Explicit alternate inbox and file-sharing reference.",
                },
            },
        },
        {
            "post_id": "vip-threat-reddit-1",
            "platform": "Reddit",
            "username": "voidpill3d",
            "content": "Long post in r/antiworkfinance: I do not buy the reform talk anymore. ISB and the other finance houses turn people into numbers, then Browning gets applause at conferences for calling it progress.",
            "timestamp": now.replace(hour=9, minute=10, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.reddit.com/user/voidpill3d/comments/vip-threat-reddit-1",
            "post_type": "comment",
            "metadata": {
                "profile_image_url": avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Fixation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Anti-corporate nihilistic grievance",
                    "rationale": "Expresses hopelessness about reform and fixation on the fictional finance company and CEO.",
                },
            },
        },
        {
            "post_id": "vip-threat-reddit-2",
            "platform": "Reddit",
            "username": "voidpill3d",
            "content": "Comment thread: these conferences are mostly executives congratulating each other. ISB Regional Finance feels like another stage for John Browning and the people who made the mess.",
            "timestamp": now.replace(hour=10, minute=28, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.reddit.com/user/voidpill3d/comments/vip-threat-reddit-2",
            "post_type": "comment",
            "metadata": {
                "profile_image_url": avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Fixation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Conference as symbolic target",
                    "rationale": "Frames the fictional conference as a symbolic gathering of corporate power and names the CEO.",
                },
            },
        },
        {
            "post_id": "vip-threat-instagram-1",
            "platform": "Instagram",
            "username": "stevebrooks98",
            "content": "Story caption over the ISB Regional Finance Conference banner downtown: same suits, same promises, same empty future.",
            "timestamp": now.replace(hour=11, minute=35, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.instagram.com/p/vip-threat-instagram-1/",
            "post_type": "post",
            "metadata": {
                "profile_image_url": vaporwave_avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Preoccupation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Conference preoccupation",
                    "rationale": "Shows attention to the fictional conference branding and grievance language without operational detail.",
                },
            },
        },
        {
            "post_id": "vip-threat-tiktok-1",
            "platform": "TikTok",
            "username": "stephenbrooks.tech",
            "content": "Spent too long tweaking a tiny 3D printed bracket today. Funny how much cleaner a build looks when everything lines up exactly.",
            "timestamp": now.replace(hour=13, minute=5, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.tiktok.com/@stephenbrooks.tech/video/vip-threat-tiktok-1",
            "post_type": "video",
            "metadata": {
                "profile_image_url": controller_avatar,
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": ["Capability interest"],
                    "underlying_theme": "3D printing and access-control interest",
                    "rationale": "Capability-adjacent post tied to access-control language.",
                },
            },
        },
        {
            "post_id": "vip-threat-bluesky-1",
            "platform": "Bluesky",
            "username": "stevebrooks.bsky.social",
            "content": "Long run: JP Pond to Roxbury Crossing, coffee on Centre, back by the Orange Line. Same loop clears my head.",
            "timestamp": now.replace(hour=15, minute=12, second=0, microsecond=0).isoformat(),
            "source_url": "https://bsky.app/profile/stevebrooks.bsky.social/post/vip-threat-bluesky-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": running_avatar,
                "identity_intel_assessment": {
                    "theme": "Pattern-of-life location disclosure",
                    "selectors": {"locations": ["Jamaica Pond", "Roxbury Crossing", "Centre Street", "Orange Line"]},
                    "rationale": "Matches the synthetic Strava and review geo bounding area.",
                },
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": [],
                    "underlying_theme": "Routine movement pattern",
                    "rationale": "",
                },
            },
        },
        {
            "post_id": "vip-threat-youtube-1",
            "platform": "YouTube",
            "username": "StephenBrooksMA",
            "content": "Uploaded an unlisted commentary edit: 'ISB, Browning, and the machine that owns tomorrow.' Mostly conference promo clips and my notes over them.",
            "timestamp": now.replace(hour=17, minute=42, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.youtube.com/watch?v=vip-threat-youtube-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": forum_avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Fixation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Corporate oligarch grievance content",
                    "rationale": "Names ISB and John Browning in grievance-focused media content tied to the conference.",
                },
            },
        },
        {
            "post_id": "vip-threat-facebook-1",
            "platform": "Facebook",
            "username": "stephen.brooks.demo",
            "content": "Looks like the ISB Regional Finance Conference is bringing John Browning to Boston. Wild how people like him can talk about markets like the damage is just a spreadsheet line.",
            "timestamp": now.replace(hour=19, minute=4, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.facebook.com/stephen.brooks.demo/posts/vip-threat-facebook-1",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Preoccupation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Named executive and conference preoccupation",
                    "rationale": "Publicly identifies the fictional CEO and conference while linking them to grievance.",
                },
            },
        },
        {
            "post_id": "vip-threat-facebook-group-1",
            "platform": "Facebook",
            "username": "stephen.brooks.demo",
            "content": "Group > Boston North Shore Gun Club: New here. Is the Saturday range orientation open to first-timers, and do you have loaner eye/ear protection or should I bring my own?",
            "timestamp": now.replace(hour=20, minute=18, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.facebook.com/groups/boston-north-shore-gun-club/posts/vip-threat-facebook-group-1",
            "post_type": "group_post",
            "metadata": {
                "profile_image_url": avatar,
                "group_name": "Boston North Shore Gun Club",
                "display_tag": "Group > Boston North Shore Gun Club",
                "group_visibility": "public",
                "collection_context": "public_facebook_group",
                "identity_intel_assessment": {
                    "theme": "Public Facebook group scrape surfaced firearm-adjacent interest",
                    "selectors": {"groups": ["Boston North Shore Gun Club"], "locations": ["North Shore", "Boston"]},
                    "rationale": "Demonstrates collection from a public Facebook group and links the profile to a local gun-club community.",
                },
                "llm_assessment": {
                    "tagged_primary": [],
                    "tagged_secondary": ["Potential capability"],
                    "underlying_theme": "Firearm-adjacent capability interest",
                    "rationale": "A public gun-club group post is capability-relevant in the synthetic VIP-threat workflow, but it is not by itself a direct threat.",
                },
            },
        },
        {
            "post_id": "vip-threat-facebook-2",
            "platform": "Facebook",
            "username": "stephen.brooks.demo",
            "content": "ISB's conference is at the Sarriot Grand Hall conference centre this year. Funny name, but the place looks exactly like the kind of grand hall where Browning would feel at home.",
            "timestamp": now.replace(hour=20, minute=47, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.facebook.com/stephen.brooks.demo/posts/vip-threat-facebook-2",
            "post_type": "post",
            "metadata": {
                "profile_image_url": avatar,
                "identity_intel_assessment": {
                    "theme": "Conference venue reference",
                    "selectors": {"locations": ["Sarriot Grand Hall conference centre"], "organizations": ["ISB"]},
                    "rationale": "Names the fictional conference venue and links it to the ISB event context.",
                },
                "llm_assessment": {
                    "tagged_primary": ["Identification Warning Behavior"],
                    "tagged_secondary": ["Preoccupation", "Personal grievance and nihilistic ideation"],
                    "underlying_theme": "Conference venue preoccupation",
                    "rationale": "Publicly references the fictional ISB conference venue and CEO in grievance-framed language.",
                },
            },
        },
    ]
    return posts + scenario_posts


def _build_vip_threat_case_playbook() -> dict[str, Any]:
    return {
        "title": "ISB conference threat demo: username to report",
        "opening_prompt": (
            "Start with @voidpill3d, show the username breach exposing silverhandsteve@protonmail.com, "
            "pivot to silverhandsteve@protonmail.com, collect supported profiles, review warning signs around "
            "ISB CEO John Browning and the ISB Regional Finance Conference, and export the report."
        ),
        "completion_criteria": [
            "Show username reuse across X, Reddit, Instagram, TikTok, YouTube, and Bluesky.",
            "Show the breach pivot from @voidpill3d to silverhandsteve@protonmail.com.",
            "Use the email pivot to identify Stephen Brooks, DOB 1998-06-03, and the fictional Boston pattern-of-life bounding area.",
            "Use collected posts and warning tags to isolate nihilistic anti-corporate grievance, target focus on ISB CEO John Browning, and conference preoccupation.",
            "Show the public Facebook group scrape as potential capability context, not standalone intent.",
            "Complete report notes and export the case report.",
        ],
        "ai_pivot_steps": [
            {"stage": "Seed selector", "query": "@voidpill3d", "expected_result": "Returns reused social profiles and the Twitter/X synthetic breach.", "talk_track": "Start from the slide threat handle and show account reuse."},
            {"stage": "Email pivot", "query": "silverhandsteve@protonmail.com", "expected_result": "Returns LinkedIn, Facebook, Strava, Etsy, PSN, and breach records.", "talk_track": "Use breach output to pivot from a handle to identity selectors."},
            {"stage": "Identity resolution", "query": "\"Stephen Brooks\" OR stephenbrooks@gmail.com OR \"1998-06-03\"", "expected_result": "Surfaces the fictional name, DOB, and mainstream profiles.", "talk_track": "Show selector corroboration and collated identity fields."},
            {"stage": "Motive and target fixation", "query": "\"ISB\" OR \"John Browning\" OR oligarch OR \"regional finance conference\"", "expected_result": "Finds nihilistic anti-corporate grievance and named executive/conference focus.", "talk_track": "Separate political grievance from actionable threat indicators and show corroboration across platforms."},
            {"stage": "Pattern of life", "query": "\"Jamaica Pond\" OR \"Roxbury Crossing\" OR \"Centre Street\" OR \"Orange Line\"", "expected_result": "Finds route and review signals bounding a Boston suburb area.", "talk_track": "Explain how location traces should be treated as leads, not certainty."},
            {"stage": "Warning signs", "query": "\"Pathway Warning Behavior\" OR \"Identification Warning Behavior\" OR \"Potential capability\"", "expected_result": "Filters collected posts to warning-tagged content.", "talk_track": "Show how collection helps prioritize analyst review."},
        ],
        "analyst_closeout": {
            "recommended_status": "Watchlist",
            "watchlist_cadence": "Daily",
            "summary": (
                "The fictional demo record supports escalation because synthetic selectors, breach pivots, "
                "pattern-of-life leads, and collected posts converge around nihilistic anti-corporate grievance, "
                "named focus on ISB CEO John Browning, conference preoccupation, and capability-adjacent signals."
            ),
        },
    }


def create_vip_threat_demo_case(db_path: str = "osint_data.db") -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    demo_avatar = "/demo_avatars/stephen-brooks-social.png"
    demo_alias_avatar = "/demo_avatars/stephen-brooks-professional.png"
    running_avatar = "/demo_avatars/stephen-brooks-running.png"
    twitter_avatar = "/demo_avatars/vaporwave-punisher-x.svg"
    reddit_avatar = "/demo_avatars/vaporwave-punisher-reddit.svg"
    controller_avatar = "/demo_avatars/gamer-controller.svg"
    vaporwave_avatar = "/demo_avatars/meme-vaporwave.svg"
    forum_avatar = "/demo_avatars/retro-forum-face.svg"
    known_profiles = [
        _demo_profile(site="Twitter/X / @voidpill3d", url="https://x.com/voidpill3d", image_url=twitter_avatar, screenshot_url="", collection_ready=True, username="voidpill3d", selector_type="username", selector_value="voidpill3d", bio="Short posts about games, printer parts, transit delays, and event-security complaints."),
        _demo_profile(site="Reddit / u/voidpill3d", url="https://www.reddit.com/user/voidpill3d", image_url=reddit_avatar, screenshot_url="", collection_ready=True, username="voidpill3d", selector_type="username", selector_value="voidpill3d", bio="Comment history mixes local Boston threads, PC troubleshooting, and hobby fabrication."),
        _demo_profile(site="Instagram / @stevebrooks98", url="https://www.instagram.com/stevebrooks98/", image_url=vaporwave_avatar, screenshot_url="", collection_ready=True, username="stevebrooks98", name="Steve Brooks", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Private account with public highlights for desk builds, concerts, and city walks."),
        _demo_profile(site="TikTok / @stephenbrooks.tech", url="https://www.tiktok.com/@stephenbrooks.tech", image_url=controller_avatar, screenshot_url="", collection_ready=True, username="stephenbrooks.tech", name="Stephen Brooks", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Short clips about controller repair, budget tools, and 3D-print cleanup."),
        _demo_profile(site="YouTube / @StephenBrooksMA", url="https://www.youtube.com/@StephenBrooksMA", image_url=demo_alias_avatar, screenshot_url="", collection_ready=True, username="StephenBrooksMA", name="Stephen Brooks", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Unpolished tutorial uploads for home lab notes, slicer settings, and scanner audio cleanup."),
        _demo_profile(site="GitHub / @voidpill3d", url="https://github.com/voidpill3d", image_url=forum_avatar, screenshot_url="", username="voidpill3d", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Small scripts for file cleanup, map exports, and printer maintenance."),
        _demo_profile(site="Twitch / @voidpill3d", url="https://www.twitch.tv/voidpill3d", image_url=controller_avatar, screenshot_url="", username="voidpill3d", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Inactive stream page used for co-op sessions and occasional speedrun attempts."),
        _demo_profile(site="Steam / voidpill3d", url="https://steamcommunity.com/id/voidpill3d", image_url=controller_avatar, screenshot_url="", username="voidpill3d", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Mostly single-player backlog, co-op weekends, and controller repair notes."),
        _demo_profile(site="Chess.com / voidpill3d", url="https://www.chess.com/member/voidpill3d", image_url=vaporwave_avatar, screenshot_url="", username="voidpill3d", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Casual blitz account with irregular late-night play."),
        _demo_profile(site="Bluesky / @stevebrooks.bsky.social", url="https://bsky.app/profile/stevebrooks.bsky.social", image_url=running_avatar, screenshot_url="", collection_ready=True, username="stevebrooks.bsky.social", name="Steve Brooks", location="Boston, MA", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Running notes, MBTA complaints, and low-volume replies to local tech accounts."),
        _demo_profile(site="LinkedIn / Stephen Brooks", url="https://www.linkedin.com/in/stephen-brooks-demo", image_url=demo_alias_avatar, screenshot_url="", name="Stephen Brooks", location="Boston, MA", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Help desk technician profile with endpoint support and hardware repair experience."),
        _demo_profile(site="Facebook / Stephen Brooks", url="https://www.facebook.com/stephen.brooks.demo", image_url=demo_avatar, screenshot_url="", collection_ready=True, name="Stephen Brooks", selector_type="email", selector_value="stephenbrooks@gmail.com", bio="Private/locked profile; public group activity remains visible."),
        _demo_profile(site="Strava / voidpill3d", url="https://www.strava.com/athletes/voidpill3d-demo", image_url=running_avatar, screenshot_url="", username="voidpill3d", name="Steve B.", location="Jamaica Plain, Boston, MA", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Runs before work, tracks shoe mileage, and keeps public notes on neighborhood routes."),
        _demo_profile(site="Etsy / silverhandsteve", url="https://www.etsy.com/people/silverhandsteve-demo", image_url=demo_alias_avatar, screenshot_url="", username="silverhandsteve", name="Steve Brooks", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Buyer account tied to replacement parts, printed accessories, and hobby electronics."),
        _demo_profile(site="PlayStation Network / voidpill3d", url="https://psnprofiles.com/voidpill3d-demo", image_url=controller_avatar, screenshot_url="", username="voidpill3d", selector_type="email", selector_value="silverhandsteve@protonmail.com", bio="Public trophy card for older shooters, racing games, and co-op titles."),
    ]
    case = create_case(
        case_name="DEMO CASE - VIP THREAT - BROOKS, Stephen",
        status="Under Investigation",
        threat_level="High Threat",
        data_retention_period="1 week",
        known_location="Boston, MA",
        poi_image_url=demo_avatar,
        case_notes={
            "name": "BROOKS, Stephen",
            "location": "Boston, MA",
            "age": "28",
            "dob": "1998-06-03",
            "akas": "Steve Brooks, Stephen A. Brooks, S. Brooks, @voidpill3d, silverhandsteve, SBrooksBoston",
            "subject_image_url": demo_avatar,
            "context": (
                "Synthetic ISB conference threat walkthrough case. The starting selector @voidpill3d expands through "
                "fictional breach records, email pivots, mainstream profiles, and location traces around Jamaica Plain "
                "and Roxbury Crossing in Boston. Collected material frames ISB CEO John Browning and the ISB Regional "
                "Finance Conference as symbols of corporate oligarch power."
            ),
            "threat_risk_assessment": (
                "High concern in the canned scenario because collected posts combine nihilistic worldview statements, "
                "anti-corporate grievances, named focus on ISB CEO John Browning, conference preoccupation, fallback "
                "communications, and capability-adjacent interest. All selectors, breaches, locations, and posts are "
                "fictional demo data."
            ),
            "personal_details": (
                "Stephen (Steve) Brooks. DOB 1998-06-03. Selectors include @voidpill3d, "
                "silverhandsteve@protonmail.com and stephenbrooks@gmail.com. "
                "Fictional pattern-of-life leads bound the Jamaica Plain / Roxbury Crossing area of Boston. "
                "The fictional target context is ISB CEO John Browning at the ISB Regional Finance Conference."
            ),
            "demo_playbook": _build_vip_threat_case_playbook(),
            "selector_emails": "silverhandsteve@protonmail.com, stephenbrooks@gmail.com",
            "selector_usernames": "@voidpill3d, silverhandsteve, stevebrooks.bsky.social, stevebrooks98, StephenBrooksMA, stephenbrooks.tech, SBrooksBoston",
            "known_profiles": known_profiles,
            "recon_snapshot": _build_vip_threat_recon_snapshot(avatar=demo_avatar, alias_avatar=demo_alias_avatar),
            "report_preferences": {
                "excluded_sections": [],
                "excluded_footprint_result_keys": [],
            },
        },
        metadata_tags=["vip-threat-demo", "synthetic", "full-walkthrough", "digital-footprint", "pattern-of-life"],
        db_path=db_path,
    )
    posts = _build_vip_threat_extra_posts(now=now, avatar=demo_avatar, alias_avatar=demo_alias_avatar)
    inserted = save_posts(posts, db_path=db_path, case_id=case["case_id"])
    return {
        "case": case,
        "inserted_posts": inserted,
    }


def seed_vip_threat_demo_posts(case_id: str, db_path: str = "osint_data.db") -> dict[str, Any]:
    clean_case_id = str(case_id or "").strip()
    if not clean_case_id:
        raise ValueError("case_id is required")
    now = datetime.now(timezone.utc)
    demo_avatar = "/demo_avatars/stephen-brooks-social.png"
    demo_alias_avatar = "/demo_avatars/stephen-brooks-professional.png"
    posts = _build_vip_threat_extra_posts(now=now, avatar=demo_avatar, alias_avatar=demo_alias_avatar)
    inserted = save_posts(posts, db_path=db_path, case_id=clean_case_id)
    return {
        "case_id": clean_case_id,
        "inserted_posts": inserted,
        "posts_total": len(posts),
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


def update_post_llm_assessments(
    *,
    updates: list[dict[str, Any]],
    db_path: str = "osint_data.db",
    case_id: str | None = None,
) -> int:
    """Persist llm_assessment metadata updates by row id."""

    init_db(db_path)
    written = 0
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        for item in updates:
            try:
                row_id = int(item.get("row_id"))
            except (TypeError, ValueError):
                continue
            metadata = item.get("metadata")
            if not isinstance(metadata, dict):
                continue
            params: list[Any] = [json.dumps(metadata, ensure_ascii=True), row_id]
            where = "id = ?"
            if case_id:
                where = "id = ? AND case_id = ?"
                params.append(case_id)
            cursor = conn.execute(
                f"""
                UPDATE twitter_posts
                SET raw_metadata = ?
                WHERE {where}
                """,
                tuple(params),
            )
            if cursor.rowcount > 0:
                written += cursor.rowcount
        conn.commit()
    touch_case(case_id, db_path=db_path)
    return written
