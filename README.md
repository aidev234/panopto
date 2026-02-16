# PANOPTO

PANOPTO is a local OSINT workflow for collecting public social posts (Twitter/X, Reddit, TikTok via alt front-ends, Bluesky, and YouTube), storing them in SQLite, tagging themes, and exploring results in a browser dashboard.

## Repository Structure

- `panopto/post_query.py`: query engine, text cleanup, filtering, and DB-to-view model mapping.
- `panopto/collection_service.py`: collection orchestration and aggregation workflow.
- `frontend/server.py`: HTTP transport layer and static file serving.
- `frontend/static/`: browser UI.
- `twitter_collection.py`, `reddit_collection.py`, `tiktok_collection.py`, `bluesky_collection.py`, `youtube_collection.py`: platform collectors.
- `twitter_storage.py`: SQLite schema and persistence.
- `theme_modeling.py`: BERTopic theme tagging.
- `tests/`: unit tests.

## Run

```bash
python frontend/server.py
```

Open `http://localhost:8000`.

## Test

```bash
PYTHONPATH=. .venv/bin/pytest -q
```
