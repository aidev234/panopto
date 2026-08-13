# Orion Webinar Demo Case

This case is fully synthetic. It is designed to show an end-to-end AI-assisted pivot from an initial selector to case closeout without using real subject data.

## Setup

1. Start Orion: `python3 panopto.py`
2. Open `http://127.0.0.1:8000`.
3. Select `Generate Demo Case`.
4. Open `DEMO CASE - POI SMITH, John R.`

## Story

The starting selector is `@demo_subject`. The case expands into linked aliases, email addresses, a phone number, developer activity, synthetic enrichment records, and posts across supported platforms. The analyst goal is to determine whether the synthetic subject should be closed, escalated, or moved to watchlist.

## Pivot Queries

Use these searches during the demo:

- `@demo_subject OR demo.subject@proton.me`
- `graymarketmaps OR demo-subject-labs`
- `route OR loading dock OR service alley`
- `ops.demo@pm.me OR burner OR fallback channel`
- `"Pathway Warning Behavior" OR "Capability interest"`

## Demo Beats

1. Case overview: show selectors, known profiles, and the synthetic-only context.
2. Footprint pivot: open the footprint view and show profile linkage from username, email, phone, PDL-style data, OSINT Industries-style records, Numverify-style data, and demo breach records.
3. Collection review: use the pivot queries to narrow posts from routine noise to high-signal route planning, venue logistics, fallback communications, and alias linkage.
4. AI assessment: show LLM warning labels and underlying themes to explain prioritization.
5. Pattern of life: show Washington, DC routine activity mixed with venue-focused posts.
6. Closeout: save as `Watchlist` with a daily cadence, then export the PDF report.

## Completion Criteria

- Cross-platform linkage is visible between `@demo_subject`, `graymarketmaps`, and `demo-subject-labs`.
- At least two selector pivots are shown: `demo.subject@proton.me`, `ops.demo@pm.me`, and `+1 202 555 0199`.
- High-signal posts are separated from ordinary Washington, DC activity.
- The final disposition is documented as `Watchlist` with daily review cadence.
