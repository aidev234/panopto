"""Username reconnaissance helpers inspired by user-scanner style checks."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha1
import json
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib.parse import quote, urlparse

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


def _osint_industries_use_premium() -> bool:
    config = load_config()
    return bool(config.get("osint_industries_use_premium"))


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
    # Twitterwebviewer pages are unreliable for screenshots; use native x.com profile page.
    match = re.search(r"twitterwebviewer\.com/@([^/?#]+)", raw_url, flags=re.IGNORECASE)
    if not match:
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

    primary_results = [
        _check_html_profile(
            site="twitter",
            profile_url=f"https://twitterwebviewer.com/@{quote(candidate, safe='')}",
            not_found_tokens=["user not found", "account suspended", "this account doesn", "doesn't exist"],
        )
        for candidate in candidates
    ]
    for result in primary_results:
        if result.get("status") == "present":
            return result

    fallback = _check_html_profile(
        site="twitter",
        profile_url=f"https://x.com/{quote(raw, safe='')}",
        not_found_tokens=[
            "this account doesn't exist",
            "this account doesn’t exist",
            "account doesn’t exist",
            "account doesn't exist",
            "user not found",
        ],
    )
    if fallback.get("status") == "present":
        fallback["profile_url"] = f"https://twitterwebviewer.com/@{quote(raw, safe='')}"
        return fallback

    any_unknown_primary = any(result.get("status") == "unknown" for result in primary_results)
    all_absent_primary = all(result.get("status") == "absent" for result in primary_results)
    if fallback.get("status") == "absent":
        if any_unknown_primary:
            return {
                "site": "twitter",
                "status": "unknown",
                "profile_url": f"https://twitterwebviewer.com/@{quote(raw, safe='')}",
                "reason": "inconclusive",
            }
        if all_absent_primary:
            return primary_results[0]
    if fallback.get("status") == "unknown" and all_absent_primary:
        return primary_results[0]

    for result in primary_results:
        if result.get("status") == "unknown":
            return result
    return fallback


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


def _normalize_selector_value(selector_type: str, raw: Any) -> str:
    value = str(raw or "").strip()
    if selector_type == "username":
        return _clean_username(value)
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


def _run_pdl_enrichment(*, selectors: list[dict[str, str]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    api_key = _pdl_api_key()
    if not api_key:
        return {
            "person_data_profiles": [],
            "pdl_leads": [],
            "pdl_collection_targets": [],
            "pdl_rows": [],
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

    for query_type, query_value in query_pairs:
        data = _fetch_pdl_profile(
            api_key=api_key,
            email=query_value if query_type == "email" else "",
            profile_url=query_value if query_type == "profile" else "",
        )
        if not data:
            continue

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
        if not isinstance(raw_value, dict):
            continue
        proper_key = str(raw_value.get("proper_key") or key_name.replace("_", " ").title()).strip()
        value = raw_value.get("value")
        parsed_values[proper_key] = value
        parsed_by_key[key_name] = value

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


def _normalize_osint_profile(
    *,
    module_name: str,
    status: str,
    reliable_source: bool,
    selector_type: str,
    selector_value: str,
    parsed_by_key: dict[str, Any],
    front_schema: dict[str, Any] | None,
) -> dict[str, Any] | None:
    first_name = _osint_stringify_value(parsed_by_key.get("first_name"))
    last_name = _osint_stringify_value(parsed_by_key.get("last_name"))
    full_name = _osint_stringify_value(parsed_by_key.get("name"))
    if not full_name:
        full_name = " ".join(part for part in [first_name, last_name] if part).strip()

    profile_url = _osint_stringify_value(parsed_by_key.get("profile_url"))
    website = _osint_stringify_value(parsed_by_key.get("website"))
    username = _osint_stringify_value(parsed_by_key.get("username"))
    email = _osint_stringify_value(parsed_by_key.get("email"))
    phone = _osint_stringify_value(parsed_by_key.get("phone"))

    image_from_front_schema = ""
    if isinstance(front_schema, dict):
        image_from_front_schema = _osint_stringify_value(front_schema.get("image"))

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
        "gender": _osint_stringify_value(parsed_by_key.get("gender")),
        "age": _osint_stringify_value(parsed_by_key.get("age")),
        "location": _osint_stringify_value(parsed_by_key.get("location")),
        "username": username,
        "profile_url": profile_url,
        "email": email,
        "phone": phone,
        "email_hint": _osint_stringify_value(parsed_by_key.get("email_hint")),
        "phone_hint": _osint_stringify_value(parsed_by_key.get("phone_hint")),
        "website": website,
        "bio": _osint_stringify_value(parsed_by_key.get("bio")),
    }

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


def _fetch_osint_profiles(*, selector_type: str, selector_value: str, api_key: str, premium: bool, timeout: int = 20) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    method = _osint_selector_method(selector_type)
    if not method:
        return ([], [])

    payload = {
        "type": method,
        "method": method,
        "query": selector_value,
        "value": selector_value,
        "selector": method,
        "selector_type": method,
    }
    if premium:
        payload["premium"] = True

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Api-Key": api_key,
        "api-key": api_key,
        "User-Agent": "panopto-osint-industries/1.0",
    }
    endpoint_paths = ["/v2/request/premium", "/v2/request"] if premium else ["/v2/request"]

    response_payload: Any = None
    for path in endpoint_paths:
        try:
            response = requests.post(
                f"{_OSINT_INDUSTRIES_BASE_URL}{path}",
                json=payload,
                headers=headers,
                timeout=timeout,
            )
        except requests.RequestException:
            continue
        if response.status_code in {404, 405}:
            continue
        try:
            response_payload = response.json()
        except ValueError:
            continue
        if isinstance(response_payload, dict):
            if str(response_payload.get("error") or "").strip():
                continue
        break

    if response_payload is None:
        return ([], [])

    profiles: list[dict[str, Any]] = []
    spec_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    response_rows: list[Any]
    if isinstance(response_payload, list):
        response_rows = response_payload
    elif isinstance(response_payload, dict):
        if isinstance(response_payload.get("results"), list):
            response_rows = response_payload.get("results")  # type: ignore[assignment]
        elif isinstance(response_payload.get("data"), list):
            response_rows = response_payload.get("data")  # type: ignore[assignment]
        else:
            response_rows = [response_payload]
    else:
        response_rows = []

    for item in response_rows:
        if not isinstance(item, dict):
            continue
        module_name = str(item.get("module") or "").strip().lower() or "osint"
        status = str(item.get("status") or "").strip().lower() or "unknown"
        reliable_source = bool(item.get("reliable_source"))
        front_schemas = item.get("front_schemas")
        front_schema = front_schemas[0] if isinstance(front_schemas, list) and front_schemas and isinstance(front_schemas[0], dict) else None
        spec_format = item.get("spec_format")
        if not isinstance(spec_format, list):
            continue
        for spec_item in spec_format:
            if not isinstance(spec_item, dict):
                continue
            parsed_values, parsed_by_key = _parse_osint_spec_item(spec_item)
            normalized = _normalize_osint_profile(
                module_name=module_name,
                status=status,
                reliable_source=reliable_source,
                selector_type=selector_type,
                selector_value=selector_value,
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
    return (profiles, spec_rows)


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


def run_recon(selectors: list[dict[str, str]]) -> dict[str, Any]:
    normalized_selectors = normalize_recon_selectors(selectors)
    if not normalized_selectors:
        raise ValueError("at least one valid selector is required")

    rows: list[dict[str, Any]] = []
    for selector in normalized_selectors:
        selector_type = selector["type"]
        selector_value = selector["value"]
        scan_rows = _run_user_scanner_selector(selector_type=selector_type, selector_value=selector_value)
        for item in scan_rows:
            status = _selector_presence_from_status(str(item.get("status") or ""))
            raw_site_name = str(item.get("site_name") or item.get("site") or "").strip()
            site_key = _site_key(raw_site_name)
            site_label = re.sub(r"\s+", " ", raw_site_name).strip() or site_key or "unknown"
            platform = _site_to_collection_platform(site_key)
            supported_for_collection = bool(platform and selector_type == "username")
            source_url = str(item.get("url") or item.get("profile_url") or "").strip()
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

            rows.append(
                {
                    "selector_type": selector_type,
                    "selector": selector_value,
                    "site": site_label,
                    "site_key": site_key,
                    "platform": platform,
                    "supported_for_collection": supported_for_collection,
                    "status": status,
                    "reason": str(item.get("reason") or "").strip(),
                    "profile_url": profile_url,
                    "site_url": source_url,
                    "has_direct_profile_url": has_direct_profile_url,
                    "category": category,
                    "source": "scanner",
                }
            )

    pdl_payload = _run_pdl_enrichment(selectors=normalized_selectors, rows=rows)
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

    osint_profiles: list[dict[str, Any]] = []
    osint_spec_results: list[dict[str, Any]] = []
    numverify_profiles: list[dict[str, Any]] = []
    osint_api_key = _osint_industries_api_key()
    osint_use_premium = _osint_industries_use_premium()
    if osint_api_key:
        seen_osint: set[str] = set()
        for selector in normalized_selectors:
            selector_type = str(selector.get("type") or "").strip()
            selector_value = str(selector.get("value") or "").strip()
            if not selector_type or not selector_value:
                continue
            profiles, spec_rows = _fetch_osint_profiles(
                selector_type=selector_type,
                selector_value=selector_value,
                api_key=osint_api_key,
                premium=osint_use_premium,
            )
            for item in profiles:
                profile_url = str(item.get("profile_url") or "").strip()
                website = str(item.get("website") or "").strip()
                username = str(item.get("username") or "").strip()
                row_url = profile_url or website
                site_key = _site_key_from_profile_url(row_url) if row_url else "osint"
                site_label = site_key or "osint"
                platform = _site_to_collection_platform(site_key)
                supported_for_collection = bool(platform and row_url)
                row_key = "|".join(
                    [
                        site_key.lower(),
                        row_url.lower(),
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
                    "site_url": row_url,
                    "has_direct_profile_url": bool(row_url),
                    "category": category,
                    "source": "osint_industries",
                    "osint_profile": item,
                }
                rows.append(row)
                osint_profiles.append(item)
            for spec_row in spec_rows:
                osint_spec_results.append(spec_row)

    numverify_key = _numverify_api_key()
    if numverify_key:
        seen_numverify_numbers: set[str] = set()
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
            shaped = _shape_numverify_profile(payload, query_value=selector_value)
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
        _append_intel_lead("Professional Email", str(profile.get("professional_email") or profile.get("work_email") or ""), profile_name=profile_name)
        personal_emails = profile.get("personal_emails") if isinstance(profile.get("personal_emails"), list) else []
        for item in personal_emails:
            _append_intel_lead("Personal Email", str(item or ""), profile_name=profile_name)
        _append_intel_lead("Mobile Phone", str(profile.get("mobile_phone") or ""), profile_name=profile_name)
        personal_phones = profile.get("personal_phones") if isinstance(profile.get("personal_phones"), list) else []
        work_phones = profile.get("professional_phones") if isinstance(profile.get("professional_phones"), list) else []
        for item in personal_phones:
            _append_intel_lead("Personal Phone", str(item or ""), profile_name=profile_name)
        for item in work_phones:
            _append_intel_lead("Professional Phone", str(item or ""), profile_name=profile_name)

    return {
        "selectors": normalized_selectors,
        "results": rows,
        "collection_targets": collection_targets,
        "leads": leads,
        "osint_profiles": osint_profiles,
        "osint_spec_results": osint_spec_results,
        "numverify_profiles": numverify_profiles,
        "person_data_profile": person_data_profiles[0] if person_data_profiles else {},
        "person_data_profiles": person_data_profiles,
        "collection_ready_profiles": supported_with_url,
        "unsupported_profiles_with_url": unsupported_with_url,
        "known_present_without_url": known_without_url,
        "checked": len(rows),
        "present_count": len([row for row in rows if row.get("status") == "present"]),
    }
