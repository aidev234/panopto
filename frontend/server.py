"""Local web server for visualizing collected social posts."""

from __future__ import annotations

import json
import sys
import threading
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from panopto.collection_service import InvalidRequestError, collect_for_targets, parse_targets
from panopto.errors import UsernameNotFoundError
from panopto.post_query import normalize_tag, query_posts
from panopto.analysis.theme_modeling import tag_posts_with_bertopic
from panopto.collection_jobs import get_collection_job_status, start_collection_job
from panopto.recon import run_username_recon
from panopto.storage.posts import clear_posts

DEFAULT_DB_PATH = ROOT_DIR / "osint_data.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"


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
            include_tags_raw = params.get("include_tags", [""])[0]
            exclude_tags_raw = params.get("exclude_tags", [""])[0]
            include_tags = {normalize_tag(tag) for tag in include_tags_raw.split(",") if tag.strip()}
            exclude_tags = {normalize_tag(tag) for tag in exclude_tags_raw.split(",") if tag.strip()}
            db_path = Path(params.get("db_path", [str(DEFAULT_DB_PATH)])[0])

            payload = query_posts(
                query=query,
                sort_order=sort,
                db_path=db_path,
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
            clear_posts(str(DEFAULT_DB_PATH))
            response = {"status": "ok", "cleared": True, "shutdown": should_shutdown}
            self._send_json(response)
            if should_shutdown:
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            return

        if parsed.path == "/api/themes/tag":
            result = tag_posts_with_bertopic(db_path=str(DEFAULT_DB_PATH))
            self._send_json(result)
            return

        if parsed.path == "/api/recon":
            body = self._read_json_body()
            if body is None:
                return
            raw_username = str(body.get("username", "")).strip()
            if not raw_username:
                self._send_json(
                    {
                        "error": {
                            "code": "invalid_request",
                            "message": "username is required",
                        }
                    },
                    status=400,
                )
                return
            try:
                payload = run_username_recon(raw_username)
            except ValueError as exc:
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
            db_path = Path(body.get("db_path", str(DEFAULT_DB_PATH)))
            targets = parse_targets(body)
            try:
                response = start_collection_job(
                    targets=targets,
                    start_date=start_date,
                    end_date=end_date,
                    db_path=db_path,
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
        db_path = Path(body.get("db_path", str(DEFAULT_DB_PATH)))
        targets = parse_targets(body)

        try:
            response = collect_for_targets(
                targets=targets,
                start_date=start_date,
                end_date=end_date,
                db_path=db_path,
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
