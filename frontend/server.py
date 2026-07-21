"""Local web server for visualizing collected social posts."""

from __future__ import annotations

import json
import base64
import binascii
import html
import ipaddress
import io
import mimetypes
import re
import subprocess
import sys
import tempfile
import threading
import socket
import textwrap
import time
import webbrowser
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, urlparse
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from panopto.collection_service import InvalidRequestError, collect_for_targets, parse_targets
from panopto.analysis.llm_warning_assessor import analyze_post_sandbox, apply_warning_assessments, estimate_warning_assessment_cost
from panopto.errors import UsernameNotFoundError
from panopto.post_query import normalize_tag, query_posts
from panopto.collection_jobs import get_collection_job_status, start_collection_job
from panopto.config import load_config, load_public_config, save_config
from panopto.recon import normalize_recon_selectors, run_recon, stream_user_scanner_selector
from panopto.face_analysis import FaceRecognitionEngine
from panopto.storage.posts import (
    build_vip_threat_demo_recon,
    clear_posts,
    create_case,
    create_demo_case,
    create_vip_threat_demo_case,
    delete_case,
    list_cases,
    save_posts,
    seed_vip_threat_demo_posts,
    update_case,
    update_post_llm_assessments,
)

DEFAULT_DB_PATH = ROOT_DIR / "osint_data.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"
DOCS_DIR = ROOT_DIR / "docs"
_ALLOWED_DB_ROOTS = [ROOT_DIR.resolve(), Path("/tmp").resolve()]
_FACE_RECOGNITION_ENGINE = FaceRecognitionEngine()
_APIFY_REQUIRED_PLATFORMS = {"twitter", "tiktok", "instagram"}
_MAX_JSON_BODY_BYTES = 2 * 1024 * 1024


def _load_architecture_markdown() -> str:
    path = DOCS_DIR / "architecture-diagram.md"
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "# Orion Architecture Diagram\n\nArchitecture diagram source is unavailable.\n"


def _extract_mermaid_block(markdown_text: str) -> str:
    match = re.search(r"```mermaid\s*\n(.*?)\n```", str(markdown_text or ""), flags=re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return str(match.group(1) or "").strip()


def _render_architecture_page_html() -> bytes:
    markdown_text = _load_architecture_markdown()
    mermaid_source = _extract_mermaid_block(markdown_text)
    body = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Orion Architecture</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #08111c;
        --panel: #0f1c2b;
        --panel-2: #13253a;
        --text: #e7eef7;
        --muted: #9eb0c6;
        --accent: #67d6ff;
        --border: rgba(158, 176, 198, 0.24);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
        background:
          radial-gradient(circle at top, rgba(103, 214, 255, 0.14), transparent 36%),
          linear-gradient(180deg, #08111c 0%, #0a1522 100%);
        color: var(--text);
      }}
      main {{
        width: min(1180px, calc(100vw - 32px));
        margin: 0 auto;
        padding: 32px 0 56px;
      }}
      h1 {{
        margin: 0 0 8px;
        font-size: clamp(2rem, 4vw, 3rem);
      }}
      p {{
        margin: 0;
        color: var(--muted);
        line-height: 1.6;
      }}
      .hero {{
        display: grid;
        gap: 12px;
        margin-bottom: 24px;
      }}
      .actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 8px;
      }}
      .actions a {{
        color: var(--text);
        text-decoration: none;
        padding: 10px 14px;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: rgba(15, 28, 43, 0.82);
      }}
      .panel {{
        background: rgba(15, 28, 43, 0.84);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
      }}
      .panel + .panel {{
        margin-top: 18px;
      }}
      .diagram {{
        width: 100%;
        display: block;
        border-radius: 12px;
        background: #07101b;
      }}
      h2 {{
        margin: 0 0 12px;
        font-size: 1.05rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}
      pre {{
        margin: 0;
        padding: 16px;
        overflow-x: auto;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: var(--panel-2);
        color: #d8f4ff;
        line-height: 1.5;
      }}
      code {{
        font-family: "IBM Plex Mono", "SFMono-Regular", monospace;
        font-size: 0.92rem;
      }}
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <h1>Orion Architecture</h1>
        <p>Mermaid markdown viewers are inconsistent here, so this page serves the diagram directly from the local server with a static SVG fallback and the original Mermaid source below.</p>
        <div class="actions">
          <a href="/docs/architecture-diagram.md">Open markdown source</a>
          <a href="/architecture-diagram.svg">Open SVG diagram</a>
          <a href="/">Back to app</a>
        </div>
      </section>
      <section class="panel">
        <h2>Diagram</h2>
        <img class="diagram" src="/architecture-diagram.svg" alt="Orion architecture diagram" />
      </section>
      <section class="panel">
        <h2>Mermaid Source</h2>
        <pre><code>{_html_escape(mermaid_source or "Mermaid source unavailable.")}</code></pre>
      </section>
    </main>
  </body>
</html>
"""
    return body.encode("utf-8")


def _resolve_api_db_path(raw_value: str | Path | None) -> Path:
    if raw_value is None:
        return DEFAULT_DB_PATH
    text = str(raw_value).strip()
    if not text:
        return DEFAULT_DB_PATH

    candidate = Path(text).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT_DIR / candidate
    resolved = candidate.resolve()

    if resolved.suffix.lower() != ".db":
        raise InvalidRequestError("db_path must reference a .db file")

    for allowed_root in _ALLOWED_DB_ROOTS:
        if resolved == allowed_root or allowed_root in resolved.parents:
            return resolved
    raise InvalidRequestError("db_path must remain inside the project directory or /tmp")


def _missing_apify_platforms(targets: list[dict[str, str]]) -> list[str]:
    requested = {
        str(item.get("platform") or "").strip().lower()
        for item in (targets or [])
        if isinstance(item, dict)
    }
    return sorted(requested.intersection(_APIFY_REQUIRED_PLATFORMS))


def _pdf_escape(text: str) -> str:
    return str(text or "").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _html_escape(text: str) -> str:
    return html.escape(str(text or ""), quote=True)


def _wrap_pdf_text(text: str, width: int) -> list[str]:
    normalized = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip():
        return [""]
    chunks: list[str] = []
    for block in normalized.split("\n"):
        block = block.strip()
        if not block:
            chunks.append("")
            continue
        chunks.extend(textwrap.wrap(block, width=width) or [""])
    return chunks or [""]


def _site_key_from_known_profile(profile: dict) -> str:
    raw_site = str(profile.get("site") or "").strip().lower()
    profile_url = str(profile.get("url") or "").strip().lower()
    if "instagram" in raw_site or "instagram.com" in profile_url:
        return "instagram"
    if "tiktok" in raw_site or "tiktok.com" in profile_url:
        return "tiktok"
    if "facebook" in raw_site or "facebook.com" in profile_url:
        return "facebook"
    return ""


def _major_profiles(profiles: list[dict]) -> list[dict]:
    output: list[dict] = []
    for item in profiles:
        if not isinstance(item, dict):
            continue
        if _site_key_from_known_profile(item) not in {"facebook", "instagram", "tiktok"}:
            continue
        output.append(item)
    return output


def _discover_profiles_from_posts(posts: list[dict]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], dict[str, str]] = {}
    for row in posts:
        platform = str(row.get("platform") or "").strip().lower()
        username = str(row.get("username") or "").strip().lstrip("@")
        if not platform or not username:
            continue
        if platform == "twitter":
            profile_url = f"https://x.com/{username}"
            site = "Twitter/X"
        elif platform == "reddit":
            profile_url = f"https://www.reddit.com/user/{username}"
            site = "Reddit"
        elif platform == "tiktok":
            profile_url = f"https://www.tiktok.com/@{username}"
            site = "TikTok"
        elif platform == "bluesky":
            profile_url = f"https://bsky.app/profile/{username}"
            site = "Bluesky"
        elif platform == "instagram":
            profile_url = f"https://www.instagram.com/{username}/"
            site = "Instagram"
        elif platform == "youtube":
            profile_url = f"https://www.youtube.com/@{username}"
            site = "YouTube"
        else:
            continue
        key = (platform, username.lower())
        if key not in grouped:
            grouped[key] = {
                "name": f"@{username}",
                "site": site,
                "url": profile_url,
                "screenshot_url": "",
            }
    return list(grouped.values())


def _guess_site_from_url(url: str) -> str:
    host = str(urlparse(str(url or "").strip()).hostname or "").lower().replace("www.", "")
    if "x.com" in host or "twitter.com" in host:
        return "Twitter/X"
    if "reddit.com" in host:
        return "Reddit"
    if "tiktok.com" in host or "tikvib.com" in host:
        return "TikTok"
    if "bsky.app" in host or "bsky.social" in host:
        return "Bluesky"
    if "instagram.com" in host or "byviewer.com" in host:
        return "Instagram"
    if "youtube.com" in host or "youtu.be" in host:
        return "YouTube"
    return host or "Unknown"


def _image_source_to_data_uri(source: str) -> str:
    value = str(source or "").strip()
    if not value:
        return ""
    if value.startswith("data:image/"):
        return value
    if value.startswith("/"):
        clean_path = value.split("?", 1)[0]
        base = STATIC_DIR.resolve()
        local = (STATIC_DIR / clean_path.lstrip("/")).resolve()
        try:
            local.relative_to(base)
        except ValueError:
            return ""
        if not local.exists() or not local.is_file():
            return ""
        mime, _ = mimetypes.guess_type(str(local))
        if not mime or not mime.lower().startswith("image/"):
            return ""
        raw = local.read_bytes()
        mime_type = mime
        encoded = base64.b64encode(raw).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"
    if value.lower().startswith("http://") or value.lower().startswith("https://"):
        return value
    return ""


def _extract_underlying_themes(posts: list[dict]) -> list[str]:
    counts: dict[str, int] = {}
    for row in posts:
        if not isinstance(row, dict):
            continue
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        llm = metadata.get("llm_assessment") if isinstance(metadata.get("llm_assessment"), dict) else {}
        theme = str(llm.get("underlying_theme") or row.get("llm_underlying_theme") or "").strip()
        if not theme:
            continue
        counts[theme] = counts.get(theme, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [item[0] for item in ranked[:10]]


def _selector_label(selector_type: str, selector_value: str) -> str:
    clean_type = str(selector_type or "").strip().lower() or "unknown"
    clean_value = str(selector_value or "").strip()
    return f"{clean_type}: {clean_value}" if clean_value else clean_type


def _selector_display_label(selector_type: str) -> str:
    clean = str(selector_type or "").strip().lower()
    if not clean:
        return "Selector"
    return clean[:1].upper() + clean[1:]


def _selector_provenance_label(selector_type: str, selector_value: str) -> str:
    display = _selector_display_label(selector_type)
    value = str(selector_value or "").strip()
    if value:
        return f"Identified via {display} selector: {value}"
    return f"Identified via {display} selector"


def _site_favicon_url(site: str, profile_url: str) -> str:
    host = str(urlparse(str(profile_url or "").strip()).hostname or "").lower().replace("www.", "")
    if not host:
        host = str(site or "").strip().lower().replace("www.", "")
    if not host:
        return ""
    return f"https://www.google.com/s2/favicons?domain={quote(host)}&sz=32"


def _footprint_entry_key(source: str, selector_type: str, selector_value: str, summary: str) -> str:
    return "|".join(
        [
            str(source or "").strip().lower(),
            str(selector_type or "").strip().lower(),
            str(selector_value or "").strip().lower(),
            str(summary or "").strip().lower(),
        ]
    )


def _normalize_case_notes_report_preferences(notes: dict) -> dict[str, set[str]]:
    prefs = notes.get("report_preferences") if isinstance(notes.get("report_preferences"), dict) else {}
    excluded_sections = {
        str(item or "").strip().lower()
        for item in (prefs.get("excluded_sections") if isinstance(prefs.get("excluded_sections"), list) else [])
        if str(item or "").strip()
        and not str(item or "").strip().lower().startswith("digital_footprint_")
    }
    excluded_footprint_keys = {
        str(item or "").strip().lower()
        for item in (
            prefs.get("excluded_footprint_result_keys")
            if isinstance(prefs.get("excluded_footprint_result_keys"), list)
            else []
        )
        if str(item or "").strip()
    }
    return {
        "excluded_sections": excluded_sections,
        "excluded_footprint_result_keys": excluded_footprint_keys,
    }


def _footprint_source_priority(source: str) -> int:
    clean = str(source or "").strip().lower()
    if clean == "osint industries":
        return 0
    if clean == "people data labs":
        return 1
    if clean.startswith("recon (osint_industries"):
        return 2
    if clean.startswith("recon (pdl"):
        return 3
    if clean == "numverify":
        return 4
    if clean.startswith("recon ("):
        return 5
    return 6


def _normalize_recon_snapshot_payload(notes: dict) -> dict:
    snapshot = notes.get("recon_snapshot") if isinstance(notes.get("recon_snapshot"), dict) else {}
    if isinstance(snapshot.get("payload"), dict):
        payload = snapshot.get("payload")
    elif any(isinstance(snapshot.get(key), list) for key in ("results", "osint_profiles", "numverify_profiles", "person_data_profiles")):
        payload = snapshot
    else:
        payload = {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _build_digital_footprint_back_matter(notes: dict) -> list[dict[str, str]]:
    payload = _normalize_recon_snapshot_payload(notes)
    preferences = _normalize_case_notes_report_preferences(notes)
    excluded_keys = preferences.get("excluded_footprint_result_keys", set())
    entries: list[dict[str, str]] = []

    def _field(label: str, value: str) -> dict[str, str] | None:
        clean_label = str(label or "").strip()
        clean_value = str(value or "").strip()
        if not clean_label or not clean_value:
            return None
        return {"label": clean_label, "value": clean_value}

    def add_item(
        *,
        source: str,
        selector_type: str,
        selector_value: str,
        site_label: str = "",
        profile_url: str = "",
        image_url: str = "",
        metadata: list[dict[str, str]] | None = None,
        exclusion_aliases: list[str] | None = None,
    ) -> None:
        clean_source = str(source or "").strip() or "Digital Footprint"
        clean_selector_type = str(selector_type or "").strip().lower()
        clean_selector_value = str(selector_value or "").strip()
        clean_site_label = str(site_label or "").strip()
        clean_profile_url = str(profile_url or "").strip()
        clean_image_url = _image_source_to_data_uri(str(image_url or "").strip())
        metadata_rows = []
        for item in metadata or []:
            if not isinstance(item, dict):
                continue
            row = _field(str(item.get("label") or ""), str(item.get("value") or ""))
            if row:
                metadata_rows.append(row)
        summary = " | ".join(f"{item['label']}: {item['value']}" for item in metadata_rows) if metadata_rows else "No details available."
        entry_key = _footprint_entry_key(
            clean_source,
            clean_selector_type,
            clean_selector_value,
            " | ".join(part for part in (clean_site_label, clean_profile_url, clean_image_url, summary) if part),
        )
        legacy_key = _footprint_entry_key(clean_source, clean_selector_type, clean_selector_value, summary)
        aliases = {
            str(item or "").strip().lower()
            for item in (exclusion_aliases or [])
            if str(item or "").strip()
        }
        if entry_key in excluded_keys or legacy_key in excluded_keys or aliases.intersection(excluded_keys):
            return
        entry = {
            "key": entry_key,
            "legacy_key": legacy_key,
            "source": clean_source,
            "selector_type": clean_selector_type,
            "selector_value": clean_selector_value,
            "selector_label": _selector_label(clean_selector_type, clean_selector_value),
            "selector_display": _selector_display_label(clean_selector_type),
            "selector_provenance": _selector_provenance_label(clean_selector_type, clean_selector_value),
            "site_label": clean_site_label or clean_source,
            "profile_url": clean_profile_url,
            "image_url": clean_image_url,
            "favicon_url": _site_favicon_url(clean_site_label, clean_profile_url),
            "summary": summary,
            "metadata": metadata_rows,
        }
        entries.append(entry)

    for item in payload.get("results", []) if isinstance(payload.get("results"), list) else []:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status") or "unknown").strip().lower() or "unknown"
        site = str(item.get("site") or item.get("site_key") or "unknown").strip() or "unknown"
        source = str(item.get("source") or "Recon").strip() or "Recon"
        profile_url = str(item.get("profile_url") or "").strip()
        reason = str(item.get("reason") or "").strip()
        add_item(
            source=f"Recon ({source})",
            selector_type=str(item.get("selector_type") or ""),
            selector_value=str(item.get("selector") or ""),
            site_label=_guess_site_from_url(profile_url) if profile_url else site,
            profile_url=profile_url,
            image_url=str(item.get("profile_image_url") or item.get("picture_url") or item.get("avatar_url") or item.get("screenshot_url") or ""),
            metadata=[row for row in [
                _field("Status", status),
                _field("Reason", reason),
            ] if row],
            exclusion_aliases=[
                _footprint_entry_key(
                    f"Recon ({source})",
                    str(item.get("selector_type") or ""),
                    str(item.get("selector") or ""),
                    " | ".join(
                        part
                        for part in (
                            f"Status: {status}",
                            f"Site: {site}" if site else "",
                            f"URL: {profile_url}" if profile_url else "",
                            f"Reason: {reason}" if reason else "",
                        )
                        if part
                    ),
                )
            ],
        )

    for item in payload.get("osint_profiles", []) if isinstance(payload.get("osint_profiles"), list) else []:
        if not isinstance(item, dict):
            continue
        module = str(item.get("module") or "osint_industries").strip() or "osint_industries"
        website = str(item.get("website") or "").strip()
        profile_url = str(item.get("profile_url") or "").strip()
        username = str(item.get("username") or "").strip()
        email = str(item.get("email") or "").strip()
        phone = str(item.get("phone") or "").strip()
        add_item(
            source="OSINT Industries",
            selector_type=str(item.get("query_type") or ""),
            selector_value=str(item.get("query_value") or ""),
            site_label=website or _guess_site_from_url(profile_url),
            profile_url=profile_url,
            image_url=str(item.get("picture_url") or item.get("avatar_url") or item.get("profile_image_url") or item.get("screenshot_url") or ""),
            metadata=[row for row in [
                _field("Module", module),
                _field("Username", username),
                _field("Email", email),
                _field("Phone", phone),
            ] if row],
        )

    for item in payload.get("numverify_profiles", []) if isinstance(payload.get("numverify_profiles"), list) else []:
        if not isinstance(item, dict):
            continue
        number = str(item.get("number") or item.get("international_format") or "").strip()
        country = str(item.get("country_name") or "").strip()
        carrier = str(item.get("carrier") or "").strip()
        line_type = str(item.get("line_type") or "").strip()
        valid = bool(item.get("valid"))
        add_item(
            source="Numverify",
            selector_type=str(item.get("query_type") or "phone"),
            selector_value=str(item.get("query_value") or ""),
            site_label="Phone Intelligence",
            metadata=[row for row in [
                _field("Valid", "yes" if valid else "no"),
                _field("Number", number),
                _field("Country", country),
                _field("Carrier", carrier),
                _field("Line Type", line_type),
            ] if row],
        )

    for item in payload.get("person_data_profiles", []) if isinstance(payload.get("person_data_profiles"), list) else []:
        if not isinstance(item, dict):
            continue
        full_name = str(item.get("full_name") or "").strip()
        location = str(item.get("location_name") or "").strip()
        job_title = str(item.get("job_title") or "").strip()
        company = str(item.get("job_company_name") or "").strip()
        linkedin = str(item.get("linkedin_url") or "").strip()
        work_email = str(item.get("professional_email") or item.get("work_email") or "").strip()
        mobile = str(item.get("mobile_phone") or "").strip()
        add_item(
            source="People Data Labs",
            selector_type=str(item.get("query_type") or ""),
            selector_value=str(item.get("query_value") or ""),
            site_label="People Data Labs",
            profile_url=linkedin,
            image_url=str(item.get("picture_url") or item.get("avatar_url") or ""),
            metadata=[row for row in [
                _field("Name", full_name),
                _field("Location", location),
                _field("Employment", f"{job_title}{(' @ ' + company) if company else ''}".strip()),
                _field("Work Email", work_email),
                _field("Mobile", mobile),
            ] if row],
        )

    return sorted(
        entries,
        key=lambda item: (
            _footprint_source_priority(str(item.get("source") or "")),
            str(item.get("site_label") or item.get("source") or "").strip().lower(),
            str(item.get("selector_value") or "").strip().lower(),
            str(item.get("profile_url") or "").strip().lower(),
        ),
    )


def _extract_pdf_text(raw_pdf: bytes) -> str:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(io.BytesIO(raw_pdf))
        chunks: list[str] = []
        for page in reader.pages:
            chunks.append(str(page.extract_text() or ""))
        text = "\n".join(chunks).strip()
        if text:
            return text
    except Exception:
        pass

    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as handle:
            tmp_path = Path(handle.name)
            handle.write(raw_pdf)
        try:
            completed = subprocess.run(
                ["pdftotext", str(tmp_path), "-"],
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
            text = str(completed.stdout or "").strip()
            if text:
                return text
        finally:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass
    except Exception:
        pass
    return ""


def _extract_uploaded_text(*, file_name: str, file_mime_type: str, file_content_base64: str) -> tuple[str, str]:
    name = str(file_name or "").strip()
    mime = str(file_mime_type or "").strip().lower()
    b64 = str(file_content_base64 or "").strip()
    if not b64:
        return "", "missing file data"
    try:
        raw = base64.b64decode(b64, validate=True)
    except (binascii.Error, ValueError):
        return "", "invalid file encoding"
    if len(raw) > 10 * 1024 * 1024:
        return "", "file too large (max 10MB)"

    suffix = Path(name).suffix.lower()
    if suffix == ".pdf" or mime == "application/pdf":
        text = _extract_pdf_text(raw)
        if not text:
            return "", "unable to extract text from PDF"
        return text, ""
    if suffix in {".txt", ".md"} or mime.startswith("text/"):
        try:
            return raw.decode("utf-8", errors="ignore").strip(), ""
        except Exception:
            return "", "unable to decode text file"
    return "", "unsupported file type (allowed: PDF, TXT, MD)"


def _build_case_notes_pdf_stylized(case_row: dict, posts: list[dict]) -> bytes:
    from playwright.sync_api import sync_playwright  # type: ignore

    notes = case_row.get("case_notes") if isinstance(case_row.get("case_notes"), dict) else {}
    name = str(notes.get("name") or case_row.get("case_name") or "Untitled").strip() or "Untitled"
    location = str(notes.get("location") or case_row.get("known_location") or "").strip() or "Unknown"
    age = str(notes.get("age") or "").strip() or "Unknown"
    akas = str(notes.get("akas") or "").strip() or "None"
    context = str(notes.get("context") or "").strip() or "No context provided."
    threat = str(notes.get("threat_risk_assessment") or "").strip() or "No threat assessment provided."
    underlying_themes = _extract_underlying_themes(posts)
    personal = str(notes.get("personal_details") or "").strip() or "No personal details provided."
    selector_emails = str(notes.get("selector_emails") or "").strip() or "None"
    selector_phones = str(notes.get("selector_phone_numbers") or "").strip() or "None"
    selector_usernames = str(notes.get("selector_usernames") or "").strip() or "None"
    report_preferences = _normalize_case_notes_report_preferences(notes)
    excluded_sections = report_preferences.get("excluded_sections", set())
    footprint_groups = _build_digital_footprint_back_matter(notes)
    subject_image = _image_source_to_data_uri(str(notes.get("subject_image_url") or case_row.get("poi_image_url") or "").strip())
    report_ref = str(case_row.get("id") or case_row.get("case_id") or case_row.get("case_name") or "UNASSIGNED").strip() or "UNASSIGNED"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    profiles_raw = notes.get("known_profiles") if isinstance(notes.get("known_profiles"), list) else []
    profiles = _major_profiles(profiles_raw) if profiles_raw else _major_profiles(_discover_profiles_from_posts(posts))
    selector_email_items = [item.strip() for item in selector_emails.split(",") if item.strip()] if selector_emails and selector_emails != "None" else []
    selector_phone_items = [item.strip() for item in selector_phones.split(",") if item.strip()] if selector_phones and selector_phones != "None" else []
    selector_username_items = [item.strip() for item in selector_usernames.split(",") if item.strip()] if selector_usernames and selector_usernames != "None" else []
    selector_total = len(selector_email_items) + len(selector_phone_items) + len(selector_username_items)

    def selector_chips(values: list[str], empty_label: str = "None") -> str:
        if not values:
            return f'<span class="selector-chip selector-chip-empty">{_html_escape(empty_label)}</span>'
        return "".join(f'<span class="selector-chip">{_html_escape(value)}</span>' for value in values)

    def profile_cards() -> str:
        if not profiles:
            return '<p class="footprint-empty">No major profiles.</p>'
        cards: list[str] = []
        for item in profiles:
            row = item if isinstance(item, dict) else {}
            profile_name = str(row.get("name") or row.get("site") or "Unknown").strip() or "Unknown"
            profile_url = str(row.get("url") or "").strip()
            profile_site = str(row.get("site") or "").strip() or _guess_site_from_url(profile_url)
            profile_shot = _image_source_to_data_uri(str(row.get("screenshot_url") or "").strip())
            cards.append(
                f"""
                <article class="profile-card">
                  <div class="profile-card-head">
                    <div>
                      <div class="profile-card-title">{_html_escape(profile_name)}</div>
                      <div class="profile-card-site">{_html_escape(profile_site)}</div>
                    </div>
                  </div>
                  <div class="profile-card-url">{_html_escape(profile_url or 'No profile URL captured')}</div>
                  <div class="profile-card-shot">
                    {f'<img src="{profile_shot}" alt="Profile screenshot" />' if profile_shot else '<div class="profile-card-shot-empty">No screenshot available</div>'}
                  </div>
                </article>
                """
            )
        return "".join(cards)

    def footprint_cards() -> str:
        entries = footprint_groups
        if not entries:
            return '<p class="footprint-empty">No associated results.</p>'
        output: list[str] = []
        for item in entries:
            metadata = item.get("metadata") if isinstance(item.get("metadata"), list) else []
            selector_provenance = str(item.get("selector_provenance") or "").strip()
            selector_label = str(item.get("selector_label") or "").strip()
            metadata_markup = "".join(
                f"""
                <div class="footprint-meta-item">
                  <div class="footprint-meta-label">{_html_escape(str(row.get("label") or ""))}</div>
                  <div class="footprint-meta-value">{_html_escape(str(row.get("value") or ""))}</div>
                </div>
                """
                for row in metadata
                if isinstance(row, dict) and str(row.get("label") or "").strip() and str(row.get("value") or "").strip()
            ) or """
                <div class="footprint-meta-item footprint-meta-item-empty">
                  <div class="footprint-meta-label">Details</div>
                  <div class="footprint-meta-value na">No associated metadata captured.</div>
                </div>
            """
            image_url = str(item.get("image_url") or "").strip()
            profile_url = str(item.get("profile_url") or "").strip()
            site_label = str(item.get("site_label") or item.get("source") or "Digital Footprint").strip() or "Digital Footprint"
            output.append(
                f"""
                <article class="footprint-card">
                  <div class="footprint-card-media">
                    {f'<img class="footprint-card-avatar" src="{_html_escape(image_url)}" alt="Profile image" />' if image_url else '<div class="footprint-card-avatar footprint-card-avatar-placeholder">No image</div>'}
                  </div>
                  <div class="footprint-card-body">
                    <div class="footprint-card-head">
                      <div class="footprint-card-site">
                        <div>
                          <div class="footprint-card-site-name">{_html_escape(site_label)}</div>
                          <div class="footprint-card-source">{_html_escape(str(item.get("source") or "Digital Footprint"))}</div>
                        </div>
                      </div>
                    </div>
                    <div class="footprint-card-evidence">
                      <div class="footprint-evidence-item">
                        <div class="footprint-evidence-label">Profile URL</div>
                        <div class="footprint-evidence-value footprint-card-url">{_html_escape(profile_url or 'No profile URL captured')}</div>
                      </div>
                      <div class="footprint-evidence-item">
                        <div class="footprint-evidence-label">Identified Via</div>
                        <div class="footprint-evidence-value">{_html_escape(selector_provenance or 'Not recorded')}</div>
                      </div>
                      <div class="footprint-evidence-item">
                        <div class="footprint-evidence-label">Evidence Type</div>
                        <div class="footprint-evidence-value">{_html_escape(selector_label or 'Digital Footprint')}</div>
                      </div>
                    </div>
                    <div class="footprint-meta-grid">{metadata_markup}</div>
                  </div>
                </article>
                """
            )
        return "".join(output)

    show_context = "context" not in excluded_sections
    show_threat = "threat_risk_assessment" not in excluded_sections
    show_personal = "personal_details" not in excluded_sections
    show_selectors = "selectors" not in excluded_sections
    show_known_profiles = "known_profiles" not in excluded_sections
    show_footprint_section = "digital_footprint" not in excluded_sections
    context_section = (
        f"""
          <section class="report-section">
            <h2>Context</h2>
            <p>{_html_escape(context)}</p>
          </section>
        """
        if show_context
        else ""
    )
    threat_section = (
        f"""
          <section class="report-section">
            <h2>Threat / Risk Assessment</h2>
            <p>{_html_escape(threat)}</p>
            <div class="section-callout">
              <span class="section-callout-label">Underlying Themes</span>
              <span class="section-callout-value">{_html_escape(', '.join(underlying_themes) if underlying_themes else 'None')}</span>
            </div>
          </section>
        """
        if show_threat
        else ""
    )
    personal_section = (
        f"""
          <section class="report-section">
            <h2>Personal Details</h2>
            <p>{_html_escape(personal)}</p>
          </section>
        """
        if show_personal
        else ""
    )
    selectors_section = (
        f"""
          <section class="report-section">
            <h2>Selectors</h2>
            <div class="selector-groups">
              <div class="selector-group">
                <div class="selector-group-label">Emails</div>
                <div class="selector-chip-row">{selector_chips(selector_email_items)}</div>
              </div>
              <div class="selector-group">
                <div class="selector-group-label">Phone Numbers</div>
                <div class="selector-chip-row">{selector_chips(selector_phone_items)}</div>
              </div>
              <div class="selector-group">
                <div class="selector-group-label">User Names</div>
                <div class="selector-chip-row">{selector_chips(selector_username_items)}</div>
              </div>
            </div>
          </section>
        """
        if show_selectors
        else ""
    )
    known_profiles_section = (
        f"""
          <section class="report-section">
            <h2>Major Profiles</h2>
            <div class="profile-grid">{profile_cards()}</div>
          </section>
        """
        if show_known_profiles
        else ""
    )
    footprint_section = ""
    if show_footprint_section:
        footprint_section = f"""
          <section class="backmatter">
            <div class="backmatter-kicker">Appendix A</div>
            <h2>Digital Footprint Evidence</h2>
            <p class="backmatter-intro">The following digital footprint material is attached as evidentiary backmatter supporting the principal case narrative.</p>
            <div class="footprint-group">
              <h3>Results <span>{len(footprint_groups)}</span></h3>
              <div class="footprint-cards">{footprint_cards()}</div>
            </div>
          </section>
        """

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          @page {{
            size: A4;
            margin: 22mm 16mm 18mm 16mm;
            @bottom-right {{
              content: "Pg " counter(page) " of " counter(pages);
              font-size: 9px;
              color: #4b5563;
            }}
          }}
          body {{ font-family: "Helvetica Neue", Arial, sans-serif; color: #111827; margin: 0; background: #eef2f7; }}
          .report {{ border: 1px solid #1f2937; padding: 14px; background: #ffffff; }}
          .header {{ margin-bottom: 14px; border: 1px solid #cbd5e1; background: linear-gradient(135deg, #0f172a 0%, #1e293b 58%, #334155 100%); color: #f8fafc; overflow: hidden; }}
          .header-shell {{ display: grid; grid-template-columns: minmax(0, 1fr) 132px; gap: 16px; padding: 16px; align-items: start; }}
          .header-kicker {{ font-size: 10px; text-transform: uppercase; letter-spacing: .18em; color: rgba(226, 232, 240, .82); margin-bottom: 8px; }}
          .header h1 {{ margin: 0; font-size: 24px; letter-spacing: .08em; }}
          .header .sub {{ margin-top: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: rgba(226, 232, 240, .9); }}
          .meta-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
          .meta-pill {{ border: 1px solid rgba(148, 163, 184, .45); padding: 5px 9px; font-size: 9px; text-transform: uppercase; letter-spacing: .08em; color: #e2e8f0; background: rgba(15, 23, 42, .32); }}
          .header-band {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: rgba(148, 163, 184, .25); border-top: 1px solid rgba(148, 163, 184, .25); }}
          .header-band-item {{ background: rgba(248, 250, 252, .08); padding: 10px 16px 12px; }}
          .header-band-label {{ font-size: 8.5px; text-transform: uppercase; letter-spacing: .14em; color: rgba(226, 232, 240, .72); margin-bottom: 4px; }}
          .header-band-value {{ font-size: 13px; font-weight: 700; color: #f8fafc; }}
          .subject-image-frame {{ width: 132px; height: 132px; padding: 6px; border: 1px solid rgba(148, 163, 184, .45); background: rgba(15, 23, 42, .42); }}
          .subject-image {{ width: 100%; height: 100%; border: 1px solid rgba(248, 250, 252, .16); object-fit: cover; background: rgba(248, 250, 252, .08); }}
          .summary-grid {{ display: grid; grid-template-columns: 1.2fr .8fr; gap: 12px; margin: 0 0 14px; }}
          .summary-panel {{ border: 1px solid #cbd5e1; background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); padding: 12px; }}
          .summary-panel-title {{ font-size: 10px; text-transform: uppercase; letter-spacing: .14em; color: #475569; margin-bottom: 8px; }}
          .summary-stats {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }}
          .summary-stat {{ border: 1px solid #dbe4ee; background: #fff; padding: 10px; }}
          .summary-stat-value {{ font-size: 20px; font-weight: 800; color: #0f172a; line-height: 1; }}
          .summary-stat-label {{ margin-top: 5px; font-size: 9px; text-transform: uppercase; letter-spacing: .1em; color: #64748b; }}
          .summary-text {{ font-size: 11px; color: #334155; line-height: 1.55; }}
          .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 10px 0 14px; }}
          .cell {{ border: 1px solid #cbd5e1; padding: 8px 10px; min-height: 44px; background: #f8fafc; }}
          .label {{ font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: #4b5563; margin-bottom: 4px; }}
          .value {{ font-size: 13px; font-weight: 600; }}
          .report-section {{ margin-bottom: 14px; padding: 0 0 2px; }}
          h2 {{ margin: 14px 0 6px; font-size: 13px; text-transform: uppercase; letter-spacing: .08em; border-bottom: 1px solid #94a3b8; padding-bottom: 4px; }}
          p {{ margin: 0; font-size: 11.5px; line-height: 1.48; white-space: pre-wrap; }}
          .section-callout {{ margin-top: 8px; padding: 8px 10px; border-left: 3px solid #0f172a; background: #f8fafc; }}
          .section-callout-label {{ display: block; font-size: 8.5px; text-transform: uppercase; letter-spacing: .1em; color: #64748b; margin-bottom: 3px; }}
          .section-callout-value {{ font-size: 10.5px; font-weight: 600; color: #0f172a; }}
          .selector-groups {{ display: grid; gap: 8px; }}
          .selector-group {{ border: 1px solid #dbe4ee; background: #f8fafc; padding: 8px 9px; }}
          .selector-group-label {{ font-size: 9px; text-transform: uppercase; letter-spacing: .1em; color: #64748b; margin-bottom: 6px; }}
          .selector-chip-row {{ display: flex; flex-wrap: wrap; gap: 6px; }}
          .selector-chip {{ display: inline-flex; align-items: center; padding: 4px 8px; border: 1px solid #cbd5e1; background: #fff; font-size: 9.5px; color: #0f172a; border-radius: 999px; word-break: break-word; }}
          .selector-chip-empty {{ color: #64748b; background: #f8fafc; }}
          .profile-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 8px; }}
          .profile-card {{ border: 1px solid #cbd5e1; background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); padding: 10px; page-break-inside: avoid; }}
          .profile-card-title {{ font-size: 13px; font-weight: 700; color: #0f172a; }}
          .profile-card-site {{ font-size: 9px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; margin-top: 3px; }}
          .profile-card-url {{ margin-top: 8px; font-size: 10px; color: #1d4ed8; word-break: break-all; }}
          .profile-card-shot {{ margin-top: 8px; }}
          .profile-card-shot img {{ width: 100%; max-height: 120px; object-fit: cover; display: block; border: 1px solid #d1d5db; }}
          .profile-card-shot-empty {{ min-height: 72px; display: flex; align-items: center; justify-content: center; border: 1px dashed #cbd5e1; background: #fff; font-size: 9px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; }}
          table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
          th, td {{ border: 1px solid #cbd5e1; padding: 6px 7px; font-size: 10.5px; vertical-align: top; text-align: left; }}
          th {{ background: #e2e8f0; text-transform: uppercase; letter-spacing: .05em; font-size: 9.5px; }}
          h3 {{ margin: 10px 0 6px; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #1f2937; display: flex; justify-content: space-between; align-items: center; }}
          h3 span {{ border: 1px solid #94a3b8; border-radius: 999px; padding: 1px 7px; font-size: 9px; background: #f8fafc; }}
          td.url {{ word-break: break-all; }}
          td img {{ width: 180px; max-height: 110px; object-fit: cover; display: block; border: 1px solid #d1d5db; }}
          .na {{ color: #6b7280; }}
          .footprint-group + .footprint-group {{ margin-top: 12px; }}
          .footprint-cards {{ display: grid; gap: 12px; }}
          .footprint-card {{ border: 1px solid #cbd5e1; padding: 12px; display: grid; grid-template-columns: 92px minmax(0, 1fr); gap: 12px; background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%); page-break-inside: avoid; box-shadow: inset 0 1px 0 rgba(255,255,255,.65); }}
          .footprint-card-media {{ display: flex; }}
          .footprint-card-avatar {{ width: 92px; height: 92px; object-fit: cover; border: 1px solid #cbd5e1; background: #e5e7eb; }}
          .footprint-card-avatar-placeholder {{ display: flex; align-items: center; justify-content: center; font-size: 9px; text-transform: uppercase; letter-spacing: .06em; color: #6b7280; background: #f1f5f9; }}
          .footprint-card-body {{ display: grid; gap: 8px; min-width: 0; }}
          .footprint-card-head {{ display: flex; align-items: start; gap: 8px; }}
          .footprint-card-site {{ display: flex; align-items: center; gap: 8px; min-width: 0; }}
          .footprint-card-site-name {{ font-size: 14px; font-weight: 700; }}
          .footprint-card-source {{ font-size: 9px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; }}
          .footprint-card-evidence {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; }}
          .footprint-evidence-item {{ border: 1px solid #dbe4ee; background: #fff; padding: 7px 8px; min-width: 0; }}
          .footprint-evidence-label {{ font-size: 8.5px; text-transform: uppercase; letter-spacing: .08em; color: #6b7280; margin-bottom: 4px; }}
          .footprint-evidence-value {{ font-size: 10px; font-weight: 600; color: #0f172a; line-height: 1.35; word-break: break-word; }}
          .footprint-card-url {{ color: #1d4ed8; }}
          .footprint-meta-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; }}
          .footprint-meta-item {{ border: 1px solid #dbe4ee; padding: 7px 8px; background: #fff; }}
          .footprint-meta-item-empty {{ grid-column: 1 / -1; }}
          .footprint-meta-label {{ font-size: 8.5px; text-transform: uppercase; letter-spacing: .08em; color: #6b7280; margin-bottom: 3px; }}
          .footprint-meta-value {{ font-size: 10px; line-height: 1.4; word-break: break-word; }}
          .footprint-empty {{ padding: 8px 10px; border: 1px dashed #94a3b8; color: #6b7280; font-size: 10px; background: #f8fafc; }}
          .backmatter {{ margin-top: 18px; padding-top: 12px; border-top: 2px solid #0f172a; break-before: page; page-break-before: always; }}
          .backmatter-kicker {{ font-size: 10px; text-transform: uppercase; letter-spacing: .14em; color: #6b7280; margin-bottom: 6px; }}
          .backmatter-intro {{ margin-bottom: 10px; font-size: 10.5px; color: #374151; }}
          .footer {{ margin-top: 10px; font-size: 9px; color: #6b7280; text-align: right; }}
        </style>
      </head>
      <body>
        <section class="report">
          <header class="header">
            <div class="header-shell">
              <div>
                <div class="header-kicker">Orion Intelligence Report</div>
                <h1>PERSON OF INTEREST REPORT</h1>
                <div class="sub">Case Intelligence Summary</div>
                <div class="meta-row">
                  <div class="meta-pill">Report Ref: {_html_escape(report_ref)}</div>
                  <div class="meta-pill">Generated: {_html_escape(generated_at)}</div>
                  <div class="meta-pill">Compiled by Orion</div>
                </div>
              </div>
              <div class="subject-image-frame">
                {f'<img class="subject-image" src="{subject_image}" alt="Subject image" />' if subject_image else '<div class="subject-image"></div>'}
              </div>
            </div>
            <div class="header-band">
              <div class="header-band-item">
                <div class="header-band-label">Primary Subject</div>
                <div class="header-band-value">{_html_escape(name)}</div>
              </div>
              <div class="header-band-item">
                <div class="header-band-label">Known Location</div>
                <div class="header-band-value">{_html_escape(location)}</div>
              </div>
              <div class="header-band-item">
                <div class="header-band-label">Known Aliases</div>
                <div class="header-band-value">{_html_escape(akas)}</div>
              </div>
            </div>
          </header>
          <section class="summary-grid">
            <div class="summary-panel">
              <div class="summary-panel-title">Assessment Snapshot</div>
              <div class="summary-text">This report consolidates the subject overview, key narrative notes, saved selectors, major profiles, and attached digital-footprint evidence into a single review document.</div>
            </div>
            <div class="summary-panel">
              <div class="summary-panel-title">Case Metrics</div>
              <div class="summary-stats">
                <div class="summary-stat">
                  <div class="summary-stat-value">{len(profiles)}</div>
                  <div class="summary-stat-label">Major Profiles</div>
                </div>
                <div class="summary-stat">
                  <div class="summary-stat-value">{len(footprint_groups)}</div>
                  <div class="summary-stat-label">Evidence Tiles</div>
                </div>
                <div class="summary-stat">
                  <div class="summary-stat-value">{selector_total}</div>
                  <div class="summary-stat-label">Saved Selectors</div>
                </div>
              </div>
            </div>
          </section>
          <section class="grid">
            <div class="cell"><div class="label">Name</div><div class="value">{_html_escape(name)}</div></div>
            <div class="cell"><div class="label">Location</div><div class="value">{_html_escape(location)}</div></div>
            <div class="cell"><div class="label">Age</div><div class="value">{_html_escape(age)}</div></div>
            <div class="cell" style="grid-column: 1 / -1;"><div class="label">A.K.A.s</div><div class="value">{_html_escape(akas)}</div></div>
          </section>
          {context_section}
          {threat_section}
          {personal_section}
          {selectors_section}
          {known_profiles_section}
          {footprint_section}
          <div class="footer">Generated by Orion</div>
        </section>
      </body>
    </html>
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1240, "height": 1754})
        page = context.new_page()
        try:
            page.set_content(html, wait_until="domcontentloaded")
            return page.pdf(format="A4", print_background=True)
        finally:
            context.close()
            browser.close()


def _build_case_notes_pdf_fallback(case_row: dict, posts: list[dict]) -> bytes:
    notes = case_row.get("case_notes") if isinstance(case_row.get("case_notes"), dict) else {}
    name = str(notes.get("name") or case_row.get("case_name") or "Untitled").strip() or "Untitled"
    location = str(notes.get("location") or case_row.get("known_location") or "").strip()
    age = str(notes.get("age") or "").strip()
    akas = str(notes.get("akas") or "").strip()
    context = str(notes.get("context") or "").strip()
    threat = str(notes.get("threat_risk_assessment") or "").strip()
    underlying_themes = _extract_underlying_themes(posts)
    personal = str(notes.get("personal_details") or "").strip()
    selector_emails = str(notes.get("selector_emails") or "").strip()
    selector_phones = str(notes.get("selector_phone_numbers") or "").strip()
    selector_usernames = str(notes.get("selector_usernames") or "").strip()
    report_preferences = _normalize_case_notes_report_preferences(notes)
    excluded_sections = report_preferences.get("excluded_sections", set())
    footprint_groups = _build_digital_footprint_back_matter(notes)
    profiles = _major_profiles(notes.get("known_profiles") if isinstance(notes.get("known_profiles"), list) else [])
    if not profiles:
        profiles = _major_profiles(_discover_profiles_from_posts(posts))

    page_width = 612
    page_height = 792
    outer_margin = 28
    content_left = 48
    content_right = page_width - content_left
    content_width = content_right - content_left
    top_y = page_height - 44
    bottom_y = 48
    banner_height = 54
    report_ref = str(case_row.get("id") or case_row.get("case_id") or case_row.get("case_name") or "UNASSIGNED").strip() or "UNASSIGNED"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    pages: list[list[str]] = []
    cursor_y = top_y

    def _chars_for_width(width: float, size: int) -> int:
        approx = int(width / max(size * 0.52, 1))
        return max(12, approx)

    def new_page() -> None:
        nonlocal cursor_y
        pages.append([])
        page = pages[-1]
        page.append(f"0 G 1 w {outer_margin} {outer_margin} {page_width - (outer_margin * 2)} {page_height - (outer_margin * 2)} re S")
        banner_y = top_y - banner_height + 10
        page.append(f"q 0.15 g 0.15 G {outer_margin} {banner_y} {page_width - (outer_margin * 2)} {banner_height} re B Q")
        page.append(f"BT 1 g /F2 19 Tf 1 0 0 1 {content_left} {top_y - 12} Tm (PERSON OF INTEREST REPORT) Tj ET")
        page.append(f"BT 1 g /F1 9 Tf 1 0 0 1 {content_left} {top_y - 28} Tm (Case Intelligence Summary) Tj ET")
        page.append(f"BT 1 g /F2 8 Tf 1 0 0 1 {content_right - 124} {top_y - 14} Tm (Report Ref.) Tj ET")
        page.append(f"BT 1 g /F1 8 Tf 1 0 0 1 {content_right - 124} {top_y - 26} Tm ({_pdf_escape(report_ref[:24])}) Tj ET")
        page.append(f"BT 0 g /F1 8 Tf 1 0 0 1 {content_left} {outer_margin + 10} Tm (Generated by Orion | { _pdf_escape(generated_at) }) Tj ET")
        page.append(f"BT 0 g /F1 8 Tf 1 0 0 1 {content_right - 175} {outer_margin + 10} Tm (Report Ref: { _pdf_escape(report_ref[:36]) }) Tj ET")
        cursor_y = top_y - banner_height - 10

    def ensure_room(required_height: int) -> None:
        nonlocal cursor_y
        if not pages:
            new_page()
        if cursor_y - required_height >= bottom_y:
            return
        new_page()

    def add_text(x: float, y: float, text: str, *, bold: bool = False, size: int = 11, gray: float = 0.0) -> None:
        font = "F2" if bold else "F1"
        safe = _pdf_escape(text)
        pages[-1].append(f"BT {gray:.3f} g /{font} {size} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({safe}) Tj ET")

    def add_wrapped_block(
        text: str,
        *,
        x: float,
        size: int = 11,
        width_chars: int = 92,
        bold: bool = False,
        gray: float = 0.0,
        gap: int | None = None,
    ) -> None:
        nonlocal cursor_y
        line_gap = gap if gap is not None else int(size * 1.45)
        lines = _wrap_pdf_text(text, width_chars)
        ensure_room((len(lines) * line_gap) + 4)
        for line in lines:
            add_text(x, cursor_y, line, bold=bold, size=size, gray=gray)
            cursor_y -= line_gap

    def add_section_header(title: str) -> None:
        nonlocal cursor_y
        ensure_room(28)
        bar_height = 16
        bar_y = cursor_y - 11
        pages[-1].append(f"q 0.90 g 0.70 G {content_left} {bar_y:.2f} {content_width} {bar_height} re B Q")
        add_text(content_left + 8, cursor_y - 7, title, bold=True, size=10, gray=0.0)
        cursor_y -= 24

    def start_backmatter() -> None:
        nonlocal cursor_y
        new_page()
        ensure_room(56)
        add_text(content_left, cursor_y, "APPENDIX A", bold=True, size=10, gray=0.35)
        cursor_y -= 16
        add_text(content_left, cursor_y, "Digital Footprint Evidence", bold=True, size=16, gray=0.0)
        cursor_y -= 18
        add_wrapped_block(
            "The following digital footprint material is attached as evidentiary backmatter supporting the principal case narrative.",
            x=content_left,
            size=9,
            width_chars=_chars_for_width(content_width, 9),
            gray=0.22,
            gap=12,
        )
        cursor_y -= 6

    def add_field_box(x: float, width: float, label: str, value: str, *, height: int = 44) -> None:
        box_y = cursor_y - height
        pages[-1].append(f"q 0.97 g 0.65 G {x:.2f} {box_y:.2f} {width:.2f} {height} re B Q")
        add_text(x + 8, cursor_y - 13, label.upper(), bold=True, size=8, gray=0.35)
        inner_width = _chars_for_width(width - 16, 11)
        value_lines = _wrap_pdf_text(value, inner_width)[:2]
        line_y = cursor_y - 28
        for line in value_lines:
            add_text(x + 8, line_y, line, bold=True, size=11, gray=0.0)
            line_y -= 13

    def add_identity_panel() -> None:
        nonlocal cursor_y
        ensure_room(124)
        panel_height = 108
        panel_y = cursor_y - panel_height
        pages[-1].append(f"q 0.985 g 0.55 G {content_left} {panel_y:.2f} {content_width} {panel_height} re B Q")
        add_text(content_left + 10, cursor_y - 15, "SUBJECT IDENTIFICATION", bold=True, size=11, gray=0.0)
        add_text(content_left + 10, cursor_y - 29, f"Case File: {name}", bold=False, size=9, gray=0.28)
        add_text(content_left + 210, cursor_y - 29, f"Compiled: {generated_at}", bold=False, size=9, gray=0.28)
        box_gap = 10
        half_width = (content_width - box_gap) / 2
        add_field_box(content_left + 10, half_width - 10, "Name", name)
        add_field_box(content_left + half_width + box_gap, half_width - 20, "Location", location or "Unknown")
        cursor_y -= 54
        add_field_box(content_left + 10, 120, "Age", age or "Unknown", height=38)
        add_field_box(content_left + 140, content_width - 150, "A.K.A.s", akas or "None", height=38)
        cursor_y = panel_y - 14

    def add_body_paragraph(text: str) -> None:
        nonlocal cursor_y
        add_wrapped_block(text or "None", x=content_left + 6, size=10, width_chars=_chars_for_width(content_width - 12, 10), gap=14)
        cursor_y -= 4

    new_page()
    add_identity_panel()

    if "context" not in excluded_sections:
        add_section_header("Context")
        add_body_paragraph(context or "None")
    if "threat_risk_assessment" not in excluded_sections:
        add_section_header("Threat / Risk Assessment")
        add_body_paragraph(threat or "None")
        add_wrapped_block(
            f"Underlying Themes: {', '.join(underlying_themes) if underlying_themes else 'None'}",
            x=content_left + 6,
            size=10,
            width_chars=_chars_for_width(content_width - 12, 10),
            bold=True,
            gap=14,
        )
        cursor_y -= 4
    if "personal_details" not in excluded_sections:
        add_section_header("Personal Details")
        add_body_paragraph(personal or "None")
    if "selectors" not in excluded_sections:
        add_section_header("Selectors")
        add_body_paragraph(f"Emails: {selector_emails or 'None'}")
        add_body_paragraph(f"Phone Numbers: {selector_phones or 'None'}")
        add_body_paragraph(f"User Names: {selector_usernames or 'None'}")
    if "known_profiles" not in excluded_sections:
        add_section_header("Major Profiles")
        if not profiles:
            add_body_paragraph("None")
        else:
            for item in profiles:
                row = item if isinstance(item, dict) else {}
                site = str(row.get("site") or "Profile").strip() or "Profile"
                url = str(row.get("url") or "").strip()
                screenshot_url = str(row.get("screenshot_url") or "").strip()
                add_wrapped_block(
                    f"[{site}] {url or 'N/A'}",
                    x=content_left + 6,
                    size=10,
                    width_chars=_chars_for_width(content_width - 12, 10),
                    bold=True,
                    gap=14,
                )
                if screenshot_url:
                    add_wrapped_block(
                        f"Screenshot: {screenshot_url}",
                        x=content_left + 18,
                        size=9,
                        width_chars=_chars_for_width(content_width - 24, 9),
                        gray=0.18,
                        gap=13,
                    )
                cursor_y -= 3
        cursor_y -= 3
    if "digital_footprint" not in excluded_sections:
        start_backmatter()
        add_section_header("Digital Footprint Evidence")
        add_wrapped_block(
            f"Results ({len(footprint_groups)})",
            x=content_left + 6,
            size=10,
            width_chars=40,
            bold=True,
            gap=14,
        )
        if not footprint_groups:
            add_body_paragraph("None")
        for item in footprint_groups:
            source = str(item.get("source") or "Digital Footprint").strip() or "Digital Footprint"
            site_label = str(item.get("site_label") or source).strip() or source
            profile_url = str(item.get("profile_url") or "").strip()
            image_url = str(item.get("image_url") or "").strip()
            selector = str(item.get("selector_provenance") or _selector_label(str(item.get("selector_type") or ""), str(item.get("selector_value") or ""))).strip()
            selector_label = str(item.get("selector_label") or "Digital Footprint").strip() or "Digital Footprint"
            metadata = item.get("metadata") if isinstance(item.get("metadata"), list) else []
            add_wrapped_block(
                f"[{source}] {site_label}",
                x=content_left + 18,
                size=9,
                width_chars=_chars_for_width(content_width - 24, 9),
                bold=True,
                gap=13,
            )
            if profile_url:
                add_wrapped_block(
                    f"URL: {profile_url}",
                    x=content_left + 30,
                    size=9,
                    width_chars=_chars_for_width(content_width - 36, 9),
                    gray=0.18,
                    gap=13,
                )
            if image_url:
                add_wrapped_block(
                    f"Profile Image: {image_url}",
                    x=content_left + 30,
                    size=9,
                    width_chars=_chars_for_width(content_width - 36, 9),
                    gray=0.18,
                    gap=13,
                )
            add_wrapped_block(
                f"Evidence Type: {selector_label}",
                x=content_left + 30,
                size=9,
                width_chars=_chars_for_width(content_width - 36, 9),
                gap=13,
            )
            add_wrapped_block(
                f"Identified Via: {selector}",
                x=content_left + 30,
                size=9,
                width_chars=_chars_for_width(content_width - 36, 9),
                bold=True,
                gap=13,
            )
            if metadata:
                for row in metadata:
                    if not isinstance(row, dict):
                        continue
                    label = str(row.get("label") or "").strip()
                    value = str(row.get("value") or "").strip()
                    if not label or not value:
                        continue
                    add_wrapped_block(
                        f"{label}: {value}",
                        x=content_left + 42,
                        size=9,
                        width_chars=_chars_for_width(content_width - 48, 9),
                        gap=13,
                    )
            else:
                add_wrapped_block(
                    "No associated metadata captured.",
                    x=content_left + 42,
                    size=9,
                    width_chars=_chars_for_width(content_width - 48, 9),
                    gap=13,
                )
            cursor_y -= 2

    objects: dict[int, bytes] = {}
    next_id = 1

    def alloc_id() -> int:
        nonlocal next_id
        out = next_id
        next_id += 1
        return out

    catalog_id = alloc_id()
    pages_id = alloc_id()
    font_regular_id = alloc_id()
    font_bold_id = alloc_id()

    page_entries: list[tuple[int, int]] = []
    total_pages = len(pages)
    for page_index, page_ops in enumerate(pages, start=1):
        page_ops.append(
            f"BT 0 g /F1 9 Tf 1 0 0 1 {content_right - 54:.2f} {outer_margin + 10:.2f} Tm (Pg {page_index} of {total_pages}) Tj ET"
        )
        stream_data = "\n".join(page_ops).encode("latin-1", errors="ignore")
        content_id = alloc_id()
        page_id = alloc_id()
        page_entries.append((page_id, content_id))
        objects[content_id] = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream_data), stream_data)

    objects[font_regular_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    objects[font_bold_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"

    for page_id, content_id in page_entries:
        objects[page_id] = (
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")

    kids = " ".join(f"{page_id} 0 R" for page_id, _ in page_entries)
    objects[pages_id] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_entries)} >>".encode("ascii")
    objects[catalog_id] = f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * next_id
    for obj_id in range(1, next_id):
        payload = objects.get(obj_id, b"<<>>")
        offsets[obj_id] = len(out)
        out.extend(f"{obj_id} 0 obj\n".encode("ascii"))
        out.extend(payload)
        out.extend(b"\nendobj\n")

    xref_offset = len(out)
    out.extend(f"xref\n0 {next_id}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for obj_id in range(1, next_id):
        out.extend(f"{offsets[obj_id]:010d} 00000 n \n".encode("ascii"))
    out.extend(
        (
            f"trailer\n<< /Size {next_id} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(out)


def _build_case_notes_pdf(case_row: dict, posts: list[dict]) -> bytes:
    try:
        return _build_case_notes_pdf_stylized(case_row, posts)
    except Exception:
        return _build_case_notes_pdf_fallback(case_row, posts)


def _merge_case_export_payload(case_row: dict, override: dict | None) -> dict:
    merged = dict(case_row) if isinstance(case_row, dict) else {}
    if not isinstance(override, dict) or not override:
        return merged

    if "case_name" in override:
        merged["case_name"] = override.get("case_name")
    if "known_location" in override:
        merged["known_location"] = override.get("known_location")
    if "poi_image_url" in override:
        merged["poi_image_url"] = override.get("poi_image_url")
    if isinstance(override.get("case_notes"), dict):
        existing_notes = merged.get("case_notes") if isinstance(merged.get("case_notes"), dict) else {}
        merged["case_notes"] = {**existing_notes, **override.get("case_notes", {})}
    return merged


class PostExplorerHandler(SimpleHTTPRequestHandler):
    def _request_is_loopback(self) -> bool:
        client = getattr(self, "client_address", None)
        if not client:
            return True
        host = str(client[0] if isinstance(client, tuple) and client else "").strip()
        if not host:
            return True
        try:
            address = ipaddress.ip_address(host.split("%", 1)[0])
            if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
                address = address.ipv4_mapped
            return bool(address.is_loopback)
        except ValueError:
            return host.lower() in {"localhost"}

    def _enforce_loopback_only(self, *, reason: str) -> bool:
        if self._request_is_loopback():
            return True
        self._send_json(
            {"error": {"code": "forbidden", "message": f"{reason} is limited to localhost requests"}},
            status=403,
        )
        return False

    def _write_body(self, body: bytes) -> None:
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError, socket.error):
            # Client closed the connection (e.g. frontend aborted stale request).
            return

    def _stream_json_line(self, payload: dict) -> bool:
        try:
            encoded = f"{json.dumps(payload, ensure_ascii=True)}\n".encode("utf-8")
            self.wfile.write(encoded)
            self.wfile.flush()
            return True
        except (BrokenPipeError, ConnectionResetError, socket.error):
            return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            if not self._enforce_loopback_only(reason="API access"):
                return
        if parsed.path == "/architecture":
            body = _render_architecture_page_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self._write_body(body)
            return
        if parsed.path == "/docs/architecture-diagram.md":
            body = _load_architecture_markdown().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self._write_body(body)
            return
        if parsed.path.startswith("/api/cases/") and parsed.path.endswith("/notes.pdf"):
            case_id = parsed.path.split("/api/cases/", 1)[1].rsplit("/notes.pdf", 1)[0].strip().strip("/")
            if not case_id:
                self._send_json({"error": {"code": "invalid_request", "message": "case_id is required"}}, status=400)
                return
            cases = list_cases(db_path=str(DEFAULT_DB_PATH))
            case_row = next((row for row in cases if str(row.get("case_id") or "").strip() == case_id), None)
            if case_row is None:
                self._send_json({"error": {"code": "not_found", "message": "case not found"}}, status=404)
                return
            posts_payload = query_posts(query="", sort_order="newest", db_path=DEFAULT_DB_PATH, case_id=case_id)
            posts = posts_payload.get("posts") if isinstance(posts_payload, dict) else []
            pdf_bytes = _build_case_notes_pdf(case_row, posts if isinstance(posts, list) else [])
            filename_slug = re.sub(r"[^a-z0-9]+", "-", str(case_row.get("case_name") or "case-notes").lower()).strip("-") or "case-notes"
            filename = f"{filename_slug}-report.pdf"
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.end_headers()
            self._write_body(pdf_bytes)
            return

        if parsed.path == "/api/cases":
            payload = {"cases": list_cases(db_path=str(DEFAULT_DB_PATH))}
            self._send_json(payload)
            return

        if parsed.path == "/api/config":
            self._send_json(load_public_config())
            return

        if parsed.path == "/api/collect/status":
            params = parse_qs(parsed.query)
            job_id = str(params.get("job_id", [""])[0]).strip()
            if not job_id:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "job_id is required"}},
                    status=400,
                )
                return
            payload = get_collection_job_status(job_id)
            if payload is None:
                self._send_json(
                    {"error": {"code": "not_found", "message": "collection job not found"}},
                    status=404,
                )
                return
            self._send_json(payload)
            return

        if parsed.path == "/api/posts":
            params = parse_qs(parsed.query)
            query = params.get("query", [""])[0]
            sort = params.get("sort", ["newest"])[0].lower()
            start_date = params.get("start_date", [""])[0]
            end_date = params.get("end_date", [""])[0]
            case_id = params.get("case_id", [""])[0]
            include_tags_raw = params.get("include_tags", [""])[0]
            exclude_tags_raw = params.get("exclude_tags", [""])[0]
            include_tags = {normalize_tag(tag) for tag in include_tags_raw.split(",") if tag.strip()}
            exclude_tags = {normalize_tag(tag) for tag in exclude_tags_raw.split(",") if tag.strip()}
            include_faces = str(params.get("include_faces", ["1"])[0]).strip().lower() in {"1", "true", "yes", "on"}
            face_refresh = str(params.get("face_refresh", [""])[0]).strip().lower() in {"1", "true", "yes", "on"}
            if face_refresh:
                include_faces = True
            try:
                db_path = _resolve_api_db_path(params.get("db_path", [str(DEFAULT_DB_PATH)])[0])
            except InvalidRequestError as exc:
                self._send_json({"error": {"code": "invalid_request", "message": str(exc)}}, status=400)
                return

            payload = query_posts(
                query=query,
                sort_order=sort,
                db_path=db_path,
                case_id=case_id,
                start_date=start_date,
                end_date=end_date,
                include_tags=include_tags,
                exclude_tags=exclude_tags,
            )
            if isinstance(payload, dict):
                post_rows = payload.get("posts")
                if isinstance(post_rows, list):
                    if include_faces:
                        face_payload = _FACE_RECOGNITION_ENGINE.annotate_posts(post_rows, force_refresh=face_refresh)
                        payload["posts"] = face_payload.get("posts", post_rows)
                        payload["face_clusters"] = face_payload.get("face_clusters", [])
                        payload["face_recognition"] = face_payload.get("face_recognition", {"available": False, "reason": "unknown"})
                    else:
                        payload["face_clusters"] = []
                        payload["face_recognition"] = {
                            "available": bool(getattr(_FACE_RECOGNITION_ENGINE, "is_available", False)),
                            "reason": "not_run",
                        }

            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self._write_body(body)
            return

        if parsed.path in {"/", ""}:
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            if not self._enforce_loopback_only(reason="API access"):
                return

        if parsed.path.startswith("/api/cases/") and parsed.path.endswith("/notes.pdf"):
            case_id = parsed.path.split("/api/cases/", 1)[1].rsplit("/notes.pdf", 1)[0].strip().strip("/")
            if not case_id:
                self._send_json({"error": {"code": "invalid_request", "message": "case_id is required"}}, status=400)
                return
            body = self._read_json_body(default={})
            if body is None:
                return
            cases = list_cases(db_path=str(DEFAULT_DB_PATH))
            case_row = next((row for row in cases if str(row.get("case_id") or "").strip() == case_id), None)
            if case_row is None:
                self._send_json({"error": {"code": "not_found", "message": "case not found"}}, status=404)
                return
            posts_payload = query_posts(query="", sort_order="newest", db_path=DEFAULT_DB_PATH, case_id=case_id)
            posts = posts_payload.get("posts") if isinstance(posts_payload, dict) else []
            export_case_row = _merge_case_export_payload(case_row, body)
            pdf_bytes = _build_case_notes_pdf(export_case_row, posts if isinstance(posts, list) else [])
            filename_slug = re.sub(r"[^a-z0-9]+", "-", str(export_case_row.get("case_name") or "case-notes").lower()).strip("-") or "case-notes"
            filename = f"{filename_slug}-report.pdf"
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(pdf_bytes)))
            self.end_headers()
            self._write_body(pdf_bytes)
            return

        if parsed.path == "/api/session/end":
            body = self._read_json_body(default={})
            if body is None:
                return
            should_shutdown = bool(body.get("shutdown", True))
            should_clear_data = bool(body.get("clear_data", True))
            should_clear_config = bool(body.get("clear_config", should_clear_data))
            if should_clear_data:
                clear_posts(str(DEFAULT_DB_PATH), clear_cases=True)
            if should_clear_config:
                save_config(
                    custom_keyword_list=[],
                    default_data_retention_period="3 months",
                    clear_pdl_api_key=True,
                    clear_osint_industries_api_key=True,
                    clear_numverify_api_key=True,
                    clear_openai_api_key=True,
                    clear_apify_api_token=True,
                )
            response = {
                "status": "ok",
                "cleared": should_clear_data,
                "config_cleared": should_clear_config,
                "shutdown": should_shutdown,
            }
            self._send_json(response)
            if should_shutdown:
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        if parsed.path == "/api/cases":
            body = self._read_json_body()
            if body is None:
                return
            case_name = str(body.get("case_name", "")).strip() or "Untitled Case"
            status = str(body.get("status", "Open")).strip()
            threat_level = str(body.get("threat_level", "Low Threat")).strip()
            data_retention_period = str(body.get("data_retention_period", "3 months")).strip()
            known_location = str(body.get("known_location", "")).strip()
            poi_image_url = str(body.get("poi_image_url", "")).strip()
            metadata_tags = body.get("metadata_tags", [])
            case_notes = body.get("case_notes", {})
            payload = create_case(
                case_name=case_name,
                status=status,
                threat_level=threat_level,
                data_retention_period=data_retention_period,
                known_location=known_location,
                poi_image_url=poi_image_url,
                case_notes=case_notes if isinstance(case_notes, dict) else {},
                metadata_tags=metadata_tags,
                db_path=str(DEFAULT_DB_PATH),
            )
            self._send_json(payload, status=201)
            return

        if parsed.path == "/api/config":
            body = self._read_json_body()
            if body is None:
                return
            payload = save_config(
                pdl_api_key=body.get("pdl_api_key"),
                osint_industries_api_key=body.get("osint_industries_api_key"),
                custom_keyword_list=body.get("custom_keyword_list"),
                default_data_retention_period=body.get("default_data_retention_period"),
                numverify_api_key=body.get("numverify_api_key"),
                openai_api_key=body.get("openai_api_key"),
                apify_api_token=body.get("apify_api_token"),
                clear_pdl_api_key=body.get("clear_pdl_api_key"),
                clear_osint_industries_api_key=body.get("clear_osint_industries_api_key"),
                clear_numverify_api_key=body.get("clear_numverify_api_key"),
                clear_openai_api_key=body.get("clear_openai_api_key"),
                clear_apify_api_token=body.get("clear_apify_api_token"),
            )
            _ = payload
            self._send_json(load_public_config())
            return

        if parsed.path == "/api/posts/manual":
            body = self._read_json_body()
            if body is None:
                return
            case_id = str(body.get("case_id", "")).strip()
            if not case_id:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "case_id is required"}},
                    status=400,
                )
                return
            text = str(body.get("text", "")).strip()
            author_name = str(body.get("author_name", "")).strip()
            source_url = str(body.get("source_url", "")).strip()
            source = str(body.get("source", "")).strip()
            file_name = str(body.get("file_name", "")).strip()
            file_mime_type = str(body.get("file_mime_type", "")).strip()
            file_content_base64 = str(body.get("file_content_base64", "")).strip()
            from_file = bool(file_name and file_content_base64)

            extracted_file_text = ""
            if from_file:
                extracted_file_text, extraction_error = _extract_uploaded_text(
                    file_name=file_name,
                    file_mime_type=file_mime_type,
                    file_content_base64=file_content_base64,
                )
                if extraction_error:
                    self._send_json(
                        {"error": {"code": "invalid_request", "message": extraction_error}},
                        status=400,
                    )
                    return

            content_parts = [part for part in [text, extracted_file_text] if str(part).strip()]
            content = "\n\n".join(content_parts).strip()
            if not content:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "text or file content is required"}},
                    status=400,
                )
                return

            username = author_name if author_name else "manual_entry"
            platform = source if source else "Manual"
            metadata = {
                "manual_insert": True,
                "manual_insert_from_file": from_file,
                "manual_insert_file_name": file_name if from_file else "",
                "manual_insert_file_type": file_mime_type if from_file else "",
                "manual_insert_author_name": author_name,
                "manual_insert_source": source,
            }
            post = {
                "post_id": f"manual-{uuid4().hex[:12]}",
                "platform": platform,
                "username": username,
                "content": content,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_url": source_url,
                "post_type": "post",
                "metadata": metadata,
            }
            inserted = save_posts([post], db_path=str(DEFAULT_DB_PATH), case_id=case_id)
            self._send_json(
                {
                    "status": "ok",
                    "inserted": inserted,
                    "from_file": from_file,
                    "content_length": len(content),
                },
                status=201,
            )
            return

        if parsed.path == "/api/posts/assessment":
            body = self._read_json_body()
            if body is None:
                return
            try:
                row_id = int(body.get("row_id"))
            except (TypeError, ValueError):
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "row_id must be an integer"}},
                    status=400,
                )
                return
            metadata = body.get("metadata")
            if not isinstance(metadata, dict):
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "metadata object is required"}},
                    status=400,
                )
                return
            case_id = str(body.get("case_id", "")).strip() or None
            llm = metadata.get("llm_assessment")
            if not isinstance(llm, dict):
                llm = {}

            def _normalize_llm_list(raw_value: object) -> list[str]:
                if not isinstance(raw_value, list):
                    return []
                output: list[str] = []
                seen: set[str] = set()
                for item in raw_value:
                    clean = str(item or "").strip()
                    if not clean:
                        continue
                    key = clean.lower()
                    if key in seen:
                        continue
                    seen.add(key)
                    output.append(clean)
                return output

            primary = _normalize_llm_list(
                llm.get("tagged_primary")
                if isinstance(llm.get("tagged_primary"), list)
                else llm.get("primary_warning_behaviours")
            )
            secondary = _normalize_llm_list(
                llm.get("tagged_secondary")
                if isinstance(llm.get("tagged_secondary"), list)
                else llm.get("secondary_risk_factors")
            )
            normalized_llm = {
                "tagged_primary": primary,
                "tagged_secondary": secondary,
                "primary_warning_behaviours": primary,
                "secondary_risk_factors": secondary,
                "underlying_theme": str(llm.get("underlying_theme") or "").strip(),
                "rationale": str(llm.get("rationale") or "").strip(),
            }
            if not primary and not secondary:
                normalized_llm["underlying_theme"] = ""
            metadata["llm_assessment"] = normalized_llm

            persisted = update_post_llm_assessments(
                updates=[{"row_id": row_id, "metadata": metadata}],
                db_path=str(DEFAULT_DB_PATH),
                case_id=case_id,
            )
            if persisted <= 0:
                self._send_json(
                    {"error": {"code": "not_found", "message": "post not found"}},
                    status=404,
                )
                return
            self._send_json(
                {
                    "status": "ok",
                    "persisted": persisted,
                    "row_id": row_id,
                }
            )
            return

        if parsed.path == "/api/llm/estimate":
            body = self._read_json_body()
            if body is None:
                return
            posts = body.get("posts")
            if not isinstance(posts, list):
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "posts list is required"}},
                    status=400,
                )
                return
            expected_output_tokens = body.get("expected_output_tokens_per_post", 220)
            try:
                estimate = estimate_warning_assessment_cost(
                    posts,
                    expected_output_tokens_per_post=int(expected_output_tokens),
                )
            except Exception as exc:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": str(exc)}},
                    status=400,
                )
                return
            self._send_json({"estimate": estimate})
            return

        if parsed.path == "/api/llm/sandbox":
            body = self._read_json_body()
            if body is None:
                return
            text = str(body.get("text", "")).strip()
            if not text:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "text is required"}},
                    status=400,
                )
                return
            username = str(body.get("username", "")).strip() or "sandbox_analyst"
            platform = str(body.get("platform", "")).strip() or "Sandbox"
            source_url = str(body.get("source_url", "")).strip()
            metadata = {
                "sandbox": True,
                "sandbox_submitted_at": datetime.now(timezone.utc).isoformat(),
            }
            post = {
                "row_id": 0,
                "post_id": f"sandbox-{uuid4().hex[:12]}",
                "platform": platform,
                "username": username,
                "content": text,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_url": source_url,
                "post_type": "post",
                "metadata": metadata,
            }
            try:
                assessed_post = analyze_post_sandbox(post)
            except Exception as exc:
                self._send_json(
                    {"error": {"code": "internal_error", "message": str(exc)}},
                    status=500,
                )
                return
            self._send_json(
                {
                    "status": "ok",
                    "post": assessed_post,
                    "analysis_status": (
                        assessed_post.get("metadata", {}).get("sandbox_analysis", {})
                        if isinstance(assessed_post.get("metadata"), dict)
                        else {}
                    ),
                }
            )
            return

        if parsed.path == "/api/llm/run":
            body = self._read_json_body()
            if body is None:
                return
            posts = body.get("posts")
            case_id = str(body.get("case_id", "")).strip()
            if not isinstance(posts, list):
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "posts list is required"}},
                    status=400,
                )
                return
            try:
                assessed_posts = apply_warning_assessments(posts)
            except Exception as exc:
                self._send_json(
                    {"error": {"code": "internal_error", "message": str(exc)}},
                    status=500,
                )
                return

            updates: list[dict[str, object]] = []
            assessed_count = 0
            for original, assessed in zip(posts, assessed_posts):
                if not isinstance(assessed, dict):
                    continue
                metadata = assessed.get("metadata")
                if not isinstance(metadata, dict):
                    continue
                llm = metadata.get("llm_assessment")
                if not isinstance(llm, dict) or not llm:
                    continue
                original_metadata = original.get("metadata") if isinstance(original, dict) else {}
                original_llm = original_metadata.get("llm_assessment") if isinstance(original_metadata, dict) else {}
                if isinstance(original_llm, dict) and original_llm:
                    continue
                assessed_count += 1
                updates.append({"row_id": assessed.get("row_id"), "metadata": metadata})

            persisted = update_post_llm_assessments(
                updates=updates,
                db_path=str(DEFAULT_DB_PATH),
                case_id=case_id or None,
            )
            self._send_json(
                {
                    "status": "ok",
                    "assessed": assessed_count,
                    "persisted": persisted,
                }
            )
            return

        if parsed.path == "/api/cases/demo":
            payload = create_demo_case(db_path=str(DEFAULT_DB_PATH))
            self._send_json(payload, status=201)
            return

        if parsed.path == "/api/cases/demo/vip-threat":
            payload = create_vip_threat_demo_case(db_path=str(DEFAULT_DB_PATH))
            self._send_json(payload, status=201)
            return

        if parsed.path.startswith("/api/cases/") and parsed.path.endswith("/demo/vip-threat/collect"):
            case_id = parsed.path.split("/api/cases/", 1)[1].split("/demo/vip-threat/collect", 1)[0].strip().strip("/")
            if not case_id:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "case_id is required"}},
                    status=400,
                )
                return
            try:
                payload = seed_vip_threat_demo_posts(case_id, db_path=str(DEFAULT_DB_PATH))
            except ValueError as exc:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": str(exc)}},
                    status=400,
                )
                return
            self._send_json(payload, status=201)
            return

        if parsed.path.startswith("/api/cases/"):
            case_id = parsed.path.split("/api/cases/", 1)[1].strip().strip("/")
            method = str(getattr(self, "command", "POST")).upper()
            if not case_id:
                self._send_json(
                    {"error": {"code": "invalid_request", "message": "case_id is required"}},
                    status=400,
                )
                return
            if method == "PATCH":
                body = self._read_json_body()
                if body is None:
                    return
                payload = update_case(
                    case_id,
                    case_name=body.get("case_name"),
                    status=body.get("status"),
                    threat_level=body.get("threat_level"),
                    data_retention_period=body.get("data_retention_period"),
                    known_location=body.get("known_location"),
                    poi_image_url=body.get("poi_image_url"),
                    case_notes=body.get("case_notes"),
                    metadata_tags=body.get("metadata_tags"),
                    db_path=str(DEFAULT_DB_PATH),
                )
                if payload is None:
                    self._send_json(
                        {"error": {"code": "not_found", "message": "case not found"}},
                        status=404,
                    )
                    return
                self._send_json(payload)
                return
            if method == "DELETE":
                deleted = delete_case(case_id, db_path=str(DEFAULT_DB_PATH), delete_posts=True)
                if not deleted:
                    self._send_json(
                        {"error": {"code": "not_found", "message": "case not found"}},
                        status=404,
                    )
                    return
                self._send_json({"status": "ok", "deleted_case_id": case_id, "deleted_posts": True})
                return

        if parsed.path == "/api/recon":
            body = self._read_json_body()
            if body is None:
                return
            selectors = normalize_recon_selectors(body.get("selectors", []))
            if not selectors:
                raw_username = str(body.get("username", "")).strip()
                raw_email = str(body.get("email", "")).strip()
                raw_selector = str(body.get("selector", "")).strip()
                raw_selector_type = str(body.get("selector_type", "")).strip().lower()
                if raw_username:
                    selectors = normalize_recon_selectors([{"type": "username", "value": raw_username}])
                elif raw_email:
                    selectors = normalize_recon_selectors([{"type": "email", "value": raw_email}])
                elif raw_selector:
                    selectors = normalize_recon_selectors([{"type": raw_selector_type or "username", "value": raw_selector}])

            if not selectors:
                self._send_json(
                    {
                        "error": {
                            "code": "invalid_request",
                            "message": "at least one selector is required",
                        }
                    },
                    status=400,
                )
                return
            try:
                payload = build_vip_threat_demo_recon(selectors) or run_recon(selectors)
            except (ValueError, RuntimeError) as exc:
                self._send_json(
                    {
                        "error": {
                            "code": "invalid_request",
                            "message": str(exc),
                        }
                    },
                    status=400,
                )
                return
            except Exception as exc:
                self._send_json(
                    {
                        "error": {
                            "code": "internal_error",
                            "message": str(exc),
                        }
                    },
                    status=500,
                )
                return

            self._send_json(payload)
            return

        if parsed.path == "/api/recon/stream":
            body = self._read_json_body()
            if body is None:
                return
            selectors = normalize_recon_selectors(body.get("selectors", []))
            if not selectors:
                raw_username = str(body.get("username", "")).strip()
                raw_email = str(body.get("email", "")).strip()
                raw_selector = str(body.get("selector", "")).strip()
                raw_selector_type = str(body.get("selector_type", "")).strip().lower()
                if raw_username:
                    selectors = normalize_recon_selectors([{"type": "username", "value": raw_username}])
                elif raw_email:
                    selectors = normalize_recon_selectors([{"type": "email", "value": raw_email}])
                elif raw_selector:
                    selectors = normalize_recon_selectors([{"type": raw_selector_type or "username", "value": raw_selector}])

            if not selectors:
                self._send_json(
                    {
                        "error": {
                            "code": "invalid_request",
                            "message": "at least one selector is required",
                        }
                    },
                    status=400,
                )
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            if not self._stream_json_line({"event": "start", "selectors_total": len(selectors)}):
                return

            streamed_scanner_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
            for index, selector in enumerate(selectors, start=1):
                selector_type = str(selector.get("type") or "").strip().lower()
                selector_value = str(selector.get("value") or "").strip()
                if not self._stream_json_line(
                    {
                        "event": "progress",
                        "stage": "selector_started",
                        "selector_index": index,
                        "selectors_total": len(selectors),
                        "selector_type": selector_type,
                        "selector_value": selector_value,
                    }
                ):
                    return
                try:
                    demo_payload = build_vip_threat_demo_recon([selector])
                    if demo_payload:
                        if not self._stream_json_line(
                            {
                                "event": "chunk",
                                "selector_index": index,
                                "selectors_total": len(selectors),
                                "selector_type": selector_type,
                                "selector_value": selector_value,
                                "payload": demo_payload,
                            }
                        ):
                            return
                        continue

                    def _emit_scanner_result(item: dict[str, Any]) -> None:
                        self._stream_json_line(
                            {
                                "event": "chunk",
                                "partial": True,
                                "selector_index": index,
                                "selectors_total": len(selectors),
                                "selector_type": selector_type,
                                "selector_value": selector_value,
                                "payload": {
                                    "selectors": [selector],
                                    "results": [],
                                    "scanner_results": [{"selector_type": selector_type, "selector": selector_value, **item}],
                                    "checked": 0,
                                    "present_count": 1,
                                    "collection_targets": [],
                                    "leads": [],
                                },
                            }
                        )

                    streamed_scanner_rows[(selector_type, selector_value)] = stream_user_scanner_selector(
                        selector_type=selector_type,
                        selector_value=selector_value,
                        on_result=_emit_scanner_result,
                    )
                except (ValueError, RuntimeError) as exc:
                    self._stream_json_line(
                        {
                            "event": "error",
                            "code": "invalid_request",
                            "message": str(exc),
                            "selector_index": index,
                            "selectors_total": len(selectors),
                            "selector_type": selector_type,
                            "selector_value": selector_value,
                        }
                    )
                    return
                except Exception as exc:
                    self._stream_json_line(
                        {
                            "event": "error",
                            "code": "internal_error",
                            "message": str(exc),
                            "selector_index": index,
                            "selectors_total": len(selectors),
                            "selector_type": selector_type,
                            "selector_value": selector_value,
                        }
                    )
                    return
            try:
                payload = build_vip_threat_demo_recon(selectors) or run_recon(selectors, scanner_rows_by_selector=streamed_scanner_rows)
            except (ValueError, RuntimeError) as exc:
                self._stream_json_line({"event": "error", "code": "invalid_request", "message": str(exc)})
                return
            except Exception as exc:
                self._stream_json_line({"event": "error", "code": "internal_error", "message": str(exc)})
                return
            if not self._stream_json_line({"event": "chunk", "final": True, "payload": payload}):
                return

            self._stream_json_line({"event": "done", "selectors_processed": len(selectors)})
            return

        if parsed.path == "/api/collect/start":
            body = self._read_json_body()
            if body is None:
                return

            start_date = str(body.get("start_date", "")).strip()
            end_date = str(body.get("end_date", "")).strip()
            case_id = str(body.get("case_id", "")).strip() or None
            try:
                db_path = _resolve_api_db_path(body.get("db_path", str(DEFAULT_DB_PATH)))
            except InvalidRequestError as exc:
                self._send_json({"error": {"code": "invalid_request", "message": str(exc)}}, status=400)
                return
            targets = parse_targets(body)
            apify_configured = bool(str(load_config().get("apify_api_token") or "").strip())
            missing_apify_for = _missing_apify_platforms(targets)
            if missing_apify_for and not apify_configured:
                human = ", ".join(missing_apify_for)
                self._send_json(
                    {
                        "error": {
                            "code": "apify_token_required",
                            "message": f"Apify API token is required for: {human}. Open Config and set Apify API Token before collecting.",
                            "platforms": missing_apify_for,
                        }
                    },
                    status=400,
                )
                return
            try:
                response = start_collection_job(
                    targets=targets,
                    start_date=start_date,
                    end_date=end_date,
                    db_path=db_path,
                    case_id=case_id,
                )
            except InvalidRequestError as exc:
                self._send_json(
                    {
                        "error": {
                            "code": "invalid_request",
                            "message": str(exc),
                        }
                    },
                    status=400,
                )
                return
            except Exception as exc:
                self._send_json(
                    {
                        "error": {
                            "code": "internal_error",
                            "message": str(exc),
                        }
                    },
                    status=500,
                )
                return

            self._send_json(response, status=202)
            return

        if parsed.path != "/api/collect":
            self.send_error(404)
            return

        body = self._read_json_body()
        if body is None:
            return

        start_date = str(body.get("start_date", "")).strip()
        end_date = str(body.get("end_date", "")).strip()
        case_id = str(body.get("case_id", "")).strip() or None
        try:
            db_path = _resolve_api_db_path(body.get("db_path", str(DEFAULT_DB_PATH)))
        except InvalidRequestError as exc:
            self._send_json({"error": {"code": "invalid_request", "message": str(exc)}}, status=400)
            return
        targets = parse_targets(body)

        try:
            response = collect_for_targets(
                targets=targets,
                start_date=start_date,
                end_date=end_date,
                db_path=db_path,
                case_id=case_id,
            )
        except InvalidRequestError as exc:
            self._send_json(
                {
                    "error": {
                        "code": "invalid_request",
                        "message": str(exc),
                    }
                },
                status=400,
            )
            return
        except UsernameNotFoundError as exc:
            self._send_json(
                {
                    "error": {
                        "code": "username_not_found",
                        "message": str(exc),
                        "platform": exc.platform,
                        "username": exc.username,
                    }
                },
                status=404,
            )
            return
        except Exception as exc:
            self._send_json(
                {
                    "error": {
                        "code": "internal_error",
                        "message": str(exc),
                    }
                },
                status=500,
            )
            return

        self._send_json(response)

    def do_PATCH(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/cases/"):
            self.command = "PATCH"
            return self.do_POST()
        self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/cases/"):
            self.command = "DELETE"
            return self.do_POST()
        self.send_error(404)

    def _read_json_body(self, default: dict | None = None):
        raw_length = str(self.headers.get("Content-Length", "")).strip()
        if raw_length:
            try:
                content_length = int(raw_length)
            except ValueError:
                self.send_error(400, "invalid content-length header")
                return None
            if content_length < 0:
                self.send_error(400, "invalid content-length header")
                return None
        else:
            content_length = 0

        if content_length == 0:
            return {} if default is None else default

        if content_length > _MAX_JSON_BODY_BYTES:
            self.send_error(413, "json body too large")
            return None

        try:
            raw_body = self.rfile.read(content_length)
        except OSError:
            self.send_error(400, "unable to read request body")
            return None
        if len(raw_body) != content_length:
            self.send_error(400, "incomplete request body")
            return None

        try:
            decoded_body = raw_body.decode("utf-8")
            parsed = json.loads(decoded_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "invalid json body")
            return None
        if isinstance(parsed, dict):
            return parsed
        if default is not None:
            return default
        self.send_error(400, "json body must be an object")
        return None

    def _send_json(self, payload: dict, *, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self._write_body(body)

    def end_headers(self):
        # Disable caching for local iterative UI development and API responses.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def run(host: str = "127.0.0.1", port: int = 8000):
    open_host = host
    if host in {"0.0.0.0", "::", ""}:
        open_host = "127.0.0.1"
    url = f"http://{open_host}:{port}"

    def _open_browser() -> None:
        # Give the server a brief head start before opening the page.
        time.sleep(0.25)
        try:
            webbrowser.open(url, new=2, autoraise=True)
        except Exception:
            pass

    server = ThreadingHTTPServer((host, port), PostExplorerHandler)
    threading.Thread(target=_open_browser, daemon=True).start()
    print(f"OSINT Post Explorer running at {url}")
    server.serve_forever()


if __name__ == "__main__":
    run()
