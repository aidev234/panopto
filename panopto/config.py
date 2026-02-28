"""Runtime configuration persistence for local PANOPTO settings."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Any

CONFIG_PATH = Path(__file__).resolve().parent.parent / ".panopto_config.json"
SECRETS_PATH = Path(__file__).resolve().parent.parent / ".panopto_secrets.enc"
SECRET_PASSPHRASE_ENV = "PANOPTO_SECRET_PASSPHRASE"

_SECRET_ENV_MAP = {
    "pdl_api_key": "PANOPTO_PDL_API_KEY",
    "osint_industries_api_key": "PANOPTO_OSINT_INDUSTRIES_API_KEY",
    "numverify_api_key": "PANOPTO_NUMVERIFY_API_KEY",
    "openai_api_key": "PANOPTO_OPENAI_API_KEY",
}
_SECRET_KEYS = tuple(_SECRET_ENV_MAP.keys())
_RUNTIME_SECRETS: dict[str, str] = {}


def _normalize_pdl_api_key(raw: Any) -> str:
    return str(raw or "").strip()


def _normalize_osint_industries_api_key(raw: Any) -> str:
    return str(raw or "").strip()


def _normalize_osint_industries_use_premium(raw: Any) -> bool:
    if isinstance(raw, bool):
        return raw
    value = str(raw or "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _normalize_numverify_api_key(raw: Any) -> str:
    return str(raw or "").strip()


def _normalize_openai_api_key(raw: Any) -> str:
    return str(raw or "").strip()


def _normalize_secret_value(key: str, raw: Any) -> str:
    if key == "pdl_api_key":
        return _normalize_pdl_api_key(raw)
    if key == "osint_industries_api_key":
        return _normalize_osint_industries_api_key(raw)
    if key == "numverify_api_key":
        return _normalize_numverify_api_key(raw)
    if key == "openai_api_key":
        return _normalize_openai_api_key(raw)
    return str(raw or "").strip()


def _default_config() -> dict[str, Any]:
    return {
        "pdl_api_key": "",
        "osint_industries_api_key": "",
        "osint_industries_use_premium": False,
        "numverify_api_key": "",
        "openai_api_key": "",
    }


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_private_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _load_non_secret_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    payload = _read_json(CONFIG_PATH)
    return {
        "osint_industries_use_premium": _normalize_osint_industries_use_premium(payload.get("osint_industries_use_premium", False)),
    }


def _save_non_secret_config(*, osint_industries_use_premium: bool) -> None:
    payload = {
        "osint_industries_use_premium": bool(osint_industries_use_premium),
    }
    _write_private_text(CONFIG_PATH, json.dumps(payload, ensure_ascii=True, indent=2) + "\n")


def _secret_passphrase() -> str:
    return str(os.environ.get(SECRET_PASSPHRASE_ENV) or "").strip()


def _encrypt_payload_json(payload: dict[str, str], passphrase: str) -> str | None:
    try:
        proc = subprocess.run(
            [
                "openssl",
                "enc",
                "-aes-256-cbc",
                "-pbkdf2",
                "-salt",
                "-a",
                "-pass",
                "env:PANOPTO_SECRET_ENC_PASS",
            ],
            input=(json.dumps(payload, ensure_ascii=True) + "\n").encode("utf-8"),
            capture_output=True,
            check=True,
            env={**os.environ, "PANOPTO_SECRET_ENC_PASS": passphrase},
        )
    except (subprocess.SubprocessError, OSError):
        return None
    return proc.stdout.decode("utf-8").strip()


def _decrypt_payload_json(ciphertext: str, passphrase: str) -> dict[str, str]:
    if not ciphertext.strip():
        return {}
    try:
        proc = subprocess.run(
            [
                "openssl",
                "enc",
                "-d",
                "-aes-256-cbc",
                "-pbkdf2",
                "-salt",
                "-a",
                "-pass",
                "env:PANOPTO_SECRET_ENC_PASS",
            ],
            input=ciphertext.encode("utf-8"),
            capture_output=True,
            check=True,
            env={**os.environ, "PANOPTO_SECRET_ENC_PASS": passphrase},
        )
    except (subprocess.SubprocessError, OSError):
        return {}
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    output: dict[str, str] = {}
    for key in _SECRET_KEYS:
        output[key] = _normalize_secret_value(key, payload.get(key, ""))
    return output


def _load_legacy_secrets() -> dict[str, str]:
    """Read plaintext legacy keys from config for one-time migration."""
    if not CONFIG_PATH.exists():
        return {}
    payload = _read_json(CONFIG_PATH)
    output: dict[str, str] = {}
    for key in _SECRET_KEYS:
        clean = _normalize_secret_value(key, payload.get(key, ""))
        if clean:
            output[key] = clean
    return output


def _load_file_secrets() -> dict[str, str]:
    passphrase = _secret_passphrase()
    if passphrase and SECRETS_PATH.exists():
        try:
            ciphertext = SECRETS_PATH.read_text(encoding="utf-8")
        except OSError:
            ciphertext = ""
        decrypted = _decrypt_payload_json(ciphertext, passphrase)
        if decrypted:
            return decrypted
    return _load_legacy_secrets()


def _save_file_secrets(secrets: dict[str, str]) -> bool:
    passphrase = _secret_passphrase()
    if not passphrase:
        return False
    payload = {key: _normalize_secret_value(key, secrets.get(key, "")) for key in _SECRET_KEYS}
    encrypted = _encrypt_payload_json(payload, passphrase)
    if not encrypted:
        return False
    _write_private_text(SECRETS_PATH, encrypted + "\n")
    return True


def _merge_secret_values(file_secrets: dict[str, str]) -> dict[str, str]:
    merged = {key: _normalize_secret_value(key, file_secrets.get(key, "")) for key in _SECRET_KEYS}
    for key in _SECRET_KEYS:
        runtime = _normalize_secret_value(key, _RUNTIME_SECRETS.get(key, ""))
        if runtime:
            merged[key] = runtime
    for key, env_name in _SECRET_ENV_MAP.items():
        env_value = _normalize_secret_value(key, os.environ.get(env_name, ""))
        if env_value:
            merged[key] = env_value
    # Backward-compatible standard env for OpenAI clients.
    openai_global = _normalize_secret_value("openai_api_key", os.environ.get("OPENAI_API_KEY", ""))
    if openai_global:
        merged["openai_api_key"] = openai_global
    return merged


def _secret_storage_mode() -> str:
    has_env_secret = any(str(os.environ.get(env_name) or "").strip() for env_name in _SECRET_ENV_MAP.values())
    if has_env_secret:
        return "env"
    if _secret_passphrase() and SECRETS_PATH.exists():
        return "encrypted_file"
    if any(str(_RUNTIME_SECRETS.get(key) or "").strip() for key in _SECRET_KEYS):
        return "runtime_only"
    return "unconfigured"


def load_config() -> dict[str, Any]:
    defaults = _default_config()
    non_secret = _load_non_secret_config()
    file_secrets = _load_file_secrets()
    secrets = _merge_secret_values(file_secrets)
    output = {**defaults, **non_secret}
    for key in _SECRET_KEYS:
        output[key] = secrets.get(key, "")
    return output


def load_public_config() -> dict[str, Any]:
    current = load_config()
    return {
        "osint_industries_use_premium": bool(current.get("osint_industries_use_premium")),
        "pdl_api_key_configured": bool(str(current.get("pdl_api_key") or "").strip()),
        "osint_industries_api_key_configured": bool(str(current.get("osint_industries_api_key") or "").strip()),
        "numverify_api_key_configured": bool(str(current.get("numverify_api_key") or "").strip()),
        "openai_api_key_configured": bool(str(current.get("openai_api_key") or "").strip()),
        "secret_storage_mode": _secret_storage_mode(),
    }


def save_config(
    *,
    pdl_api_key: str | None = None,
    osint_industries_api_key: str | None = None,
    osint_industries_use_premium: bool | None = None,
    numverify_api_key: str | None = None,
    openai_api_key: str | None = None,
    clear_pdl_api_key: bool | None = None,
    clear_osint_industries_api_key: bool | None = None,
    clear_numverify_api_key: bool | None = None,
    clear_openai_api_key: bool | None = None,
) -> dict[str, Any]:
    non_secret = _load_non_secret_config()
    if osint_industries_use_premium is not None:
        non_secret["osint_industries_use_premium"] = _normalize_osint_industries_use_premium(osint_industries_use_premium)
    _save_non_secret_config(
        osint_industries_use_premium=_normalize_osint_industries_use_premium(
            non_secret.get("osint_industries_use_premium", False)
        )
    )

    current_secrets = _merge_secret_values(_load_file_secrets())
    updates = {
        "pdl_api_key": pdl_api_key,
        "osint_industries_api_key": osint_industries_api_key,
        "numverify_api_key": numverify_api_key,
        "openai_api_key": openai_api_key,
    }
    clears = {
        "pdl_api_key": bool(clear_pdl_api_key),
        "osint_industries_api_key": bool(clear_osint_industries_api_key),
        "numverify_api_key": bool(clear_numverify_api_key),
        "openai_api_key": bool(clear_openai_api_key),
    }
    for key in _SECRET_KEYS:
        if clears.get(key):
            current_secrets[key] = ""
            continue
        raw = updates.get(key)
        if raw is None:
            continue
        clean = _normalize_secret_value(key, raw)
        if clean:
            current_secrets[key] = clean

    _RUNTIME_SECRETS.update({key: current_secrets.get(key, "") for key in _SECRET_KEYS})
    _save_file_secrets(current_secrets)
    return load_config()
