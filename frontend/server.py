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
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from panopto.collection_service import InvalidRequestError, collect_for_targets, parse_targets
from panopto.analysis.llm_warning_assessor import apply_warning_assessments, estimate_warning_assessment_cost
from panopto.errors import UsernameNotFoundError
from panopto.post_query import normalize_tag, query_posts
from panopto.collection_jobs import get_collection_job_status, start_collection_job
from panopto.config import load_public_config, save_config
from panopto.recon import normalize_recon_selectors, run_recon
from panopto.face_analysis import FaceRecognitionEngine
from panopto.storage.posts import (
    clear_posts,
    create_case,
    create_demo_case,
    delete_case,
    list_cases,
    save_posts,
    update_case,
    update_post_llm_assessments,
)

DEFAULT_DB_PATH = ROOT_DIR / "osint_data.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"
_ALLOWED_DB_ROOTS = [ROOT_DIR.resolve(), Path("/tmp").resolve()]
_FACE_RECOGNITION_ENGINE = FaceRecognitionEngine()


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
    subject_image = _image_source_to_data_uri(str(notes.get("subject_image_url") or case_row.get("poi_image_url") or "").strip())
    profiles_raw = notes.get("known_profiles") if isinstance(notes.get("known_profiles"), list) else []
    profiles = profiles_raw if profiles_raw else _discover_profiles_from_posts(posts)

    rows: list[str] = []
    for item in profiles:
        row = item if isinstance(item, dict) else {}
        profile_name = str(row.get("name") or row.get("site") or "Unknown").strip() or "Unknown"
        profile_url = str(row.get("url") or "").strip()
        profile_site = str(row.get("site") or "").strip() or _guess_site_from_url(profile_url)
        profile_shot = _image_source_to_data_uri(str(row.get("screenshot_url") or "").strip())
        rows.append(
            f"""
            <tr>
              <td>{_html_escape(profile_name)}</td>
              <td>{_html_escape(profile_site)}</td>
              <td class="url">{_html_escape(profile_url or 'N/A')}</td>
              <td>{f'<img src="{profile_shot}" alt="screenshot" />' if profile_shot else '<span class="na">N/A</span>'}</td>
            </tr>
            """
        )

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          @page {{ size: A4; margin: 22mm 16mm 18mm 16mm; }}
          body {{ font-family: "Helvetica Neue", Arial, sans-serif; color: #111827; margin: 0; }}
          .report {{ border: 1.5px solid #111827; padding: 14px; }}
          .header {{ border-bottom: 2px solid #111827; padding-bottom: 10px; margin-bottom: 12px; display: grid; grid-template-columns: 1fr auto; gap: 10px; }}
          .header h1 {{ margin: 0; font-size: 22px; letter-spacing: .08em; }}
          .header .sub {{ margin-top: 5px; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: #374151; }}
          .classification {{ font-size: 10px; text-transform: uppercase; letter-spacing: .07em; color: #374151; margin-top: 8px; }}
          .subject-image {{ width: 120px; height: 120px; border: 1px solid #111827; object-fit: cover; background: #f3f4f6; }}
          .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin: 10px 0 14px; }}
          .cell {{ border: 1px solid #9ca3af; padding: 6px 8px; min-height: 40px; }}
          .label {{ font-size: 10px; text-transform: uppercase; letter-spacing: .06em; color: #4b5563; margin-bottom: 4px; }}
          .value {{ font-size: 13px; font-weight: 600; }}
          h2 {{ margin: 14px 0 6px; font-size: 13px; text-transform: uppercase; letter-spacing: .08em; border-bottom: 1px solid #9ca3af; padding-bottom: 4px; }}
          p {{ margin: 0; font-size: 11.5px; line-height: 1.48; white-space: pre-wrap; }}
          table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
          th, td {{ border: 1px solid #9ca3af; padding: 6px 7px; font-size: 10.5px; vertical-align: top; text-align: left; }}
          th {{ background: #e5e7eb; text-transform: uppercase; letter-spacing: .05em; font-size: 9.5px; }}
          td.url {{ word-break: break-all; }}
          td img {{ width: 180px; max-height: 110px; object-fit: cover; display: block; border: 1px solid #d1d5db; }}
          .na {{ color: #6b7280; }}
          .footer {{ margin-top: 10px; font-size: 9px; color: #6b7280; text-align: right; }}
        </style>
      </head>
      <body>
        <section class="report">
          <header class="header">
            <div>
              <h1>PERSON OF INTEREST REPORT</h1>
              <div class="sub">Case Intelligence Summary</div>
              <div class="classification">Official Use Only</div>
            </div>
            {f'<img class="subject-image" src="{subject_image}" alt="Subject image" />' if subject_image else '<div class="subject-image"></div>'}
          </header>
          <section class="grid">
            <div class="cell"><div class="label">Name</div><div class="value">{_html_escape(name)}</div></div>
            <div class="cell"><div class="label">Location</div><div class="value">{_html_escape(location)}</div></div>
            <div class="cell"><div class="label">Age</div><div class="value">{_html_escape(age)}</div></div>
            <div class="cell" style="grid-column: 1 / -1;"><div class="label">A.K.A.s</div><div class="value">{_html_escape(akas)}</div></div>
          </section>
          <section>
            <h2>Context</h2>
            <p>{_html_escape(context)}</p>
          </section>
          <section>
            <h2>Threat / Risk Assessment</h2>
            <p>{_html_escape(threat)}</p>
            <p>{_html_escape('Underlying Themes: ' + (', '.join(underlying_themes) if underlying_themes else 'None'))}</p>
          </section>
          <section>
            <h2>Personal Details</h2>
            <p>{_html_escape(personal)}</p>
          </section>
          <section>
            <h2>Known Accounts</h2>
            <table>
              <thead>
                <tr>
                  <th style="width: 18%;">Name</th>
                  <th style="width: 15%;">Site</th>
                  <th style="width: 37%;">URL</th>
                  <th style="width: 30%;">Screenshot</th>
                </tr>
              </thead>
              <tbody>
                {''.join(rows) if rows else '<tr><td colspan="4" class="na">No known accounts.</td></tr>'}
              </tbody>
            </table>
          </section>
          <div class="footer">Generated by PANOPTO</div>
        </section>
      </body>
    </html>
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1240, "height": 1754})
        page = context.new_page()
        try:
            page.set_content(html, wait_until="networkidle")
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
    profiles = notes.get("known_profiles") if isinstance(notes.get("known_profiles"), list) else []
    if not profiles:
        profiles = _discover_profiles_from_posts(posts)

    page_width = 612
    page_height = 792
    margin_left = 54
    margin_top = 748
    margin_bottom = 54

    pages: list[list[str]] = [[]]
    cursor_y = margin_top

    def ensure_room(required_height: int) -> None:
        nonlocal cursor_y
        if cursor_y - required_height >= margin_bottom:
            return
        pages.append([])
        cursor_y = margin_top

    def add_rule() -> None:
        pages[-1].append(f"0.8 w {margin_left} {cursor_y} m {page_width - margin_left} {cursor_y} l S")

    def add_line(text: str, *, bold: bool = False, size: int = 11, gap: int | None = None) -> None:
        nonlocal cursor_y
        line_gap = gap if gap is not None else int(size * 1.45)
        ensure_room(line_gap)
        font = "F2" if bold else "F1"
        safe = _pdf_escape(text)
        pages[-1].append(f"BT /{font} {size} Tf 1 0 0 1 {margin_left} {cursor_y} Tm ({safe}) Tj ET")
        cursor_y -= line_gap

    def add_wrapped(text: str, *, bold: bool = False, size: int = 11, width: int = 92) -> None:
        for line in _wrap_pdf_text(text, width):
            add_line(line, bold=bold, size=size)

    add_line("PANOPTO CASE NOTES REPORT", bold=True, size=10, gap=12)
    add_line(name, bold=True, size=24, gap=34)
    add_rule()
    cursor_y -= 16
    add_line(f"Location: {location or 'Unknown'}", bold=False, size=11, gap=16)
    add_line(f"Age: {age or 'Unknown'}", bold=False, size=11, gap=16)
    add_line(f"A.K.A.s: {akas or 'None'}", bold=False, size=11, gap=20)
    add_line("Context", bold=True, size=13, gap=20)
    add_wrapped(context or "None", width=95)
    cursor_y -= 4
    add_line("Threat / Risk Assessment", bold=True, size=13, gap=20)
    add_wrapped(threat or "None", width=95)
    cursor_y -= 3
    add_line("Underlying Themes", bold=True, size=12, gap=16)
    add_wrapped(", ".join(underlying_themes) if underlying_themes else "None", width=95)
    cursor_y -= 4
    add_line("Personal Details", bold=True, size=13, gap=20)
    add_wrapped(personal or "None", width=95)
    cursor_y -= 4
    add_line("Known Profiles", bold=True, size=13, gap=20)
    if not profiles:
        add_line("None", size=11)
    else:
        for item in profiles:
            site = str(item.get("site") or "Profile").strip() or "Profile"
            url = str(item.get("url") or "").strip()
            screenshot_url = str(item.get("screenshot_url") or "").strip()
            add_wrapped(f"- {site}", bold=True, size=11, width=95)
            add_wrapped(f"  URL: {url or 'N/A'}", size=10, width=98)
            if screenshot_url:
                add_wrapped(f"  Screenshot: {screenshot_url}", size=10, width=98)
            cursor_y -= 3

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
    for page_ops in pages:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            if not self._enforce_loopback_only(reason="API access"):
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

        if parsed.path == "/api/session/end":
            body = self._read_json_body(default={})
            should_shutdown = bool(body.get("shutdown", True))
            should_clear_data = bool(body.get("clear_data", True))
            if should_clear_data:
                clear_posts(str(DEFAULT_DB_PATH), clear_cases=True)
            response = {"status": "ok", "cleared": should_clear_data, "shutdown": should_shutdown}
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
            known_location = str(body.get("known_location", "")).strip()
            poi_image_url = str(body.get("poi_image_url", "")).strip()
            metadata_tags = body.get("metadata_tags", [])
            case_notes = body.get("case_notes", {})
            payload = create_case(
                case_name=case_name,
                status=status,
                threat_level=threat_level,
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
                osint_industries_use_premium=body.get("osint_industries_use_premium"),
                custom_keyword_list=body.get("custom_keyword_list"),
                numverify_api_key=body.get("numverify_api_key"),
                openai_api_key=body.get("openai_api_key"),
                clear_pdl_api_key=body.get("clear_pdl_api_key"),
                clear_osint_industries_api_key=body.get("clear_osint_industries_api_key"),
                clear_numverify_api_key=body.get("clear_numverify_api_key"),
                clear_openai_api_key=body.get("clear_openai_api_key"),
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
                payload = run_recon(selectors)
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
        raw_length = str(self.headers.get("Content-Length", "0")).strip()
        content_length = int(raw_length) if raw_length.isdigit() else 0
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            parsed = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            if default is not None:
                return default
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
