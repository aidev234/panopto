"""LLM-backed behavioural warning assessment helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from functools import lru_cache
import math
import os
from pathlib import Path
import re
from typing import Any
import zipfile
import xml.etree.ElementTree as ET

import requests

from panopto.config import load_config

ASSETS_DIR = Path(__file__).resolve().parent / "assets" / "llm_warning_assessment"
PROMPT_PATH = ASSETS_DIR / "prompt.txt"
GUIDE_PATH = ASSETS_DIR / "llm_assessment_guide.docx"
DEMO_DATASET_PATH = ASSETS_DIR / "demo_dataset.xlsx"

XLSX_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

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
    return _normalize_assessment_payload(
        {
            "tagged_primary": list(entry.get("primary_warning_behaviours") or []),
            "tagged_secondary": list(entry.get("secondary_risk_factors") or []),
            "underlying_theme": str(entry.get("underlying_theme") or "").strip(),
            "rationale": "",
        }
    )


def _normalize_assessment_payload(payload: dict[str, Any]) -> dict[str, Any]:
    primary_raw = payload.get("tagged_primary")
    if not isinstance(primary_raw, list):
        primary_raw = payload.get("primary_warning_behaviours")
    secondary_raw = payload.get("tagged_secondary")
    if not isinstance(secondary_raw, list):
        secondary_raw = payload.get("secondary_risk_factors")
    primary = [str(item).strip() for item in (primary_raw if isinstance(primary_raw, list) else []) if str(item).strip()]
    secondary = [str(item).strip() for item in (secondary_raw if isinstance(secondary_raw, list) else []) if str(item).strip()]
    tagged_primary = list(dict.fromkeys(primary))
    tagged_secondary = list(dict.fromkeys(secondary))
    underlying_theme = str(payload.get("underlying_theme") or "").strip()
    if not tagged_primary and not tagged_secondary:
        underlying_theme = ""
    return {
        "tagged_primary": tagged_primary,
        "tagged_secondary": tagged_secondary,
        "underlying_theme": underlying_theme,
        "rationale": str(payload.get("rationale") or "").strip(),
    }


def _build_chat_messages(content: str) -> list[dict[str, str]]:
    assets = load_assessment_assets()
    prompt_text = str(assets.get("prompt_text") or "").strip()
    guide_text = str(assets.get("guide_text") or "").strip()
    system_prompt = (
        "You are a behavioural threat assessment analyst. "
        "Return strict JSON only with this schema: "
        "{\"tagged_primary\": string[], \"tagged_secondary\": string[], "
        "\"underlying_theme\": string, \"rationale\": string}. "
        "Do not include markdown fences. Use concise rationale. "
        "If no clear indicator exists, keep arrays empty."
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
    return _normalize_assessment_payload(parsed)


def _assess_with_openai(content: str) -> dict[str, Any] | None:
    api_key = str(os.getenv("OPENAI_API_KEY") or "").strip()
    if not api_key:
        try:
            api_key = str(load_config().get("openai_api_key") or "").strip()
        except Exception:
            api_key = ""
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
            metadata["llm_assessment"] = _normalize_assessment_payload(existing)
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
            metadata["llm_assessment"] = _normalize_assessment_payload(assessment)

        row["metadata"] = metadata
        output.append(row)
    return output


def estimate_warning_assessment_cost(
    posts: list[dict[str, Any]],
    *,
    expected_output_tokens_per_post: int = 220,
) -> dict[str, Any]:
    """Approximate token/cost for running OpenAI assessment on provided posts."""

    model = str(os.getenv("PANOPTO_LLM_MODEL") or "gpt-4.1-mini").strip()
    input_cost_per_1m = float(str(os.getenv("PANOPTO_LLM_INPUT_COST_PER_1M") or "0.40").strip() or "0.40")
    output_cost_per_1m = float(str(os.getenv("PANOPTO_LLM_OUTPUT_COST_PER_1M") or "1.60").strip() or "1.60")
    expected_output_tokens_per_post = max(1, int(expected_output_tokens_per_post))

    candidates: list[dict[str, Any]] = []
    for post in posts:
        if not isinstance(post, dict):
            continue
        metadata = post.get("metadata") if isinstance(post.get("metadata"), dict) else {}
        existing = metadata.get("llm_assessment") if isinstance(metadata.get("llm_assessment"), dict) else {}
        content = str(post.get("content") or "").strip()
        if not content:
            continue
        if existing:
            continue
        candidates.append(post)

    total_input_tokens = 0
    for post in candidates:
        content = str(post.get("content") or "").strip()
        # Approximate by converting message payload size to tokens (4 chars/token heuristic).
        messages = _build_chat_messages(content)
        payload_chars = len(json.dumps(messages, ensure_ascii=True))
        input_tokens = max(1, math.ceil(payload_chars / 4))
        total_input_tokens += input_tokens

    total_output_tokens = expected_output_tokens_per_post * len(candidates)
    estimated_input_cost = (total_input_tokens / 1_000_000.0) * input_cost_per_1m
    estimated_output_cost = (total_output_tokens / 1_000_000.0) * output_cost_per_1m
    total_estimated_cost = estimated_input_cost + estimated_output_cost

    return {
        "model": model,
        "total_posts": len(posts),
        "candidate_posts": len(candidates),
        "expected_output_tokens_per_post": expected_output_tokens_per_post,
        "estimated_input_tokens": total_input_tokens,
        "estimated_output_tokens": total_output_tokens,
        "input_cost_per_1m": input_cost_per_1m,
        "output_cost_per_1m": output_cost_per_1m,
        "estimated_input_cost_usd": round(estimated_input_cost, 6),
        "estimated_output_cost_usd": round(estimated_output_cost, 6),
        "estimated_total_cost_usd": round(total_estimated_cost, 6),
    }


def build_demo_posts(*, username: str = "demo_subject", now: datetime | None = None) -> list[dict[str, Any]]:
    """Build demo posts seeded from the curated spreadsheet dataset."""

    dc_tz = timezone(timedelta(hours=-5))
    base_now = now if now is not None else datetime.now(dc_tz)
    if base_now.tzinfo is None:
        base_now = base_now.replace(tzinfo=dc_tz)
    else:
        base_now = base_now.astimezone(dc_tz)
    assets = load_assessment_assets()
    entries = list(assets.get("dataset_entries") or [])
    posts: list[dict[str, Any]] = []
    local_hours = [8, 9, 10, 12, 13, 15, 17, 18, 19, 20, 21]
    for index, entry in enumerate(entries[:28]):
        content = str(entry.get("content") or "").strip()
        if not content:
            continue
        target_hour = local_hours[index % len(local_hours)]
        target_minute = (index * 7) % 60
        post_time = (base_now - timedelta(days=index // len(local_hours))).replace(
            hour=target_hour,
            minute=target_minute,
            second=0,
            microsecond=0,
        )
        date_hint = str(entry.get("date") or "").strip()
        if date_hint:
            try:
                day = datetime.fromisoformat(f"{date_hint}T00:00:00-05:00")
                post_time = day.replace(
                    hour=target_hour,
                    minute=target_minute,
                    second=0,
                    microsecond=0,
                )
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
                        "tagged_primary": list(entry.get("primary_warning_behaviours") or []),
                        "tagged_secondary": list(entry.get("secondary_risk_factors") or []),
                        "underlying_theme": str(entry.get("underlying_theme") or "").strip(),
                        "rationale": "",
                    },
                },
            }
        )
    extra_posts = [
        {
            "post_id": "demo-noise-1",
            "platform": "Twitter",
            "username": username,
            "content": "Traffic around Dupont Circle was gridlocked again. Looking for a quieter route into downtown Washington DC.",
            "timestamp": base_now.replace(hour=18, minute=12, second=0, microsecond=0).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-noise-1",
            "post_type": "post",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Travel planning and commuting", "rationale": ""}},
        },
        {
            "post_id": "demo-selector-1",
            "platform": "Reddit",
            "username": username,
            "content": "Email me at demo.subject@proton.me with the Capitol Hill sublet checklist.",
            "timestamp": base_now.replace(hour=16, minute=30, second=0, microsecond=0).isoformat(),
            "source_url": f"https://www.reddit.com/user/{username}/comments/demo-selector-1",
            "post_type": "comment",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Operational logistics", "rationale": ""}},
        },
        {
            "post_id": "demo-selector-2",
            "platform": "Twitter",
            "username": username,
            "content": "Call +1 202 555 0199 after 8pm if the Navy Yard meetup location changes. Backup on Telegram @demo_subject_ops.",
            "timestamp": base_now.replace(hour=20, minute=5, second=0, microsecond=0).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-selector-2",
            "post_type": "post",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Coordination and rendezvous", "rationale": ""}},
        },
        {
            "post_id": "demo-noise-2",
            "platform": "Instagram",
            "username": username,
            "content": "Coffee near Union Station before heading to a meeting by the National Mall in Washington, DC.",
            "timestamp": base_now.replace(hour=8, minute=45, second=0, microsecond=0).isoformat(),
            "source_url": f"https://www.instagram.com/p/demo-noise-2/",
            "post_type": "post",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Daily routine", "rationale": ""}},
        },
        {
            "post_id": "demo-noise-3",
            "platform": "YouTube",
            "username": username,
            "content": "Uploaded: Late-night drive playlist and DC skyline timelapse from Georgetown waterfront.",
            "timestamp": base_now.replace(hour=21, minute=10, second=0, microsecond=0).isoformat(),
            "source_url": "https://www.youtube.com/watch?v=demo-noise-3",
            "post_type": "post",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Media sharing", "rationale": ""}},
        },
        {
            "post_id": "demo-selector-3",
            "platform": "Bluesky",
            "username": username,
            "content": "Backup contact: ops.demo@pm.me - use this if the NoMa inbox bounces. Matrix handle: @demo_subject:example.org",
            "timestamp": base_now.replace(hour=14, minute=25, second=0, microsecond=0).isoformat(),
            "source_url": f"https://bsky.app/profile/{username}.bsky.social/post/demo-selector-3",
            "post_type": "post",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "Fallback communication channel", "rationale": ""}},
        },
        {
            "post_id": "demo-noise-4",
            "platform": "Twitter",
            "username": username,
            "content": "Watching highlights after getting back from Adams Morgan. Long day in Washington DC.",
            "timestamp": base_now.replace(hour=22, minute=5, second=0, microsecond=0).isoformat(),
            "source_url": f"https://x.com/{username}/status/demo-noise-4",
            "post_type": "reply",
            "metadata": {"llm_assessment": {"tagged_primary": [], "tagged_secondary": [], "underlying_theme": "End-of-day debrief", "rationale": ""}},
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
