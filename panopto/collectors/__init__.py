"""Collection adapters for supported platforms."""

from panopto.collectors.bluesky import collect_bluesky_posts, normalize_bluesky_username
from panopto.collectors.instagram import collect_instagram_posts, normalize_instagram_username
from panopto.collectors.reddit import collect_reddit_posts
from panopto.collectors.tiktok import collect_tiktok_posts
from panopto.collectors.twitter import collect_twitter_posts
from panopto.collectors.youtube import collect_youtube_posts, normalize_youtube_username, youtube_videos_url

__all__ = [
    "collect_bluesky_posts",
    "collect_instagram_posts",
    "collect_reddit_posts",
    "collect_tiktok_posts",
    "collect_twitter_posts",
    "collect_youtube_posts",
    "normalize_bluesky_username",
    "normalize_instagram_username",
    "normalize_youtube_username",
    "youtube_videos_url",
]
