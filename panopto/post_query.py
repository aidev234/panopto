"""Post querying and filtering logic."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from panopto.ner import extract_entities
from panopto.threat_signals import build_signal_tags, extract_threat_and_selector_signals

_METRIC_TAIL = re.compile(
    r"(?:\b\d+(?:[.,]\d+)?\s*[kKmM]?\s*(?:likes?|retweets?|reposts?|replies?|comments?|views?)\b)\s*$",
    re.IGNORECASE,
)
_ACTION_TAIL = re.compile(
    r"(?:\b(?:screenshot|share|view profile|watch on twitter(?:/x)?|"
    r"download(?: video| gif| image)?)\b)\s*$",
    re.IGNORECASE,
)
_NUMERIC_COUNTER_TAIL = re.compile(
    r"(?:\b\d+(?:[.,]\d+)?\s*[kKmM]?\b(?:\s+\b\d+(?:[.,]\d+)?\s*[kKmM]?\b){1,7})\s*$",
    re.IGNORECASE,
)
_PROFILE_TIME_FRAGMENT = re.compile(r"\b\d+\s*[smhdw]\b\s+view profile\b", re.IGNORECASE)
_VIEW_PROFILE = re.compile(r"\bview profile\b", re.IGNORECASE)


def parse_day(raw: str) -> date | None:
    if not raw:
        return None
    value = raw.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def normalize_tag(tag: str) -> str:
    value = tag.strip().lower()
    aliases = {
        "comments": "comment",
        "replies": "reply",
        "posts": "post",
        "retweet": "repost",
        "retweets": "repost",
    }
    return aliases.get(value, value)


def _tokenize_boolean_query(query: str) -> list[str]:
    token_pattern = re.compile(r'\s*(\(|\)|\bAND\b|\bOR\b|\bNOT\b|"[^"]+"|[^\s()]+)', re.IGNORECASE)
    tokens = [match.group(1) for match in token_pattern.finditer(query) if match.group(1).strip()]
    return [token.upper() if token.upper() in {"AND", "OR", "NOT", "(", ")"} else token for token in tokens]


def _to_rpn(tokens: list[str]) -> list[str]:
    precedence = {"NOT": 3, "AND": 2, "OR": 1}
    operators = set(precedence)
    output: list[str] = []
    stack: list[str] = []

    for token in tokens:
        if token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()
        elif token in operators:
            while stack and stack[-1] in operators and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)

    while stack:
        output.append(stack.pop())

    return output


def _normalize_term(token: str) -> str:
    value = token[1:-1] if token.startswith('"') and token.endswith('"') else token
    value = value.strip().lower()
    if value.startswith("@") and len(value) > 1:
        value = value[1:]
    return value


def _evaluate_rpn(rpn_tokens: list[str], haystack: str) -> bool:
    stack: list[bool] = []

    for token in rpn_tokens:
        if token == "NOT":
            operand = stack.pop() if stack else False
            stack.append(not operand)
        elif token in {"AND", "OR"}:
            right = stack.pop() if stack else False
            left = stack.pop() if stack else False
            stack.append(left and right if token == "AND" else left or right)
        else:
            stack.append(_normalize_term(token) in haystack)

    return stack[-1] if stack else True


def _matches_query(post: dict[str, str], query: str) -> bool:
    query = query.strip()
    if not query:
        return True

    entity_text = " ".join(
        str(item.get("text", ""))
        for item in post.get("entities", [])
        if isinstance(item, dict)
    )
    threat_text = " ".join(str(item) for item in post.get("threat_matches", []) if str(item).strip())
    selector_text = " ".join(str(item) for item in post.get("selector_matches", []) if str(item).strip())
    llm_primary_text = " ".join(str(item) for item in post.get("llm_primary_warning_behaviours", []) if str(item).strip())
    llm_secondary_text = " ".join(str(item) for item in post.get("llm_secondary_risk_factors", []) if str(item).strip())
    llm_theme_text = str(post.get("llm_underlying_theme", "") or "")
    haystack = " ".join(
        [
            str(post.get("username", "") or ""),
            str(post.get("display_name", "") or ""),
            str(post.get("platform", "") or ""),
            str(post.get("post_type", "") or ""),
            " ".join(post.get("tags", [])),
            entity_text,
            threat_text,
            selector_text,
            llm_primary_text,
            llm_secondary_text,
            llm_theme_text,
            str(post.get("content", "") or ""),
        ]
    ).lower()

    tokens = _tokenize_boolean_query(query)
    if not tokens:
        return True

    try:
        return _evaluate_rpn(_to_rpn(tokens), haystack)
    except Exception:
        return query.lower() in haystack


def _query_terms(query: str) -> list[str]:
    tokens = _tokenize_boolean_query(query.strip())
    return [
        term
        for token in tokens
        if token not in {"AND", "OR", "NOT", "(", ")"}
        if (term := _normalize_term(token))
    ]


def _query_rank(post: dict[str, Any], query: str) -> tuple[int, int, int, int, int]:
    normalized_query = query.strip().lower()
    if not normalized_query:
        return (0, 0, 0, 0, 0)

    username = str(post.get("username", "") or "").lower()
    display_name = str(post.get("display_name", "") or "").lower()
    content = str(post.get("content", "") or "").lower()
    platform = str(post.get("platform", "") or "").lower()
    post_type = str(post.get("post_type", "") or "").lower()
    tags = " ".join(str(tag) for tag in post.get("tags", [])).lower()
    entities = " ".join(str(item.get("text", "")) for item in post.get("entities", []) if isinstance(item, dict)).lower()
    threat_matches = " ".join(str(item) for item in post.get("threat_matches", []) if str(item).strip()).lower()
    selector_matches = " ".join(str(item) for item in post.get("selector_matches", []) if str(item).strip()).lower()
    llm_primary = " ".join(str(item) for item in post.get("llm_primary_warning_behaviours", []) if str(item).strip()).lower()
    llm_secondary = " ".join(str(item) for item in post.get("llm_secondary_risk_factors", []) if str(item).strip()).lower()
    llm_theme = str(post.get("llm_underlying_theme", "") or "").lower()
    metadata_text = " ".join(
        segment
        for segment in [tags, entities, threat_matches, selector_matches, llm_primary, llm_secondary, llm_theme, platform, post_type]
        if segment
    )
    primary_text = " ".join(segment for segment in [username, display_name, content] if segment)
    terms = _query_terms(query)

    direct_phrase = int(bool(normalized_query and normalized_query in primary_text))
    identity_exact = int(normalized_query == username or normalized_query == display_name or normalized_query == f"@{username}")
    identity_prefix = int(
        bool(normalized_query)
        and (
            username.startswith(normalized_query)
            or display_name.startswith(normalized_query)
            or (normalized_query.startswith("@") and username.startswith(normalized_query[1:]))
        )
    )
    term_primary_hits = sum(1 for term in terms if term in primary_text)
    term_metadata_hits = sum(1 for term in terms if term in metadata_text)
    return (direct_phrase, identity_exact, identity_prefix, term_primary_hits, term_metadata_hits)


def _parse_timestamp(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(day, datetime.max.time(), tzinfo=timezone.utc)
    return start, end


def _extract_display_name(content: str, username: str) -> str:
    match = re.search(rf"^\s*([^@\n]{{1,80}}?)\s+@{re.escape(username)}\b", content, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip(" .-·•")
    return username


def _strip_noise(content: str, username: str) -> str:
    if not content:
        return ""

    text = content.strip()
    text = re.sub(
        rf"^\s*[^@\n]{{1,80}}\s+@{re.escape(username)}\s*(?:[·•-]\s*[^ \n]+)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s*[·•|]\s*", " ", text)
    text = _PROFILE_TIME_FRAGMENT.sub(" ", text)
    text = _VIEW_PROFILE.sub(" ", text)
    text = re.sub(r"\breplying to\s+@\w+\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*[\w ._-]{1,80}\s+reposted\b", "", text, flags=re.IGNORECASE)

    while True:
        updated = _METRIC_TAIL.sub("", text).strip()
        updated = _ACTION_TAIL.sub("", updated).strip()
        updated = _NUMERIC_COUNTER_TAIL.sub("", updated).strip()
        if updated == text:
            break
        text = updated

    return re.sub(r"\s+", " ", text).strip(" .-")


def _matches_tags(post: dict[str, Any], include_tags: set[str], exclude_tags: set[str]) -> bool:
    tags = {normalize_tag(tag) for tag in post.get("tags", [])}
    include_tags = {normalize_tag(tag) for tag in include_tags}
    exclude_tags = {normalize_tag(tag) for tag in exclude_tags}

    type_tags = {"post", "repost", "reply", "quote", "comment"}
    platform_tags = {"twitter", "reddit", "tiktok", "bluesky", "instagram", "youtube"}
    include_platform_tags = include_tags.intersection(platform_tags)
    include_types = include_tags.intersection(type_tags)
    include_non_types = include_tags - type_tags - platform_tags

    if include_non_types and not include_non_types.issubset(tags):
        return False
    if include_platform_tags:
        known_platform_present = bool(tags.intersection(platform_tags))
        if known_platform_present and not tags.intersection(include_platform_tags):
            return False
    if include_types and post.get("post_type") not in include_types:
        return False
    if exclude_tags and tags.intersection(exclude_tags):
        return False
    return True


def _post_rank(post: dict[str, Any]) -> tuple[int, int]:
    return (
        1 if post.get("source_url") else 0,
        len(post.get("content", "")),
    )


def _parse_metadata(raw_metadata: str | None) -> dict[str, Any]:
    if not raw_metadata:
        return {}
    try:
        parsed = json.loads(raw_metadata)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def _fetch_posts(db_path: Path, case_id: str = "") -> Iterable[dict[str, str]]:
    if not db_path.exists():
        return []

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        columns = {row[1] for row in conn.execute("PRAGMA table_info(twitter_posts)").fetchall()}
        select_parts = [
            "id",
            "source_post_id",
            "username",
            "content",
            "timestamp",
            "collected_at",
            "case_id" if "case_id" in columns else "NULL AS case_id",
            "raw_metadata" if "raw_metadata" in columns else "NULL AS raw_metadata",
            "platform" if "platform" in columns else "'Twitter' AS platform",
            "post_type" if "post_type" in columns else "'post' AS post_type",
            "source_url" if "source_url" in columns else "NULL AS source_url",
            "referenced_username" if "referenced_username" in columns else "NULL AS referenced_username",
        ]
        rows = conn.execute(f"SELECT {', '.join(select_parts)} FROM twitter_posts").fetchall()

    posts: list[dict[str, Any]] = []
    for row in rows:
        row_case_id = str(row["case_id"] or "") if "case_id" in row.keys() else ""
        if case_id and row_case_id != case_id:
            continue
        username = row["username"] or "unknown"
        platform = (row["platform"] if "platform" in row.keys() else "Twitter") or "Twitter"
        platform_slug = platform.strip().lower()
        raw_content = row["content"] or ""
        cleaned_content = _strip_noise(raw_content, username) if platform_slug == "twitter" else " ".join(raw_content.split())
        if not cleaned_content:
            continue
        post_type = normalize_tag(row["post_type"]) if "post_type" in row.keys() else "post"
        source_url = row["source_url"] if "source_url" in row.keys() else None
        referenced_username = row["referenced_username"] if "referenced_username" in row.keys() else None
        metadata = _parse_metadata(row["raw_metadata"] if "raw_metadata" in row.keys() else None)
        llm_assessment_raw = metadata.get("llm_assessment") if isinstance(metadata.get("llm_assessment"), dict) else {}
        llm_primary_source = llm_assessment_raw.get("tagged_primary")
        if not isinstance(llm_primary_source, list):
            llm_primary_source = llm_assessment_raw.get("primary_warning_behaviours")
        llm_secondary_source = llm_assessment_raw.get("tagged_secondary")
        if not isinstance(llm_secondary_source, list):
            llm_secondary_source = llm_assessment_raw.get("secondary_risk_factors")
        llm_primary = [str(item).strip() for item in llm_primary_source if str(item).strip()] if isinstance(llm_primary_source, list) else []
        llm_secondary = [str(item).strip() for item in llm_secondary_source if str(item).strip()] if isinstance(llm_secondary_source, list) else []
        llm_theme = str(llm_assessment_raw.get("underlying_theme") or "").strip()
        if not llm_primary and not llm_secondary:
            llm_theme = ""
        llm_rationale = str(llm_assessment_raw.get("rationale") or "").strip()
        llm_assessment = {
            "tagged_primary": llm_primary,
            "tagged_secondary": llm_secondary,
            "underlying_theme": llm_theme,
            "rationale": llm_rationale,
        }
        tags = [platform_slug, post_type]
        if referenced_username:
            tags.append("has_reference")
        entities = extract_entities(cleaned_content)
        signals = extract_threat_and_selector_signals(cleaned_content)
        for entity in entities:
            entity_type = str(entity.get("type") or "").strip().lower()
            entity_tag = str(entity.get("tag") or "").strip().lower()
            if entity_type:
                tags.append(f"ner:{entity_type}")
            if entity_tag:
                tags.append(entity_tag)
        tags.extend(build_signal_tags(signals))
        if llm_primary:
            tags.append("llm:primary-warning")
        if llm_secondary:
            tags.append("llm:secondary-risk")
        tags = list(dict.fromkeys(tags))
        platform_name = {"twitter": "Twitter", "reddit": "Reddit", "tiktok": "TikTok", "bluesky": "Bluesky", "instagram": "Instagram", "youtube": "YouTube"}.get(
            platform_slug, platform.strip() or "Unknown"
        )
        posts.append(
            {
                "row_id": row["id"] if "id" in row.keys() else None,
                "post_id": row["source_post_id"] if "source_post_id" in row.keys() else None,
                "username": username,
                "display_name": _extract_display_name(raw_content, username) if platform_slug == "twitter" else username,
                "platform": platform_name,
                "post_type": post_type,
                "source_url": source_url,
                "referenced_username": referenced_username,
                "tags": tags,
                "entities": entities,
                "threat_matches": signals.get("threat_matches", []),
                "threat_categories": signals.get("threat_categories", []),
                "threat_signal_categories": signals.get("threat_signal_categories", []),
                "ideological_matches": signals.get("ideological_matches", []),
                "selector_matches": signals.get("selector_matches", []),
                "emails": signals.get("emails", []),
                "phones": signals.get("phones", []),
                "content": cleaned_content,
                "timestamp": row["timestamp"] or row["collected_at"] or "",
                "metadata": metadata,
                "llm_assessment": llm_assessment,
                "llm_primary_warning_behaviours": llm_primary,
                "llm_secondary_risk_factors": llm_secondary,
                "llm_underlying_theme": llm_theme,
                "llm_rationale": llm_rationale,
                "case_id": row_case_id,
            }
        )

    return posts


def query_posts(
    query: str = "",
    sort_order: str = "newest",
    db_path: Path = Path("osint_data.db"),
    *,
    case_id: str = "",
    start_date: str = "",
    end_date: str = "",
    include_tags: set[str] | None = None,
    exclude_tags: set[str] | None = None,
) -> dict[str, object]:
    include_tags = include_tags or set()
    exclude_tags = exclude_tags or set()
    start_day = parse_day(start_date)
    end_day = parse_day(end_date)
    start_dt = _day_bounds(start_day)[0] if start_day else None
    end_dt = _day_bounds(end_day)[1] if end_day else None

    posts = []
    for post in _fetch_posts(db_path, case_id=case_id):
        if not _matches_query(post, query):
            continue
        if not _matches_tags(post, include_tags=include_tags, exclude_tags=exclude_tags):
            continue
        post_dt = _parse_timestamp(post.get("timestamp", ""))
        # Keep undated rows visible; dropping them hides valid Apify items that omit timestamps.
        if (start_dt or end_dt) and post_dt is None:
            posts.append(post)
            continue
        if start_dt and post_dt and post_dt < start_dt:
            continue
        if end_dt and post_dt and post_dt > end_dt:
            continue
        posts.append(post)

    deduped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for post in posts:
        identity = str(post.get("post_id") or "").strip()
        if not identity:
            identity = f"{post.get('timestamp','')}|{post.get('content','')}"
        key = (
            str(post.get("platform", "")).strip().lower(),
            post.get("username", ""),
            identity,
        )
        existing = deduped.get(key)
        if not existing or _post_rank(post) > _post_rank(existing):
            deduped[key] = post

    final_posts = list(deduped.values())
    final_posts.sort(key=lambda post: post.get("timestamp") or "", reverse=sort_order != "oldest")
    if query.strip():
        final_posts.sort(key=lambda post: _query_rank(post, query), reverse=True)
    return {"count": len(final_posts), "posts": final_posts}
