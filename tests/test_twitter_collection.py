import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import twitter_collection


HAS_HTML_DEPS = (
    twitter_collection.requests is not None
    and twitter_collection.BeautifulSoup is not None
)


class TestTwitterCollection(unittest.TestCase):
    @unittest.skipUnless(HAS_HTML_DEPS, "requires requests and beautifulsoup4")
    def test_extract_posts_from_html_parses_content_timestamp_and_stats(self):
        html = """
        <article data-tweet-id="1">
            <div class="tweet-text">Hello from OSINT</div>
            <time datetime="2026-01-01T12:00:00Z">Jan 01, 2026</time>
            <div>12 Likes 7 Retweets 3 Replies</div>
        </article>
        """

        posts = twitter_collection._extract_posts_from_html("sama", html)

        self.assertEqual(len(posts), 1)
        post = posts[0]
        self.assertEqual(post.content, "Hello from OSINT")
        self.assertEqual(post.likes, 12)
        self.assertEqual(post.retweets, 7)
        self.assertEqual(post.replies, 3)
        self.assertEqual(post.post_id, "1")
        self.assertEqual(post.timestamp, datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc))

    @unittest.skipUnless(HAS_HTML_DEPS, "requires requests and beautifulsoup4")
    def test_collect_filters_window_and_deduplicates(self):
        now = datetime.now(timezone.utc)
        recent_iso = (now - timedelta(days=1)).isoformat()
        old_iso = (now - timedelta(days=20)).isoformat()

        html = f"""
        <article data-tweet-id="x1">
            <div class="tweet-text">Recent post</div>
            <time datetime="{recent_iso}"></time>
        </article>
        <article data-tweet-id="x1">
            <div class="tweet-text">Recent post</div>
            <time datetime="{recent_iso}"></time>
        </article>
        <article data-tweet-id="x2">
            <div class="tweet-text">Old post</div>
            <time datetime="{old_iso}"></time>
        </article>
        """

        with patch("twitter_collection._iter_pages", return_value=[html]):
            results = twitter_collection.collect_twitter_posts(
                "@sama",
                "1 week",
                request_delay_seconds=0,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Recent post")
        self.assertEqual(results[0]["username"], "sama")

    def test_collection_window_validation(self):
        if not HAS_HTML_DEPS:
            self.skipTest("requires requests and beautifulsoup4")
        with self.assertRaises(ValueError):
            twitter_collection.collect_twitter_posts("sama", "yesterday")


if __name__ == "__main__":
    unittest.main()
