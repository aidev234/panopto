# PANOPTO

PANOPTO is a local OSINT workstation for collecting public social content, storing it in SQLite, and working through cases in a browser UI. The current stack covers:

- Post collection for Twitter/X, Reddit, TikTok, Bluesky, Instagram, and YouTube
- Recon for username and email selectors
- Case management, report export, and manual post ingestion
- Optional enrichments through People Data Labs, OSINT Industries, Numverify, Apify, and OpenAI
- Local-first serving, with both API and default server bind restricted to loopback clients

Recon uses a vendored `user_scanner` copy in `panopto/_vendor/user_scanner`, so there is no separate `pip install user-scanner` step.

## Quick start

Create a virtualenv, install dependencies, then launch the local server:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 panopto.py
```

You can also start it with:

```bash
python3 -m panopto
```

Then open `http://127.0.0.1:8000`.

`panopto.py` will prefer the repo-local virtualenv when `.venv/bin/python` exists, so using the launcher is the simplest path for local runs.
Both CLI entrypoints now default to `127.0.0.1`; only pass `--host 0.0.0.0` if you intentionally want LAN exposure during development.

## What the app does

The browser UI is case-first rather than just post-first. A typical workflow is:

1. Create or open a case.
2. Run recon on usernames, emails, or other selectors to discover leads.
3. Start collection jobs for supported platforms and date ranges.
4. Review posts, tags, face clusters, and warning assessments.
5. Add manual notes or uploads and export a PDF report.

The default database file is `osint_data.db` in the repository root. Some API reads can target a different `.db` file, but only within the repo or `/tmp`.

## Main entry points

- `panopto.py`: local launcher that re-execs into `.venv` when available.
- `panopto/__main__.py`: `python -m panopto` entrypoint.
- `frontend/server.py`: HTTP server, API routes, and static file hosting.
- `frontend/static/`: self-contained frontend assets.
- `panopto/collection_service.py`: target parsing and multi-platform collection orchestration.
- `panopto/recon.py`: selector recon, enrichment, screenshots, and lead generation.
- `panopto/storage/posts.py`: SQLite schema, persistence, and case storage.
- `tests/`: unit and API tests.

## Project layout

- `panopto/collectors/`: source-specific collectors.
- `panopto/analysis/`: LLM warning assessment logic and demo assets.
- `panopto/storage/known_entities.py`: archive and restore case entities.
- `run_collection.py`: minimal terminal collector helper for direct Twitter collection experiments.
- `scripts/secret_scan.py`: simple local secret pattern scan.

## Configuration and secrets

PANOPTO supports both UI-managed config and environment variables.

Files written locally:

- `.panopto_config.json`: non-secret settings such as retention defaults and custom keywords.
- `.panopto_secrets.enc`: encrypted secret bundle when `PANOPTO_SECRET_PASSPHRASE` is set.
- `osint_data.db`: primary SQLite database.

Secrets can be provided in either place:

- Through `Configuration` in the UI
- Through environment variables

Supported secret env vars:

- `PANOPTO_PDL_API_KEY`
- `PANOPTO_OSINT_INDUSTRIES_API_KEY`
- `PANOPTO_NUMVERIFY_API_KEY`
- `PANOPTO_OPENAI_API_KEY`
- `PANOPTO_APIFY_API_TOKEN`

Compatibility fallbacks also exist for:

- `OPENAI_API_KEY`
- `APIFY_API_TOKEN`

If you want secrets encrypted on disk, set:

```bash
export PANOPTO_SECRET_PASSPHRASE="choose-a-local-passphrase"
```

The app will continue to work without encrypted storage, but secrets will then only come from runtime config or env vars.

## Optional integrations

### People Data Labs

- Used during recon for person enrichment.
- Email selectors are sent as email-based enrichment requests.
- Username recon can use discovered profile URLs for enrichment.
- Results are surfaced as `person_data_profiles` and folded into recon leads.

Configure through the UI or `PANOPTO_PDL_API_KEY`.

### OSINT Industries

- Used during recon streaming and profile discovery.
- Configure through the UI or `PANOPTO_OSINT_INDUSTRIES_API_KEY`.

### Numverify

- Used for phone selector enrichment.
- Configure through the UI or `PANOPTO_NUMVERIFY_API_KEY`.

### Apify

Instagram, TikTok, and Twitter/X collection can use Apify actor calls. Those platforms require an Apify token before `/api/collect/start` will accept the request.

- `PANOPTO_APIFY_API_TOKEN`: required token
- `PANOPTO_APIFY_INSTAGRAM_ACTOR_ID`: defaults to `apify/instagram-scraper`
- `PANOPTO_APIFY_TIKTOK_ACTOR_ID`: defaults to `clockworks/tiktok-scraper`
- `PANOPTO_APIFY_TWITTER_ACTOR_ID`: defaults to `apidojo/tweet-scraper`

Example:

```bash
export PANOPTO_APIFY_API_TOKEN="apify_api_..."
python3 panopto.py
```

### OpenAI warning assessment

Post-level warning assessments are stored in `metadata.llm_assessment`.

- Demo case generation at `/api/cases/demo` seeds sample assessment data.
- Manual and batch LLM assessment routes are exposed through `/api/llm/estimate`, `/api/llm/run`, and `/api/posts/assessment`.

Environment variables:

- `OPENAI_API_KEY` or `PANOPTO_OPENAI_API_KEY`: enables OpenAI-backed assessment
- `PANOPTO_LLM_MODEL`: defaults to `gpt-4.1-mini`
- `PANOPTO_LLM_TIMEOUT_SECONDS`: defaults to `25`
- `PANOPTO_LLM_DISABLE`: set `1` or `true` to skip OpenAI calls
- `PANOPTO_LLM_INPUT_COST_PER_1M`: optional local estimator override
- `PANOPTO_LLM_OUTPUT_COST_PER_1M`: optional local estimator override

### Face recognition

`/api/posts` can annotate post results with face clusters. The implementation uses `insightface`, `onnxruntime`, and `opencv-python-headless`.

Optional environment variable:

- `PANOPTO_INSIGHTFACE_HOME`: model cache directory, defaults to `/tmp/panopto_insightface_models`

If the models or runtime are unavailable, the API reports that face recognition is not available instead of crashing.

### Playwright

Playwright is optional but useful for:

- Recon profile screenshots
- Browser-assisted collection fallbacks on some platforms

If you want those paths, install Playwright and Chromium separately:

```bash
python3 -m pip install playwright
playwright install chromium
```

## HTTP API overview

The UI is built entirely on the local HTTP API in `frontend/server.py`. API requests are restricted to loopback clients.

Core routes:

- `GET /api/posts`: query posts, filters, case scoping, and optional face clustering
- `POST /api/collect`: synchronous collection
- `POST /api/collect/start`: background collection job
- `GET /api/collect/status?job_id=...`: poll collection job status
- `POST /api/recon`: run recon for selectors
- `POST /api/recon/stream`: newline-delimited streaming recon responses
- `GET /api/cases`: list cases
- `POST /api/cases`: create case
- `PATCH /api/cases/{case_id}`: update case
- `DELETE /api/cases/{case_id}`: delete case and its posts
- `POST /api/cases/demo`: seed a demo case and posts
- `GET /api/cases/{case_id}/notes.pdf`: export a case report PDF
- `GET /api/config`: read public config
- `POST /api/config`: save config and secrets
- `POST /api/posts/manual`: create a manual post from text or uploaded file content
- `POST /api/posts/assessment`: persist edited LLM assessment metadata for a post
- `POST /api/llm/estimate`: estimate assessment cost
- `POST /api/llm/run`: assess posts that do not already have LLM metadata
- `POST /api/known-entities/archive-case`: archive a case into known entities
- `POST /api/known-entities/match`: match selectors against archived entities
- `POST /api/known-entities/restore`: restore an archived case
- `POST /api/session/end`: clear local data/config and optionally shut down the server

## Collection details

`parse_targets()` accepts either a legacy single `username` field or a `targets` array:

```json
{
  "targets": [
    {"platform": "twitter", "username": "nasa"},
    {"platform": "reddit", "username": "spez"},
    {"platform": "youtube", "username": "@veritasium"}
  ],
  "start_date": "2026-02-01",
  "end_date": "2026-02-29"
}
```

Supported platform keys:

- `twitter`
- `reddit`
- `tiktok`
- `bluesky`
- `instagram`
- `youtube`

Date parsing accepts `YYYY-MM-DD` and common U.S. numeric forms such as `MM/DD/YYYY`.

## Frontend

The frontend is intentionally self-contained. There are no CDN dependencies for React, Tailwind, or runtime JS frameworks, which keeps local preview reliable in restricted environments.

Frontend-specific notes live in [frontend/README.md](/home/osint/Documents/panopto/frontend/README.md).

Production handover notes live in [HANDOVER.md](/home/osint/Documents/panopto/HANDOVER.md).

## Development

Run tests with:

```bash
PYTHONPATH=. .venv/bin/pytest -q
```

Useful focused test targets:

```bash
PYTHONPATH=. .venv/bin/pytest tests/test_frontend_api.py -q
PYTHONPATH=. .venv/bin/pytest tests/test_recon.py -q
```

## Notes and constraints

- PANOPTO is built for local operator workflows, not multi-user deployment.
- Static and API content is served from the built-in Python HTTP server.
- Some platform collectors depend on third-party availability and anti-bot behaviour, so collection quality will vary by source.
- The repo may contain generated recon screenshots in `frontend/static/recon_shots/` from prior local runs.
