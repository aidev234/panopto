from panopto.collection_service import parse_targets


def test_parse_targets_normalizes_and_deduplicates():
    payload = {
        "targets": [
            {"platform": "twitter", "username": "@sama"},
            {"platform": "twitter", "username": "sama"},
            {"platform": "twitter", "username": "https://x.com/sama/status/123"},
            {"platform": "reddit", "username": "u/Cautious_Dirt8409"},
            {"platform": "reddit", "username": "Cautious_Dirt8409"},
            {"platform": "reddit", "username": "https://www.reddit.com/user/Cautious_Dirt8409/"},
            {"platform": "tiktok", "username": "@aoc"},
            {"platform": "tiktok", "username": "aoc"},
            {"platform": "tiktok", "username": "https://www.tiktok.com/@aoc"},
            {"platform": "x", "username": "@sama"},
            {"platform": "bluesky", "username": "https://bsky.app/profile/aoc.bsky.social"},
            {"platform": "bluesky", "username": "aoc"},
            {"platform": "instagram", "username": "https://www.instagram.com/AOC/"},
            {"platform": "instagram", "username": "@AOC"},
            {"platform": "youtube", "username": "https://www.youtube.com/@AOC/videos"},
            {"platform": "youtube", "username": "@AOC"},
        ]
    }

    targets = parse_targets(payload)

    assert targets == [
        {"platform": "twitter", "username": "sama"},
        {"platform": "reddit", "username": "Cautious_Dirt8409"},
        {"platform": "tiktok", "username": "aoc"},
        {"platform": "bluesky", "username": "aoc"},
        {"platform": "instagram", "username": "AOC"},
        {"platform": "youtube", "username": "AOC"},
    ]


def test_parse_targets_fallback_username_normalizes_twitter_url():
    payload = {"username": "https://x.com/Sama/status/12345"}

    targets = parse_targets(payload)

    assert targets == [{"platform": "twitter", "username": "sama"}]
