"""Collection orchestration service used by HTTP handlers."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote

from panopto.collectors.bluesky import collect_bluesky_posts, normalize_bluesky_username
from panopto.collectors.instagram import collect_instagram_posts, normalize_instagram_username
from panopto.errors import SourceAccessBlockedError, UsernameNotFoundError
from panopto.collectors.reddit import collect_reddit_posts
from panopto.collectors.tiktok import collect_tiktok_posts
from panopto.analysis.theme_modeling import tag_posts_with_bertopic
from panopto.collectors.twitter import collect_twitter_posts
from panopto.storage.posts import save_posts
from panopto.collectors.youtube import collect_youtube_posts, normalize_youtube_username

from panopto.post_query import parse_day, query_posts

_DATE_TOKEN_RE = re.compile(
    r"(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4})"
)


class InvalidRequestError(ValueError):
    """Raised when API request input is invalid."""


def _normalize_username(raw: Any) -> str:
    text = str(raw or "").strip()
    text = re.sub(r"^@+", "", text)
    text = re.sub(r"^u/", "", text, flags=re.IGNORECASE)
    return text.strip()


def _normalize_twitter_username(raw: Any) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    match = re.match(r"^https?://(?:www\.)?(?:x|twitter)\.com/([^/?#]+)", text, flags=re.IGNORECASE)
    if match:
        text = unquote(match.group(1))
    text = text.split("/", 1)[0]
    text = re.sub(r"^@+", "", text).strip().lower()
    return text


def _normalize_reddit_username(raw: Any) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    match = re.match(r"^https?://(?:www\.)?reddit\.com/(?:user|u)/([^/?#]+)", text, flags=re.IGNORECASE)
    if match:
        text = unquote(match.group(1))
    text = text.strip().strip("/")
    text = re.sub(r"^u/", "", text, flags=re.IGNORECASE)
    return text.split("/", 1)[0].strip()


def _normalize_tiktok_username(raw: Any) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    match = re.match(r"^https?://(?:www\.)?tiktok\.com/@([^/?#]+)", text, flags=re.IGNORECASE)
    if match:
        text = unquote(match.group(1))
    text = text.split("/", 1)[0]
    text = re.sub(r"^@+", "", text).strip().lower()
    return text


def _normalize_target_username(platform: str, raw: Any) -> str:
    if platform == "twitter":
        return _normalize_twitter_username(raw)
    if platform == "reddit":
        return _normalize_reddit_username(raw)
    if platform == "tiktok":
        return _normalize_tiktok_username(raw)
    if platform == "bluesky":
        return normalize_bluesky_username(raw)
    if platform == "instagram":
        return normalize_instagram_username(raw)
    if platform == "youtube":
        return normalize_youtube_username(raw)
    return _normalize_username(raw)


def parse_targets(payload: dict[str, Any]) -> list[dict[str, str]]:
    username = _normalize_username(payload.get("username", ""))
    fallback_twitter_username = _normalize_twitter_username(payload.get("username", ""))
    targets_raw = payload.get("targets", [])
    platform_aliases = {
        "x": "twitter",
        "twitter/x": "twitter",
        "x.com": "twitter",
    }

    targets: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    if isinstance(targets_raw, list) and targets_raw:
        for item in targets_raw:
            if not isinstance(item, dict):
                continue
            platform = str(item.get("platform", "twitter")).strip().lower()
            platform = platform_aliases.get(platform, platform)
            raw_username = _normalize_target_username(platform, item.get("username", ""))
            if not raw_username or platform not in {"twitter", "reddit", "tiktok", "bluesky", "instagram", "youtube"}:
                continue
            key = (platform, raw_username.lower())
            if key in seen:
                continue
            seen.add(key)
            targets.append({"platform": platform, "username": raw_username})
    elif fallback_twitter_username:
        targets.append({"platform": "twitter", "username": fallback_twitter_username})
    elif username:
        targets.append({"platform": "twitter", "username": username})

    return targets


def collect_for_targets(
    *,
    targets: list[dict[str, str]],
    start_date: str,
    end_date: str,
    db_path: Path,
    fail_on_total_failure: bool = True,
) -> dict[str, Any]:
    if not targets:
        raise InvalidRequestError("at least one target is required")

    start_day = parse_day(start_date)
    end_day = parse_day(end_date)
    if not start_day or not end_day:
        date_tokens = _DATE_TOKEN_RE.findall(f"{start_date} {end_date}")
        parsed_tokens = [parsed for token in date_tokens if (parsed := parse_day(token))]
        if not start_day and parsed_tokens:
            start_day = parsed_tokens[0]
        if not end_day and len(parsed_tokens) >= 2:
            end_day = parsed_tokens[1]
    if not start_day or not end_day:
        raise InvalidRequestError("start_date and end_date must be valid dates (YYYY-MM-DD or MM/DD/YYYY)")
    if end_day < start_day:
        raise InvalidRequestError("end_date must be on/after start_date")

    today = datetime.now(timezone.utc).date()
    lookback_start = min(start_day, today)
    lookback_days = max(1, (today - lookback_start).days + 1)
    collection_window = f"{lookback_days} days"
    max_pages = 5 if lookback_days <= 14 else 8

    def _collect_target(target: dict[str, str]) -> tuple[dict[str, str], list[dict[str, Any]]]:
        platform = target["platform"]
        handle = target["username"]

        if platform == "twitter":
            posts = collect_twitter_posts(
                username=handle,
                collection_window=collection_window,
                max_pages=max_pages,
                request_delay_seconds=0.8,
                timeout=30,
                browser_fallback=True,
                browser_enrich_existing=True,
            )
            for post in posts:
                post["platform"] = "Twitter"
            return target, posts

        if platform == "tiktok":
            posts = collect_tiktok_posts(
                username=handle,
                collection_window=collection_window,
                max_pages=max_pages,
                request_delay_seconds=0.8,
                timeout=45,
                browser_fallback=True,
            )
            for post in posts:
                post["platform"] = "TikTok"
            return target, posts

        if platform == "bluesky":
            posts = collect_bluesky_posts(
                username=handle,
                collection_window=collection_window,
                max_pages=max_pages,
                request_delay_seconds=0.8,
                timeout=30,
            )
            for post in posts:
                post["platform"] = "Bluesky"
            return target, posts

        if platform == "instagram":
            posts = collect_instagram_posts(
                username=handle,
                collection_window=collection_window,
                max_pages=max_pages,
                request_delay_seconds=0.8,
                timeout=30,
                browser_fallback=True,
            )
            for post in posts:
                post["platform"] = "Instagram"
            return target, posts

        if platform == "youtube":
            posts = collect_youtube_posts(
                username=handle,
                collection_window=collection_window,
                max_pages=1,
                request_delay_seconds=0.0,
                timeout=30,
            )
            for post in posts:
                post["platform"] = "YouTube"
            return target, posts

        posts = collect_reddit_posts(
            username=handle,
            collection_window=collection_window,
            max_pages=4 if lookback_days <= 14 else 6,
            request_delay_seconds=1.0,
            timeout=30,
        )
        return target, posts

    posts: list[dict[str, Any]] = []
    per_target: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(4, len(targets))) as executor:
        futures = {executor.submit(_collect_target, target): target for target in targets}
        for future in as_completed(futures):
            target = futures[future]
            try:
                target, collected_posts = future.result()
                posts.extend(collected_posts)
                per_target.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "status": "ok",
                        "collected": len(collected_posts),
                    }
                )
            except UsernameNotFoundError:
                per_target.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "status": "username_not_found",
                        "collected": 0,
                    }
                )
                failures.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "code": "username_not_found",
                        "message": f"{target['platform']} username '{target['username']}' not found",
                    }
                )
            except SourceAccessBlockedError as exc:
                per_target.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "status": "blocked",
                        "collected": 0,
                    }
                )
                failures.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "code": "blocked_by_protection",
                        "message": str(exc),
                    }
                )
            except Exception as exc:
                per_target.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "status": "error",
                        "collected": 0,
                    }
                )
                failures.append(
                    {
                        "platform": target["platform"],
                        "username": target["username"],
                        "code": "collection_error",
                        "message": str(exc),
                    }
                )

    if not posts and failures and fail_on_total_failure:
        first = failures[0]
        if first["code"] == "username_not_found":
            raise UsernameNotFoundError(platform=str(first["platform"]), username=str(first["username"]))
        raise InvalidRequestError(f"collection failed: {first['message']}")

    inserted = save_posts(posts, db_path=str(db_path))
    theme_result = tag_posts_with_bertopic(db_path=str(db_path))
    payload = query_posts(
        query="",
        sort_order="newest",
        db_path=db_path,
        start_date=start_date,
        end_date=end_date,
        include_tags={target["platform"] for target in targets},
    )

    return {
        "collected": len(posts),
        "inserted": inserted,
        "count": payload["count"],
        "posts": payload["posts"],
        "themes": payload.get("themes", []),
        "targets": targets,
        "per_target": per_target,
        "errors": failures,
        "start_date": start_date,
        "end_date": end_date,
        "theme_tagging": theme_result,
    }
