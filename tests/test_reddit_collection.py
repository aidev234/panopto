from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import reddit_collection
from panopto.errors import UsernameNotFoundError


class _FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        raise RuntimeError(f"status {self.status_code}")


def test_collect_reddit_posts_includes_submitted_and_comments():
    now = datetime.now(timezone.utc)
    submitted = {
        "data": {
            "after": None,
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "name": "t3_abc",
                        "created_utc": now.timestamp(),
                        "title": "Launch update",
                        "selftext": "We shipped a new build",
                        "num_comments": 12,
                        "score": 42,
                        "subreddit": "test",
                        "permalink": "/r/test/comments/abc/launch_update/",
                    },
                }
            ],
        }
    }
    comments = {
        "data": {
            "after": None,
            "children": [
                {
                    "kind": "t1",
                    "data": {
                        "name": "t1_def",
                        "created_utc": now.timestamp(),
                        "body": "Nice work",
                        "score": 7,
                        "subreddit": "test",
                        "link_author": "some_author",
                        "permalink": "/r/test/comments/abc/launch_update/def/",
                    },
                }
            ],
        }
    }

    with patch("reddit_collection._iter_listing", side_effect=[submitted["data"]["children"], comments["data"]["children"]]):
        rows = reddit_collection.collect_reddit_posts("Cautious_Dirt8409", "7 days", request_delay_seconds=0)

    assert len(rows) == 2
    assert {row["post_type"] for row in rows} == {"post", "comment"}
    assert all(row["platform"] == "Reddit" for row in rows)


def test_collect_reddit_posts_respects_window():
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=20)
    payload = {
        "data": {
            "after": None,
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "name": "t3_old",
                        "created_utc": old.timestamp(),
                        "title": "Old post",
                        "selftext": "",
                        "num_comments": 0,
                        "score": 1,
                        "subreddit": "test",
                        "permalink": "/r/test/comments/old/old/",
                    },
                }
            ],
        }
    }
    with patch("reddit_collection._iter_listing", side_effect=[payload["data"]["children"], []]):
        rows = reddit_collection.collect_reddit_posts("Cautious_Dirt8409", "7 days", request_delay_seconds=0)
    assert rows == []


def test_retrying_get_raises_username_not_found_on_404():
    class _FakeSession:
        def get(self, url, params=None, timeout=20):
            return _FakeResponse(payload={}, status_code=404)

    try:
        reddit_collection._retrying_get(
            _FakeSession(),
            "https://www.reddit.com/user/missing/submitted/.json",
            params={},
            timeout=20,
            username="missing",
        )
    except UsernameNotFoundError as exc:
        assert exc.platform == "reddit"
        assert exc.username == "missing"
        return

    raise AssertionError("Expected UsernameNotFoundError for 404 response")


def test_collect_reddit_posts_extracts_media_metadata():
    now = datetime.now(timezone.utc)
    submitted = {
        "data": {
            "after": None,
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "name": "t3_media",
                        "created_utc": now.timestamp(),
                        "title": "Post with media",
                        "selftext": "",
                        "num_comments": 3,
                        "score": 21,
                        "subreddit": "test",
                        "permalink": "/r/test/comments/media/post_with_media/",
                        "preview": {
                            "images": [
                                {
                                    "source": {"url": "https://preview.redd.it/sample-image.jpg?width=1080&amp;format=pjpg&amp;auto=webp"},
                                }
                            ]
                        },
                        "secure_media": {
                            "reddit_video": {
                                "fallback_url": "https://v.redd.it/abc123/DASH_720.mp4"
                            }
                        },
                        "thumbnail": "https://preview.redd.it/thumb.jpg",
                    },
                }
            ],
        }
    }

    with patch("reddit_collection._iter_listing", side_effect=[submitted["data"]["children"], []]):
        rows = reddit_collection.collect_reddit_posts("example_user", "7 days", request_delay_seconds=0)

    assert len(rows) == 1
    metadata = rows[0]["metadata"]
    assert metadata["video_url"] == "https://v.redd.it/abc123/DASH_720.mp4"
    assert "https://preview.redd.it/sample-image.jpg?width=1080&format=pjpg&auto=webp" in metadata["image_urls"]
    assert metadata["thumbnail_url"].startswith("https://preview.redd.it/")
    assert len(metadata["media"]) >= 2
