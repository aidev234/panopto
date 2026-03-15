import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from panopto.errors import SourceUnavailableError
import panopto.collectors.twitter as twitter_collection


class TestTwitterCollection(unittest.TestCase):
    def test_collect_filters_window_and_deduplicates(self):
        now = datetime.now(timezone.utc)
        rows = [
            twitter_collection.TwitterPost(
                post_id="x1",
                username="sama",
                content="Recent post",
                timestamp=now - timedelta(days=1),
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/x1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
            twitter_collection.TwitterPost(
                post_id="x1",
                username="sama",
                content="Recent post",
                timestamp=now - timedelta(days=1),
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/x1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
            twitter_collection.TwitterPost(
                post_id="x2",
                username="sama",
                content="Old post",
                timestamp=now - timedelta(days=20),
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/x2",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
        ]

        with patch("panopto.collectors.twitter._collect_from_apify", return_value=rows):
            results = twitter_collection.collect_twitter_posts("@sama", "1 week", request_delay_seconds=0)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Recent post")
        self.assertEqual(results[0]["username"], "sama")

    def test_extract_metric_supports_compact_suffix(self):
        self.assertEqual(twitter_collection._extract_metric("1.2K likes", ["likes"]), 1200)
        self.assertEqual(twitter_collection._extract_metric("3M retweets", ["retweets"]), 3000000)
        self.assertIsNone(twitter_collection._extract_metric("likes: .", ["likes"]))

    def test_build_apify_search_terms_includes_profile_and_date_ranges(self):
        cutoff = datetime(2024, 1, 1, tzinfo=timezone.utc)
        now = datetime(2024, 12, 15, tzinfo=timezone.utc)

        terms = twitter_collection._build_apify_search_terms(
            username="NASA",
            cutoff=cutoff,
            now_utc=now,
        )

        self.assertGreaterEqual(len(terms), 2)
        self.assertEqual(terms[0], "from:nasa")
        self.assertIn("from:nasa since:2024-01-01 until:2024-06-29", terms)

    def test_collect_uses_apify_rows(self):
        apify_post = twitter_collection.TwitterPost(
            post_id="1728108619189874825",
            username="aoc",
            content="More than 10 per human on average",
            timestamp=datetime(2026, 2, 10, 12, 0, 0, tzinfo=timezone.utc),
            likes=104121,
            retweets=11311,
            replies=6526,
            source_url="https://x.com/aoc/status/1728108619189874825",
            post_type="post",
            referenced_username=None,
            raw_metadata={
                "profile_image_url": "https://pbs.twimg.com/profile_images/example.jpg",
                "source": "Twitter for Android",
            },
        )

        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[apify_post]):
            results = twitter_collection.collect_twitter_posts(
                "AOC",
                "30 days",
                request_delay_seconds=0,
                now_utc=datetime(2026, 3, 12, tzinfo=timezone.utc),
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["post_id"], "1728108619189874825")
        self.assertEqual(results[0]["username"], "aoc")
        self.assertEqual(results[0]["metadata"]["profile_image_url"], "https://pbs.twimg.com/profile_images/example.jpg")

    def test_apify_item_to_post_maps_tweet_scraper_schema(self):
        record = {
            "type": "tweet",
            "id": "1728108619189874825",
            "url": "https://x.com/elonmusk/status/1728108619189874825",
            "text": "More than 10 per human on average",
            "retweetCount": 11311,
            "replyCount": 6526,
            "likeCount": 104121,
            "quoteCount": 2915,
            "createdAt": "Fri Nov 24 17:49:36 +0000 2023",
            "lang": "en",
            "isReply": False,
            "isRetweet": False,
            "isQuote": True,
            "author": {
                "userName": "elonmusk",
                "profilePicture": "https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_normal.jpg",
            },
            "photos": [{"url": "https://pbs.twimg.com/media/abc123.jpg"}],
            "videoUrl": "https://video.twimg.com/ext_tw_video/123/pu/vid/1280x720/a.mp4",
            "quotedTweet": {
                "id": "1728108619000000000",
                "text": "Quoted payload text",
                "author": {"userName": "nasa"},
            },
        }

        post = twitter_collection._apify_item_to_post(record, fallback_username="aoc")

        self.assertIsNotNone(post)
        assert post is not None
        self.assertEqual(post.post_id, "1728108619189874825")
        self.assertEqual(post.username, "elonmusk")
        self.assertEqual(post.post_type, "quote")
        self.assertEqual(post.likes, 104121)
        self.assertEqual(post.retweets, 11311)
        self.assertEqual(post.replies, 6526)
        self.assertEqual(post.referenced_username, "nasa")
        self.assertEqual(post.raw_metadata.get("quote_text"), "Quoted payload text")
        self.assertEqual(post.raw_metadata.get("quote_url"), "https://x.com/nasa/status/1728108619000000000")
        self.assertIn("https://pbs.twimg.com/media/abc123.jpg", post.raw_metadata.get("image_urls", []))
        self.assertTrue(str(post.raw_metadata.get("video_url") or "").startswith("https://video.twimg.com/"))

    def test_collect_twitter_posts_includes_quote_nest_fields_for_ui(self):
        now = datetime.now(timezone.utc)
        post = twitter_collection.TwitterPost(
            post_id="1700000000000000000",
            username="aoc",
            content="Commentary on quoted post",
            timestamp=now,
            likes=12,
            retweets=2,
            replies=1,
            source_url="https://x.com/aoc/status/1700000000000000000",
            post_type="quote",
            referenced_username="nasa",
            raw_metadata={
                "quote_text": "Quoted content body",
                "quote_url": "https://x.com/nasa/status/1699999999999999999",
                "media": [{"type": "image", "url": "https://pbs.twimg.com/media/xyz.jpg"}],
            },
        )
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[post]):
            rows = twitter_collection.collect_twitter_posts("aoc", "30 days", request_delay_seconds=0)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["post_type"], "quote")
        self.assertEqual(rows[0]["referenced_username"], "nasa")
        self.assertEqual(rows[0]["metadata"].get("quote_text"), "Quoted content body")
        self.assertEqual(rows[0]["metadata"].get("quote_url"), "https://x.com/nasa/status/1699999999999999999")

    def test_parse_datetime_accepts_unix_epoch_values(self):
        parsed = twitter_collection._parse_datetime(1769451494)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed.tzinfo, timezone.utc)
        self.assertEqual(parsed.year, 2026)

    def test_collect_from_apify_supports_nested_tweets_records(self):
        dataset = [
            {
                "tweets": [
                    {
                        "id": "123456",
                        "text": "Nested tweet payload",
                        "createdAt": 1769451494,
                        "author": {"userName": "aoc"},
                    }
                ]
            }
        ]
        with patch("panopto.collectors.twitter.run_actor_sync_get_items", return_value=dataset):
            rows = twitter_collection._collect_from_apify(
                normalized_username="aoc",
                cutoff=datetime(2025, 1, 1, tzinfo=timezone.utc),
                now_utc=datetime(2026, 3, 1, tzinfo=timezone.utc),
                timeout=20,
                max_pages=2,
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].post_id, "123456")
        self.assertEqual(rows[0].username, "aoc")

    def test_collect_excludes_reposts(self):
        now = datetime.now(timezone.utc)
        rows = [
            twitter_collection.TwitterPost(
                post_id="a1",
                username="sama",
                content="Normal post",
                timestamp=now,
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/a1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
            twitter_collection.TwitterPost(
                post_id="a2",
                username="sama",
                content="Repost post",
                timestamp=now,
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/a2",
                post_type="repost",
                referenced_username=None,
                raw_metadata={},
            ),
        ]
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=rows):
            results = twitter_collection.collect_twitter_posts("sama", "7 days", request_delay_seconds=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["post_id"], "a1")

    def test_collect_returns_empty_when_apify_returns_empty(self):
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[]):
            results = twitter_collection.collect_twitter_posts("sama", "30 days", request_delay_seconds=0)
        self.assertEqual(results, [])

    def test_dedupes_by_post_id_preferring_richer_content(self):
        now = datetime.now(timezone.utc)
        rows = [
            twitter_collection.TwitterPost(
                post_id="dup1",
                username="sama",
                content="Short",
                timestamp=now,
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/dup1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
            twitter_collection.TwitterPost(
                post_id="dup1",
                username="sama",
                content="Much longer canonical tweet content",
                timestamp=now,
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/dup1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
        ]
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=rows):
            results = twitter_collection.collect_twitter_posts("sama", "30 days", request_delay_seconds=0)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Much longer canonical tweet content")
        self.assertEqual(results[0]["post_type"], "post")

    def test_collection_window_validation(self):
        with self.assertRaises(ValueError):
            twitter_collection.collect_twitter_posts("sama", "yesterday")

    def test_collect_returns_empty_for_unknown_user_when_apify_empty(self):
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[]):
            results = twitter_collection.collect_twitter_posts("missing_user", "7 days", request_delay_seconds=0)
        self.assertEqual(results, [])

    def test_collect_surfaces_apify_errors(self):
        with patch(
            "panopto.collectors.twitter._collect_from_apify",
            side_effect=twitter_collection.ApifyRequestError("blocked"),
        ):
            with self.assertRaises(SourceUnavailableError):
                twitter_collection.collect_twitter_posts("sama", "30 days", request_delay_seconds=0)


if __name__ == "__main__":
    unittest.main()
