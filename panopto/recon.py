"""Username reconnaissance helpers inspired by user-scanner style checks."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha1
from html import unescape as html_unescape
import json
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.parse import quote, unquote, urlparse

import requests

from panopto.collectors.bluesky import normalize_bluesky_username
from panopto.collectors.youtube import normalize_youtube_username
from panopto.config import load_config

_DEFAULT_TIMEOUT = 12
_SCREENSHOT_NAV_TIMEOUT = 24
_MAX_RECON_SCREENSHOTS = 24
_RECON_SHOTS_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static" / "recon_shots"
_PDL_ENRICH_URL = "https://api.peopledatalabs.com/v5/person/enrich"
_OSINT_INDUSTRIES_BASE_URL = "https://api.osint.industries"
_BREACHVIP_SEARCH_URLS = (
    "https://breach.vip/search",
    "https://api.breach.vip/search",
    "https://breach.vip/api/search",
)
_NUMVERIFY_BASE_URL = "http://apilayer.net/api/validate"
_NUMVERIFY_HTTPS_BASE_URL = "https://apilayer.net/api/validate"
_NUMVERIFY_APILAYER_URL = "https://api.apilayer.com/number_verification/validate"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def _pdl_api_key() -> str:
    config = load_config()
    return str(config.get("pdl_api_key") or "").strip()


def _osint_industries_api_key() -> str:
    config = load_config()
    return str(config.get("osint_industries_api_key") or "").strip()


def _numverify_api_key() -> str:
    config = load_config()
    return str(config.get("numverify_api_key") or "").strip()


def _fetch_pdl_profile(*, api_key: str, email: str = "", profile_url: str = "", timeout: int = 16) -> dict[str, Any] | None:
    params: dict[str, str] = {}
    if email:
        params["email"] = str(email).strip().lower()
    if profile_url:
        params["profile"] = str(profile_url).strip()
    if not params:
        return None
    try:
        response = requests.get(
            _PDL_ENRICH_URL,
            params=params,
            headers={
                "X-Api-Key": api_key,
                "Accept": "application/json",
                "User-Agent": "panopto-pdl-enrichment/1.0",
            },
            timeout=timeout,
        )
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    try:
        payload = response.json()
    except ValueError:
        return None
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not isinstance(data, dict):
        return None
    return data


def _safe_slug(value: str) -> str:
    raw = str(value or "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return slug or "site"


def _capture_profile_screenshot(*, site: str, profile_url: str, timeout: int = _SCREENSHOT_NAV_TIMEOUT) -> str:
    url = str(profile_url or "").strip()
    if not url:
        return ""
    if not re.match(r"^https?://", url, flags=re.IGNORECASE):
        return ""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        return ""

    _RECON_SHOTS_DIR.mkdir(parents=True, exist_ok=True)
    digest = sha1(f"{site}|{url}".encode("utf-8")).hexdigest()[:16]
    filename = f"{_safe_slug(site)}-{digest}.png"
    output_path = _RECON_SHOTS_DIR / filename

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 880},
                user_agent=_HEADERS["User-Agent"],
            )
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=timeout * 1000)
                page.wait_for_timeout(2200)
                page.screenshot(path=str(output_path), full_page=False)
            finally:
                context.close()
                browser.close()
    except Exception:
        return ""
    if not output_path.exists():
        return ""
    return f"/recon_shots/{filename}?v={int(time.time())}"


def _screenshot_profile_url(site: str, profile_url: str) -> str:
    site_name = str(site or "").strip().lower()
    raw_url = str(profile_url or "").strip()
    if site_name != "twitter":
        return raw_url
    if not raw_url:
        return raw_url
    match = re.search(r"(?:x|twitter)\.com/([^/?#]+)", raw_url, flags=re.IGNORECASE)
    if not match:
        return raw_url
    handle = str(match.group(1) or "").strip().lstrip("@")
    if not handle:
        return raw_url
    return f"https://x.com/{quote(handle, safe='')}"


def _clean_username(raw: Any) -> str:
    value = str(raw or "").strip()
    return value[1:] if value.startswith("@") else value


def _clean_reddit_username(raw: str) -> str:
    value = raw.strip()
    value = re.sub(r"^u/", "", value, flags=re.IGNORECASE)
    return value.strip("/")


def _check_html_profile(
    *,
    site: str,
    profile_url: str,
    not_found_tokens: list[str],
    timeout: int = _DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    try:
        response = requests.get(
            profile_url,
            headers=_HEADERS,
            timeout=timeout,
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        return {"site": site, "status": "unknown", "profile_url": profile_url, "reason": str(exc)}

    if response.status_code in {404, 410}:
        return {"site": site, "status": "absent", "profile_url": profile_url, "reason": f"http_{response.status_code}"}
    if response.status_code >= 500:
        return {"site": site, "status": "unknown", "profile_url": profile_url, "reason": f"http_{response.status_code}"}
    if response.status_code >= 400:
        return {"site": site, "status": "absent", "profile_url": profile_url, "reason": f"http_{response.status_code}"}

    body = response.text.lower()
    for token in not_found_tokens:
        if token.lower() in body:
            return {"site": site, "status": "absent", "profile_url": profile_url, "reason": "not_found_marker"}

    return {"site": site, "status": "present", "profile_url": profile_url, "reason": ""}


def _check_reddit(username: str) -> dict[str, Any]:
    normalized = _clean_reddit_username(username)
    profile_url = f"https://www.reddit.com/user/{quote(normalized, safe='')}"
    api_url = f"{profile_url}/about.json"
    try:
        response = requests.get(
            api_url,
            headers={"User-Agent": "panopto-recon/1.0", "Accept": "application/json"},
            timeout=_DEFAULT_TIMEOUT,
        )
    except requests.RequestException as exc:
        return {"site": "reddit", "status": "unknown", "profile_url": profile_url, "reason": str(exc)}

    if response.status_code == 200:
        return {"site": "reddit", "status": "present", "profile_url": profile_url, "reason": ""}
    if response.status_code == 404:
        return {"site": "reddit", "status": "absent", "profile_url": profile_url, "reason": "http_404"}
    if response.status_code >= 500:
        return {"site": "reddit", "status": "unknown", "profile_url": profile_url, "reason": f"http_{response.status_code}"}
    return {"site": "reddit", "status": "absent", "profile_url": profile_url, "reason": f"http_{response.status_code}"}


def _check_bluesky(username: str) -> dict[str, Any]:
    normalized = normalize_bluesky_username(username)
    actor = normalized if normalized.startswith("did:") or "." in normalized else f"{normalized}.bsky.social"
    profile_url = f"https://bsky.app/profile/{actor}"
    try:
        response = requests.get(
            "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile",
            params={"actor": actor},
            headers={"User-Agent": "panopto-recon/1.0", "Accept": "application/json"},
            timeout=_DEFAULT_TIMEOUT,
        )
    except requests.RequestException as exc:
        return {"site": "bluesky", "status": "unknown", "profile_url": profile_url, "reason": str(exc)}

    if response.status_code == 200:
        return {"site": "bluesky", "status": "present", "profile_url": profile_url, "reason": ""}
    if response.status_code in {400, 404}:
        return {"site": "bluesky", "status": "absent", "profile_url": profile_url, "reason": f"http_{response.status_code}"}
    return {"site": "bluesky", "status": "unknown", "profile_url": profile_url, "reason": f"http_{response.status_code}"}


def _check_twitter(username: str) -> dict[str, Any]:
    raw = _clean_username(username).strip()
    if not raw:
        return {"site": "twitter", "status": "absent", "profile_url": "", "reason": "empty_username"}

    candidates = [raw]
    lowered = raw.lower()
    if lowered != raw:
        candidates.append(lowered)

    results = [
        _check_html_profile(
            site="twitter",
            profile_url=f"https://x.com/{quote(candidate, safe='')}",
            not_found_tokens=[
                "this account doesn't exist",
                "this account doesn’t exist",
                "account doesn’t exist",
                "account doesn't exist",
                "user not found",
            ],
        )
        for candidate in candidates
    ]
    for result in results:
        if result.get("status") == "present":
            return result
    for result in results:
        if result.get("status") == "unknown":
            return result
    return results[0]


def _check_tiktok(username: str) -> dict[str, Any]:
    normalized = _clean_username(username)
    return _check_html_profile(
        site="tiktok",
        profile_url=f"https://www.tikvib.com/profile/{quote(normalized, safe='')}",
        not_found_tokens=["user not found", "profile not found", "this account does not exist"],
    )


def _check_instagram(username: str) -> dict[str, Any]:
    normalized = _clean_username(username)
    byviewer_url = f"https://www.byviewer.com/detail?username={quote(normalized, safe='')}"
    byviewer_result = _check_html_profile(
        site="instagram",
        profile_url=byviewer_url,
        not_found_tokens=["user not found", "profile not found", "no user found", "account does not exist"],
    )
    if byviewer_result.get("status") == "present":
        try:
            body = requests.get(byviewer_url, headers=_HEADERS, timeout=_DEFAULT_TIMEOUT).text.lower()
        except requests.RequestException:
            body = ""
        if not ("just a moment" in body and "/cdn-cgi/challenge-platform/" in body):
            return byviewer_result
    elif byviewer_result.get("status") == "absent":
        reason = str(byviewer_result.get("reason") or "").lower()
        # Hard absent signals from byviewer can be trusted. Bot/challenge status (403/429) should fallback.
        if reason in {"http_404", "http_410", "not_found_marker"}:
            return byviewer_result

    # Fallback check against Instagram profile page when byviewer is blocked/uncertain.
    instagram_url = f"https://www.instagram.com/{quote(normalized, safe='')}/"
    instagram_result = _check_html_profile(
        site="instagram",
        profile_url=instagram_url,
        not_found_tokens=["sorry, this page isn't available", "page isn't available", "user not found"],
    )
    if instagram_result.get("status") == "present":
        instagram_result["profile_url"] = byviewer_url
    return instagram_result


def _check_youtube(username: str) -> dict[str, Any]:
    normalized = normalize_youtube_username(username)
    return _check_html_profile(
        site="youtube",
        profile_url=f"https://www.youtube.com/@{quote(normalized, safe='')}/videos",
        not_found_tokens=["this channel does not exist", "channel unavailable", "404 not found"],
    )


def _check_linkedin(username: str) -> dict[str, Any]:
    normalized = _clean_username(username)
    profile_url = f"https://www.linkedin.com/in/{quote(normalized, safe='')}"
    try:
        response = requests.get(
            profile_url,
            headers={
                **_HEADERS,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=_DEFAULT_TIMEOUT,
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        return {"site": "linkedin", "status": "unknown", "profile_url": profile_url, "reason": str(exc)}

    status_code = int(response.status_code)
    if status_code == 404:
        return {"site": "linkedin", "status": "absent", "profile_url": profile_url, "reason": "http_404"}
    if status_code in {403, 429, 999}:
        # LinkedIn commonly blocks anonymous requests; avoid false "absent".
        return {"site": "linkedin", "status": "unknown", "profile_url": profile_url, "reason": f"http_{status_code}"}
    if status_code >= 500:
        return {"site": "linkedin", "status": "unknown", "profile_url": profile_url, "reason": f"http_{status_code}"}
    if status_code >= 400:
        return {"site": "linkedin", "status": "absent", "profile_url": profile_url, "reason": f"http_{status_code}"}

    body = response.text.lower()
    if any(token in body for token in ["this page doesn't exist", "profile not found", "page not found"]):
        return {"site": "linkedin", "status": "absent", "profile_url": profile_url, "reason": "not_found_marker"}
    if "sign in to view profile" in body or "join to view profile" in body:
        return {"site": "linkedin", "status": "present", "profile_url": profile_url, "reason": "authwall"}
    return {"site": "linkedin", "status": "present", "profile_url": profile_url, "reason": ""}


def _check_facebook(username: str) -> dict[str, Any]:
    normalized = _clean_username(username)
    profile_url = f"https://www.facebook.com/{quote(normalized, safe='')}/"
    if not normalized:
        return {"site": "facebook", "status": "absent", "profile_url": "", "reason": "empty_username"}

    urls = [
        profile_url,
        f"https://m.facebook.com/{quote(normalized, safe='')}/",
        f"https://mbasic.facebook.com/{quote(normalized, safe='')}/",
    ]
    session = requests.Session()
    session.headers.update(
        {
            **_HEADERS,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    absent_tokens = [
        "content isn't available right now",
        "this content isn't available",
        "page isn't available",
        "the link you followed may be broken",
        "profile not found",
    ]
    block_tokens = ["temporarily blocked", "security check", "captcha", "too many requests", "login.php"]

    saw_unknown = False
    for candidate_url in urls:
        try:
            response = session.get(candidate_url, timeout=_DEFAULT_TIMEOUT, allow_redirects=True)
        except requests.RequestException:
            saw_unknown = True
            continue
        status_code = int(response.status_code)
        body = str(response.text or "").lower()
        if status_code in {403, 429}:
            saw_unknown = True
            continue
        if status_code == 404:
            return {"site": "facebook", "status": "absent", "profile_url": profile_url, "reason": "http_404"}
        if status_code >= 500:
            saw_unknown = True
            continue
        if any(token in body for token in absent_tokens):
            return {"site": "facebook", "status": "absent", "profile_url": profile_url, "reason": "not_found_marker"}
        if any(token in body for token in block_tokens):
            saw_unknown = True
            continue
        return {"site": "facebook", "status": "present", "profile_url": profile_url, "reason": ""}

    if saw_unknown:
        return {"site": "facebook", "status": "unknown", "profile_url": profile_url, "reason": "blocked_or_inconclusive"}
    return {"site": "facebook", "status": "absent", "profile_url": profile_url, "reason": "inconclusive_absent"}


def _check_generic(site: str, profile_url: str) -> dict[str, Any]:
    return _check_html_profile(
        site=site,
        profile_url=profile_url,
        not_found_tokens=["not found", "page not found", "does not exist", "isn't available"],
    )


def run_username_recon(raw_username: str) -> dict[str, Any]:
    """Check username presence across supported + lead platforms."""
    username = _clean_username(raw_username)
    if not username:
        raise ValueError("username is required")

    checks: list[dict[str, Any]] = [
        {"site": "twitter", "platform": "twitter", "supported_for_collection": True, "fn": lambda: _check_twitter(username)},
        {"site": "reddit", "platform": "reddit", "supported_for_collection": True, "fn": lambda: _check_reddit(username)},
        {"site": "tiktok", "platform": "tiktok", "supported_for_collection": True, "fn": lambda: _check_tiktok(username)},
        {"site": "bluesky", "platform": "bluesky", "supported_for_collection": True, "fn": lambda: _check_bluesky(username)},
        {"site": "instagram", "platform": "instagram", "supported_for_collection": True, "fn": lambda: _check_instagram(username)},
        {"site": "youtube", "platform": "youtube", "supported_for_collection": True, "fn": lambda: _check_youtube(username)},
        {"site": "linkedin", "platform": None, "supported_for_collection": False, "fn": lambda: _check_linkedin(username)},
        {"site": "facebook", "platform": None, "supported_for_collection": False, "fn": lambda: _check_facebook(username)},
        {
            "site": "threads",
            "platform": None,
            "supported_for_collection": False,
            "fn": lambda: _check_generic("threads", f"https://www.threads.net/@{quote(username, safe='')}"),
        },
        {
            "site": "github",
            "platform": None,
            "supported_for_collection": False,
            "fn": lambda: _check_generic("github", f"https://github.com/{quote(username, safe='')}"),
        },
        {
            "site": "gitlab",
            "platform": None,
            "supported_for_collection": False,
            "fn": lambda: _check_generic("gitlab", f"https://gitlab.com/{quote(username, safe='')}"),
        },
        {
            "site": "twitch",
            "platform": None,
            "supported_for_collection": False,
            "fn": lambda: _check_generic("twitch", f"https://www.twitch.tv/{quote(username, safe='')}"),
        },
        {
            "site": "medium",
            "platform": None,
            "supported_for_collection": False,
            "fn": lambda: _check_generic("medium", f"https://medium.com/@{quote(username, safe='')}"),
        },
    ]

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(8, len(checks))) as executor:
        future_map = {executor.submit(item["fn"]): item for item in checks}
        for future in as_completed(future_map):
            config = future_map[future]
            base = {
                "site": config["site"],
                "platform": config["platform"],
                "supported_for_collection": config["supported_for_collection"],
            }
            try:
                result = future.result()
                base.update(result)
            except Exception as exc:  # pragma: no cover - defensive
                base.update(
                    {
                        "status": "unknown",
                        "reason": str(exc),
                        "profile_url": "",
                    }
                )
            results.append(base)

    site_order = {item["site"]: i for i, item in enumerate(checks)}
    results.sort(key=lambda item: site_order.get(str(item.get("site")), 999))

    # Best-effort screenshot capture for present profiles to support UI hover previews.
    screenshot_inputs = [
        (
            idx,
            str(row.get("site") or ""),
            _screenshot_profile_url(str(row.get("site") or ""), str(row.get("profile_url") or "").strip()),
        )
        for idx, row in enumerate(results)
        if row.get("status") == "present" and str(row.get("profile_url") or "").strip()
    ]
    if screenshot_inputs:
        with ThreadPoolExecutor(max_workers=min(4, len(screenshot_inputs))) as executor:
            future_map = {
                executor.submit(_capture_profile_screenshot, site=site, profile_url=profile_url): idx
                for idx, site, profile_url in screenshot_inputs
            }
            for future in as_completed(future_map):
                idx = future_map[future]
                try:
                    screenshot_url = str(future.result() or "").strip()
                except Exception:
                    screenshot_url = ""
                if screenshot_url:
                    results[idx]["screenshot_url"] = screenshot_url

    collection_targets: list[dict[str, str]] = []
    leads: list[dict[str, str]] = []
    for row in results:
        if row.get("status") != "present":
            continue
        platform = row.get("platform")
        if row.get("supported_for_collection") and platform:
            normalized_target = username
            if platform == "reddit":
                normalized_target = _clean_reddit_username(username)
            elif platform == "bluesky":
                normalized_target = normalize_bluesky_username(username)
            elif platform == "youtube":
                normalized_target = normalize_youtube_username(username)
            else:
                normalized_target = _clean_username(username)
            if normalized_target:
                collection_targets.append({"platform": str(platform), "username": normalized_target})
        else:
            lead_row = {"site": str(row.get("site") or ""), "profile_url": str(row.get("profile_url") or "")}
            screenshot_url = str(row.get("screenshot_url") or "").strip()
            if screenshot_url:
                lead_row["screenshot_url"] = screenshot_url
            leads.append(lead_row)

    return {
        "username": username,
        "results": results,
        "collection_targets": collection_targets,
        "leads": leads,
        "checked": len(results),
        "present_count": len([row for row in results if row.get("status") == "present"]),
    }


def _normalize_selector_type(raw: Any) -> str:
    value = str(raw or "").strip().lower()
    if value in {"username", "user", "handle"}:
        return "username"
    if value in {"email", "mail"}:
        return "email"
    if value in {"phone", "phone_number", "telephone", "mobile", "msisdn"}:
        return "phone"
    if value in {"name", "full_name", "person"}:
        return "name"
    if value in {"wallet", "crypto", "crypto_wallet", "address"}:
        return "wallet"
    return ""


def _normalize_recon_username(raw: Any) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""

    match = re.match(r"^https?://(?:www\.)?(?:x|twitter)\.com/([^/?#]+)", value, flags=re.IGNORECASE)
    if match:
        value = unquote(match.group(1))
    else:
        match = re.match(r"^https?://(?:www\.)?reddit\.com/(?:user|u)/([^/?#]+)", value, flags=re.IGNORECASE)
        if match:
            value = unquote(match.group(1))
        else:
            match = re.match(r"^https?://(?:www\.)?tiktok\.com/@([^/?#]+)", value, flags=re.IGNORECASE)
            if match:
                value = unquote(match.group(1))
            else:
                match = re.match(r"^https?://(?:www\.)?bsky\.app/profile/([^/?#]+)", value, flags=re.IGNORECASE)
                if match:
                    value = normalize_bluesky_username(unquote(match.group(1)))
                else:
                    match = re.match(r"^https?://(?:www\.)?instagram\.com/([^/?#]+)", value, flags=re.IGNORECASE)
                    if match:
                        value = unquote(match.group(1))
                    else:
                        match = re.match(r"^https?://(?:www\.)?youtube\.com/@([^/?#]+)", value, flags=re.IGNORECASE)
                        if match:
                            value = normalize_youtube_username(unquote(match.group(1)))

    value = str(value).strip().split("/", 1)[0]
    value = re.sub(r"^u/", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^@+", "", value).strip()
    return value


def _normalize_selector_value(selector_type: str, raw: Any) -> str:
    value = str(raw or "").strip()
    if selector_type == "username":
        return _normalize_recon_username(value)
    if selector_type == "email":
        return value.lower()
    if selector_type == "phone":
        compact = re.sub(r"[\s().-]+", "", value)
        return compact
    return value


def _is_valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", str(value or "").strip()))


def _is_valid_phone(value: str) -> bool:
    compact = re.sub(r"[^\d+]", "", str(value or "").strip())
    if not compact.startswith("+"):
        return False
    if compact.count("+") > 1:
        return False
    digits = re.sub(r"\D", "", compact)
    return 7 <= len(digits) <= 15


def normalize_recon_selectors(raw_selectors: Any) -> list[dict[str, str]]:
    items = raw_selectors if isinstance(raw_selectors, list) else []
    normalized: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        selector_type = _normalize_selector_type(item.get("type"))
        if not selector_type:
            continue
        value = _normalize_selector_value(selector_type, item.get("value"))
        if not value:
            continue
        if selector_type == "email" and not _is_valid_email(value):
            continue
        if selector_type == "phone" and not _is_valid_phone(value):
            continue
        key = (selector_type, value.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        normalized.append({"type": selector_type, "value": value})
    return normalized


def _load_user_scanner_engine():
    try:
        from user_scanner.core import engine  # type: ignore
        return engine
    except Exception:
        pass

    # Fallback to vendored copy in panopto/_vendor/user_scanner.
    vendor_root = Path(__file__).resolve().parent / "_vendor"
    if str(vendor_root) not in sys.path:
        sys.path.insert(0, str(vendor_root))
    try:
        from user_scanner.core import engine  # type: ignore
        return engine
    except Exception:
        return None


def _selector_presence_from_status(status: str) -> str:
    value = str(status or "").strip().lower()
    if value in {"present", "absent", "unknown"}:
        return value
    if value in {"found", "registered"}:
        return "present"
    if value in {"not found", "not registered"}:
        return "absent"
    return "unknown"


def _site_key(raw: Any) -> str:
    compact = re.sub(r"[^a-z0-9]+", "", str(raw or "").strip().lower())
    aliases = {
        "x": "twitter",
        "xtwitter": "twitter",
        "twitter": "twitter",
    }
    return aliases.get(compact, compact)


def _site_key_from_profile_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    try:
        host = str(urlparse(value).hostname or "").lower().replace("www.", "")
    except Exception:
        return ""
    if host in {"x.com", "twitter.com"} or host.endswith(".x.com") or host.endswith(".twitter.com"):
        return "twitter"
    if "reddit.com" in host:
        return "reddit"
    if "tiktok.com" in host:
        return "tiktok"
    if "bsky.app" in host or "bsky.social" in host:
        return "bluesky"
    if "instagram.com" in host:
        return "instagram"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "linkedin.com" in host:
        return "linkedin"
    if "facebook.com" in host:
        return "facebook"
    if "threads.net" in host:
        return "threads"
    if "github.com" in host:
        return "github"
    if "gitlab.com" in host:
        return "gitlab"
    if "twitch.tv" in host:
        return "twitch"
    if "medium.com" in host:
        return "medium"
    return host


def _site_to_collection_platform(site_key: str) -> str | None:
    mapping = {
        "twitter": "twitter",
        "reddit": "reddit",
        "tiktok": "tiktok",
        "bluesky": "bluesky",
        "instagram": "instagram",
        "youtube": "youtube",
    }
    return mapping.get(site_key)


def _build_profile_url_for_username(site_key: str, username: str) -> str:
    clean_username = _clean_username(username)
    if not clean_username:
        return ""
    if site_key == "twitter":
        return f"https://x.com/{quote(clean_username, safe='')}"
    if site_key == "reddit":
        return f"https://www.reddit.com/user/{quote(_clean_reddit_username(clean_username), safe='')}"
    if site_key == "tiktok":
        return f"https://www.tiktok.com/@{quote(clean_username, safe='')}"
    if site_key == "bluesky":
        return f"https://bsky.app/profile/{quote(normalize_bluesky_username(clean_username), safe='')}"
    if site_key == "instagram":
        return f"https://www.instagram.com/{quote(clean_username, safe='')}/"
    if site_key == "youtube":
        return f"https://www.youtube.com/@{quote(normalize_youtube_username(clean_username), safe='')}"
    if site_key == "threads":
        return f"https://www.threads.net/@{quote(clean_username, safe='')}"
    if site_key == "github":
        return f"https://github.com/{quote(clean_username, safe='')}"
    if site_key == "gitlab":
        return f"https://gitlab.com/{quote(clean_username, safe='')}"
    if site_key == "twitch":
        return f"https://www.twitch.tv/{quote(clean_username, safe='')}"
    if site_key == "medium":
        return f"https://medium.com/@{quote(clean_username, safe='')}"
    if site_key == "linkedin":
        return f"https://www.linkedin.com/in/{quote(clean_username, safe='')}"
    if site_key == "facebook":
        return f"https://www.facebook.com/{quote(clean_username, safe='')}/"
    return ""


def _looks_like_direct_profile_url(url: str, selector_value: str) -> bool:
    value = str(url or "").strip()
    if not re.match(r"^https?://", value, flags=re.IGNORECASE):
        return False
    selector = _clean_username(selector_value).lower()
    if not selector:
        return False
    parsed = re.sub(r"^https?://", "", value, flags=re.IGNORECASE).lower()
    path = parsed.split("/", 1)[1] if "/" in parsed else ""
    if not path:
        return False
    if selector in path:
        return True
    if f"@{selector}" in path:
        return True
    return False


_GENERIC_NON_PROFILE_PATH_SEGMENTS = {
    "about",
    "account",
    "accounts",
    "app",
    "apps",
    "blog",
    "careers",
    "company",
    "contact",
    "dashboard",
    "developers",
    "discover",
    "docs",
    "download",
    "explore",
    "features",
    "help",
    "home",
    "jobs",
    "join",
    "legal",
    "login",
    "pricing",
    "privacy",
    "products",
    "search",
    "settings",
    "signup",
    "support",
    "terms",
}


def _is_probable_profile_url(url: str) -> bool:
    value = str(url or "").strip()
    if not re.match(r"^https?://", value, flags=re.IGNORECASE):
        return False
    try:
        parsed = urlparse(value)
    except Exception:
        return False
    host = str(parsed.hostname or "").strip().lower()
    if not host or "." not in host:
        return False
    segments = [part for part in str(parsed.path or "").split("/") if part]
    if not segments:
        return False
    first = segments[0].lower()
    if first in _GENERIC_NON_PROFILE_PATH_SEGMENTS:
        return False
    if len(segments) == 1 and first in {"www", "m"}:
        return False
    return True


def _normalize_collection_username(platform: str, value: str) -> str:
    if platform == "reddit":
        return _clean_reddit_username(value)
    if platform == "bluesky":
        return normalize_bluesky_username(value)
    if platform == "youtube":
        return normalize_youtube_username(value)
    return _clean_username(value)


def _collection_target_from_profile_url(url: str) -> tuple[str, str] | None:
    value = str(url or "").strip()
    if not value:
        return None
    try:
        parsed = urlparse(value)
    except Exception:
        return None
    platform = _site_to_collection_platform(_site_key_from_profile_url(value))
    if not platform:
        return None
    parts = [part for part in str(parsed.path or "").split("/") if part]
    if not parts:
        return None

    username = ""
    if platform == "twitter":
        username = parts[0].lstrip("@")
    elif platform == "reddit":
        if len(parts) >= 2 and parts[0].lower() in {"user", "u"}:
            username = parts[1]
    elif platform == "tiktok":
        username = parts[0].lstrip("@")
    elif platform == "bluesky":
        if len(parts) >= 2 and parts[0].lower() == "profile":
            username = parts[1]
        elif parts:
            username = parts[0]
    elif platform == "instagram":
        username = parts[0].lstrip("@")
    elif platform == "youtube":
        if parts[0].startswith("@"):
            username = parts[0][1:]

    username = _normalize_collection_username(platform, username)
    if not username:
        return None
    return (platform, username)


def _extract_pdl_social_profile_urls(data: dict[str, Any]) -> list[str]:
    candidates: list[str] = []
    profiles = data.get("profiles")
    if isinstance(profiles, list):
        candidates.extend(str(item).strip() for item in profiles)
    social_profiles = data.get("social_profiles")
    if isinstance(social_profiles, list):
        for item in social_profiles:
            if not isinstance(item, dict):
                continue
            candidates.append(str(item.get("url") or "").strip())

    for key, raw_value in data.items():
        if not str(key).lower().endswith("_url"):
            continue
        candidates.append(str(raw_value or "").strip())

    output: list[str] = []
    seen: set[str] = set()
    for value in candidates:
        if not re.match(r"^https?://", value, flags=re.IGNORECASE):
            continue
        normalized = value.strip()
        if normalized.lower() in seen:
            continue
        seen.add(normalized.lower())
        output.append(normalized)
    return output


def _shape_person_data_profile(data: dict[str, Any], *, query_type: str, query_value: str) -> dict[str, Any]:
    def _extract_email_value(raw: Any) -> str:
        if isinstance(raw, dict):
            for key in ("address", "email", "value"):
                value = str(raw.get(key) or "").strip()
                if value:
                    return value
            return ""
        return str(raw or "").strip()

    def _extract_phone_value(raw: Any) -> str:
        if isinstance(raw, dict):
            for key in ("number", "value", "phone"):
                value = str(raw.get(key) or "").strip()
                if value:
                    return value
            return ""
        return str(raw or "").strip()

    full_name = str(data.get("full_name") or data.get("name") or "").strip()
    location = str(data.get("location_name") or "").strip()
    linkedin_url = str(data.get("linkedin_url") or "").strip()
    personal_emails = data.get("personal_emails")
    if not isinstance(personal_emails, list):
        personal_emails = []
    extra_emails_raw = data.get("emails")
    if isinstance(extra_emails_raw, list):
        personal_emails.extend(_extract_email_value(item) for item in extra_emails_raw)
    if isinstance(data.get("personal_email"), str):
        personal_emails.append(str(data.get("personal_email") or "").strip())
    fallback_email = ""
    if isinstance(personal_emails, list) and personal_emails:
        fallback_email = str(personal_emails[0] or "").strip()
    primary_email = str(data.get("work_email") or fallback_email).strip()
    dedup_personal_emails: list[str] = []
    seen_emails: set[str] = set()
    for item in personal_emails:
        clean = str(item).strip().lower()
        if not clean or clean in seen_emails:
            continue
        seen_emails.add(clean)
        dedup_personal_emails.append(clean)
    personal_emails = dedup_personal_emails
    personal_phones_raw = data.get("personal_phones")
    work_phones_raw = data.get("work_phones")
    personal_phones = [_extract_phone_value(item) for item in personal_phones_raw] if isinstance(personal_phones_raw, list) else []
    work_phones = [_extract_phone_value(item) for item in work_phones_raw] if isinstance(work_phones_raw, list) else []
    mobile_phone = str(data.get("mobile_phone") or "").strip()
    if not mobile_phone:
        mobile_phone = str(data.get("phone") or data.get("phone_number") or "").strip()
    phone_numbers_raw = data.get("phone_numbers")
    if isinstance(phone_numbers_raw, list):
        for item in phone_numbers_raw:
            if isinstance(item, dict):
                number = str(item.get("number") or item.get("value") or "").strip()
                label = str(item.get("type") or item.get("label") or "").strip().lower()
                if not number:
                    continue
                if label in {"work", "professional", "office", "business"}:
                    work_phones.append(number)
                elif label in {"mobile", "cell", "cellphone"}:
                    if not mobile_phone:
                        mobile_phone = number
                    personal_phones.append(number)
                else:
                    personal_phones.append(number)
            else:
                number = _extract_phone_value(item)
                if number:
                    personal_phones.append(number)
    for key in ("home_phone", "personal_phone", "phone_home"):
        value = str(data.get(key) or "").strip()
        if value:
            personal_phones.append(value)
    for key in ("professional_phone", "business_phone", "phone_work", "office_phone"):
        value = str(data.get(key) or "").strip()
        if value:
            work_phones.append(value)
    dedup_personal_phones: list[str] = []
    seen_personal_phones: set[str] = set()
    for item in personal_phones:
        clean = str(item or "").strip()
        key = clean.lower()
        if not clean or key in seen_personal_phones:
            continue
        seen_personal_phones.add(key)
        dedup_personal_phones.append(clean)
    personal_phones = dedup_personal_phones
    dedup_work_phones: list[str] = []
    seen_work_phones: set[str] = set()
    for item in work_phones:
        clean = str(item or "").strip()
        key = clean.lower()
        if not clean or key in seen_work_phones:
            continue
        seen_work_phones.add(key)
        dedup_work_phones.append(clean)
    work_phones = dedup_work_phones
    location_lat = data.get("location_latitude")
    location_lon = data.get("location_longitude")
    try:
        latitude = float(location_lat)
    except (TypeError, ValueError):
        latitude = None
    try:
        longitude = float(location_lon)
    except (TypeError, ValueError):
        longitude = None
    return {
        "query_type": query_type,
        "query_value": query_value,
        "full_name": full_name,
        "job_title": str(data.get("job_title") or "").strip(),
        "job_company_name": str(data.get("job_company_name") or "").strip(),
        "location_name": location,
        "linkedin_url": linkedin_url,
        "facebook_url": str(data.get("facebook_url") or "").strip(),
        "twitter_url": str(data.get("twitter_url") or "").strip(),
        "github_url": str(data.get("github_url") or "").strip(),
        "professional_email": str(data.get("work_email") or "").strip(),
        "work_email": str(data.get("work_email") or "").strip(),
        "personal_emails": [item for item in personal_emails if item],
        "email": primary_email,
        "mobile_phone": mobile_phone,
        "personal_phones": [item for item in personal_phones if item],
        "professional_phones": [item for item in work_phones if item],
        "phone": mobile_phone or (work_phones[0] if work_phones else "") or (personal_phones[0] if personal_phones else ""),
        "location_latitude": latitude,
        "location_longitude": longitude,
        "raw": data,
    }


def _run_user_scanner_selector(*, selector_type: str, selector_value: str) -> list[dict[str, Any]]:
    if selector_type not in {"username", "email"}:
        return []
    engine = _load_user_scanner_engine()
    if engine is None:
        if selector_type == "username":
            payload = run_username_recon(selector_value)
            rows = payload.get("results") if isinstance(payload, dict) else []
            return rows if isinstance(rows, list) else []
        # Degraded fallback: return explicit unknown rows instead of hard-failing.
        fallback_sites = [
            ("X (Twitter)", "https://x.com"),
            ("Reddit", "https://www.reddit.com"),
            ("TikTok", "https://www.tiktok.com"),
            ("Bluesky", "https://bsky.app"),
            ("Instagram", "https://www.instagram.com"),
            ("YouTube", "https://www.youtube.com"),
            ("Github", "https://github.com"),
            ("Gitlab", "https://gitlab.com"),
            ("Threads", "https://www.threads.net"),
            ("Twitch", "https://www.twitch.tv"),
            ("Medium", "https://medium.com"),
        ]
        return [
            {
                "site_name": site_name,
                "status": "Error",
                "reason": "email scanner dependencies unavailable (install requirements.txt)",
                "url": site_url,
            }
            for site_name, site_url in fallback_sites
        ]

    is_email = selector_type == "email"
    checked = asyncio.run(engine.check_all(selector_value, is_email=is_email))
    rows: list[dict[str, Any]] = []
    for item in checked:
        if hasattr(item, "as_dict") and callable(getattr(item, "as_dict")):
            entry = item.as_dict()
        elif isinstance(item, dict):
            entry = item
        else:
            continue
        if isinstance(entry, dict):
            rows.append(entry)
    return rows


def _scanner_result_is_confirmed(item: dict[str, Any]) -> bool:
    """A scanner tile represents a discovered account, not an availability check."""
    return str(item.get("status") or "").strip().lower() in {"found", "registered"}


def _profile_record_from_scanner_row(row: dict[str, Any], *, enrichment_status: str) -> dict[str, Any]:
    """Attach a stable, provenance-aware profile shape to a confirmed finding."""
    fields = {
        key: value
        for key, value in row.items()
        if key in {
            "full_name", "display_name", "name", "bio", "description", "summary", "about",
            "avatar_url", "picture_url", "profile_image_url", "banner_url", "header_url", "location",
            "website", "company", "followers", "following", "posts", "public_repos", "karma",
            "joined_at", "created_at",
        }
        and value not in (None, "", [], {})
    }
    status = str(row.get("status") or "").strip().lower()
    return {
        **row,
        "profile_record": {
            "presence_status": "confirmed",
            "confidence": 0.9 if status == "found" else 0.8,
            "source_url": str(row.get("profile_url") or row.get("url") or "").strip(),
            "extractor": "user_scanner",
            "checked_at": int(time.time()),
            "enrichment_status": enrichment_status,
            "fields": fields,
        },
    }


def _strip_profile_html(value: Any) -> str:
    text = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", html_unescape(text)).strip()


def _scanner_profile_data(site_key: str, username: str) -> dict[str, Any]:
    """Fetch public metadata for scanner modules with stable profile endpoints."""
    user = _clean_username(username)
    if not user:
        return {}
    headers = {**_HEADERS, "Accept": "application/json"}
    try:
        if site_key == "github":
            response = requests.get(f"https://api.github.com/users/{quote(user, safe='')}", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": data.get("html_url"), "full_name": data.get("name"), "bio": data.get("bio"),
                "avatar_url": data.get("avatar_url"), "location": data.get("location"), "website": data.get("blog"),
                "company": data.get("company"), "followers": data.get("followers"), "following": data.get("following"),
                "public_repos": data.get("public_repos"),
            }
        if site_key == "gitlab":
            response = requests.get("https://gitlab.com/api/v4/users", params={"username": user}, headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200 or not isinstance(response.json(), list) or not response.json():
                return {}
            data = response.json()[0]
            return {
                "profile_url": data.get("web_url"), "full_name": data.get("name"), "bio": data.get("bio"),
                "avatar_url": data.get("avatar_url"), "location": data.get("location"), "website": data.get("website_url"),
            }
        if site_key == "bluesky":
            actor = user if "." in user or user.startswith("did:") else f"{user}.bsky.social"
            response = requests.get("https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile", params={"actor": actor}, headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": f"https://bsky.app/profile/{data.get('handle') or actor}", "full_name": data.get("displayName"),
                "bio": data.get("description"), "avatar_url": data.get("avatar"), "banner_url": data.get("banner"),
                "followers": data.get("followersCount"), "following": data.get("followsCount"), "posts": data.get("postsCount"),
            }
        if site_key == "mastodon":
            response = requests.get("https://mastodon.social/api/v1/accounts/lookup", params={"acct": user}, headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": data.get("url"), "full_name": data.get("display_name"), "bio": _strip_profile_html(data.get("note")),
                "avatar_url": data.get("avatar"), "header_url": data.get("header"), "followers": data.get("followers_count"),
                "following": data.get("following_count"), "posts": data.get("statuses_count"),
            }
        if site_key == "devto":
            response = requests.get("https://dev.to/api/users/by_username", params={"url": user}, headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": data.get("website_url") or f"https://dev.to/{user}", "full_name": data.get("name"),
                "bio": data.get("summary"), "avatar_url": data.get("profile_image_90") or data.get("profile_image"),
                "location": data.get("location"), "website": data.get("website_url"), "joined_at": data.get("joined_at"),
            }
        if site_key == "codeberg":
            response = requests.get(f"https://codeberg.org/api/v1/users/{quote(user, safe='')}", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": data.get("html_url"), "full_name": data.get("full_name"), "bio": data.get("description"),
                "avatar_url": data.get("avatar_url"), "location": data.get("location"), "website": data.get("website"),
            }
        if site_key == "huggingface":
            response = requests.get(f"https://huggingface.co/api/users/{quote(user, safe='')}", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {
                "profile_url": f"https://huggingface.co/{data.get('user') or user}", "full_name": data.get("fullname"),
                "bio": data.get("bio"), "avatar_url": data.get("avatarUrl"), "website": data.get("website"),
            }
        if site_key == "hackernews":
            response = requests.get(f"https://hacker-news.firebaseio.com/v0/user/{quote(user, safe='')}.json", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            if not isinstance(data, dict):
                return {}
            return {"profile_url": f"https://news.ycombinator.com/user?id={quote(user, safe='')}", "full_name": data.get("id"), "bio": _strip_profile_html(data.get("about")), "karma": data.get("karma"), "created_at": data.get("created")}
        if site_key == "lichess":
            response = requests.get(f"https://lichess.org/api/user/{quote(user, safe='')}", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            profile = data.get("profile") if isinstance(data.get("profile"), dict) else {}
            return {
                "profile_url": f"https://lichess.org/@/{data.get('username') or user}", "full_name": profile.get("firstName") or data.get("username"),
                "bio": profile.get("bio"), "location": profile.get("location"), "followers": data.get("count", {}).get("followed") if isinstance(data.get("count"), dict) else None,
                "following": data.get("count", {}).get("following") if isinstance(data.get("count"), dict) else None,
            }
        if site_key == "chesscom":
            response = requests.get(f"https://api.chess.com/pub/player/{quote(user, safe='')}", headers=headers, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json()
            return {"profile_url": data.get("url"), "full_name": data.get("name"), "bio": data.get("status"), "avatar_url": data.get("avatar"), "location": data.get("location"), "followers": data.get("followers"), "joined_at": data.get("joined")}
        if site_key == "reddit":
            response = requests.get(f"https://www.reddit.com/user/{quote(user, safe='')}/about.json", headers={"User-Agent": "panopto-recon/1.0", "Accept": "application/json"}, timeout=_DEFAULT_TIMEOUT)
            if response.status_code != 200:
                return {}
            data = response.json().get("data", {})
            if not isinstance(data, dict):
                return {}
            subreddit = data.get("subreddit") if isinstance(data.get("subreddit"), dict) else {}
            return {"profile_url": f"https://www.reddit.com/user/{data.get('name') or user}", "full_name": subreddit.get("title"), "bio": subreddit.get("public_description"), "avatar_url": subreddit.get("icon_img") or subreddit.get("banner_img"), "karma": (data.get("link_karma") or 0) + (data.get("comment_karma") or 0), "created_at": data.get("created_utc")}
    except (requests.RequestException, ValueError, TypeError, AttributeError):
        return {}
    return {}


def _enrich_user_scanner_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    confirmed = [row for row in rows if _scanner_result_is_confirmed(row)]
    enrichable = [row for row in confirmed if not bool(row.get("is_email"))]
    if not confirmed:
        return rows

    def enrich(row: dict[str, Any]) -> dict[str, Any]:
        username = str(row.get("username") or "").strip()
        metadata = _scanner_profile_data(_site_key(row.get("site_name") or row.get("site")), username)
        enriched = row if not metadata else {**row, **{key: value for key, value in metadata.items() if value not in (None, "", [], {})}}
        return _profile_record_from_scanner_row(enriched, enrichment_status="complete")

    replacements: dict[int, dict[str, Any]] = {}
    if enrichable:
        with ThreadPoolExecutor(max_workers=min(8, len(enrichable))) as executor:
            enriched = list(executor.map(enrich, enrichable))
        replacements = {id(original): replacement for original, replacement in zip(enrichable, enriched)}
    return [
        replacements.get(id(row), _profile_record_from_scanner_row(row, enrichment_status="complete"))
        if _scanner_result_is_confirmed(row)
        else row
        for row in rows
    ]


def stream_user_scanner_selector(
    *,
    selector_type: str,
    selector_value: str,
    on_result: Any,
) -> list[dict[str, Any]]:
    """Call ``on_result`` for each confirmed scanner match as its check settles."""
    if selector_type not in {"username", "email"}:
        return []
    engine = _load_user_scanner_engine()
    if engine is None or not hasattr(engine, "check_all_stream"):
        rows = [row for row in _run_user_scanner_selector(selector_type=selector_type, selector_value=selector_value) if _scanner_result_is_confirmed(row)]
        for row in rows:
            on_result(_profile_record_from_scanner_row(row, enrichment_status="pending"))
        rows = _enrich_user_scanner_results(rows)
        for row in rows:
            on_result(row)
        return rows

    streamed: list[dict[str, Any]] = []

    async def _scan() -> None:
        async for item in engine.check_all_stream(selector_value, is_email=selector_type == "email"):
            if hasattr(item, "as_dict") and callable(getattr(item, "as_dict")):
                row = item.as_dict()
            elif isinstance(item, dict):
                row = dict(item)
            else:
                continue
            if not _scanner_result_is_confirmed(row):
                continue
            on_result(_profile_record_from_scanner_row(row, enrichment_status="pending"))
            enriched = _enrich_user_scanner_results([row])[0]
            streamed.append(enriched)
            on_result(enriched)

    asyncio.run(_scan())
    return streamed


def _run_pdl_enrichment(*, selectors: list[dict[str, str]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    api_key = _pdl_api_key()
    if not api_key:
        return {
            "person_data_profiles": [],
            "pdl_leads": [],
            "pdl_collection_targets": [],
            "pdl_rows": [],
            "query_success_count": 0,
        }

    profile_queries = [
        str(row.get("profile_url") or "").strip()
        for row in rows
        if str(row.get("selector_type") or "").strip() == "username"
        and str(row.get("status") or "").strip().lower() == "present"
        and str(row.get("profile_url") or "").strip()
    ]
    email_queries = [
        str(selector.get("value") or "").strip().lower()
        for selector in selectors
        if str(selector.get("type") or "").strip() == "email"
        and str(selector.get("value") or "").strip()
    ]

    query_pairs: list[tuple[str, str]] = []
    seen_queries: set[tuple[str, str]] = set()
    for email in email_queries:
        key = ("email", email)
        if key not in seen_queries:
            seen_queries.add(key)
            query_pairs.append(key)
    for profile_url in profile_queries:
        key = ("profile", profile_url)
        if key not in seen_queries:
            seen_queries.add(key)
            query_pairs.append(key)

    person_data_profiles: list[dict[str, Any]] = []
    pdl_leads: list[dict[str, str]] = []
    pdl_collection_targets: list[dict[str, str]] = []
    pdl_rows: list[dict[str, Any]] = []
    seen_profile_fingerprints: set[str] = set()
    seen_leads: set[str] = set()
    seen_targets: set[tuple[str, str]] = set()
    seen_rows: set[str] = set()
    query_success_count = 0

    for query_type, query_value in query_pairs:
        data = _fetch_pdl_profile(
            api_key=api_key,
            email=query_value if query_type == "email" else "",
            profile_url=query_value if query_type == "profile" else "",
        )
        if not data:
            continue
        query_success_count += 1

        fingerprint = str(data.get("id") or data.get("full_name") or data.get("name") or query_value).strip().lower()
        if fingerprint and fingerprint in seen_profile_fingerprints:
            continue
        if fingerprint:
            seen_profile_fingerprints.add(fingerprint)
        person_data_profiles.append(_shape_person_data_profile(data, query_type=query_type, query_value=query_value))

        for social_url in _extract_pdl_social_profile_urls(data):
            site_key = _site_key_from_profile_url(social_url)
            site = site_key or "lead"
            lead_key = f"{site.lower()}|{social_url.lower()}"
            if lead_key not in seen_leads:
                seen_leads.add(lead_key)
                pdl_leads.append({"site": site, "profile_url": social_url, "source": "pdl"})

            row_key = f"{site.lower()}|{social_url.lower()}"
            if row_key not in seen_rows:
                seen_rows.add(row_key)
                platform = _site_to_collection_platform(site_key)
                supported = bool(platform)
                category = "supported_with_url" if supported else "unsupported_with_url"
                pdl_rows.append(
                    {
                        "selector_type": query_type,
                        "selector": query_value,
                        "site": site or "unknown",
                        "site_key": site_key or "unknown",
                        "platform": platform,
                        "supported_for_collection": supported,
                        "status": "present",
                        "reason": "pdl_enriched",
                        "profile_url": social_url,
                        "site_url": social_url,
                        "has_direct_profile_url": True,
                        "category": category,
                        "source": "pdl",
                    }
                )

            target = _collection_target_from_profile_url(social_url)
            if not target:
                continue
            target_key = (target[0], target[1].lower())
            if target_key in seen_targets:
                continue
            seen_targets.add(target_key)
            pdl_collection_targets.append({"platform": target[0], "username": target[1]})

    return {
        "person_data_profiles": person_data_profiles,
        "pdl_leads": pdl_leads,
        "pdl_collection_targets": pdl_collection_targets,
        "pdl_rows": pdl_rows,
        "query_success_count": query_success_count,
    }


def _osint_selector_method(selector_type: str) -> str:
    mapping = {
        "username": "username",
        "email": "email",
        "phone": "phone",
        "name": "name",
        "wallet": "wallet",
    }
    return mapping.get(str(selector_type or "").strip().lower(), "")


def _osint_stringify_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(parts)
    if isinstance(value, dict):
        try:
            return json.dumps(value, ensure_ascii=True, sort_keys=True)
        except Exception:
            return str(value).strip()
    return str(value).strip()


def _parse_osint_spec_item(spec_item: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    parsed_values: dict[str, Any] = {}
    parsed_by_key: dict[str, Any] = {}

    for key, raw_value in spec_item.items():
        key_name = str(key or "").strip()
        if not key_name:
            continue
        if key_name == "platform_variables":
            continue
        if isinstance(raw_value, dict):
            proper_key = str(raw_value.get("proper_key") or key_name.replace("_", " ").title()).strip()
            value = raw_value.get("value")
            if value is None and any(field in raw_value for field in ("url", "href", "value")):
                value = raw_value.get("url") or raw_value.get("href") or raw_value.get("value")
            if value is None and len(raw_value) == 1:
                value = next(iter(raw_value.values()))
            if value is None:
                value = raw_value
            parsed_values[proper_key] = value
            parsed_by_key[key_name] = value
            continue
        proper_key = key_name.replace("_", " ").title().strip()
        parsed_values[proper_key] = raw_value
        parsed_by_key[key_name] = raw_value

    platform_variables = spec_item.get("platform_variables")
    if isinstance(platform_variables, list):
        for item in platform_variables:
            if not isinstance(item, dict):
                continue
            value_type = str(item.get("type") or "").strip().lower()
            # Keep platform variable parsing stable/simple per OSINT guide.
            if value_type not in {"str", "int", "float"}:
                continue
            key_name = str(item.get("key") or "").strip()
            proper_key = str(item.get("proper_key") or key_name.replace("_", " ").title()).strip()
            value = item.get("value")
            if proper_key:
                parsed_values[proper_key] = value
            if key_name:
                parsed_by_key[key_name] = value

    return parsed_values, parsed_by_key


def _iter_osint_spec_items(item: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()

    def _append_candidate(raw: Any) -> None:
        if not isinstance(raw, dict):
            return
        try:
            key = json.dumps(raw, ensure_ascii=True, sort_keys=True)
        except Exception:
            key = str(raw)
        if key in seen:
            return
        seen.add(key)
        candidates.append(raw)

    spec_format = item.get("spec_format")
    if isinstance(spec_format, list):
        for spec_item in spec_format:
            _append_candidate(spec_item)
    elif isinstance(spec_format, dict):
        _append_candidate(spec_format)

    for key in ("data", "result", "profile", "account"):
        nested = item.get(key)
        if isinstance(nested, dict):
            _append_candidate(nested)
        elif isinstance(nested, list):
            for row in nested:
                _append_candidate(row)

    nested_results = item.get("results")
    if isinstance(nested_results, list):
        for row in nested_results:
            _append_candidate(row)

    nested_profiles = item.get("profiles")
    if isinstance(nested_profiles, list):
        for row in nested_profiles:
            _append_candidate(row)

    if not candidates:
        _append_candidate(item)
    return candidates


def _osint_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        parsed = float(value)
        if parsed != parsed:  # NaN
            return None
        return parsed
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = float(raw)
    except ValueError:
        return None
    if parsed != parsed:  # NaN
        return None
    return parsed


def _osint_lat_key(value: str) -> bool:
    key = str(value or "").strip().lower()
    return key in {"lat", "latitude"} or key.endswith("_lat") or key.endswith("_latitude") or "latitude" in key


def _osint_lon_key(value: str) -> bool:
    key = str(value or "").strip().lower()
    return (
        key in {"lon", "lng", "longitude", "long"}
        or key.endswith("_lon")
        or key.endswith("_lng")
        or key.endswith("_longitude")
        or "longitude" in key
    )


def _osint_lat_lon_from_mapping(value: dict[str, Any]) -> tuple[float, float] | None:
    if not isinstance(value, dict):
        return None
    lowered_map: dict[str, Any] = {str(key).strip().lower(): raw for key, raw in value.items()}
    lat_candidates = [key for key in lowered_map if _osint_lat_key(key)]
    lon_candidates = [key for key in lowered_map if _osint_lon_key(key)]
    for lat_key in lat_candidates:
        lat_value = _osint_float(lowered_map.get(lat_key))
        if lat_value is None:
            continue
        for lon_key in lon_candidates:
            lon_value = _osint_float(lowered_map.get(lon_key))
            if lon_value is None:
                continue
            if -90 <= lat_value <= 90 and -180 <= lon_value <= 180:
                return (lat_value, lon_value)
            if -90 <= lon_value <= 90 and -180 <= lat_value <= 180:
                # Some providers invert latitude/longitude in loose schemas.
                return (lon_value, lat_value)
    return None


def _osint_coordinate_pair(value: Any) -> tuple[float, float] | None:
    if isinstance(value, dict):
        return _osint_lat_lon_from_mapping(value)
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        lat = _osint_float(value[0])
        lon = _osint_float(value[1])
        if lat is None or lon is None:
            return None
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return (lat, lon)
        if -90 <= lon <= 90 and -180 <= lat <= 180:
            return (lon, lat)
    return None


def _iter_osint_nodes(value: Any, path: tuple[str, ...] = (), *, depth: int = 0, max_depth: int = 7):
    yield (path, value)
    if depth >= max_depth:
        return
    if isinstance(value, dict):
        for key, nested in value.items():
            key_name = str(key or "").strip()
            if not key_name:
                continue
            yield from _iter_osint_nodes(nested, path + (key_name,), depth=depth + 1, max_depth=max_depth)
        return
    if isinstance(value, list):
        for index, nested in enumerate(value[:220]):
            yield from _iter_osint_nodes(nested, path + (f"[{index}]",), depth=depth + 1, max_depth=max_depth)


def _decode_google_polyline(encoded: str, *, max_points: int = 1800) -> list[dict[str, float]]:
    text = str(encoded or "").strip()
    if not text:
        return []
    points: list[dict[str, float]] = []
    index = 0
    lat = 0
    lon = 0
    length = len(text)
    try:
        while index < length and len(points) < max_points:
            result = 1
            shift = 0
            while True:
                byte = ord(text[index]) - 63 - 1
                index += 1
                result += byte << shift
                shift += 5
                if byte < 0x1F:
                    break
            dlat = ~(result >> 1) if result & 1 else (result >> 1)
            lat += dlat

            result = 1
            shift = 0
            while True:
                byte = ord(text[index]) - 63 - 1
                index += 1
                result += byte << shift
                shift += 5
                if byte < 0x1F:
                    break
            dlon = ~(result >> 1) if result & 1 else (result >> 1)
            lon += dlon

            lat_value = lat * 1e-5
            lon_value = lon * 1e-5
            if -90 <= lat_value <= 90 and -180 <= lon_value <= 180:
                points.append({"lat": round(lat_value, 6), "lon": round(lon_value, 6)})
    except Exception:
        return []
    return points


def _osint_route_hint(path: tuple[str, ...]) -> bool:
    joined = " ".join(path).lower()
    return any(token in joined for token in ("route", "polyline", "path", "track", "segment", "geometry", "line"))


def _osint_signal_text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return ""


def _osint_extract_detail(value: Any) -> str:
    if not isinstance(value, dict):
        return _osint_signal_text(value)[:220]
    preferred_keys = (
        "review",
        "review_text",
        "comment",
        "description",
        "bio",
        "caption",
        "summary",
        "body",
        "text",
        "title",
        "name",
        "address",
        "location",
    )
    for key in preferred_keys:
        if key not in value:
            continue
        clean = _osint_signal_text(value.get(key))
        if clean:
            return clean[:220]
    return ""


def _osint_extract_timestamp(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    keys = (
        "timestamp",
        "datetime",
        "date",
        "created_at",
        "updated_at",
        "time",
        "activity_date",
        "start_date",
        "end_date",
        "last_seen",
    )
    for key in keys:
        if key not in value:
            continue
        raw = _osint_signal_text(value.get(key))
        if raw:
            return raw[:64]
    return ""


def _normalize_route_coordinates(value: Any, *, max_points: int = 800) -> list[dict[str, float]]:
    coords: list[dict[str, float]] = []
    if not isinstance(value, list):
        return coords
    for item in value:
        pair = _osint_coordinate_pair(item)
        if not pair:
            continue
        coords.append({"lat": round(float(pair[0]), 6), "lon": round(float(pair[1]), 6)})
        if len(coords) >= max_points:
            break
    return coords


def _extract_osint_geo_signals(
    *,
    module_name: str,
    profile_title: str,
    profile_url: str,
    spec_item: dict[str, Any] | None,
    parsed_by_key: dict[str, Any],
    front_schema: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    roots: list[Any] = []
    if isinstance(spec_item, dict):
        roots.append(spec_item)
    if isinstance(parsed_by_key, dict):
        roots.append(parsed_by_key)
    if isinstance(front_schema, dict):
        roots.append(front_schema)

    signals: list[dict[str, Any]] = []
    seen_points: set[str] = set()
    seen_routes: set[str] = set()

    for root in roots:
        for path, node in _iter_osint_nodes(root):
            if isinstance(node, dict):
                pair = _osint_lat_lon_from_mapping(node)
                if pair:
                    lat, lon = pair
                    point_key = f"{lat:.6f}|{lon:.6f}"
                    if point_key not in seen_points:
                        seen_points.add(point_key)
                        path_label = ".".join(path) if path else "location"
                        signals.append(
                            {
                                "kind": "point",
                                "module": module_name,
                                "profile_title": profile_title,
                                "profile_url": profile_url,
                                "path": path_label,
                                "label": str(node.get("name") or node.get("title") or node.get("location") or "geo point").strip(),
                                "detail": _osint_extract_detail(node),
                                "timestamp": _osint_extract_timestamp(node),
                                "lat": round(lat, 6),
                                "lon": round(lon, 6),
                            }
                        )
                continue

            if isinstance(node, str):
                if path and "polyline" in str(path[-1]).lower():
                    route_points = _decode_google_polyline(node)
                    if len(route_points) >= 2:
                        route_key = f"polyline|{sha1(node.encode('utf-8')).hexdigest()}"
                        if route_key in seen_routes:
                            continue
                        seen_routes.add(route_key)
                        path_label = ".".join(path)
                        signals.append(
                            {
                                "kind": "polyline",
                                "module": module_name,
                                "profile_title": profile_title,
                                "profile_url": profile_url,
                                "path": path_label,
                                "label": "route",
                                "detail": "",
                                "coordinates": route_points[:800],
                            }
                        )
                continue

            if isinstance(node, list) and _osint_route_hint(path):
                route_points = _normalize_route_coordinates(node)
                if len(route_points) >= 2:
                    route_key = "|".join(
                        [
                            "route",
                            f"{route_points[0]['lat']:.6f}",
                            f"{route_points[0]['lon']:.6f}",
                            f"{route_points[-1]['lat']:.6f}",
                            f"{route_points[-1]['lon']:.6f}",
                            str(len(route_points)),
                        ]
                    )
                    if route_key in seen_routes:
                        continue
                    seen_routes.add(route_key)
                    path_label = ".".join(path) if path else "route"
                    signals.append(
                        {
                            "kind": "polyline",
                            "module": module_name,
                            "profile_title": profile_title,
                            "profile_url": profile_url,
                            "path": path_label,
                            "label": "route",
                            "detail": "",
                            "coordinates": route_points[:800],
                        }
                    )
    return signals[:80]


def _normalize_osint_profile(
    *,
    module_name: str,
    status: str,
    reliable_source: bool,
    selector_type: str,
    selector_value: str,
    spec_item: dict[str, Any] | None,
    parsed_by_key: dict[str, Any],
    front_schema: dict[str, Any] | None,
) -> dict[str, Any] | None:
    def _first_text(*keys: str) -> str:
        for key in keys:
            clean = _osint_stringify_value(parsed_by_key.get(key))
            if clean:
                return clean
        return ""

    first_name = _osint_stringify_value(parsed_by_key.get("first_name"))
    last_name = _osint_stringify_value(parsed_by_key.get("last_name"))
    full_name = _osint_stringify_value(parsed_by_key.get("name"))
    if not full_name:
        full_name = " ".join(part for part in [first_name, last_name] if part).strip()

    raw_profile_url = _osint_stringify_value(parsed_by_key.get("profile_url"))
    profile_url = raw_profile_url if _is_probable_profile_url(raw_profile_url) else ""
    website = _osint_stringify_value(parsed_by_key.get("website"))
    if not website and raw_profile_url and not profile_url:
        website = raw_profile_url
    username = _osint_stringify_value(parsed_by_key.get("username"))
    email = _osint_stringify_value(parsed_by_key.get("email"))
    phone = _osint_stringify_value(parsed_by_key.get("phone"))

    image_from_front_schema = ""
    front_timeline: dict[str, Any] = {}
    if isinstance(front_schema, dict):
        image_from_front_schema = _osint_stringify_value(front_schema.get("image"))
        timeline_value = front_schema.get("timeline")
        if isinstance(timeline_value, dict):
            front_timeline = timeline_value

    creation_date = _osint_stringify_value(parsed_by_key.get("creation_date"))
    if not creation_date:
        creation_date = _osint_stringify_value(front_timeline.get("registered_date"))
    last_seen = _osint_stringify_value(parsed_by_key.get("last_seen"))
    if not last_seen:
        last_seen = _osint_stringify_value(front_timeline.get("last_seen_date"))
    biolocation = _first_text("biolocation", "bio_location", "bio-location")
    location = _first_text("location", "location_name", "city")
    if not location:
        location = biolocation

    title = (
        full_name
        or username
        or email
        or phone
        or profile_url
        or website
        or module_name
        or selector_value
    )

    normalized = {
        "source": "osint_industries",
        "module": module_name,
        "status": status,
        "reliable_source": reliable_source,
        "query_type": selector_type,
        "query_value": selector_value,
        "title": title,
        "name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "picture_url": _osint_stringify_value(parsed_by_key.get("picture_url")) or image_from_front_schema,
        "banner_url": _osint_stringify_value(parsed_by_key.get("banner_url")),
        "gender": _osint_stringify_value(parsed_by_key.get("gender")),
        "age": _osint_stringify_value(parsed_by_key.get("age")),
        "language": _osint_stringify_value(parsed_by_key.get("language")),
        "location": location,
        "biolocation": biolocation,
        "username": username,
        "profile_url": profile_url,
        "email": email,
        "phone": phone,
        "email_hint": _osint_stringify_value(parsed_by_key.get("email_hint")),
        "phone_hint": _osint_stringify_value(parsed_by_key.get("phone_hint")),
        "website": website,
        "bio": _osint_stringify_value(parsed_by_key.get("bio")),
        "registered": _osint_stringify_value(parsed_by_key.get("registered")),
        "breach": _osint_stringify_value(parsed_by_key.get("breach")),
        "id": _osint_stringify_value(parsed_by_key.get("id")),
        "followers": _osint_stringify_value(parsed_by_key.get("followers")),
        "following": _osint_stringify_value(parsed_by_key.get("following")),
        "verified": _osint_stringify_value(parsed_by_key.get("verified")),
        "premium": _osint_stringify_value(parsed_by_key.get("premium")),
        "private": _osint_stringify_value(parsed_by_key.get("private")),
        "last_seen": last_seen,
        "creation_date": creation_date,
    }
    geo_signals = _extract_osint_geo_signals(
        module_name=module_name,
        profile_title=title,
        profile_url=profile_url or website,
        spec_item=spec_item,
        parsed_by_key=parsed_by_key,
        front_schema=front_schema,
    )
    if geo_signals:
        normalized["geo_signals"] = geo_signals

    has_primary = any(
        str(normalized.get(field) or "").strip()
        for field in (
            "name",
            "first_name",
            "last_name",
            "profile_url",
            "website",
            "username",
            "email",
            "phone",
            "picture_url",
            "bio",
        )
    )
    if not has_primary:
        return None
    return normalized


def _fetch_osint_profiles(
    *, selector_type: str, selector_value: str, api_key: str, timeout: int = 20
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], bool]:
    method = _osint_selector_method(selector_type)
    if not method:
        return ([], [], False)

    headers = {
        "Accept": "application/json",
        "api-key": api_key,
        "X-Api-Key": api_key,
        "User-Agent": "panopto-osint-industries/1.0",
    }

    clamped_timeout = max(5, min(int(timeout), 80))
    successful_query = False
    streamed_payloads: list[Any] = []
    pending_data_lines: list[str] = []

    def _flush_pending() -> None:
        nonlocal pending_data_lines
        if not pending_data_lines:
            return
        joined = "\n".join(pending_data_lines).strip()
        pending_data_lines = []
        if not joined:
            return
        try:
            streamed_payloads.append(json.loads(joined))
        except ValueError:
            pass

    try:
        response = requests.get(
            f"{_OSINT_INDUSTRIES_BASE_URL}/v2/request/stream",
            params={
                "type": method,
                "query": selector_value,
                "timeout": clamped_timeout,
            },
            headers=headers,
            timeout=timeout + 4,
            stream=True,
        )
    except requests.RequestException:
        response = None

    if response is None:
        return ([], [], False)
    if response.status_code >= 400:
        return ([], [], False)

    successful_query = True
    for raw_line in response.iter_lines(decode_unicode=True):
        line = str(raw_line or "").strip()
        if not line:
            _flush_pending()
            continue
        if line.startswith("event:"):
            continue
        if line.startswith("data:"):
            payload_text = line[5:].strip()
            if payload_text == "[DONE]":
                _flush_pending()
                continue
            pending_data_lines.append(payload_text)
            continue
        _flush_pending()
        try:
            streamed_payloads.append(json.loads(line))
        except ValueError:
            continue
    _flush_pending()

    if not streamed_payloads:
        return ([], [], successful_query)

    profiles: list[dict[str, Any]] = []
    spec_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    response_rows: list[Any] = []
    for payload in streamed_payloads:
        if isinstance(payload, dict):
            if str(payload.get("error") or "").strip():
                continue
            ok_flag = payload.get("ok")
            if ok_flag is False:
                continue
            if isinstance(payload.get("results"), list):
                response_rows.extend(payload.get("results") or [])
                continue
            if isinstance(payload.get("data"), list):
                response_rows.extend(payload.get("data") or [])
                continue
            response_rows.append(payload)
            continue
        if isinstance(payload, list):
            response_rows.extend(payload)

    for item in response_rows:
        if not isinstance(item, dict):
            continue
        module_name = str(item.get("module") or "").strip().lower() or "osint"
        status = str(item.get("status") or "").strip().lower() or "unknown"
        reliable_source = bool(item.get("reliable_source"))
        front_schemas = item.get("front_schemas")
        front_schema = front_schemas[0] if isinstance(front_schemas, list) and front_schemas and isinstance(front_schemas[0], dict) else None
        for spec_item in _iter_osint_spec_items(item):
            parsed_values, parsed_by_key = _parse_osint_spec_item(spec_item)
            normalized = _normalize_osint_profile(
                module_name=module_name,
                status=status,
                reliable_source=reliable_source,
                selector_type=selector_type,
                selector_value=selector_value,
                spec_item=spec_item,
                parsed_by_key=parsed_by_key,
                front_schema=front_schema,
            )
            if not normalized:
                continue
            key = "|".join(
                [
                    str(normalized.get("module") or "").strip().lower(),
                    str(normalized.get("profile_url") or "").strip().lower(),
                    str(normalized.get("website") or "").strip().lower(),
                    str(normalized.get("username") or "").strip().lower(),
                    str(normalized.get("email") or "").strip().lower(),
                    str(normalized.get("phone") or "").strip().lower(),
                    str(normalized.get("title") or "").strip().lower(),
                ]
            )
            if key in seen:
                continue
            seen.add(key)
            normalized["spec_format"] = spec_item
            normalized["parsed_values"] = parsed_values
            profiles.append(normalized)
            spec_rows.append(
                {
                    "module": module_name,
                    "status": status,
                    "reliable_source": reliable_source,
                    "query_type": selector_type,
                    "query_value": selector_value,
                    "title": str(normalized.get("title") or "").strip(),
                    "spec_format": spec_item,
                    "parsed_values": parsed_values,
                }
            )
    return (profiles, spec_rows, successful_query)


def _normalize_numverify_phone(value: str) -> str:
    compact = re.sub(r"[^\d+]", "", str(value or "").strip())
    if compact.count("+") > 1:
        compact = compact.replace("+", "")
    if "+" in compact and not compact.startswith("+"):
        compact = compact.replace("+", "")
    return compact


def _fetch_numverify_profile(*, phone: str, api_key: str, timeout: int = 16) -> dict[str, Any] | None:
    normalized_phone = _normalize_numverify_phone(phone)
    if not normalized_phone or not api_key:
        return None

    attempts: list[tuple[str, dict[str, str], dict[str, str]]] = [
        (
            _NUMVERIFY_BASE_URL,
            {"access_key": api_key, "number": normalized_phone, "format": "1"},
            {"Accept": "application/json", "User-Agent": "panopto-numverify/1.0"},
        ),
        (
            _NUMVERIFY_HTTPS_BASE_URL,
            {"access_key": api_key, "number": normalized_phone, "format": "1"},
            {"Accept": "application/json", "User-Agent": "panopto-numverify/1.0"},
        ),
        (
            _NUMVERIFY_APILAYER_URL,
            {"number": normalized_phone},
            {
                "Accept": "application/json",
                "User-Agent": "panopto-numverify/1.0",
                "apikey": api_key,
            },
        ),
    ]

    for url, params, headers in attempts:
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        except requests.RequestException:
            continue
        if response.status_code >= 400:
            continue
        try:
            payload = response.json()
        except ValueError:
            continue
        if not isinstance(payload, dict):
            continue
        if isinstance(payload.get("error"), dict):
            info = payload.get("error_info")
            message = str(info or payload["error"].get("info") or payload["error"].get("message") or "").strip().lower()
            if message:
                if "https" in message or "http" in message:
                    continue
            if payload["error"].get("code") in {101, 102, 103, 104}:
                return None
            continue
        return payload
    return None


def _shape_numverify_profile(payload: dict[str, Any], *, query_value: str) -> dict[str, Any]:
    international_format = str(payload.get("international_format") or "").strip()
    local_format = str(payload.get("local_format") or "").strip()
    e164 = str(payload.get("e164") or "").strip()
    number = str(payload.get("number") or "").strip() or international_format or e164 or local_format or query_value
    country_name = str(payload.get("country_name") or "").strip()
    location = str(payload.get("location") or "").strip()
    carrier = str(payload.get("carrier") or "").strip()
    line_type = str(payload.get("line_type") or "").strip()
    country_code = str(payload.get("country_code") or "").strip()
    title = number
    if country_name:
        title = f"{number} ({country_name})"
    return {
        "source": "numverify",
        "title": title,
        "query_type": "phone",
        "query_value": query_value,
        "number": number,
        "international_format": international_format,
        "local_format": local_format,
        "e164": e164,
        "country_name": country_name,
        "country_code": country_code,
        "country_prefix": str(payload.get("country_prefix") or "").strip(),
        "location": location,
        "carrier": carrier,
        "line_type": line_type,
        "valid": bool(payload.get("valid")),
        "raw": payload,
    }


def run_recon(
    selectors: list[dict[str, str]],
    *,
    scanner_rows_by_selector: dict[tuple[str, str], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    normalized_selectors = normalize_recon_selectors(selectors)
    if not normalized_selectors:
        raise ValueError("at least one valid selector is required")

    rows: list[dict[str, Any]] = []
    # Keep the vendor output separate from normalized profile rows. Enrichment can
    # promote a row later, but the UI still needs every scanner response.
    scanner_results: list[dict[str, Any]] = []
    row_presence_index: dict[tuple[str, str, str], int] = {}

    def _append_row_from_scan_item(
        *,
        selector_type: str,
        selector_value: str,
        item: dict[str, Any],
        source: str = "scanner",
    ) -> None:
        status = _selector_presence_from_status(str(item.get("status") or ""))
        raw_site_name = str(item.get("site_name") or item.get("site") or "").strip()
        site_key = _site_key(raw_site_name)
        if not site_key:
            site_key = _site_key_from_profile_url(str(item.get("url") or item.get("profile_url") or ""))
        site_label = re.sub(r"\s+", " ", raw_site_name).strip() or site_key or "unknown"
        if not site_key:
            site_key = "unknown"
        platform = _site_to_collection_platform(site_key)
        supported_for_collection = bool(platform and selector_type == "username")
        source_url = str(item.get("profile_url") or item.get("url") or "").strip()
        profile_url = ""
        if selector_type == "username":
            guessed = _build_profile_url_for_username(site_key, selector_value)
            if guessed:
                profile_url = guessed
            elif _looks_like_direct_profile_url(source_url, selector_value):
                profile_url = source_url

        has_direct_profile_url = bool(profile_url)
        category = ""
        if status == "present":
            if has_direct_profile_url and supported_for_collection:
                category = "supported_with_url"
            elif has_direct_profile_url:
                category = "unsupported_with_url"
            else:
                category = "known_without_url"

        row = {
            "selector_type": selector_type,
            "selector": selector_value,
            "site": site_label,
            "site_key": site_key,
            "platform": platform,
            "supported_for_collection": supported_for_collection,
            "status": status,
            "reason": str(item.get("reason") or "").strip(),
            "scanner_category": str(item.get("category") or "").strip(),
            "scanner_username": str(item.get("username") or "").strip(),
            "scanner_is_email": bool(item.get("is_email")),
            "profile_url": profile_url,
            "site_url": source_url,
            "has_direct_profile_url": has_direct_profile_url,
            "category": category,
            "source": source,
            "scanner_result": dict(item) if source == "scanner" else None,
        }

        dedupe_key = (selector_type, selector_value.strip().lower(), site_key)
        existing_index = row_presence_index.get(dedupe_key)
        if existing_index is None:
            row_presence_index[dedupe_key] = len(rows)
            rows.append(row)
            return

        existing = rows[existing_index]

        def _rank(candidate: dict[str, Any]) -> tuple[int, int, int]:
            candidate_status = str(candidate.get("status") or "").strip().lower()
            status_rank = 2 if candidate_status == "present" else (1 if candidate_status == "unknown" else 0)
            direct_rank = 1 if bool(candidate.get("has_direct_profile_url")) else 0
            supported_rank = 1 if bool(candidate.get("supported_for_collection")) else 0
            return (status_rank, direct_rank, supported_rank)

        if _rank(row) > _rank(existing):
            rows[existing_index] = row

    api_modules_queried: list[dict[str, Any]] = []
    osint_profiles: list[dict[str, Any]] = []
    osint_spec_results: list[dict[str, Any]] = []
    numverify_profiles: list[dict[str, Any]] = []

    osint_api_key = _osint_industries_api_key()
    numverify_key = _numverify_api_key()

    def _task_scanner() -> list[tuple[str, str, list[dict[str, Any]]]]:
        output: list[tuple[str, str, list[dict[str, Any]]]] = []
        for selector in normalized_selectors:
            selector_type = str(selector.get("type") or "").strip()
            selector_value = str(selector.get("value") or "").strip()
            if not selector_type or not selector_value:
                continue
            cached_rows = (scanner_rows_by_selector or {}).get((selector_type, selector_value))
            if cached_rows is not None:
                output.append((selector_type, selector_value, cached_rows))
                continue
            scan_rows = _run_user_scanner_selector(selector_type=selector_type, selector_value=selector_value)
            confirmed_rows = [row for row in scan_rows if isinstance(row, dict) and _scanner_result_is_confirmed(row)] if isinstance(scan_rows, list) else []
            output.append((selector_type, selector_value, _enrich_user_scanner_results(confirmed_rows)))
        return output

    def _task_osint() -> tuple[list[tuple[str, str, list[dict[str, Any]], list[dict[str, Any]]]], int]:
        if not osint_api_key:
            return ([], 0)
        output: list[tuple[str, str, list[dict[str, Any]], list[dict[str, Any]]]] = []
        query_success_count = 0
        for selector in normalized_selectors:
            selector_type = str(selector.get("type") or "").strip()
            selector_value = str(selector.get("value") or "").strip()
            if not selector_type or not selector_value:
                continue
            profiles, spec_rows, query_succeeded = _fetch_osint_profiles(
                selector_type=selector_type,
                selector_value=selector_value,
                api_key=osint_api_key,
            )
            if query_succeeded:
                query_success_count += 1
            output.append((selector_type, selector_value, profiles, spec_rows))
        return (output, query_success_count)

    def _task_numverify() -> tuple[list[tuple[str, dict[str, Any]]], int]:
        if not numverify_key:
            return ([], 0)
        output: list[tuple[str, dict[str, Any]]] = []
        query_success_count = 0
        for selector in normalized_selectors:
            selector_type = str(selector.get("type") or "").strip().lower()
            if selector_type != "phone":
                continue
            selector_value = str(selector.get("value") or "").strip()
            if not selector_value:
                continue
            payload = _fetch_numverify_profile(phone=selector_value, api_key=numverify_key)
            if not payload:
                continue
            query_success_count += 1
            output.append((selector_value, _shape_numverify_profile(payload, query_value=selector_value)))
        return (output, query_success_count)

    scan_batches: list[tuple[str, str, list[dict[str, Any]]]] = []
    osint_batches: list[tuple[str, str, list[dict[str, Any]], list[dict[str, Any]]]] = []
    numverify_batches: list[tuple[str, dict[str, Any]]] = []
    osint_query_success_count = 0
    numverify_query_success_count = 0

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Start OSINT stream fetch first so streaming begins immediately.
        future_osint = executor.submit(_task_osint)
        future_scanner = executor.submit(_task_scanner)
        future_numverify = executor.submit(_task_numverify)

        scan_batches = future_scanner.result()
        osint_batches, osint_query_success_count = future_osint.result()
        numverify_batches, numverify_query_success_count = future_numverify.result()

    for selector_type, selector_value, scan_rows in scan_batches:
        for item in scan_rows:
            if not isinstance(item, dict):
                continue
            scanner_results.append(
                {
                    "selector_type": selector_type,
                    "selector": selector_value,
                    **item,
                }
            )
            _append_row_from_scan_item(
                selector_type=selector_type,
                selector_value=selector_value,
                item=item,
                source="scanner",
            )

    seen_osint: set[str] = set()
    for selector_type, selector_value, profiles, spec_rows in osint_batches:
        for item in profiles:
            profile_url = str(item.get("profile_url") or "").strip()
            website = str(item.get("website") or "").strip()
            username = str(item.get("username") or "").strip()
            row_url = profile_url
            site_ref = row_url or website
            site_key = _site_key_from_profile_url(site_ref) if site_ref else "osint"
            site_label = site_key or "osint"
            platform = _site_to_collection_platform(site_key)
            supported_for_collection = bool(platform and row_url)
            if row_url:
                # If multiple OSINT modules return the same canonical URL, keep one row.
                row_key = f"url|{site_key.lower()}|{row_url.lower()}"
            else:
                row_key = "|".join(
                    [
                        "identity",
                        site_key.lower(),
                        username.lower(),
                        str(item.get("email") or "").strip().lower(),
                        str(item.get("phone") or "").strip().lower(),
                    ]
                )
            if row_key in seen_osint:
                continue
            seen_osint.add(row_key)
            category = "known_without_url"
            if row_url:
                category = "supported_with_url" if supported_for_collection else "unsupported_with_url"
            row = {
                "selector_type": selector_type,
                "selector": selector_value,
                "site": site_label,
                "site_key": site_key or "osint",
                "platform": platform,
                "supported_for_collection": supported_for_collection,
                "status": "present",
                "reason": "osint_industries",
                "profile_url": row_url,
                "site_url": site_ref,
                "has_direct_profile_url": bool(row_url),
                "category": category,
                "source": "osint_industries",
                "osint_profile": item,
            }
            rows.append(row)
            osint_profiles.append(item)
        for spec_row in spec_rows:
            osint_spec_results.append(spec_row)

    seen_numverify_numbers: set[str] = set()
    for selector_value, shaped in numverify_batches:
        dedupe_key = str(shaped.get("number") or selector_value).strip().lower()
        if not dedupe_key or dedupe_key in seen_numverify_numbers:
            continue
        seen_numverify_numbers.add(dedupe_key)
        numverify_profiles.append(shaped)

        status = "present" if shaped.get("valid") is True else "absent"
        rows.append(
            {
                "selector_type": "phone",
                "selector": selector_value,
                "site": "numverify",
                "site_key": "numverify",
                "platform": None,
                "supported_for_collection": False,
                "status": status,
                "reason": "numverify_phone_lookup",
                "profile_url": "",
                "site_url": "",
                "has_direct_profile_url": False,
                "category": "known_without_url" if status == "present" else "",
                "source": "numverify",
                "numverify_profile": shaped,
            }
        )

    if osint_query_success_count > 0:
        api_modules_queried.append(
            {
                "module": "osint_industries",
                "label": "OSINT Industries",
                "query_success_count": osint_query_success_count,
            }
        )
    if numverify_query_success_count > 0:
        api_modules_queried.append(
            {
                "module": "numverify",
                "label": "Numverify",
                "query_success_count": numverify_query_success_count,
            }
        )

    # Second-stage pivot after scanner + OSINT + numverify rows are known.
    pdl_payload = _run_pdl_enrichment(selectors=normalized_selectors, rows=rows)
    pdl_query_success_count = int(pdl_payload.get("query_success_count") or 0)
    if pdl_query_success_count > 0:
        api_modules_queried.append(
            {
                "module": "people_data_labs",
                "label": "People Data Labs",
                "query_success_count": pdl_query_success_count,
            }
        )
    pdl_rows = pdl_payload.get("pdl_rows") if isinstance(pdl_payload.get("pdl_rows"), list) else []
    if pdl_rows:
        existing_row_keys: dict[str, int] = {}
        for idx, row in enumerate(rows):
            profile_url = str(row.get("profile_url") or "").strip()
            if not profile_url:
                continue
            row_key = f"{str(row.get('site_key') or '').lower()}|{profile_url.lower()}"
            existing_row_keys[row_key] = idx
        for pdl_row in pdl_rows:
            row_key = f"{str(pdl_row.get('site_key') or '').lower()}|{str(pdl_row.get('profile_url') or '').strip().lower()}"
            if row_key in existing_row_keys:
                existing = rows[existing_row_keys[row_key]]
                # PDL confirmations should promote rows to present/profile-url categories.
                existing["source"] = "pdl"
                existing["status"] = str(pdl_row.get("status") or existing.get("status") or "present")
                existing["reason"] = str(pdl_row.get("reason") or existing.get("reason") or "")
                existing["category"] = str(pdl_row.get("category") or existing.get("category") or "")
                existing["supported_for_collection"] = bool(
                    pdl_row.get("supported_for_collection")
                    if "supported_for_collection" in pdl_row
                    else existing.get("supported_for_collection")
                )
                existing["has_direct_profile_url"] = bool(
                    pdl_row.get("has_direct_profile_url")
                    if "has_direct_profile_url" in pdl_row
                    else existing.get("has_direct_profile_url")
                )
                if str(pdl_row.get("platform") or "").strip():
                    existing["platform"] = str(pdl_row.get("platform") or "").strip()
                if str(pdl_row.get("profile_url") or "").strip():
                    existing["profile_url"] = str(pdl_row.get("profile_url") or "").strip()
                if str(pdl_row.get("site") or "").strip():
                    existing["site"] = str(pdl_row.get("site") or "").strip()
                if str(pdl_row.get("site_key") or "").strip():
                    existing["site_key"] = str(pdl_row.get("site_key") or "").strip()
                continue
            existing_row_keys[row_key] = len(rows)
            rows.append(pdl_row)

    # Best-effort screenshot capture for present rows that include a direct profile URL.
    screenshot_inputs = [
        (idx, str(row.get("site_key") or row.get("site") or ""), _screenshot_profile_url(str(row.get("site_key") or row.get("site") or ""), str(row.get("profile_url") or "")))
        for idx, row in enumerate(rows)
        if row.get("status") == "present" and str(row.get("profile_url") or "").strip()
    ][: _MAX_RECON_SCREENSHOTS]
    if screenshot_inputs:
        with ThreadPoolExecutor(max_workers=min(4, len(screenshot_inputs))) as executor:
            future_map = {
                executor.submit(_capture_profile_screenshot, site=site, profile_url=profile_url): idx
                for idx, site, profile_url in screenshot_inputs
            }
            for future in as_completed(future_map):
                idx = future_map[future]
                try:
                    screenshot_url = str(future.result() or "").strip()
                except Exception:
                    screenshot_url = ""
                if screenshot_url:
                    rows[idx]["screenshot_url"] = screenshot_url

    collection_targets: list[dict[str, str]] = []
    leads: list[dict[str, Any]] = []
    supported_with_url: list[dict[str, Any]] = []
    unsupported_with_url: list[dict[str, Any]] = []
    known_without_url: list[dict[str, Any]] = []
    seen_targets: set[tuple[str, str]] = set()
    for row in rows:
        category = str(row.get("category") or "")
        if category == "supported_with_url":
            supported_with_url.append(row)
            platform = str(row.get("platform") or "").strip().lower()
            username = ""
            from_profile = _collection_target_from_profile_url(str(row.get("profile_url") or ""))
            if from_profile and from_profile[0] == platform:
                username = from_profile[1]
            if not username:
                username = _normalize_collection_username(platform, str(row.get("selector") or ""))
            if platform and username:
                key = (platform, username.lower())
                if key not in seen_targets:
                    seen_targets.add(key)
                    collection_targets.append({"platform": platform, "username": username})
        elif category == "unsupported_with_url":
            unsupported_with_url.append(row)
            lead_row = {
                "site": str(row.get("site") or ""),
                "profile_url": str(row.get("profile_url") or ""),
                "source": str(row.get("source") or "scanner"),
            }
            screenshot_url = str(row.get("screenshot_url") or "").strip()
            if screenshot_url:
                lead_row["screenshot_url"] = screenshot_url
            leads.append(lead_row)
        elif category == "known_without_url":
            known_without_url.append(row)
    person_data_profiles = (
        pdl_payload.get("person_data_profiles")
        if isinstance(pdl_payload.get("person_data_profiles"), list)
        else []
    )
    pdl_leads = pdl_payload.get("pdl_leads") if isinstance(pdl_payload.get("pdl_leads"), list) else []
    pdl_collection_targets = (
        pdl_payload.get("pdl_collection_targets")
        if isinstance(pdl_payload.get("pdl_collection_targets"), list)
        else []
    )

    existing_leads = {f"{str(item.get('site') or '').lower()}|{str(item.get('profile_url') or '').lower()}" for item in leads}
    for lead in pdl_leads:
        key = f"{str(lead.get('site') or '').lower()}|{str(lead.get('profile_url') or '').lower()}"
        if key in existing_leads:
            continue
        existing_leads.add(key)
        lead_row = {
            "site": str(lead.get("site") or ""),
            "profile_url": str(lead.get("profile_url") or ""),
            "source": "pdl",
        }
        leads.append(lead_row)

    for target in pdl_collection_targets:
        platform = str(target.get("platform") or "").strip().lower()
        username = str(target.get("username") or "").strip()
        if not platform or not username:
            continue
        key = (platform, username.lower())
        if key in seen_targets:
            continue
        seen_targets.add(key)
        collection_targets.append({"platform": platform, "username": username})

    def _append_intel_lead(label: str, value: str, *, profile_name: str = "", source: str = "pdl") -> None:
        clean = str(value or "").strip()
        if not clean:
            return
        leads.append(
            {
                "site": "person_data",
                "profile_url": "",
                "source": source,
                "lead_type": "attribute",
                "attribute": label,
                "value": clean,
                "profile_name": str(profile_name or "").strip(),
            }
        )

    for profile in person_data_profiles:
        profile_name = str(profile.get("full_name") or "").strip()
        _append_intel_lead("Full Name", profile_name, profile_name=profile_name)
        _append_intel_lead("Location", str(profile.get("location_name") or ""), profile_name=profile_name)
        _append_intel_lead("Job Title", str(profile.get("job_title") or ""), profile_name=profile_name)
        _append_intel_lead("Company", str(profile.get("job_company_name") or ""), profile_name=profile_name)
        personal_emails = profile.get("personal_emails") if isinstance(profile.get("personal_emails"), list) else []
        for item in personal_emails:
            _append_intel_lead("Personal Email", str(item or ""), profile_name=profile_name)
        _append_intel_lead(
            "Professional Email",
            str(profile.get("professional_email") or profile.get("work_email") or ""),
            profile_name=profile_name,
        )
        personal_phones = profile.get("personal_phones") if isinstance(profile.get("personal_phones"), list) else []
        work_phones = profile.get("professional_phones") if isinstance(profile.get("professional_phones"), list) else []
        for item in personal_phones:
            _append_intel_lead("Personal Phone", str(item or ""), profile_name=profile_name)
        _append_intel_lead("Mobile Phone", str(profile.get("mobile_phone") or ""), profile_name=profile_name)
        for item in work_phones:
            _append_intel_lead("Professional Phone", str(item or ""), profile_name=profile_name)

    return {
        "selectors": normalized_selectors,
        "results": rows,
        "scanner_results": scanner_results,
        "collection_targets": collection_targets,
        "leads": leads,
        "osint_profiles": osint_profiles,
        "osint_spec_results": osint_spec_results,
        "numverify_profiles": numverify_profiles,
        "person_data_profile": person_data_profiles[0] if person_data_profiles else {},
        "person_data_profiles": person_data_profiles,
        "api_modules_queried": api_modules_queried,
        "collection_ready_profiles": supported_with_url,
        "unsupported_profiles_with_url": unsupported_with_url,
        "known_present_without_url": known_without_url,
        "checked": len(rows),
        "present_count": len([row for row in rows if row.get("status") == "present"]),
    }
