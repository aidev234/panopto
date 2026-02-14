"""Local web server for visualizing collected social posts."""

from __future__ import annotations

import json
import re
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlparse

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "osint_data.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"


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
    return token[1:-1].lower() if token.startswith('"') and token.endswith('"') else token.lower()


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

    haystack = " ".join([post.get("username", ""), post.get("platform", ""), post.get("content", "")]).lower()

    tokens = _tokenize_boolean_query(query)
    if not tokens:
        return True

    try:
        return _evaluate_rpn(_to_rpn(tokens), haystack)
    except Exception:
        return query.lower() in haystack


def _fetch_posts(db_path: Path) -> Iterable[dict[str, str]]:
    if not db_path.exists():
        return []

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT username, content, timestamp, collected_at FROM twitter_posts").fetchall()

    return [
        {
            "username": row["username"] or "unknown",
            "platform": "Twitter",
            "content": row["content"] or "",
            "timestamp": row["timestamp"] or row["collected_at"] or "",
        }
        for row in rows
    ]


def query_posts(query: str = "", sort_order: str = "newest", db_path: Path = DEFAULT_DB_PATH) -> dict[str, object]:
    posts = [post for post in _fetch_posts(db_path) if _matches_query(post, query)]
    posts.sort(key=lambda post: post["timestamp"] or "", reverse=sort_order != "oldest")
    return {"count": len(posts), "posts": posts}


class PostExplorerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/posts":
            params = parse_qs(parsed.query)
            query = params.get("query", [""])[0]
            sort = params.get("sort", ["newest"])[0].lower()
            db_path = Path(params.get("db_path", [str(DEFAULT_DB_PATH)])[0])
            payload = query_posts(query=query, sort_order=sort, db_path=db_path)

            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path in {"/", ""}:
            self.path = "/index.html"

        return super().do_GET()


def run(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadingHTTPServer((host, port), PostExplorerHandler)
    print(f"OSINT Post Explorer running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
