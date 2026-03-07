# PANOPTO

PANOPTO is a local OSINT workflow for collecting public social posts (Twitter/X, Reddit, TikTok, Bluesky, Instagram, and YouTube), storing them in SQLite, and exploring results in a browser dashboard.

Recon supports batch selectors for both usernames and emails, powered by a vendored `user_scanner` integration in `panopto/_vendor/user_scanner` (no separate `pip install user-scanner` required).

## Repository Structure

- `panopto/post_query.py`: query engine, text cleanup, filtering, and DB-to-view model mapping.
- `panopto/collection_service.py`: collection orchestration and aggregation workflow.
- `panopto/collectors/`: platform collectors (`twitter.py`, `reddit.py`, `tiktok.py`, `bluesky.py`, `instagram.py`, `youtube.py`).
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

## Apify Setup (Instagram + TikTok + Twitter/X)

Instagram, TikTok, and Twitter/X collection can run through Apify actor calls.

Environment variables:

- `PANOPTO_APIFY_API_TOKEN`: required Apify API token.
- `PANOPTO_APIFY_INSTAGRAM_ACTOR_ID` (optional): actor ID override. Defaults to `apify/instagram-scraper`.
- `PANOPTO_APIFY_TIKTOK_ACTOR_ID` (optional): actor ID override. Defaults to `clockworks/tiktok-scraper`.
- `PANOPTO_APIFY_TWITTER_ACTOR_ID` (optional): actor ID override. Defaults to `apidojo/tweet-scraper`.

Example:

```bash
export PANOPTO_APIFY_API_TOKEN="apify_api_..."
export PANOPTO_APIFY_INSTAGRAM_ACTOR_ID="apify/instagram-scraper"
export PANOPTO_APIFY_TIKTOK_ACTOR_ID="clockworks/tiktok-scraper"
export PANOPTO_APIFY_TWITTER_ACTOR_ID="apidojo/tweet-scraper"
python3 panopto.py
```

Twitter actor input templates used by the collector:

Fetch tweets from a profile:

```json
{
  "searchTerms": ["from:NASA"],
  "sort": "Latest"
}
```

Fetch tweets with date ranges:

```json
{
  "searchTerms": [
    "from:NASA since:2024-01-01 until:2024-06-01",
    "from:NASA since:2024-06-01 until:2024-12-01"
  ],
  "sort": "Latest"
}
```
