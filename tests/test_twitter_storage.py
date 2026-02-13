import sqlite3
import tempfile
import unittest
from pathlib import Path

from twitter_storage import init_db, save_posts


class TestTwitterStorage(unittest.TestCase):
    def test_init_db_and_save_posts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = str(Path(tmpdir) / "osint_data.db")
            init_db(db_path)

            posts = [
                {
                    "post_id": "abc123",
                    "username": "sama",
                    "content": "Hello",
                    "timestamp": "2026-01-01T12:00:00+00:00",
                    "likes": 10,
                    "retweets": 2,
                    "replies": 1,
                    "metadata": {"raw_timestamp": "2026-01-01T12:00:00Z"},
                }
            ]

            inserted_first = save_posts(posts, db_path=db_path)
            inserted_second = save_posts(posts, db_path=db_path)

            self.assertEqual(inserted_first, 1)
            self.assertEqual(inserted_second, 0)

            with sqlite3.connect(db_path) as conn:
                row_count = conn.execute("SELECT COUNT(*) FROM twitter_posts").fetchone()[0]

            self.assertEqual(row_count, 1)


if __name__ == "__main__":
    unittest.main()
