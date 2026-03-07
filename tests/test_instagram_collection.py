from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from panopto.collectors.apify import ApifyActorInputError
from panopto.collectors.instagram import collect_instagram_posts, normalize_instagram_username
from panopto.errors import SourceUnavailableError


def test_normalize_instagram_username():
    assert normalize_instagram_username("@aoc") == "aoc"
    assert normalize_instagram_username("https://www.instagram.com/AOC/") == "AOC"


def test_collect_instagram_posts_filters_window_and_dedupes():
    now = datetime.now(timezone.utc)
    recent_iso = (now - timedelta(days=1)).isoformat()
    old_iso = (now - timedelta(days=50)).isoformat()
    dataset = [
        {
            "shortCode": "r1",
            "url": "https://www.instagram.com/p/r1/",
            "caption": "Recent IG",
            "timestamp": recent_iso,
            "ownerUsername": "aoc",
        },
        {
            "shortCode": "r1",
            "url": "https://www.instagram.com/p/r1/",
            "caption": "Recent IG with more detail",
            "timestamp": recent_iso,
            "ownerUsername": "aoc",
        },
        {
            "shortCode": "o1",
            "url": "https://www.instagram.com/p/o1/",
            "caption": "Old IG",
            "timestamp": old_iso,
            "ownerUsername": "aoc",
        },
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "14 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] == "r1"
    assert rows[0]["content"] == "Recent IG with more detail"


def test_collect_instagram_posts_falls_back_to_direct_urls_input():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "shortCode": "abc123",
            "caption": "Fallback input path works",
            "timestamp": now.isoformat(),
            "url": "https://www.instagram.com/p/abc123/",
        }
    ]
    with patch(
        "panopto.collectors.instagram.run_actor_sync_get_items",
        side_effect=[
            ApifyActorInputError("usernames not allowed"),
            dataset,
        ],
    ) as run_mock:
        rows = collect_instagram_posts("aoc", "14 days", timeout=12)

    assert len(rows) == 1
    assert rows[0]["post_id"] == "abc123"
    assert run_mock.call_count == 2
    first_payload = run_mock.call_args_list[0].kwargs["actor_input"]
    second_payload = run_mock.call_args_list[1].kwargs["actor_input"]
    assert "username" in first_payload
    assert "directUrls" in second_payload


def test_collect_instagram_posts_raises_unavailable_when_actor_input_rejected():
    with patch(
        "panopto.collectors.instagram.run_actor_sync_get_items",
        side_effect=ApifyActorInputError("bad schema"),
    ):
        try:
            collect_instagram_posts("aoc", "30 days")
        except SourceUnavailableError as exc:
            assert exc.platform == "instagram"
            assert exc.username == "aoc"
            assert "input rejected" in exc.reason
        else:
            raise AssertionError("Expected SourceUnavailableError for rejected actor input")


def test_collect_instagram_posts_maps_latest_posts_shape():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "username": "aoc",
            "latestPosts": [
                {
                    "shortCode": "nested1",
                    "caption": "nested row",
                    "timestamp": now.isoformat(),
                    "displayUrl": "https://cdn.example.com/1.jpg",
                }
            ],
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "14 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] == "nested1"
    assert rows[0]["source_url"] == "https://www.instagram.com/p/nested1/"
    assert rows[0]["metadata"]["image_urls"] == ["https://cdn.example.com/1.jpg"]


def test_collect_instagram_posts_retries_when_first_input_returns_empty():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "shortCode": "abc999",
            "caption": "Returned on fallback input",
            "timestamp": now.isoformat(),
            "url": "https://www.instagram.com/p/abc999/",
        }
    ]
    with patch(
        "panopto.collectors.instagram.run_actor_sync_get_items",
        side_effect=[[], dataset],
    ) as run_mock:
        rows = collect_instagram_posts("aoc", "14 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] == "abc999"
    assert run_mock.call_count == 2


def test_collect_instagram_posts_skips_posts_not_owned_by_target_when_tagged():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "id": "3829044966723868326",
            "shortCode": "DUjgBwuktam",
            "caption": "sample caption",
            "url": "https://www.instagram.com/p/DUjgBwuktam/",
            "displayUrl": "https://cdn.example.com/post.jpg",
            "videoUrl": "https://cdn.example.com/post.mp4",
            "timestamp": now.isoformat(),
            "ownerUsername": "uaw.union",
            "taggedUsers": [
                {
                    "username": "aoc",
                    "profile_pic_url": "https://cdn.example.com/aoc.jpg",
                }
            ],
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "30 days")

    assert rows == []


def test_collect_instagram_posts_uses_owner_profile_pic_and_primary_image_only():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "id": "3829044966723868326",
            "shortCode": "DUjgBwuktam",
            "caption": "sample caption",
            "url": "https://www.instagram.com/p/DUjgBwuktam/",
            "displayUrl": "https://cdn.example.com/post-1.jpg",
            "images": ["https://cdn.example.com/post-2.jpg", "https://cdn.example.com/post-3.jpg"],
            "timestamp": now.isoformat(),
            "ownerUsername": "aoc",
            "ownerProfilePicUrl": "https://cdn.example.com/aoc-owner.jpg",
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "30 days")

    assert len(rows) == 1
    assert rows[0]["content"] == "sample caption"
    assert rows[0]["source_url"] == "https://www.instagram.com/p/DUjgBwuktam/"
    assert rows[0]["metadata"]["profile_image_url"] == "https://cdn.example.com/aoc-owner.jpg"
    assert rows[0]["metadata"]["image_urls"] == ["https://cdn.example.com/post-1.jpg"]


def test_collect_instagram_posts_does_not_build_shortcode_from_numeric_id():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "id": "3829044966723868326",
            "caption": "numeric id only",
            "timestamp": now.isoformat(),
            "ownerUsername": "aoc",
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "30 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] is None
    assert rows[0]["source_url"] == "https://www.instagram.com/aoc/"


def test_collect_instagram_posts_supports_caption_object_shape():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "shortCode": "objcap1",
            "caption": {"text": "caption from object"},
            "timestamp": now.isoformat(),
            "url": "https://www.instagram.com/p/objcap1/",
            "ownerUsername": "aoc",
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "30 days")

    assert len(rows) == 1
    assert rows[0]["content"] == "caption from object"


def test_collect_instagram_posts_ignores_profile_only_item_and_uses_fallback_posts():
    now = datetime.now(timezone.utc)
    profile_only = [
        {
            "username": "aoc",
            "fullName": "Alexandria Ocasio-Cortez",
            "url": "https://www.instagram.com/aoc/",
        }
    ]
    dataset = [
        {
            "shortCode": "realpost1",
            "caption": "real post from fallback input",
            "timestamp": now.isoformat(),
            "url": "https://www.instagram.com/p/realpost1/",
            "displayUrl": "https://cdn.example.com/realpost1.jpg",
            "ownerUsername": "aoc",
        }
    ]
    with patch(
        "panopto.collectors.instagram.run_actor_sync_get_items",
        side_effect=[profile_only, dataset],
    ) as run_mock:
        rows = collect_instagram_posts("aoc", "14 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] == "realpost1"
    assert rows[0]["content"] == "real post from fallback input"
    assert rows[0]["source_url"] == "https://www.instagram.com/p/realpost1/"
    assert run_mock.call_count == 2


def test_collect_instagram_posts_supports_nested_items_shape():
    now = datetime.now(timezone.utc)
    dataset = [
        {
            "items": [
                {
                    "shortCode": "nestedshape1",
                    "captionText": "nested list payload",
                    "created_time": int(now.timestamp()),
                    "url": "https://www.instagram.com/p/nestedshape1/",
                    "ownerUsername": "aoc",
                }
            ]
        }
    ]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        rows = collect_instagram_posts("aoc", "30 days")

    assert len(rows) == 1
    assert rows[0]["post_id"] == "nestedshape1"
    assert rows[0]["content"] == "nested list payload"


def test_collect_instagram_posts_raises_unavailable_on_actor_error_items():
    dataset = [{"error": "profile_not_found", "errorDescription": "username missing"}]
    with patch("panopto.collectors.instagram.run_actor_sync_get_items", return_value=dataset):
        try:
            collect_instagram_posts("aoc", "30 days")
        except SourceUnavailableError as exc:
            assert exc.platform == "instagram"
            assert "profile_not_found" in str(exc)
        else:
            assert False, "expected SourceUnavailableError"
