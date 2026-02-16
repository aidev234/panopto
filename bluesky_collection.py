"""Bluesky collection helpers for local OSINT workflows."""

from __future__ import annotations

import random
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import unquote

import requests

from panopto.errors import UsernameNotFoundError

DEFAULT_HEADERS = {
    "User-Agent": "panopto-osint-collector/1.0 (+local; respectful-rate-limit)",
    "Accept": "application/json",
}

_PROFILE_URL_RE = re.compile(r"^https?://(?:www\.)?bsky\.app/profile/([^/?#]+)", re.IGNORECASE)


def _parse_collection_window(collection_window: str) -> timedelta:
    value = collection_window.strip().lower()
    units = {
        "week": 7,
        "weeks": 7,
        "w": 7,
        "day": 1,
        "days": 1,
        "d": 1,
        "hour": 1 / 24,
        "hours": 1 / 24,
        "h": 1 / 24,
    }
    amount = int(value.split()[0]) if value and value.split()[0].isdigit() else None
    unit = value.split()[1] if len(value.split()) > 1 else value[-1:] if amount is not None else ""
    if amount is None or unit not in units:
        raise ValueError("Unsupported collection_window format. Use e.g. '1 week' or '7 days'.")
    return timedelta(days=amount * units[unit])


def normalize_bluesky_username(raw: Any) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""

    match = _PROFILE_URL_RE.match(text)
    if match:
        text = unquote(match.group(1))

    text = re.sub(r"^@+", "", text).strip()
    if text.lower().startswith("did:"):
        return text
    text = text.lower()
    if text.endswith(".bsky.social"):
        text = text[: -len(".bsky.social")]
    return text.strip()


def _actor_for_api(username: str) -> str:
    lowered = username.lower()
    if lowered.startswith("did:"):
        return username
    if "." in username:
        return lowered
    return f"{lowered}.bsky.social"


def _parse_timestamp(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    try:
        parsed = datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _source_url(author_handle: str | None, uri: str | None) -> str | None:
    if not author_handle or not uri:
        return None
    if not uri.startswith("at://"):
        return None
    rkey = uri.rsplit("/", 1)[-1].strip()
    if not rkey:
        return None
    return f"https://bsky.app/profile/{author_handle}/post/{rkey}"


def collect_bluesky_posts(
    username: str,
    collection_window: str,
    *,
    max_pages: int = 4,
    request_delay_seconds: float = 1.0,
    timeout: int = 20,
    proxies: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Collect Bluesky profile feed posts for a user."""
    normalized_username = normalize_bluesky_username(username)
    if not normalized_username:
        raise ValueError("username must be a non-empty string")

    cutoff = datetime.now(timezone.utc) - _parse_collection_window(collection_window)
    actor = _actor_for_api(normalized_username)
    rows: list[dict[str, Any]] = []

    with requests.Session() as session:
        session.headers.update(DEFAULT_HEADERS)
        if proxies:
            session.proxies.update(proxies)

        profile_response = session.get(
            "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile",
            params={"actor": actor},
            timeout=timeout,
        )
        if profile_response.status_code in {400, 404}:
            raise UsernameNotFoundError(platform="bluesky", username=normalized_username)
        profile_response.raise_for_status()
        profile = profile_response.json() if profile_response.content else {}
        actor_ref = str(profile.get("did") or actor).strip() or actor

        cursor: str | None = None
        for page in range(max_pages):
            params: dict[str, Any] = {"actor": actor_ref, "limit": 100}
            if cursor:
                params["cursor"] = cursor

            response = session.get(
                "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed",
                params=params,
                timeout=timeout,
            )
            if response.status_code in {400, 404}:
                raise UsernameNotFoundError(platform="bluesky", username=normalized_username)
            response.raise_for_status()
            payload = response.json() if response.content else {}

            feed = payload.get("feed") if isinstance(payload, dict) else None
            if not isinstance(feed, list) or not feed:
                break

            for item in feed:
                if not isinstance(item, dict):
                    continue
                post = item.get("post") if isinstance(item.get("post"), dict) else {}
                record = post.get("record") if isinstance(post.get("record"), dict) else {}
                created_at = _parse_timestamp(
                    str(record.get("createdAt") or post.get("indexedAt") or "").strip()
                )
                if created_at and created_at < cutoff:
                    continue

                author = post.get("author") if isinstance(post.get("author"), dict) else {}
                author_handle = str(author.get("handle") or "").strip()
                reason = item.get("reason") if isinstance(item.get("reason"), dict) else {}
                reason_type = str(reason.get("$type") or "").lower()

                post_type = "post"
                if "reasonrepost" in reason_type:
                    post_type = "repost"
                elif isinstance(record.get("reply"), dict):
                    post_type = "reply"
                elif isinstance(record.get("embed"), dict):
                    embed_type = str(record["embed"].get("$type") or "").lower()
                    if "embed.record" in embed_type:
                        post_type = "quote"

                uri = str(post.get("uri") or "").strip()
                post_id = uri.rsplit("/", 1)[-1] if uri else None
                content = str(record.get("text") or "").strip()
                if not content:
                    content = "(no text content)"
                timestamp = created_at.isoformat() if created_at else None
                source_url = _source_url(author_handle, uri)

                replies = post.get("replyCount")
                reposts = post.get("repostCount")
                likes = post.get("likeCount")
                quote_count = post.get("quoteCount")

                rows.append(
                    {
                        "post_id": post_id,
                        "platform": "Bluesky",
                        "username": normalized_username,
                        "content": content,
                        "timestamp": timestamp,
                        "likes": int(likes) if isinstance(likes, int) else None,
                        "retweets": int(reposts) if isinstance(reposts, int) else None,
                        "replies": int(replies) if isinstance(replies, int) else None,
                        "source_url": source_url,
                        "post_type": post_type,
                        "referenced_username": normalize_bluesky_username(author_handle)
                        if post_type in {"repost", "quote"}
                        else None,
                        "metadata": {
                            "uri": uri,
                            "author_handle": author_handle,
                            "quote_count": int(quote_count) if isinstance(quote_count, int) else None,
                            "viewer_reason": reason_type or None,
                        },
                    }
                )

            cursor = payload.get("cursor") if isinstance(payload, dict) else None
            if not cursor:
                break
            if request_delay_seconds > 0 and page + 1 < max_pages:
                time.sleep(request_delay_seconds + random.uniform(0.0, 0.35))

    deduped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (
            "id" if row.get("post_id") else "body",
            row.get("post_id") or f"{row.get('timestamp') or ''}|{row.get('content') or ''}",
        )
        existing = deduped.get(key)
        if existing is None or len(str(row.get("content") or "")) > len(str(existing.get("content") or "")):
            deduped[key] = row

    results = list(deduped.values())
    results.sort(key=lambda post: post.get("timestamp") or "", reverse=True)
    return results
