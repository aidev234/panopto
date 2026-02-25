"""Runtime configuration persistence for local PANOPTO settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent.parent / ".panopto_config.json"


def _normalize_pdl_api_key(raw: Any) -> str:
    return str(raw or "").strip()


def _default_config() -> dict[str, str]:
    return {"pdl_api_key": ""}


def load_config() -> dict[str, str]:
    defaults = _default_config()
    if not CONFIG_PATH.exists():
        return defaults
    try:
        payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return defaults
    if not isinstance(payload, dict):
        return defaults
    return {"pdl_api_key": _normalize_pdl_api_key(payload.get("pdl_api_key", ""))}


def save_config(*, pdl_api_key: str | None = None) -> dict[str, str]:
    current = load_config()
    if pdl_api_key is not None:
        current["pdl_api_key"] = _normalize_pdl_api_key(pdl_api_key)
    CONFIG_PATH.write_text(json.dumps(current, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return current

