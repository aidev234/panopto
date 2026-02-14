const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');

let requestTimer;
let controller;

function renderPosts(posts) {
  if (!posts.length) {
    resultsEl.innerHTML = '<div class="empty">No posts matched your query.</div>';
    return;
  }

  resultsEl.innerHTML = posts
    .map(
      (post) => `
      <article class="card">
        <div class="meta">
          <div class="badges">
            <span class="badge user">@${escapeHtml(post.username || 'unknown')}</span>
            <span class="badge platform">${escapeHtml(post.platform || 'Unknown')}</span>
          </div>
          <time>${escapeHtml(post.timestamp || 'Unknown date')}</time>
        </div>
        <div class="content">${escapeHtml(post.content || '(no text content)')}</div>
      </article>
    `,
    )
    .join('');
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

async function refreshPosts() {
  if (controller) controller.abort();
  controller = new AbortController();

  const query = searchInput.value.trim();
  const sort = sortSelect.value;
  const params = new URLSearchParams({ query, sort });

  statusEl.textContent = 'Refreshing results…';

  try {
    const response = await fetch(`/api/posts?${params.toString()}`, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    renderPosts(data.posts || []);
    const count = data.count || 0;
    statusEl.textContent = `${count} result${count === 1 ? '' : 's'}`;
  } catch (error) {
    if (error.name === 'AbortError') return;
    console.error(error);
    statusEl.textContent = 'Failed to load posts.';
    resultsEl.innerHTML = '<div class="empty">Could not load data from /api/posts.</div>';
  }
}

function queueRefresh() {
  clearTimeout(requestTimer);
  requestTimer = setTimeout(refreshPosts, 250);
}

searchInput.addEventListener('input', queueRefresh);
sortSelect.addEventListener('change', queueRefresh);

refreshPosts();
