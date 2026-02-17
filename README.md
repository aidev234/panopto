# PANOPTO

PANOPTO is a local OSINT workflow for collecting public social posts (Twitter/X, Reddit, TikTok via alt front-ends, Bluesky, and YouTube), storing them in SQLite, tagging themes, and exploring results in a browser dashboard.

## Repository Structure

- `panopto/post_query.py`: query engine, text cleanup, filtering, and DB-to-view model mapping.
- `panopto/collection_service.py`: collection orchestration and aggregation workflow.
- `panopto/collectors/`: platform collectors (`twitter.py`, `reddit.py`, `tiktok.py`, `bluesky.py`, `youtube.py`).
- `panopto/storage/posts.py`: SQLite schema and persistence.
- `panopto/analysis/theme_modeling.py`: BERTopic theme tagging.
- `frontend/server.py`: HTTP transport layer and static file serving.
- `frontend/static/`: browser UI.
- `tests/`: unit tests.

## Run

```bash
python3 panopto.py
```

Or:

```bash
python -m panopto
```

Open `http://localhost:8000`.

Alternative:

```bash
python frontend/server.py
```

## Test

```bash
PYTHONPATH=. .venv/bin/pytest -q
```
