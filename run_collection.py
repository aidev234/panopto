"""Temporary terminal frontend for collecting and storing Twitter OSINT data."""

from __future__ import annotations

from twitter_collection import collect_twitter_posts
from twitter_storage import save_posts


def main() -> None:
    username = input("Enter target @username: ").strip()
    collection_window = input("Enter collection period (e.g. 1 week, 3 days): ").strip()

    try:
        posts = collect_twitter_posts(username=username, collection_window=collection_window)
        inserted = save_posts(posts, db_path="osint_data.db")
    except Exception as exc:
        print(f"collection failed: {exc}")
        return

    print("collection complete")
    print(f"stored rows: {inserted}")


if __name__ == "__main__":
    main()
