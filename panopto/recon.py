"""Username reconnaissance helpers inspired by user-scanner style checks."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from typing import Any
from urllib.parse import quote

import requests

from panopto.collectors.bluesky import normalize_bluesky_username
from panopto.collectors.youtube import normalize_youtube_username

_DEFAULT_TIMEOUT = 12
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


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
            leads.append({"site": str(row.get("site") or ""), "profile_url": str(row.get("profile_url") or "")})

    return {
        "username": username,
        "results": results,
        "collection_targets": collection_targets,
        "leads": leads,
        "checked": len(results),
        "present_count": len([row for row in results if row.get("status") == "present"]),
    }
