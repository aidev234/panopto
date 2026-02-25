# PANOPTO

PANOPTO is a local OSINT workflow for collecting public social posts (Twitter/X, Reddit, TikTok via alt front-ends, Bluesky, and YouTube), storing them in SQLite, and exploring results in a browser dashboard.

Recon supports batch selectors for both usernames and emails, powered by a vendored `user_scanner` integration in `panopto/_vendor/user_scanner` (no separate `pip install user-scanner` required).

## Repository Structure

- `panopto/post_query.py`: query engine, text cleanup, filtering, and DB-to-view model mapping.
- `panopto/collection_service.py`: collection orchestration and aggregation workflow.
- `panopto/collectors/`: platform collectors (`twitter.py`, `reddit.py`, `tiktok.py`, `bluesky.py`, `youtube.py`).
- `panopto/storage/posts.py`: SQLite schema and persistence.
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

## LLM Warning Assessments

- Post-level behavioural warning assessments are attached in `metadata.llm_assessment`.
- Demo case generation (`/api/cases/demo`) seeds coded LLM indicators from `panopto/analysis/assets/llm_warning_assessment/demo_dataset.xlsx`.
- Live collection can call OpenAI per post when `OPENAI_API_KEY` is set.

Environment variables:

- `OPENAI_API_KEY`: enables OpenAI-backed assessment during collection.
- `PANOPTO_LLM_MODEL` (optional): defaults to `gpt-4.1-mini`.
- `PANOPTO_LLM_TIMEOUT_SECONDS` (optional): defaults to `25`.
- `PANOPTO_LLM_DISABLE` (optional): set `1`/`true` to skip OpenAI calls.

## People Data Labs Enrichment

- Configure your PDL key in the UI via `Configuration -> People Data Labs API Key`.
- Recon with `email` selectors calls PDL Person Enrichment with the email parameter.
- Recon with `username` selectors calls PDL Person Enrichment for discovered profile URLs.
- PDL social profiles are surfaced in `Person Data Profile` and merged into recon leads/collection targets.
