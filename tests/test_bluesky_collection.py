from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import panopto.collectors.bluesky as bluesky_collection
from panopto.errors import UsernameNotFoundError


class _FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.content = b"{}"

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")


class _FakeSession:
    def __init__(self, profile_payload, feed_payloads, profile_status=200):
        self._profile_payload = profile_payload
        self._feed_payloads = list(feed_payloads)
        self._profile_status = profile_status
        self.headers = {}
        self.proxies = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, url, params=None, timeout=20):
        if "app.bsky.actor.getProfile" in url:
            return _FakeResponse(self._profile_payload, status_code=self._profile_status)
        if "app.bsky.feed.getAuthorFeed" in url:
            payload = self._feed_payloads.pop(0) if self._feed_payloads else {"feed": []}
            return _FakeResponse(payload, status_code=200)
        return _FakeResponse({}, status_code=404)


def test_normalize_bluesky_username_accepts_profile_url():
    assert (
        bluesky_collection.normalize_bluesky_username("https://bsky.app/profile/aoc.bsky.social")
        == "aoc"
    )
    assert bluesky_collection.normalize_bluesky_username("@aoc.bsky.social") == "aoc"
    assert bluesky_collection.normalize_bluesky_username("aoc") == "aoc"
    assert bluesky_collection.normalize_bluesky_username("AOC.bsky.social") == "aoc"


def test_collect_bluesky_posts_filters_by_window_and_maps_post_types():
    now = datetime.now(timezone.utc)
    recent = (now - timedelta(days=1)).isoformat()
    old = (now - timedelta(days=20)).isoformat()

    profile = {"did": "did:plc:testdid", "handle": "aoc.bsky.social"}
    feed_payload = {
        "feed": [
            {
                "post": {
                    "uri": "at://did:plc:testdid/app.bsky.feed.post/xyz",
                    "indexedAt": recent,
                    "author": {"handle": "aoc.bsky.social"},
                    "record": {"createdAt": recent, "text": "Main post"},
                    "replyCount": 3,
                    "repostCount": 4,
                    "likeCount": 10,
                    "quoteCount": 1,
                }
            },
            {
                "reason": {"$type": "app.bsky.feed.defs#reasonRepost"},
                "post": {
                    "uri": "at://did:plc:other/app.bsky.feed.post/abc",
                    "indexedAt": recent,
                    "author": {"handle": "other.bsky.social"},
                    "record": {"createdAt": recent, "text": "Other post"},
                    "replyCount": 1,
                    "repostCount": 2,
                    "likeCount": 5,
                    "quoteCount": 0,
                },
            },
            {
                "post": {
                    "uri": "at://did:plc:testdid/app.bsky.feed.post/old",
                    "indexedAt": old,
                    "author": {"handle": "aoc.bsky.social"},
                    "record": {"createdAt": old, "text": "Too old"},
                }
            },
        ],
        "cursor": None,
    }

    fake_session = _FakeSession(profile, [feed_payload])
    with patch("panopto.collectors.bluesky.requests.Session", return_value=fake_session):
        rows = bluesky_collection.collect_bluesky_posts(
            "https://bsky.app/profile/aoc.bsky.social",
            "7 days",
            request_delay_seconds=0,
        )

    assert len(rows) == 2
    assert rows[0]["username"] == "aoc"
    assert rows[0]["platform"] == "Bluesky"
    assert rows[0]["source_url"].startswith("https://bsky.app/profile/")
    assert {row["post_type"] for row in rows} == {"post", "repost"}


def test_collect_bluesky_posts_raises_username_not_found_on_404():
    fake_session = _FakeSession(profile_payload={}, feed_payloads=[], profile_status=404)
    with patch("panopto.collectors.bluesky.requests.Session", return_value=fake_session):
        try:
            bluesky_collection.collect_bluesky_posts("missing", "7 days", request_delay_seconds=0)
        except UsernameNotFoundError as exc:
            assert exc.platform == "bluesky"
            assert exc.username == "missing"
            return

    raise AssertionError("Expected UsernameNotFoundError for 404 response")


def test_collect_bluesky_posts_raises_username_not_found_on_400():
    fake_session = _FakeSession(profile_payload={}, feed_payloads=[], profile_status=400)
    with patch("panopto.collectors.bluesky.requests.Session", return_value=fake_session):
        try:
            bluesky_collection.collect_bluesky_posts("AOC.bsky.social", "7 days", request_delay_seconds=0)
        except UsernameNotFoundError as exc:
            assert exc.platform == "bluesky"
            assert exc.username == "aoc"
            return

    raise AssertionError("Expected UsernameNotFoundError for 400 response")
