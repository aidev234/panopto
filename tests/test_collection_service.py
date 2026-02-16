from panopto.collection_service import parse_targets


def test_parse_targets_normalizes_and_deduplicates():
    payload = {
        "targets": [
            {"platform": "twitter", "username": "@sama"},
            {"platform": "twitter", "username": "sama"},
            {"platform": "reddit", "username": "u/Cautious_Dirt8409"},
            {"platform": "reddit", "username": "Cautious_Dirt8409"},
            {"platform": "tiktok", "username": "@aoc"},
            {"platform": "tiktok", "username": "aoc"},
            {"platform": "bluesky", "username": "https://bsky.app/profile/aoc.bsky.social"},
            {"platform": "bluesky", "username": "aoc"},
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
        {"platform": "youtube", "username": "AOC"},
    ]
