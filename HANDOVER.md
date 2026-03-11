# PANOPTO Handover Notes

This repo is a strong concept prototype. The current test suite passes, the app runs locally, and the main productionisation work is now about hardening boundaries, reducing file size concentration, and replacing prototype-era in-process patterns with deployable services.

## How the codebase is organized

- `frontend/server.py`: single-process HTTP server that serves static files and almost all API routes. This is the current orchestration center.
- `panopto/collection_service.py`: normalizes collection requests, runs platform collectors in parallel, stores posts, and emits progressive snapshots back to the UI/job layer.
- `panopto/collection_jobs.py`: wraps collection in an in-memory background job registry for polling from the browser.
- `panopto/recon.py`: selector normalization, third-party enrichment calls, screenshot capture, and profile lead generation.
- `panopto/storage/posts.py`: SQLite schema management plus case/post persistence.
- `panopto/post_query.py`: post shaping, enrichment tags, boolean query matching, and date/tag filters.
- `frontend/static/`: self-contained frontend assets with no CDN runtime dependency.

## Immediate fixes applied in this review

- Changed both CLI entrypoints to bind `127.0.0.1` by default instead of `0.0.0.0`. This matches the repo’s local-only positioning and avoids exposing the static UI on all interfaces by accident.
- Updated repo documentation to call out the loopback default and how to opt into non-local binding intentionally.

## What to streamline next

- Split `frontend/server.py` by concern.
  It currently combines static hosting, request parsing, API routing, PDF generation, file ingestion, config persistence wiring, and process lifecycle. This is the largest maintainability bottleneck in the repo.
- Split `panopto/recon.py` into selector normalization, external providers, screenshot capture, and result assembly modules.
  The current file is doing too many jobs and makes provider-specific changes expensive.
- Move background job state out of process memory if production deployment is planned.
  `panopto/collection_jobs.py` keeps all job state in `_JOBS`, which is fine for a single local operator but not for restarts, multiple workers, or observability.
- Introduce a collector/provider interface layer.
  The collection and recon code already share common result shapes. Formalizing them behind typed adapters will reduce branching and make provider swaps less risky.
- Add structured logging.
  Most failure paths currently return API payloads without emitting durable operational logs. Production work should add consistent request, collector, and provider logging with correlation IDs.

## Risks to address before production

- Third-party collectors and enrichment providers are network-fragile by design. Timeouts, anti-bot changes, and schema drift should be treated as normal operating conditions.
- SQLite plus in-process jobs is appropriate for a local workstation, not for multi-user deployment.
- Several optional integrations fail closed by swallowing exceptions and returning partial results. That is good for operator continuity, but production telemetry needs those events recorded.
- Recon screenshot capture depends on optional Playwright/Chromium availability. Production packaging should make that dependency explicit instead of best-effort.

## Recommended production target shape

- Put the API behind a real web framework with explicit route modules.
- Keep SQLite only for single-user desktop mode; otherwise move persistence and job state to managed services.
- Isolate external-provider calls behind thin clients with retry, timeout, and response-shape tests.
- Preserve the self-contained frontend build approach. Avoid reintroducing CDN runtime dependencies.

## Verification baseline

- Full suite currently passes with `.venv/bin/pytest`.
- `python -m compileall panopto frontend` succeeds.
