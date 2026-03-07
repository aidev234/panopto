import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

import requests

from panopto.errors import SourceUnavailableError
import panopto.collectors.twitter as twitter_collection


class TestTwitterCollection(unittest.TestCase):
    def test_source_hosts_prefers_env_override(self):
        with patch.dict("os.environ", {"TWITTER_SOURCE_HOSTS": "xcancel.com, nitter.net"}):
            hosts = twitter_collection._source_hosts()
        self.assertEqual(hosts, ["xcancel.com", "nitter.net"])

    def test_iter_pages_ignores_request_exceptions_and_uses_next_candidate(self):
        html = "<article data-tweet-id='1'><div class='tweet-text'>ok</div></article>"
        session = SimpleNamespace()
        responses = iter(
            [
                requests.ConnectionError("dns fail"),
                SimpleNamespace(status_code=200, text=html),
            ]
        )

        def _fake_get(*_args, **_kwargs):
            value = next(responses, SimpleNamespace(status_code=404, text=""))
            if isinstance(value, Exception):
                raise value
            return value

        session.get = _fake_get
        with patch("panopto.collectors.twitter._source_hosts", return_value=["twitterwebviewer.com"]):
            pages = list(
                twitter_collection._iter_pages(
                    username="sama",
                    session=session,
                    max_pages=1,
                    delay_seconds=0.0,
                    timeout=2,
                    render_proxy_template=None,
                )
            )
        self.assertEqual(len(pages), 1)
        self.assertIn("tweet-text", pages[0])

    def test_iter_pages_raises_source_unavailable_when_all_requests_fail(self):
        session = SimpleNamespace()

        def _always_fail(*_args, **_kwargs):
            raise requests.ConnectionError("dns fail")

        session.get = _always_fail

        with patch("panopto.collectors.twitter._source_hosts", return_value=["twitterwebviewer.com"]):
            with self.assertRaises(SourceUnavailableError):
                list(
                    twitter_collection._iter_pages(
                        username="sama",
                        session=session,
                        max_pages=1,
                        delay_seconds=0.0,
                        timeout=2,
                        render_proxy_template=None,
                    )
                )

    def test_iter_pages_retries_transient_request_failure(self):
        html = "<article data-tweet-id='1'><div class='tweet-text'>ok</div></article>"
        session = SimpleNamespace()
        call_count = {"count": 0}

        def _flaky_get(*_args, **_kwargs):
            call_count["count"] += 1
            if call_count["count"] == 1:
                raise requests.ConnectionError("transient")
            return SimpleNamespace(status_code=200, text=html)

        session.get = _flaky_get

        with (
            patch("panopto.collectors.twitter._source_hosts", return_value=["twitterwebviewer.com"]),
            patch("panopto.collectors.twitter._candidate_page_urls", return_value=["https://twitterwebviewer.com/u/sama"]),
        ):
            pages = list(
                twitter_collection._iter_pages(
                    username="sama",
                    session=session,
                    max_pages=1,
                    delay_seconds=0.0,
                    timeout=2,
                    render_proxy_template=None,
                    request_retries=1,
                    max_workers=1,
                )
            )

        self.assertEqual(len(pages), 1)
        self.assertGreaterEqual(call_count["count"], 2)

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

    def test_extract_from_embedded_data_payload(self):
        html = r"""
        <html><body>
            <script>
                self.__next_f.push([1, "{\\\"full_text\\\":\\\"Embedded hello\\\",\\\"created_at\\\":\\\"2026-01-02T12:00:00Z\\\",\\\"id_str\\\":\\\"42\\\"}"]);
            </script>
        </body></html>
        """

        posts = twitter_collection._extract_posts_from_html("sama", html)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].content, "Embedded hello")
        self.assertEqual(posts[0].post_id, "42")
        self.assertEqual(posts[0].timestamp, datetime(2026, 1, 2, 12, 0, 0, tzinfo=timezone.utc))

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

    def test_collect_prefers_apify_when_actor_returns_rows(self):
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
                browser_fallback=False,
                request_delay_seconds=0,
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

    def test_classifies_repost_and_sets_source_url(self):
        html = """
        <article>
            <div class="tweet-text">Elon Musk reposted Something interesting</div>
            <a href="https://x.com/elonmusk/status/2020000000000000000">Open</a>
            <time datetime="2026-02-10T12:00:00Z"></time>
        </article>
        """

        posts = twitter_collection._extract_posts_from_html("elonmusk", html)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].post_type, "repost")
        self.assertEqual(posts[0].source_url, "https://x.com/elonmusk/status/2020000000000000000")

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

    def test_collect_uses_apify_rows_directly(self):
        now = datetime.now(timezone.utc)
        rows = [
            twitter_collection.TwitterPost(
                post_id="r1",
                username="sama",
                content="Request post",
                timestamp=now,
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/r1",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
            twitter_collection.TwitterPost(
                post_id="b2",
                username="sama",
                content="Loaded more tweet",
                timestamp=now - timedelta(days=1),
                likes=None,
                retweets=None,
                replies=None,
                source_url="https://x.com/sama/status/b2",
                post_type="post",
                referenced_username=None,
                raw_metadata={},
            ),
        ]
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=rows):
            results = twitter_collection.collect_twitter_posts("sama", "30 days", request_delay_seconds=0)
        self.assertEqual(len(results), 2)
        self.assertEqual({post["post_id"] for post in results}, {"r1", "b2"})

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

    def test_multi_status_links_prefers_target_user(self):
        html = """
        <article>
            <div class="tweet-text">Quoted style post</div>
            <a href="https://x.com/other/status/111"></a>
            <a href="https://x.com/sama/status/222"></a>
            <time datetime="2026-02-10T12:00:00Z"></time>
        </article>
        """

        posts = twitter_collection._extract_posts_from_html("sama", html)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].post_id, "222")
        self.assertEqual(posts[0].post_type, "quote")

    def test_collection_window_validation(self):
        with self.assertRaises(ValueError):
            twitter_collection.collect_twitter_posts("sama", "yesterday")

    def test_extracts_media_metadata_from_html(self):
        html = """
        <article data-tweet-id="m1">
            <div class="tweet-text">Media rich tweet</div>
            <video poster="https://pbs.twimg.com/ext_tw_video_thumb/123/pu/img/poster.jpg">
                <source src="https://video.twimg.com/ext_tw_video/123/pu/vid/720x720/clip.mp4" />
            </video>
            <img src="https://pbs.twimg.com/media/abc123.jpg" />
            <time datetime="2026-02-10T12:00:00Z"></time>
        </article>
        """

        posts = twitter_collection._extract_posts_from_html("sama", html)

        self.assertEqual(len(posts), 1)
        metadata = posts[0].raw_metadata
        self.assertEqual(
            metadata.get("video_url"),
            "https://video.twimg.com/ext_tw_video/123/pu/vid/720x720/clip.mp4",
        )
        self.assertIn("https://pbs.twimg.com/media/abc123.jpg", metadata.get("image_urls", []))
        self.assertEqual(
            metadata.get("thumbnail_url"),
            "https://pbs.twimg.com/ext_tw_video_thumb/123/pu/img/poster.jpg",
        )
        self.assertGreaterEqual(len(metadata.get("media", [])), 2)

    def test_collect_returns_empty_for_unknown_user_when_apify_empty(self):
        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[]):
            results = twitter_collection.collect_twitter_posts("missing_user", "7 days", request_delay_seconds=0)
        self.assertEqual(results, [])

    def test_collect_uses_apify_results(self):
        rss_post = twitter_collection.TwitterPost(
            post_id="909090",
            username="sama",
            content="RSS fallback tweet",
            timestamp=datetime(2026, 2, 10, 12, 0, 0, tzinfo=timezone.utc),
            likes=None,
            retweets=None,
            replies=None,
            source_url="https://xcancel.com/sama/status/909090",
            post_type="post",
            referenced_username=None,
            raw_metadata={"raw_timestamp": "Mon, 10 Feb 2026 12:00:00 GMT"},
        )

        with patch("panopto.collectors.twitter._collect_from_apify", return_value=[rss_post]):
            results = twitter_collection.collect_twitter_posts(
                "sama",
                "30 days",
                request_delay_seconds=0,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["post_id"], "909090")
        self.assertEqual(results[0]["content"], "RSS fallback tweet")


if __name__ == "__main__":
    unittest.main()
