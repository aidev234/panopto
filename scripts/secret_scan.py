#!/usr/bin/env python3
"""Lightweight secret scanner for PANOPTO source files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Pattern:
    name: str
    regex: re.Pattern[str]


PATTERNS = [
    Pattern("PDL key", re.compile(r"\bpdl_[A-Za-z0-9]{16,}\b")),
    Pattern("OSINT Industries key", re.compile(r"\boi_[A-Za-z0-9]{16,}\b")),
    Pattern("OpenAI key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b")),
    Pattern("API key assignment", re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?key|secret)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]")),
    Pattern("Bearer token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9_\-]{24,}")),
]

EXCLUDE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".db", ".sqlite", ".lock"}
EXCLUDE_PATH_PARTS = {".venv", "__pycache__", ".git", "node_modules"}


def _run_git(args: list[str]) -> list[str]:
    try:
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True, text=True)
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def _candidate_files(mode: str) -> list[Path]:
    if mode == "staged":
        files = _run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"])
    else:
        files = _run_git(["ls-files"])
    candidates: list[Path] = []
    for item in files:
        rel = Path(item)
        if any(part in EXCLUDE_PATH_PARTS for part in rel.parts):
            continue
        if rel.suffix.lower() in EXCLUDE_SUFFIXES:
            continue
        path = ROOT / rel
        if path.is_file():
            candidates.append(path)
    return candidates


def _scan_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    findings: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in PATTERNS:
            if pattern.regex.search(line):
                findings.append(f"{path.relative_to(ROOT)}:{lineno}: {pattern.name}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan repository files for likely secrets.")
    parser.add_argument("--staged", action="store_true", help="Scan staged files only.")
    args = parser.parse_args()
    mode = "staged" if args.staged else "all"
    files = _candidate_files(mode)
    findings: list[str] = []
    for path in files:
        findings.extend(_scan_file(path))
    if findings:
        print("Potential secrets detected:")
        for item in findings:
            print(f"  - {item}")
        print("\nBlock commit. Remove or rotate exposed secrets.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
