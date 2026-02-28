import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

import requests

from panopto.errors import UsernameNotFoundError
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

        with patch("panopto.collectors.twitter._iter_pages", return_value=[html]):
            results = twitter_collection.collect_twitter_posts(
                "@sama",
                "1 week",
                request_delay_seconds=0,
            )

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
        now = datetime.now(timezone.utc).isoformat()
        html = f"""
        <article data-tweet-id="a1">
            <div class="tweet-text">Normal post</div>
            <a href="https://x.com/sama/status/100"></a>
            <time datetime="{now}"></time>
        </article>
        <article data-tweet-id="a2">
            <div class="tweet-text">Elon Musk reposted Something</div>
            <a href="https://x.com/sama/status/101"></a>
            <time datetime="{now}"></time>
        </article>
        """

        with patch("panopto.collectors.twitter._iter_pages", return_value=[html]):
            results = twitter_collection.collect_twitter_posts("sama", "7 days", request_delay_seconds=0)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["post_id"], "a1")

    def test_browser_fallback_used_when_request_pages_are_empty(self):
        browser_html = """
        <article data-tweet-id="b1">
            <div class="tweet-text">Browser fallback post</div>
            <time datetime="2026-02-10T12:00:00Z"></time>
        </article>
        """

        with (
            patch("panopto.collectors.twitter._iter_pages", return_value=["<html></html>"]),
            patch("panopto.collectors.twitter._iter_rendered_pages", return_value=[browser_html]),
        ):
            results = twitter_collection.collect_twitter_posts(
                "sama",
                "30 days",
                browser_fallback=True,
                request_delay_seconds=0,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "Browser fallback post")

    def test_browser_enrich_existing_merges_additional_paginated_posts(self):
        request_html = """
        <article data-tweet-id="r1">
            <div class="tweet-text">Request post</div>
            <time datetime="2026-02-10T12:00:00Z"></time>
        </article>
        """
        browser_html = """
        <article data-tweet-id="b2">
            <div class="tweet-text">Loaded more tweet</div>
            <time datetime="2026-02-09T12:00:00Z"></time>
        </article>
        """

        with (
            patch("panopto.collectors.twitter._iter_pages", return_value=[request_html]),
            patch("panopto.collectors.twitter._iter_rendered_pages", return_value=[browser_html]),
        ):
            results = twitter_collection.collect_twitter_posts(
                "sama",
                "30 days",
                browser_fallback=True,
                browser_enrich_existing=True,
                request_delay_seconds=0,
            )

        self.assertEqual(len(results), 2)
        self.assertEqual({post["post_id"] for post in results}, {"r1", "b2"})

    def test_dedupes_by_post_id_preferring_richer_content(self):
        now = datetime.now(timezone.utc).isoformat()
        html = f"""
        <article data-tweet-id="dup1">
            <a href="https://x.com/sama/status/dup1">View</a>
            <div class="tweet-text">Short</div>
            <time datetime="{now}"></time>
        </article>
        <article data-tweet-id="dup1">
            <a href="https://x.com/sama/status/dup1">View</a>
            <div class="tweet-text">Much longer canonical tweet content</div>
            <time datetime="{now}"></time>
        </article>
        """

        with patch("panopto.collectors.twitter._iter_pages", return_value=[html]):
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

    def test_collect_raises_username_not_found_on_missing_account_signal(self):
        missing_html = "<html><body><p>User not found</p></body></html>"

        with patch("panopto.collectors.twitter._iter_pages", return_value=[missing_html]):
            with self.assertRaises(UsernameNotFoundError):
                twitter_collection.collect_twitter_posts(
                    "missing_user",
                    "7 days",
                    browser_fallback=False,
                    request_delay_seconds=0,
                )

    def test_collect_uses_rss_fallback_when_html_pages_empty(self):
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

        with (
            patch("panopto.collectors.twitter._iter_pages", return_value=["<html></html>"]),
            patch("panopto.collectors.twitter._iter_rss_posts", return_value=[rss_post]),
        ):
            results = twitter_collection.collect_twitter_posts(
                "sama",
                "30 days",
                browser_fallback=False,
                request_delay_seconds=0,
            )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["post_id"], "909090")
        self.assertEqual(results[0]["content"], "RSS fallback tweet")


if __name__ == "__main__":
    unittest.main()
