"""LLM-backed behavioural warning assessment helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from functools import lru_cache
import os
from pathlib import Path
import re
from typing import Any
import zipfile
import xml.etree.ElementTree as ET

import requests

ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "llm_warning_assessment"
PROMPT_PATH = ASSETS_DIR / "prompt.txt"
GUIDE_PATH = ASSETS_DIR / "llm_assessment_guide.docx"
DEMO_DATASET_PATH = ASSETS_DIR / "demo_dataset.xlsx"

XLSX_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

RISK_LEVEL_ALIASES = {
    "very high": "Very High",
    "high": "High",
    "moderate": "Moderate",
    "medium": "Moderate",
    "low": "Low",
}


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _split_labels(value: str) -> list[str]:
    items = []
    seen: set[str] = set()
    for part in str(value or "").split(","):
        clean = re.sub(r"\s+", " ", part).strip().strip(".")
        if not clean:
            continue
        key = clean.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(clean)
    return items


def _normalize_risk_level(value: str) -> str:
    clean = _normalize_text(value)
    if not clean:
        return "Unknown"
    if clean in RISK_LEVEL_ALIASES:
        return RISK_LEVEL_ALIASES[clean]
    for key, label in RISK_LEVEL_ALIASES.items():
        if key in clean:
            return label
    return "Unknown"


def _column_to_index(column_name: str) -> int:
    total = 0
    for char in column_name:
        total = total * 26 + (ord(char) - 64)
    return total - 1


def _extract_docx_text(path: Path) -> str:
    if not path.exists():
        return ""
    with zipfile.ZipFile(path) as archive:
        if "word/document.xml" not in archive.namelist():
            return ""
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs: list[str] = []
    for paragraph in root.findall(f".//{{{WORD_NS}}}p"):
        parts = [node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")]
        line = "".join(parts).strip()
        if line:
            paragraphs.append(line)
    return "\n".join(paragraphs)


def _extract_xlsx_rows(path: Path) -> list[list[str]]:
    if not path.exists():
        return []

    with zipfile.ZipFile(path) as archive:
        if "xl/worksheets/sheet1.xml" not in archive.namelist():
            return []

        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            sst = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in sst.findall(f".//{{{XLSX_NS}}}si"):
                text = "".join(node.text or "" for node in item.findall(f".//{{{XLSX_NS}}}t"))
                shared_strings.append(text)

        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    row_maps: list[dict[int, str]] = []
    max_col_index = -1
    for row in sheet.findall(f".//{{{XLSX_NS}}}sheetData/{{{XLSX_NS}}}row"):
        mapped: dict[int, str] = {}
        for cell in row.findall(f"{{{XLSX_NS}}}c"):
            reference = cell.attrib.get("r", "A1")
            match = re.match(r"([A-Z]+)(\d+)", reference)
            if not match:
                continue
            col_idx = _column_to_index(match.group(1))
            raw_node = cell.find(f"{{{XLSX_NS}}}v")
            if raw_node is None:
                value = ""
            else:
                raw_value = raw_node.text or ""
                if cell.attrib.get("t") == "s":
                    try:
                        value = shared_strings[int(raw_value)]
                    except (IndexError, ValueError):
                        value = raw_value
                else:
                    value = raw_value
            mapped[col_idx] = value
            max_col_index = max(max_col_index, col_idx)
        row_maps.append(mapped)

    if max_col_index < 0:
        return []

    output: list[list[str]] = []
    for mapped in row_maps:
        output.append([mapped.get(idx, "") for idx in range(max_col_index + 1)])
    return output


def _excel_serial_to_iso_day(serial: str) -> str:
    text = str(serial or "").strip()
    if not text:
        return ""
    try:
        day_offset = int(float(text))
    except ValueError:
        return ""
    # Excel's 1900 date system with leap-year bug compatibility.
    base_day = datetime(1899, 12, 30, tzinfo=timezone.utc)
    return (base_day + timedelta(days=day_offset)).date().isoformat()


@lru_cache(maxsize=1)
def load_assessment_assets() -> dict[str, Any]:
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8") if PROMPT_PATH.exists() else ""
    guide_text = _extract_docx_text(GUIDE_PATH)
    rows = _extract_xlsx_rows(DEMO_DATASET_PATH)

    entries: list[dict[str, Any]] = []
    for row in rows[1:]:
        content = str(row[0] if len(row) > 0 else "").strip()
        if not content:
            continue
        primary = _split_labels(row[1] if len(row) > 1 else "")
        secondary = _split_labels(row[2] if len(row) > 2 else "")
        theme = str(row[3] if len(row) > 3 else "").strip()
        raw_date = str(row[4] if len(row) > 4 else "").strip()
        entries.append(
            {
                "content": content,
                "lookup": _normalize_text(content),
                "primary_warning_behaviours": primary,
                "secondary_risk_factors": secondary,
                "underlying_theme": theme,
                "date": _excel_serial_to_iso_day(raw_date),
            }
        )

    by_content = {entry["lookup"]: entry for entry in entries}
    return {
        "prompt_text": prompt_text,
        "guide_text": guide_text,
        "dataset_entries": entries,
        "dataset_lookup": by_content,
    }


def _find_demo_assessment(text: str) -> dict[str, Any] | None:
    assets = load_assessment_assets()
    lookup = assets.get("dataset_lookup") or {}
    key = _normalize_text(text)
    entry = lookup.get(key)
    if not isinstance(entry, dict):
        return None
    return {
        "primary_warning_behaviours": list(entry.get("primary_warning_behaviours") or []),
        "secondary_risk_factors": list(entry.get("secondary_risk_factors") or []),
        "underlying_theme": str(entry.get("underlying_theme") or "").strip(),
        "risk_level": _derive_risk_level(
            list(entry.get("primary_warning_behaviours") or []),
            list(entry.get("secondary_risk_factors") or []),
        ),
        "confidence": "high",
        "source": "demo_dataset",
    }


def _derive_risk_level(primary: list[str], secondary: list[str]) -> str:
    prim = {str(item).strip().lower() for item in primary if str(item).strip()}
    sec = {str(item).strip().lower() for item in secondary if str(item).strip()}
    if not prim and not sec:
        return "Unknown"
    high_triggers = {
        "pathway",
        "directly communicated threat",
        "last resort",
        "testing violence (novel aggression)",
        "violent identification",
    }
    moderate_triggers = {
        "fixation",
        "leakage",
        "violent ideation",
        "suicidal ideation",
        "capability (resources)",
        "capability (knowledge)",
        "capability (access)",
    }
    if prim.intersection(high_triggers):
        return "High"
    if prim.intersection(moderate_triggers) or sec.intersection(moderate_triggers):
        return "Moderate"
    return "Low"


def _build_chat_messages(content: str) -> list[dict[str, str]]:
    assets = load_assessment_assets()
    prompt_text = str(assets.get("prompt_text") or "").strip()
    guide_text = str(assets.get("guide_text") or "").strip()
    system_prompt = (
        "You are a behavioural threat assessment analyst. "
        "Return strict JSON only with this schema: "
        "{\"primary_warning_behaviours\": string[], \"secondary_risk_factors\": string[], "
        "\"underlying_theme\": string, \"risk_level\": string, \"confidence\": string, \"rationale\": string}. "
        "Do not include markdown fences. Use concise rationale. "
        "If no clear indicator exists, keep arrays empty and risk_level as Low or Unknown."
    )
    if prompt_text:
        system_prompt = f"{system_prompt}\n\nOperator brief:\n{prompt_text}"
    if guide_text:
        system_prompt = f"{system_prompt}\n\nAssessment guide:\n{guide_text}"

    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Assess this post for warning indicators and risk factors. "
                f"Post text: {content}"
            ),
        },
    ]


def _parse_openai_response(payload: dict[str, Any]) -> dict[str, Any] | None:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        return None
    content = str(message.get("content") or "").strip()
    if not content:
        return None
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.IGNORECASE | re.MULTILINE).strip()
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    primary = [str(item).strip() for item in parsed.get("primary_warning_behaviours", []) if str(item).strip()] if isinstance(parsed.get("primary_warning_behaviours"), list) else []
    secondary = [str(item).strip() for item in parsed.get("secondary_risk_factors", []) if str(item).strip()] if isinstance(parsed.get("secondary_risk_factors"), list) else []
    risk_level = _normalize_risk_level(str(parsed.get("risk_level") or ""))
    confidence_raw = str(parsed.get("confidence") or "").strip().lower()
    confidence = confidence_raw if confidence_raw in {"low", "medium", "high"} else "medium"
    return {
        "primary_warning_behaviours": list(dict.fromkeys(primary)),
        "secondary_risk_factors": list(dict.fromkeys(secondary)),
        "underlying_theme": str(parsed.get("underlying_theme") or "").strip(),
        "risk_level": risk_level,
        "confidence": confidence,
        "rationale": str(parsed.get("rationale") or "").strip(),
        "source": "openai",
    }


def _assess_with_openai(content: str) -> dict[str, Any] | None:
    api_key = str(os.getenv("OPENAI_API_KEY") or "").strip()
    disabled = str(os.getenv("PANOPTO_LLM_DISABLE") or "").strip().lower() in {"1", "true", "yes"}
    if disabled or not api_key:
        return None

    model = str(os.getenv("PANOPTO_LLM_MODEL") or "gpt-4.1-mini").strip()
    timeout = float(str(os.getenv("PANOPTO_LLM_TIMEOUT_SECONDS") or "25").strip() or "25")

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": _build_chat_messages(content),
            "response_format": {"type": "json_object"},
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    parsed = _parse_openai_response(response.json())
    if not parsed:
        return None
    parsed["model"] = model
    return parsed


def apply_warning_assessments(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach behavioural warning assessments to each post metadata when possible."""

    output: list[dict[str, Any]] = []
    for post in posts:
        row = dict(post)
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        metadata = dict(metadata)

        existing = metadata.get("llm_assessment")
        if isinstance(existing, dict) and existing:
            row["metadata"] = metadata
            output.append(row)
            continue

        content = str(row.get("content") or "").strip()
        if not content:
            row["metadata"] = metadata
            output.append(row)
            continue

        assessment = _find_demo_assessment(content)
        if assessment is None:
            try:
                assessment = _assess_with_openai(content)
            except Exception:
                assessment = None

        if isinstance(assessment, dict) and assessment:
            assessment["assessed_at"] = datetime.now(timezone.utc).isoformat()
            metadata["llm_assessment"] = assessment

        row["metadata"] = metadata
        output.append(row)
    return output


def build_demo_posts(*, username: str = "demo_subject", now: datetime | None = None) -> list[dict[str, Any]]:
    """Build demo posts seeded from the curated spreadsheet dataset."""

    base_now = now if now is not None else datetime.now(timezone.utc)
    assets = load_assessment_assets()
    entries = list(assets.get("dataset_entries") or [])
    posts: list[dict[str, Any]] = []
    for index, entry in enumerate(entries[:28]):
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        post_time = base_now - timedelta(hours=index * 3)
        date_hint = str(entry.get("date") or "").strip()
        if date_hint:
            try:
                day = datetime.fromisoformat(f"{date_hint}T00:00:00+00:00")
                post_time = day + timedelta(minutes=index)
            except ValueError:
                pass

        posts.append(
            {
                "post_id": f"demo-llm-{index + 1}",
                "platform": "Twitter",
                "username": username,
                "content": content,
                "timestamp": post_time.isoformat(),
                "source_url": f"https://x.com/{username}/status/demo-llm-{index + 1}",
                "post_type": "post",
                "metadata": {
                    "profile_image_url": "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=256&q=80",
                    "llm_assessment": {
                        "primary_warning_behaviours": list(entry.get("primary_warning_behaviours") or []),
                        "secondary_risk_factors": list(entry.get("secondary_risk_factors") or []),
                        "underlying_theme": str(entry.get("underlying_theme") or "").strip(),
                        "risk_level": _derive_risk_level(
                            list(entry.get("primary_warning_behaviours") or []),
                            list(entry.get("secondary_risk_factors") or []),
                        ),
                        "confidence": "high",
                        "source": "demo_dataset",
                        "assessed_at": base_now.isoformat(),
                    },
                },
            }
        )
    extra_posts = [
        {
            "post_id": "demo-noise-1",
            "platform": "Twitter",
            "username": username,
            "content": "Rain all week in Queens. Anyone know a good indoor climbing gym?",
            "timestamp": (base_now - timedelta(hours=7)).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-noise-1",
            "post_type": "post",
        },
        {
            "post_id": "demo-selector-1",
            "platform": "Reddit",
            "username": username,
            "content": "Email me at demo.subject@proton.me with the lease template please.",
            "timestamp": (base_now - timedelta(hours=9)).isoformat(),
            "source_url": f"https://www.reddit.com/user/{username}/comments/demo-selector-1",
            "post_type": "comment",
        },
        {
            "post_id": "demo-selector-2",
            "platform": "Twitter",
            "username": username,
            "content": "Call +1 646 555 0199 after 8pm if the meetup location changes.",
            "timestamp": (base_now - timedelta(hours=10)).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-selector-2",
            "post_type": "post",
        },
        {
            "post_id": "demo-noise-2",
            "platform": "Instagram",
            "username": username,
            "content": "Coffee + notebook + subway delays. Standard Tuesday.",
            "timestamp": (base_now - timedelta(hours=12)).isoformat(),
            "source_url": f"https://www.instagram.com/p/demo-noise-2/",
            "post_type": "post",
        },
        {
            "post_id": "demo-noise-3",
            "platform": "YouTube",
            "username": username,
            "content": "Uploaded: Late-night drive playlist and city timelapse.",
            "timestamp": (base_now - timedelta(hours=15)).isoformat(),
            "source_url": "https://www.youtube.com/watch?v=demo-noise-3",
            "post_type": "post",
            "metadata": {"embed_url": "https://www.youtube.com/embed/demo-noise-3"},
        },
        {
            "post_id": "demo-selector-3",
            "platform": "Bluesky",
            "username": username,
            "content": "Backup contact: ops.demo@pm.me - use this if the main inbox bounces.",
            "timestamp": (base_now - timedelta(hours=18)).isoformat(),
            "source_url": f"https://bsky.app/profile/{username}.bsky.social/post/demo-selector-3",
            "post_type": "post",
        },
        {
            "post_id": "demo-noise-4",
            "platform": "Twitter",
            "username": username,
            "content": "Watching Knicks highlights. Defense finally looks organized.",
            "timestamp": (base_now - timedelta(hours=22)).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-noise-4",
            "post_type": "reply",
        },
    ]
    default_avatar = "https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&w=256&q=80"
    for row in extra_posts:
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        metadata = dict(metadata)
        metadata.setdefault("profile_image_url", default_avatar)
        row["metadata"] = metadata
        posts.append(row)
    return posts
