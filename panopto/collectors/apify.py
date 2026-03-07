"""Shared Apify actor invocation helpers for collectors."""

from __future__ import annotations

import os
import time
from typing import Any
from urllib.parse import quote

import requests


APIFY_API_BASE = "https://api.apify.com/v2"
APIFY_TOKEN_ENV = "PANOPTO_APIFY_API_TOKEN"
APIFY_TOKEN_ENV_FALLBACK = "APIFY_API_TOKEN"


class ApifyConfigurationError(ValueError):
    """Raised when Apify runtime settings are missing or invalid."""


class ApifyRequestError(RuntimeError):
    """Raised when an Apify actor run fails or returns a bad response."""


class ApifyActorInputError(ApifyRequestError):
    """Raised when actor input is rejected by Apify."""


def _extract_items(payload: Any) -> list[dict[str, Any]] | None:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return None

    for key in ("items", "datasetItems", "results"):
        nested = payload.get(key)
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, dict)]

    nested_data = payload.get("data")
    if isinstance(nested_data, list):
        return [item for item in nested_data if isinstance(item, dict)]
    if isinstance(nested_data, dict):
        for key in ("items", "datasetItems", "results"):
            nested = nested_data.get(key)
            if isinstance(nested, list):
                return [item for item in nested if isinstance(item, dict)]

    return None


def _extract_run_info(payload: Any) -> tuple[str, str, str]:
    if not isinstance(payload, dict):
        return "", "", ""
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    if not isinstance(data, dict):
        return "", "", ""
    run_id = str(data.get("id") or "").strip()
    status = str(data.get("status") or "").strip().upper()
    dataset_id = str(data.get("defaultDatasetId") or "").strip()
    return run_id, dataset_id, status


def _apify_get_json(url: str, *, params: dict[str, str], timeout_seconds: int) -> tuple[int, str, Any]:
    try:
        response = requests.get(url, params=params, timeout=max(15, timeout_seconds))
    except requests.RequestException as exc:
        raise ApifyRequestError(f"apify request failed: {exc}") from exc

    body = str(response.text or "")
    if response.status_code in {401, 403}:
        raise ApifyRequestError("apify authentication failed")
    if response.status_code == 404:
        return 404, body, {}
    if response.status_code >= 500:
        raise ApifyRequestError(f"apify temporary failure ({response.status_code})")
    if response.status_code >= 400:
        raise ApifyRequestError(f"apify request failed ({response.status_code}): {body[:300]}")
    try:
        return response.status_code, body, response.json()
    except ValueError as exc:
        raise ApifyRequestError("apify response was not valid JSON") from exc


def _fetch_dataset_items(*, dataset_id: str, token: str, timeout_seconds: int) -> list[dict[str, Any]]:
    clean_dataset_id = str(dataset_id or "").strip()
    if not clean_dataset_id:
        raise ApifyRequestError("apify run missing default dataset id")
    url = f"{APIFY_API_BASE}/datasets/{quote(clean_dataset_id, safe='~:@$()!*,;=')}/items"
    _status, _body, payload = _apify_get_json(
        url,
        params={"token": token, "clean": "true", "format": "json"},
        timeout_seconds=timeout_seconds,
    )
    items = _extract_items(payload)
    if items is not None:
        return items
    raise ApifyRequestError("apify dataset response did not contain a list of items")


def _wait_for_run_dataset_id(
    *,
    run_id: str,
    token: str,
    timeout_seconds: int,
    initial_dataset_id: str = "",
    initial_status: str = "",
) -> tuple[str, str]:
    clean_run_id = str(run_id or "").strip()
    if not clean_run_id:
        raise ApifyRequestError("apify response did not include a run id")

    dataset_id = str(initial_dataset_id or "").strip()
    status = str(initial_status or "").strip().upper()
    deadline = time.monotonic() + max(15, timeout_seconds)
    terminal_ok = {"SUCCEEDED", "SUCCEEDED_WITH_WARNINGS"}
    terminal_error = {"FAILED", "ABORTED", "TIMED-OUT"}

    while True:
        if status in terminal_ok and dataset_id:
            return dataset_id, status
        if status in terminal_error:
            raise ApifyRequestError(f"apify run {clean_run_id} ended with status {status.lower()}")
        if time.monotonic() >= deadline:
            raise ApifyRequestError(f"apify run {clean_run_id} did not finish before timeout")

        url = f"{APIFY_API_BASE}/actor-runs/{quote(clean_run_id, safe='~:@$()!*,;=')}"
        status_code, _body, payload = _apify_get_json(
            url,
            params={"token": token},
            timeout_seconds=min(timeout_seconds, 20),
        )
        if status_code == 404:
            raise ApifyRequestError(f"apify run not found: {clean_run_id}")
        fetched_run_id, fetched_dataset_id, fetched_status = _extract_run_info(payload)
        if fetched_run_id and fetched_run_id != clean_run_id:
            raise ApifyRequestError("apify run status response did not match requested run id")
        if fetched_dataset_id:
            dataset_id = fetched_dataset_id
        if fetched_status:
            status = fetched_status
        time.sleep(1.0)


def load_apify_token() -> str:
    preferred = str(os.environ.get(APIFY_TOKEN_ENV) or "").strip()
    if preferred:
        return preferred
    fallback = str(os.environ.get(APIFY_TOKEN_ENV_FALLBACK) or "").strip()
    if fallback:
        return fallback
    try:
        from panopto.config import load_config

        configured = str(load_config().get("apify_api_token") or "").strip()
        if configured:
            return configured
    except Exception:
        return ""
    return ""


def run_actor_sync_get_items(
    *,
    actor_id: str,
    actor_input: dict[str, Any],
    timeout_seconds: int = 180,
) -> list[dict[str, Any]]:
    token = load_apify_token()
    if not token:
        raise ApifyConfigurationError(f"missing {APIFY_TOKEN_ENV} (or {APIFY_TOKEN_ENV_FALLBACK})")

    clean_actor_id = str(actor_id or "").strip()
    if not clean_actor_id:
        raise ApifyConfigurationError("missing Apify actor id")

    url = f"{APIFY_API_BASE}/acts/{quote(clean_actor_id, safe='~:@$()!*,;=')}/run-sync-get-dataset-items"
    params = {
        "token": token,
        "clean": "true",
        "format": "json",
    }

    try:
        response = requests.post(url, params=params, json=actor_input, timeout=max(30, timeout_seconds))
    except requests.RequestException as exc:
        raise ApifyRequestError(f"apify request failed: {exc}") from exc

    body = str(response.text or "")
    if response.status_code in {400, 422}:
        raise ApifyActorInputError(body[:400] or f"apify input rejected ({response.status_code})")
    if response.status_code in {401, 403}:
        raise ApifyRequestError("apify authentication failed")
    if response.status_code == 404:
        raise ApifyRequestError(f"apify actor not found: {clean_actor_id}")
    if response.status_code >= 500:
        raise ApifyRequestError(f"apify temporary failure ({response.status_code})")
    if response.status_code >= 400:
        raise ApifyRequestError(f"apify request failed ({response.status_code}): {body[:300]}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise ApifyRequestError("apify response was not valid JSON") from exc

    items = _extract_items(payload)
    if items is not None:
        return items

    run_id, dataset_id, status = _extract_run_info(payload)
    if run_id:
        ready_dataset_id, _final_status = _wait_for_run_dataset_id(
            run_id=run_id,
            token=token,
            timeout_seconds=timeout_seconds,
            initial_dataset_id=dataset_id,
            initial_status=status,
        )
        return _fetch_dataset_items(
            dataset_id=ready_dataset_id,
            token=token,
            timeout_seconds=timeout_seconds,
        )

    raise ApifyRequestError("apify response did not contain dataset items or run metadata")
