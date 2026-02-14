# OSINT Post Explorer Frontend

This local UI visualizes collected posts from `osint_data.db` in a modern dark theme.

## Why preview now works reliably
The previous implementation depended on CDN-hosted assets (React, Babel, Tailwind). In restricted preview environments those requests can fail, leaving a blank page.

This version is fully self-contained and served from local files only (`index.html`, `styles.css`, `app.js`), so it works offline and in constrained previews.

## Features
- Displays username, platform, timestamp, and full post content.
- Sort control for newest/oldest posts.
- Search bar with nested boolean logic support via backend query parser:
  - Example: `"New York" AND ("live in" OR "moving to")`
- Debounced refreshes against `/api/posts` as you type.

## Run locally
1. Start the local server from repository root:
   ```bash
   python frontend/server.py
   ```
2. Open `http://localhost:8000` in your browser.

By default, the API reads from `./osint_data.db`.
