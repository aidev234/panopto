"""LLM-backed behavioural warning assessment helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from functools import lru_cache
import math
import os
from pathlib import Path
import re
import time
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
    def _normalize_label_values(raw_value: Any) -> list[str]:
        values: list[str] = []
        if isinstance(raw_value, list):
            for item in raw_value:
                if isinstance(item, dict):
                    label = str(item.get("label") or item.get("tag") or item.get("name") or item.get("value") or "").strip()
                    if label:
                        values.append(label)
                else:
                    label = str(item or "").strip()
                    if label:
                        values.append(label)
        elif isinstance(raw_value, str):
            values.extend(_split_labels(raw_value))
        seen: set[str] = set()
        output: list[str] = []
        for item in values:
            clean = re.sub(r"\s+", " ", str(item).strip())
            if not clean:
                continue
            key = clean.lower()
            if key in seen:
                continue
            seen.add(key)
            output.append(clean)
        return output

    primary_raw = (
        payload.get("tagged_primary")
        or payload.get("primary_warning_behaviours")
        or payload.get("primary")
        or payload.get("primary_tags")
        or payload.get("warning_behaviours")
    )
    secondary_raw = (
        payload.get("tagged_secondary")
        or payload.get("secondary_risk_factors")
        or payload.get("secondary")
        or payload.get("secondary_tags")
        or payload.get("risk_factors")
    )
    primary = _normalize_label_values(primary_raw)
    secondary = _normalize_label_values(secondary_raw)
    tagged_primary = list(dict.fromkeys(primary))
    tagged_secondary = list(dict.fromkeys(secondary))
    underlying_theme = str(
        payload.get("underlying_theme")
        or payload.get("theme")
        or payload.get("summary")
        or ""
    ).strip()
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
        "Return valid strict JSON only with this exact schema and no extra keys: "
        "{\"tagged_primary\": string[], \"tagged_secondary\": string[], "
        "\"underlying_theme\": string, \"rationale\": string}. "
        "Do not include markdown fences, prose, commentary, or code blocks. "
        "Use double-quoted JSON keys and string values. "
        "Use concise rationale. "
        "If no clear indicator exists, keep arrays empty and set underlying_theme to an empty string. "
        "Keep the entire JSON response under 200 words total. "
        "The response must be parseable by json.loads."
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
                "Return JSON only. "
                f"Post text: {content}"
            ),
        },
    ]


def _build_identity_intel_messages(content: str) -> list[dict[str, str]]:
    system_prompt = (
        "You are an identity and selectors extraction analyst. "
        "Return valid strict JSON only with this exact schema and no extra keys: "
        "{\"tags\": [{\"label\": string, \"intel\": \"none\"|\"stated\"|\"inferred\"}], "
        "\"theme\": string}. "
        "Do not include markdown fences, prose, commentary, or code blocks. "
        "Use double-quoted JSON keys and string values. "
        "Keep the entire JSON response under 200 words total. "
        "Extract identifying intel only, not threats. "
        "Prioritize: employer, occupation, location, venue_area, industry, affiliation, school, handle, email, phone, wallet, vehicle, alias, demographic, family_role. "
        "Use labels in the exact form 'category: value'. "
        "Use 'stated' when the text directly says the fact. "
        "Use 'inferred' only for reasonable deductions such as industry or likely base of activity. "
        "Never invent facts not supported by the text. "
        "When both city and street/venue are present, include both. "
        "If useful intel exists, return tags; do not return an empty array when employer, job title, city, school, selector, or venue is explicitly present. "
        "If no useful intel exists, return tags as [] and theme as ''. "
        "Theme must be one short sentence fragment summarizing the strongest identity insight. "
        "Example output: {\"tags\":[{\"label\":\"employer: Northern Trust Bank\",\"intel\":\"stated\"},{\"label\":\"occupation: fraud analyst\",\"intel\":\"stated\"},{\"label\":\"location: Auckland\",\"intel\":\"stated\"},{\"label\":\"venue_area: Queen Street\",\"intel\":\"stated\"},{\"label\":\"industry: financial services\",\"intel\":\"inferred\"}],\"theme\":\"User likely works in financial services and is active in central Auckland\"}. "
        "The response must be parseable by json.loads."
    )
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Extract identifying intel from this text. Return JSON only. "
                f"Text: {content}"
            ),
        },
    ]


def _build_combined_sandbox_messages(content: str) -> list[dict[str, str]]:
    assets = load_assessment_assets()
    prompt_text = str(assets.get("prompt_text") or "").strip()
    guide_text = str(assets.get("guide_text") or "").strip()
    system_prompt = (
        "You are an analyst producing two structured outputs for the same post. "
        "Return valid strict JSON only with this exact schema and no extra keys: "
        "{\"threat\":{\"tagged_primary\": string[], \"tagged_secondary\": string[], \"underlying_theme\": string, \"rationale\": string},"
        "\"identity\":{\"tags\": [{\"label\": string, \"intel\": \"none\"|\"stated\"|\"inferred\"}], \"theme\": string}}. "
        "Do not include markdown fences, prose, commentary, or code blocks. "
        "Use double-quoted JSON keys and string values. "
        "Keep the entire JSON response under 200 words total. "
        "For threat: if no clear indicator exists, keep arrays empty and set underlying_theme to an empty string. "
        "For identity: prioritize employer, occupation, location, venue_area, industry, affiliation, school, handle, email, phone, wallet, vehicle, alias, demographic, family_role. "
        "Use labels in the exact form 'category: value'. "
        "Use 'stated' when directly stated and 'inferred' only for reasonable deductions. "
        "If useful identity intel exists, do not return an empty tags array. "
        "The response must be parseable by json.loads."
    )
    if prompt_text:
        system_prompt = f"{system_prompt}\n\nThreat operator brief:\n{prompt_text}"
    if guide_text:
        system_prompt = f"{system_prompt}\n\nThreat assessment guide:\n{guide_text}"
    return [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Analyze this post and return one JSON object containing both threat and identity outputs only. "
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
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            return None
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(parsed, dict):
        return None
    return parsed


def _normalize_identity_intel_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw_tags = payload.get("tags")
    if not isinstance(raw_tags, list):
        for alternate_key in ("items", "entities", "identities", "selectors", "details"):
            candidate = payload.get(alternate_key)
            if isinstance(candidate, list):
                raw_tags = candidate
                break
    if not isinstance(raw_tags, list):
        for alternate_key in ("tags_by_category", "attributes", "fields"):
            candidate = payload.get(alternate_key)
            if isinstance(candidate, dict):
                raw_tags = []
                for category, value in candidate.items():
                    if isinstance(value, list):
                        for item in value:
                            raw_tags.append({"category": category, "value": item})
                    else:
                        raw_tags.append({"category": category, "value": value})
                break
    tags: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    if isinstance(raw_tags, list):
        for item in raw_tags:
            label = ""
            intel = "inferred"
            if isinstance(item, dict):
                direct_label = str(item.get("label") or item.get("tag") or item.get("name") or "").strip()
                category = str(item.get("category") or item.get("type") or "").strip().lower().replace(" ", "_")
                value = str(item.get("value") or item.get("text") or item.get("detail") or "").strip()
                if direct_label:
                    label = direct_label
                elif category and value:
                    label = f"{category}: {value}"
                elif value:
                    label = value
                intel = str(
                    item.get("intel")
                    or item.get("confidence")
                    or item.get("status")
                    or item.get("support")
                    or ""
                ).strip().lower()
            elif isinstance(item, str):
                label = item.strip()
            else:
                continue
            label = re.sub(r"\s+", " ", str(label).strip())
            if intel not in {"none", "stated", "inferred"}:
                if intel in {"direct", "explicit", "quoted", "observed"}:
                    intel = "stated"
                elif intel in {"derived", "deduced", "likely", "possible", "probable"}:
                    intel = "inferred"
                else:
                    intel = "inferred"
            if not label:
                continue
            key = (label.lower(), intel)
            if key in seen:
                continue
            seen.add(key)
            tags.append({"label": label, "intel": intel})
    theme = re.sub(
        r"\s+",
        " ",
        str(
            payload.get("theme")
            or payload.get("summary")
            or payload.get("assessment")
            or payload.get("comment")
            or ""
        ).strip(),
    )
    if not tags:
        theme = ""
    return {
        "tags": tags,
        "theme": theme,
    }


def _openai_api_key() -> str:
    api_key = str(os.getenv("OPENAI_API_KEY") or "").strip()
    if api_key:
        return api_key
    try:
        return str(load_config().get("openai_api_key") or "").strip()
    except Exception:
        return ""


def _openai_disabled() -> bool:
    return str(os.getenv("PANOPTO_LLM_DISABLE") or "").strip().lower() in {"1", "true", "yes"}


def _openai_model() -> str:
    return str(os.getenv("PANOPTO_LLM_MODEL") or "gpt-4.1-mini").strip()


def _openai_timeout_seconds() -> float:
    return float(str(os.getenv("PANOPTO_LLM_TIMEOUT_SECONDS") or "25").strip() or "25")


def _run_openai_json_request(messages: list[dict[str, str]]) -> dict[str, Any] | None:
    api_key = _openai_api_key()
    if _openai_disabled() or not api_key:
        return None

    last_error: Exception | None = None
    for attempt in range(3):
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _openai_model(),
                "messages": messages,
                "response_format": {"type": "json_object"},
                "temperature": 0,
                "max_tokens": 220,
            },
            timeout=_openai_timeout_seconds(),
        )
        if response.status_code != 429:
            response.raise_for_status()
            return _parse_openai_response(response.json())
        last_error = requests.HTTPError(
            f"429 Client Error: Too Many Requests for url: {response.url}",
            response=response,
        )
        retry_after_header = str(response.headers.get("Retry-After") or "").strip()
        try:
            retry_after = float(retry_after_header) if retry_after_header else 0.0
        except ValueError:
            retry_after = 0.0
        backoff_seconds = retry_after if retry_after > 0 else min(4.0, 1.0 + attempt)
        time.sleep(backoff_seconds)
    if last_error is not None:
        raise last_error
    return None


def _assess_with_openai(content: str) -> dict[str, Any] | None:
    parsed = _run_openai_json_request(_build_chat_messages(content))
    if not parsed:
        return None
    parsed = _normalize_assessment_payload(parsed)
    model = _openai_model()
    parsed["model"] = model
    return parsed


def _assess_identity_intel_with_openai(content: str) -> dict[str, Any] | None:
    parsed = _run_openai_json_request(_build_identity_intel_messages(content))
    if not parsed:
        return None
    normalized = _normalize_identity_intel_payload(parsed)
    normalized["model"] = _openai_model()
    return normalized


def _assess_combined_sandbox_with_openai(content: str) -> dict[str, Any] | None:
    parsed = _run_openai_json_request(_build_combined_sandbox_messages(content))
    if not parsed:
        return None
    threat_raw = parsed.get("threat") if isinstance(parsed.get("threat"), dict) else {}
    identity_raw = parsed.get("identity") if isinstance(parsed.get("identity"), dict) else {}
    return {
        "threat_raw": threat_raw,
        "identity_raw": identity_raw,
        "threat": _normalize_assessment_payload(threat_raw if isinstance(threat_raw, dict) else {}),
        "identity": _normalize_identity_intel_payload(identity_raw if isinstance(identity_raw, dict) else {}),
        "model": _openai_model(),
    }


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


def analyze_post_sandbox(post: dict[str, Any]) -> dict[str, Any]:
    row = dict(post)
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    metadata = dict(metadata)
    content = str(row.get("content") or "").strip()
    if not content:
        row["metadata"] = metadata
        return row

    threat_result: dict[str, Any] | None = None
    identity_result: dict[str, Any] | None = None
    threat_error = ""
    identity_error = ""
    demo_threat = _find_demo_assessment(content)
    if demo_threat is not None:
        threat_result = demo_threat
        try:
            identity_result = _assess_identity_intel_with_openai(content)
        except Exception as exc:
            identity_result = None
            identity_error = str(exc or "").strip()
    else:
        try:
            combined_result = _assess_combined_sandbox_with_openai(content)
            if isinstance(combined_result, dict):
                threat_result = combined_result.get("threat_raw") if isinstance(combined_result.get("threat_raw"), dict) else combined_result.get("threat")
                identity_result = combined_result.get("identity_raw") if isinstance(combined_result.get("identity_raw"), dict) else combined_result.get("identity")
        except Exception as exc:
            threat_error = str(exc or "").strip()
            identity_error = threat_error

    threat_normalized = _normalize_assessment_payload(threat_result) if isinstance(threat_result, dict) and threat_result else {
        "tagged_primary": [],
        "tagged_secondary": [],
        "underlying_theme": "",
        "rationale": "",
    }
    identity_normalized = _normalize_identity_intel_payload(identity_result) if isinstance(identity_result, dict) and identity_result else {
        "tags": [],
        "theme": "",
    }

    metadata["llm_assessment"] = threat_normalized
    metadata["identity_intel_assessment"] = identity_normalized
    metadata["sandbox_debug"] = {
        "request_text": content,
        "threat_messages": _build_chat_messages(content),
        "identity_messages": _build_identity_intel_messages(content),
        "combined_messages": _build_combined_sandbox_messages(content),
        "threat_error": threat_error,
        "identity_error": identity_error,
        "threat_raw": threat_result if isinstance(threat_result, dict) else {},
        "threat_normalized": threat_normalized,
        "identity_raw": identity_result if isinstance(identity_result, dict) else {},
        "identity_normalized": identity_normalized,
    }
    metadata["sandbox_analysis"] = {
        "threat_checked": not bool(threat_error),
        "identity_checked": not bool(identity_error),
        "threat_present": bool(
            threat_normalized.get("tagged_primary")
            or threat_normalized.get("tagged_secondary")
            or str(threat_normalized.get("underlying_theme") or "").strip()
        ),
        "identity_present": bool(
            identity_normalized.get("tags")
            or str(identity_normalized.get("theme") or "").strip()
        ),
    }

    row["metadata"] = metadata
    return row


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
