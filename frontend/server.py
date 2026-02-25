"""Local web server for visualizing collected social posts."""

from __future__ import annotations

import json
import base64
import html
import mimetypes
import re
import sys
import threading
import socket
import textwrap
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from panopto.collection_service import InvalidRequestError, collect_for_targets, parse_targets
from panopto.errors import UsernameNotFoundError
from panopto.post_query import normalize_tag, query_posts
from panopto.collection_jobs import get_collection_job_status, start_collection_job
from panopto.config import load_config, save_config
from panopto.recon import normalize_recon_selectors, run_recon
from panopto.storage.posts import (
    clear_posts,
    create_case,
    create_demo_case,
    delete_case,
    list_cases,
    update_case,
)

DEFAULT_DB_PATH = ROOT_DIR / "osint_data.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"


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
        local = STATIC_DIR / clean_path.lstrip("/")
        if not local.exists() or not local.is_file():
            return ""
        raw = local.read_bytes()
        mime, _ = mimetypes.guess_type(str(local))
        mime_type = mime or "application/octet-stream"
        encoded = base64.b64encode(raw).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"
    if value.lower().startswith("http://") or value.lower().startswith("https://"):
        return value
    return ""


def _build_case_notes_pdf_stylized(case_row: dict, posts: list[dict]) -> bytes:
    from playwright.sync_api import sync_playwright  # type: ignore

    notes = case_row.get("case_notes") if isinstance(case_row.get("case_notes"), dict) else {}
    name = str(notes.get("name") or case_row.get("case_name") or "Untitled").strip() or "Untitled"
    location = str(notes.get("location") or case_row.get("known_location") or "").strip() or "Unknown"
    age = str(notes.get("age") or "").strip() or "Unknown"
    akas = str(notes.get("akas") or "").strip() or "None"
    context = str(notes.get("context") or "").strip() or "No context provided."
    threat = str(notes.get("threat_risk_assessment") or "").strip() or "No threat assessment provided."
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
            self._send_json(load_config())
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
            db_path = Path(params.get("db_path", [str(DEFAULT_DB_PATH)])[0])

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

        if parsed.path == "/api/session/end":
            body = self._read_json_body(default={})
            should_shutdown = bool(body.get("shutdown", True))
            clear_posts(str(DEFAULT_DB_PATH), clear_cases=True)
            response = {"status": "ok", "cleared": True, "shutdown": should_shutdown}
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
            payload = save_config(pdl_api_key=body.get("pdl_api_key"))
            self._send_json(payload)
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
            db_path = Path(body.get("db_path", str(DEFAULT_DB_PATH)))
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
        db_path = Path(body.get("db_path", str(DEFAULT_DB_PATH)))
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


def run(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadingHTTPServer((host, port), PostExplorerHandler)
    print(f"OSINT Post Explorer running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
