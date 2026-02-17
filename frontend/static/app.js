const searchInput = document.getElementById('searchInput');
const sortSelect = document.getElementById('sortSelect');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const setupModal = document.getElementById('setupModal');
const setupForm = document.getElementById('setupForm');
const setupStatus = document.getElementById('setupStatus');
const closeSetupBtn = document.getElementById('closeSetupBtn');
const targetsList = document.getElementById('targetsList');
const addTargetBtn = document.getElementById('addTargetBtn');
const autofillTargetsBtn = document.getElementById('autofillTargetsBtn');
const startDateInput = document.getElementById('startDateInput');
const endDateInput = document.getElementById('endDateInput');
const collectBtn = document.getElementById('collectBtn');
const newCollectionBtn = document.getElementById('newCollectionBtn');
const retagThemesBtn = document.getElementById('retagThemesBtn');
const quitBtn = document.getElementById('quitBtn');
const filterToggleBtn = document.getElementById('filterToggleBtn');
const filterPanel = document.getElementById('filterPanel');
const filterTwitter = document.getElementById('filterTwitter');
const filterReddit = document.getElementById('filterReddit');
const filterTiktok = document.getElementById('filterTiktok');
const filterBluesky = document.getElementById('filterBluesky');
const filterYoutube = document.getElementById('filterYoutube');
const filterPost = document.getElementById('filterPost');
const filterRepost = document.getElementById('filterRepost');
const filterReply = document.getElementById('filterReply');
const filterQuote = document.getElementById('filterQuote');
const filterComment = document.getElementById('filterComment');
const filterSelectors = document.getElementById('filterSelectors');
const filterIdeologicalIndicators = document.getElementById('filterIdeologicalIndicators');
const filterThreatSignals = document.getElementById('filterThreatSignals');
const timelineChart = document.getElementById('timelineChart');
const timelineEmpty = document.getElementById('timelineEmpty');
const timelineTotal = document.getElementById('timelineTotal');
const keywordChart = document.getElementById('keywordChart');
const keywordEmpty = document.getElementById('keywordEmpty');
const typeMix = document.getElementById('typeMix');
const themeMix = document.getElementById('themeMix');
const themeMixEmpty = document.getElementById('themeMixEmpty');
const locationMap = document.getElementById('locationMap');
const locationMapEmpty = document.getElementById('locationMapEmpty');
const locationMapTotal = document.getElementById('locationMapTotal');
const entityMix = document.getElementById('entityMix');
const entityMixEmpty = document.getElementById('entityMixEmpty');
const threatMix = document.getElementById('threatMix');
const threatMixEmpty = document.getElementById('threatMixEmpty');
const threatSignalMix = document.getElementById('threatSignalMix');
const threatSignalMixEmpty = document.getElementById('threatSignalMixEmpty');
const selectorMix = document.getElementById('selectorMix');
const selectorMixEmpty = document.getElementById('selectorMixEmpty');

let requestTimer;
let controller;
let activeStartDate = '';
let activeEndDate = '';
let activeUsername = '';
let activeTargets = [];
let latestPosts = [];
const activeEntityFilters = new Set();
let locationMapLibraryPromise;
let locationMapInstance;
let locationMapLayer;
const STOP_WORDS = new Set([
  'about', 'after', 'again', 'also', 'and', 'any', 'are', 'back', 'because', 'been', 'before',
  'being', 'both', 'but', 'can', 'cant', 'could', 'did', 'does', 'dont', 'from', 'get', 'got',
  'had', 'has', 'have', 'here', 'how', 'into', 'its', 'just', 'like', 'more', 'most', 'much',
  'need', 'now', 'our', 'out', 'over', 'really', 'said', 'should', 'some', 'such', 'than',
  'that', 'the', 'their', 'them', 'then', 'there', 'they', 'this', 'those', 'time', 'today',
  'too', 'use', 'very', 'want', 'was', 'were', 'what', 'when', 'where', 'which', 'while',
  'will', 'with', 'would', 'you', 'your',
]);
const LOCATION_COORDS_BY_TAG = {
  'loc:new-york': { name: 'New York', lat: 40.7128, lon: -74.0060 },
  'loc:washington-dc': { name: 'Washington DC', lat: 38.9072, lon: -77.0369 },
  'loc:washington': { name: 'Washington', lat: 47.7511, lon: -120.7401 },
  'loc:los-angeles': { name: 'Los Angeles', lat: 34.0522, lon: -118.2437 },
  'loc:san-francisco': { name: 'San Francisco', lat: 37.7749, lon: -122.4194 },
  'loc:boston': { name: 'Boston', lat: 42.3601, lon: -71.0589 },
  'loc:chicago': { name: 'Chicago', lat: 41.8781, lon: -87.6298 },
  'loc:texas': { name: 'Texas', lat: 31.0, lon: -100.0 },
  'loc:california': { name: 'California', lat: 36.7783, lon: -119.4179 },
  'loc:florida': { name: 'Florida', lat: 27.6648, lon: -81.5158 },
  'loc:ukraine': { name: 'Ukraine', lat: 48.3794, lon: 31.1656 },
  'loc:israel': { name: 'Israel', lat: 31.0461, lon: 34.8516 },
  'loc:palestine': { name: 'Palestine', lat: 31.9522, lon: 35.2332 },
  'loc:gaza': { name: 'Gaza', lat: 31.3547, lon: 34.3088 },
  'loc:london': { name: 'London', lat: 51.5072, lon: -0.1276 },
  'loc:paris': { name: 'Paris', lat: 48.8566, lon: 2.3522 },
  'loc:berlin': { name: 'Berlin', lat: 52.52, lon: 13.405 },
  'loc:tokyo': { name: 'Tokyo', lat: 35.6762, lon: 139.6503 },
  'loc:beijing': { name: 'Beijing', lat: 39.9042, lon: 116.4074 },
  'loc:moscow': { name: 'Moscow', lat: 55.7558, lon: 37.6173 },
};

function toDateInputValue(date) {
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const day = String(date.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function initializeDateInputs() {
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  startDateInput.value = toDateInputValue(weekAgo);
  endDateInput.value = toDateInputValue(now);
}

function addTargetRow(platform = 'twitter', username = '') {
  const row = document.createElement('div');
  row.className = 'target-row';
  row.innerHTML = `
    <select class="target-platform" aria-label="Target platform">
      <option value="twitter">Twitter/X</option>
      <option value="reddit">Reddit</option>
      <option value="tiktok">TikTok</option>
      <option value="bluesky">Bluesky</option>
      <option value="youtube">YouTube</option>
    </select>
    <input class="target-username" type="text" placeholder="@johnsmith, Cautious_Dirt8409, bsky.app/profile/aoc.bsky.social, or youtube.com/@AOC/videos" autocomplete="off" />
    <button class="icon-btn target-remove" type="button" title="Remove target">×</button>
  `;
  targetsList.appendChild(row);
  row.querySelector('.target-platform').value = platform;
  row.querySelector('.target-username').value = username;
}

function normalizeTargetUsername(platform, rawUsername) {
  let username = String(rawUsername || '').trim().replace(/^@+/, '').replace(/^u\//i, '');
  if (platform === 'bluesky') {
    const match = username.match(/^https?:\/\/(?:www\.)?bsky\.app\/profile\/([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
    username = username.replace(/^@+/, '');
    username = username.replace(/\.bsky\.social$/i, '');
  }
  if (platform === 'youtube') {
    const match = username.match(/^https?:\/\/(?:www\.)?youtube\.com\/@([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
    username = username.replace(/^@+/, '');
  }
  return username.trim();
}

function getTargetsFromForm() {
  const targets = [];
  for (const row of targetsList.querySelectorAll('.target-row')) {
    const platformEl = row.querySelector('.target-platform');
    const usernameEl = row.querySelector('.target-username');
    if (!platformEl || !usernameEl) continue;
    const platform = platformEl.value.trim().toLowerCase();
    const username = normalizeTargetUsername(platform, usernameEl.value);
    if (!username) continue;
    targets.push({ platform, username });
  }
  return targets;
}

function formatRecency(timestamp) {
  if (!timestamp) return 'Unknown date';
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return 'Unknown date';

  const diffSeconds = Math.max(0, Math.floor((Date.now() - date.getTime()) / 1000));
  if (diffSeconds < 60) return 'just now';
  if (diffSeconds < 3600) return `${Math.floor(diffSeconds / 60)}m ago`;
  if (diffSeconds < 86400) return `${Math.floor(diffSeconds / 3600)}h ago`;
  if (diffSeconds < 604800) return `${Math.floor(diffSeconds / 86400)}d ago`;
  if (diffSeconds < 2628000) return `${Math.floor(diffSeconds / 604800)}w ago`;
  if (diffSeconds < 31536000) return `${Math.floor(diffSeconds / 2628000)}mo ago`;
  return `${Math.floor(diffSeconds / 31536000)}y ago`;
}

function accountTag(post) {
  const username = (post.username || 'unknown').replace(/^@+/, '');
  const displayName = (post.display_name || username).trim();
  if (displayName.toLowerCase() === username.toLowerCase()) {
    return `@${username}`;
  }
  return `${displayName} (@${username})`;
}

function renderPosts(posts) {
  latestPosts = Array.isArray(posts) ? posts : [];
  if (!posts.length) {
    resultsEl.innerHTML = '<div class="empty">No posts matched your query.</div>';
    renderVisuals([]);
    return;
  }

  resultsEl.innerHTML = posts
    .map(
      (post, index) => `
      <article id="post-card-${index}" class="card" data-post-index="${index}">
        <div class="meta">
          <div class="account-line">
            <span class="account-tag">${escapeHtml(accountTag(post))}</span>
            <span class="source-tag">${escapeHtml((post.platform || 'Unknown').toUpperCase())}</span>
            <span class="type-tag">${escapeHtml((post.post_type || 'post').toUpperCase())}</span>
          </div>
          <div class="meta-right">
            <time class="recency">${escapeHtml(formatRecency(post.timestamp))}</time>
            ${post.source_url ? `<a class="url-icon" href="${escapeHtml(post.source_url)}" target="_blank" rel="noopener noreferrer" title="Open source post">🔗</a>` : ''}
          </div>
        </div>
        <div class="content">${renderContentWithSignals(primaryPostText(post), searchInput.value, post)}</div>
        ${renderQuoteNest(post)}
        ${renderPostMedia(post)}
      </article>
    `,
    )
    .join('');
  renderVisuals(posts);
}

function primaryPostText(post) {
  const content = String(post?.content || '(no text content)');
  if (String(post?.post_type || '').toLowerCase() !== 'quote') return content;
  const metadata = post?.metadata || {};
  const quoteText = String(metadata.quote_text || metadata.quoted_text || '').trim();
  if (quoteText) {
    const loweredQuote = quoteText.toLowerCase();
    const index = content.toLowerCase().indexOf(loweredQuote);
    if (index > 0) return content.slice(0, index).trim();
  }
  const splitMarkers = ['“', '"', 'http://', 'https://'];
  for (const marker of splitMarkers) {
    const idx = content.indexOf(marker);
    if (idx > 0) return content.slice(0, idx).trim();
  }
  return content;
}

function scrollToPost(index) {
  const target = document.getElementById(`post-card-${index}`);
  if (!target) return;
  target.scrollIntoView({ behavior: 'smooth', block: 'center' });
  target.classList.add('card-focus');
  window.setTimeout(() => target.classList.remove('card-focus'), 1400);
}

function inferQuotedText(post) {
  const metadata = post?.metadata || {};
  const explicit = String(metadata.quote_text || metadata.quoted_text || '').trim();
  if (explicit) return explicit;

  const full = String(post?.content || '').trim();
  const primary = primaryPostText(post).trim();
  if (full && primary && full.toLowerCase().startsWith(primary.toLowerCase())) {
    const remaining = full.slice(primary.length).trim().replace(/^[\s:,\-–—"“”']+/, '').trim();
    if (remaining) return remaining;
  }

  const quotedMatch = full.match(/[“"]([^”"]{12,})[”"]/);
  if (quotedMatch) return quotedMatch[1].trim();
  return '';
}

function renderQuoteNest(post) {
  if (String(post?.post_type || '').toLowerCase() !== 'quote') return '';
  const metadata = post?.metadata || {};
  const referenced = String(post?.referenced_username || '').trim();
  const quoteText = inferQuotedText(post);
  if (!quoteText) return '';
  const quoteUrl = String(metadata.quote_url || post?.source_url || '').trim();
  return `
    <blockquote class="quote-nest">
      <div class="quote-meta">${referenced ? `@${escapeHtml(referenced)}` : 'Quoted'}</div>
      <div class="quote-text">${renderContentWithSignals(quoteText, searchInput.value, post)}</div>
      ${isHttpUrl(quoteUrl) ? `<a class="quote-link" href="${escapeHtml(quoteUrl)}" target="_blank" rel="noopener noreferrer">Open quoted post</a>` : ''}
    </blockquote>
  `;
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function extractSearchTerms(query) {
  const terms = [];
  const seen = new Set();
  const tokenPattern = /"([^"]+)"|[^\s()]+/g;
  const matches = String(query || '').matchAll(tokenPattern);
  for (const match of matches) {
    const raw = (match[1] || match[0] || '').trim();
    if (!raw) continue;
    if (/^(and|or|not)$/i.test(raw)) continue;
    const normalized = raw.toLowerCase();
    if (seen.has(normalized)) continue;
    seen.add(normalized);
    terms.push(raw);
  }
  terms.sort((a, b) => b.length - a.length);
  return terms;
}

function renderContentWithKeyterms(content, query) {
  const text = String(content || '');
  const terms = extractSearchTerms(query);
  if (!terms.length) return escapeHtml(text);

  const pattern = new RegExp(terms.map((term) => escapeRegExp(term)).join('|'), 'gi');
  let rendered = '';
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    const start = match.index;
    const end = start + match[0].length;
    rendered += escapeHtml(text.slice(lastIndex, start));
    rendered += `<span class="keyterm-text">${escapeHtml(text.slice(start, end))}</span>`;
    lastIndex = end;
  }
  rendered += escapeHtml(text.slice(lastIndex));
  return rendered;
}

function _termRegex(term) {
  const value = String(term || '').trim();
  if (!value) return null;
  const escaped = escapeRegExp(value);
  if (/[A-Za-z0-9]/.test(value)) {
    return new RegExp(`(?<!\\w)${escaped}(?!\\w)`, 'gi');
  }
  return new RegExp(escaped, 'gi');
}

function _collectRanges(text, terms, clsName, priority) {
  const ranges = [];
  for (const term of terms) {
    const rx = _termRegex(term);
    if (!rx) continue;
    let match;
    while ((match = rx.exec(text)) !== null) {
      ranges.push({
        start: match.index,
        end: match.index + match[0].length,
        cls: clsName,
        priority,
      });
      if (match.index === rx.lastIndex) rx.lastIndex += 1;
    }
  }
  return ranges;
}

function renderContentWithSignals(content, query, post) {
  const text = String(content || '');
  const searchTerms = extractSearchTerms(query);
  const threatTerms = Array.isArray(post?.threat_matches) ? post.threat_matches : [];
  const selectorTerms = Array.isArray(post?.selector_matches) ? post.selector_matches : [];

  const ranges = [
    ..._collectRanges(text, searchTerms, 'keyterm-text', 1),
    ..._collectRanges(text, threatTerms, 'signal-threat', 2),
    ..._collectRanges(text, selectorTerms, 'signal-selector', 3),
  ];
  if (!ranges.length) return escapeHtml(text);

  ranges.sort((a, b) => a.start - b.start || b.priority - a.priority || (b.end - b.start) - (a.end - a.start));
  const accepted = [];
  for (const range of ranges) {
    const overlap = accepted.find((item) => !(range.end <= item.start || range.start >= item.end));
    if (overlap) continue;
    accepted.push(range);
  }
  accepted.sort((a, b) => a.start - b.start);

  let out = '';
  let cursor = 0;
  for (const range of accepted) {
    out += escapeHtml(text.slice(cursor, range.start));
    out += `<span class="${range.cls}">${escapeHtml(text.slice(range.start, range.end))}</span>`;
    cursor = range.end;
  }
  out += escapeHtml(text.slice(cursor));
  return out;
}

function isHttpUrl(value) {
  return /^https?:\/\//i.test(String(value || '').trim());
}

function isVideoUrl(url) {
  const value = String(url || '').toLowerCase();
  return (
    /\.mp4(?:\?|$)/.test(value)
    || /\.m3u8(?:\?|$)/.test(value)
    || value.includes('video.twimg.com/')
    || value.includes('v.redd.it/')
  );
}

function isImageUrl(url) {
  const value = String(url || '').toLowerCase();
  return /\.(?:jpg|jpeg|png|webp|gif)(?:\?|$)/.test(value) || value.includes('pbs.twimg.com/media/') || value.includes('preview.redd.it/');
}

function normalizeMedia(post) {
  const metadata = post?.metadata || {};
  const seen = new Set();
  const media = [];
  const addMedia = (type, url, thumbnailUrl = '') => {
    const value = String(url || '').trim();
    if (!isHttpUrl(value)) return;
    const normalizedType = String(type || '').trim().toLowerCase();
    const inferredType = normalizedType || (isVideoUrl(value) ? 'video' : 'image');
    const key = `${inferredType}|${value}`;
    if (seen.has(key)) return;
    seen.add(key);
    media.push({
      type: inferredType,
      url: value,
      thumbnail_url: isHttpUrl(thumbnailUrl) ? String(thumbnailUrl).trim() : '',
    });
  };

  if (Array.isArray(metadata.media)) {
    for (const item of metadata.media) {
      if (!item || typeof item !== 'object') continue;
      addMedia(item.type, item.url, item.thumbnail_url);
    }
  }

  const fallbackCandidates = [metadata.video_url, metadata.play_url, metadata.media_url];
  for (const candidate of fallbackCandidates) {
    const value = String(candidate || '').trim();
    if (!isHttpUrl(value) || !isVideoUrl(value)) continue;
    addMedia('video', value, metadata.thumbnail_url);
  }

  if (Array.isArray(metadata.image_urls)) {
    for (const candidate of metadata.image_urls) {
      const value = String(candidate || '').trim();
      if (!isHttpUrl(value) || !isImageUrl(value)) continue;
      addMedia('image', value);
    }
  }

  if (Array.isArray(metadata.media_urls)) {
    for (const candidate of metadata.media_urls) {
      const value = String(candidate || '').trim();
      if (!isHttpUrl(value)) continue;
      if (isVideoUrl(value)) {
        addMedia('video', value, metadata.thumbnail_url);
      } else if (isImageUrl(value)) {
        addMedia('image', value);
      }
    }
  }

  // Single-value image fields used by some collectors.
  const imageFallbackCandidates = [metadata.image_url, metadata.image, metadata.thumbnail_url, metadata.preview_image_url];
  const hasVideo = media.some((item) => item.type === 'video');
  for (const candidate of imageFallbackCandidates) {
    const value = String(candidate || '').trim();
    if (!isHttpUrl(value)) continue;
    if (isVideoUrl(value)) continue;
    if (hasVideo && value === String(metadata.thumbnail_url || '').trim()) continue;
    addMedia('image', value);
  }

  // Avoid thumbnail duplication when a video is present.
  const videoThumbs = new Set(
    media
      .filter((item) => item.type === 'video')
      .map((item) => String(item.thumbnail_url || '').trim())
      .filter(Boolean),
  );
  if (videoThumbs.size) {
    return media.filter((item) => item.type !== 'image' || !videoThumbs.has(String(item.url || '').trim()));
  }

  return media;
}

function renderPostMedia(post) {
  const embedUrl = String(post?.metadata?.embed_url || '').trim();
  if (isHttpUrl(embedUrl) && /youtube\.com\/embed\//i.test(embedUrl)) {
    return `
      <div class="media-wrap">
        <iframe
          class="post-embed"
          src="${escapeHtml(embedUrl)}"
          title="Embedded video"
          loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen
        ></iframe>
      </div>
    `;
  }
  const media = normalizeMedia(post);
  if (!media.length) return '';

  const videos = media.filter((item) => item.type === 'video');
  const images = media.filter((item) => item.type !== 'video');
  const fallbackPoster = isHttpUrl(post?.metadata?.thumbnail_url) ? String(post.metadata.thumbnail_url).trim() : '';
  const videoMarkup = videos
    .map((item) => {
      const posterUrl = item.thumbnail_url || fallbackPoster;
      const posterAttr = posterUrl ? ` poster="${escapeHtml(posterUrl)}"` : '';
      return `
        <div class="media-wrap">
          <video class="post-video" controls preload="metadata"${posterAttr}>
            <source src="${escapeHtml(item.url)}" type="video/mp4" />
          </video>
        </div>
      `;
    })
    .join('');
  const imageMarkup = images.length
    ? `
      <div class="media-grid">
        ${images
          .map(
            (item) => `
              <a class="media-link" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
                <img class="post-image" loading="lazy" src="${escapeHtml(item.url)}" alt="Post media" />
              </a>
            `,
          )
          .join('')}
      </div>
    `
    : '';

  return `
    <div class="media-stack">
      ${videoMarkup}
      ${imageMarkup}
    </div>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function selectedTags() {
  const include = [];

  if (filterTwitter.checked) include.push('twitter');
  if (filterReddit.checked) include.push('reddit');
  if (filterTiktok.checked) include.push('tiktok');
  if (filterBluesky.checked) include.push('bluesky');
  if (filterYoutube.checked) include.push('youtube');
  if (filterPost.checked) include.push('post');
  if (filterRepost.checked) include.push('repost');
  if (filterReply.checked) include.push('reply');
  if (filterQuote.checked) include.push('quote');
  if (filterComment.checked) include.push('comment');
  for (const tag of activeEntityFilters) include.push(tag);

  return { include };
}

function applySignalTypeFilter(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  const selectorsOn = Boolean(filterSelectors?.checked);
  const ideologicalOn = Boolean(filterIdeologicalIndicators?.checked);
  const threatOn = Boolean(filterThreatSignals?.checked);
  if (!selectorsOn && !ideologicalOn && !threatOn) return rows;
  return rows.filter((post) => {
    const hasSelectors = Array.isArray(post?.selector_matches) && post.selector_matches.length > 0;
    const hasIdeologicalIndicators = Array.isArray(post?.threat_categories) && post.threat_categories.length > 0;
    const hasThreatSignals = Array.isArray(post?.threat_matches) && post.threat_matches.length > 0;
    return (
      (selectorsOn && hasSelectors)
      || (ideologicalOn && hasIdeologicalIndicators)
      || (threatOn && hasThreatSignals)
    );
  });
}

function dayKey(timestamp) {
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return '';
  return date.toISOString().slice(0, 10);
}

function daysBetween(startDate, endDate) {
  const days = [];
  const cursor = new Date(`${startDate}T00:00:00Z`);
  const final = new Date(`${endDate}T00:00:00Z`);
  while (cursor <= final) {
    days.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return days;
}

function shortDayLabel(day) {
  const date = new Date(`${day}T00:00:00Z`);
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', timeZone: 'UTC' });
}

function renderTimeline(posts) {
  timelineTotal.textContent = `${posts.length} post${posts.length === 1 ? '' : 's'}`;
  if (!posts.length) {
    timelineChart.innerHTML = '';
    timelineEmpty.classList.remove('hidden');
    return;
  }

  const counts = new Map();
  for (const post of posts) {
    const key = dayKey(post.timestamp);
    if (!key) continue;
    counts.set(key, (counts.get(key) || 0) + 1);
  }

  if (!counts.size) {
    timelineChart.innerHTML = '';
    timelineEmpty.classList.remove('hidden');
    return;
  }
  timelineEmpty.classList.add('hidden');

  const sortedDays = Array.from(counts.keys()).sort();
  const fullDays = daysBetween(sortedDays[0], sortedDays[sortedDays.length - 1]);
  const values = fullDays.map((day) => counts.get(day) || 0);

  const width = 380;
  const height = 170;
  const left = 30;
  const right = 12;
  const top = 16;
  const bottom = 34;
  const chartWidth = width - left - right;
  const chartHeight = height - top - bottom;
  const maxValue = Math.max(...values, 1);
  const stepX = fullDays.length > 1 ? chartWidth / (fullDays.length - 1) : chartWidth / 2;
  const points = values.map((value, index) => {
    const x = fullDays.length > 1 ? left + stepX * index : left + chartWidth / 2;
    const y = top + chartHeight - (value / maxValue) * chartHeight;
    return { x, y, value };
  });

  const path = points.map((point, i) => `${i === 0 ? 'M' : 'L'} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`).join(' ');
  const area = `${path} L ${(points[points.length - 1] || { x: left }).x.toFixed(2)} ${(top + chartHeight).toFixed(2)} L ${(points[0] || { x: left }).x.toFixed(2)} ${(top + chartHeight).toFixed(2)} Z`;

  timelineChart.innerHTML = `
    <line x1="${left}" y1="${top + chartHeight}" x2="${width - right}" y2="${top + chartHeight}" class="axis-line"></line>
    <path d="${area}" class="timeline-area"></path>
    <path d="${path}" class="timeline-line"></path>
    ${points
      .map(
        (point, index) =>
          `<circle cx="${point.x.toFixed(2)}" cy="${point.y.toFixed(2)}" r="2.8" class="timeline-point"><title>${point.value} posts on ${shortDayLabel(fullDays[index])}</title></circle>`,
      )
      .join('')}
    <text x="${left}" y="${height - 10}" class="axis-label">${escapeHtml(shortDayLabel(fullDays[0]))}</text>
    <text x="${width - right}" y="${height - 10}" text-anchor="end" class="axis-label">${escapeHtml(shortDayLabel(fullDays[fullDays.length - 1]))}</text>
    <text x="${left}" y="${top + 8}" class="axis-label">max ${maxValue}</text>
  `;
}

function extractKeywords(posts) {
  const counts = new Map();
  const monthWords = new Set([
    'jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april', 'may', 'jun', 'june',
    'jul', 'july', 'aug', 'august', 'sep', 'sept', 'september', 'oct', 'october', 'nov', 'november', 'dec', 'december',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
  ]);
  for (const post of posts) {
    const cleaned = (post.content || '')
      .toLowerCase()
      .replace(/https?:\/\/\S+/g, ' ')
      .replace(/\b\d{4}-\d{1,2}-\d{1,2}\b/g, ' ')
      .replace(/\b\d{1,2}\/\d{1,2}\/\d{2,4}\b/g, ' ')
      .replace(/\b\d{1,2}-\d{1,2}-\d{2,4}\b/g, ' ')
      .replace(/[@#][a-z0-9_]+/g, ' ');
    const words = cleaned.split(/[^a-z0-9]+/g);
    for (const word of words) {
      if (!word || word.length < 3) continue;
      if (/^\d+$/.test(word)) continue;
      if (/^\d{4}$/.test(word)) continue;
      if (/^\d+(st|nd|rd|th)$/.test(word)) continue;
      if (monthWords.has(word)) continue;
      if (STOP_WORDS.has(word)) continue;
      counts.set(word, (counts.get(word) || 0) + 1);
    }
  }
  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 8);
}

function renderKeywordChart(posts) {
  const topKeywords = extractKeywords(posts);
  if (!topKeywords.length) {
    keywordChart.innerHTML = '';
    keywordEmpty.classList.remove('hidden');
    return;
  }
  keywordEmpty.classList.add('hidden');

  const maxValue = topKeywords[0][1];
  keywordChart.innerHTML = topKeywords
    .map(([word, count]) => {
      const widthPct = Math.max(10, Math.round((count / maxValue) * 100));
      return `
        <div class="keyword-row">
          <span class="keyword-label">${escapeHtml(word)}</span>
          <div class="keyword-bar-wrap">
            <div class="keyword-bar" style="width:${widthPct}%"></div>
          </div>
          <span class="keyword-count">${count}</span>
        </div>
      `;
    })
    .join('');
}

function renderTypeMix(posts) {
  const counts = new Map();
  for (const post of posts) {
    const type = String(post.post_type || 'post').toLowerCase();
    counts.set(type, (counts.get(type) || 0) + 1);
  }
  const order = ['post', 'comment', 'reply', 'quote', 'repost'];
  const items = Array.from(counts.entries()).sort((a, b) => {
    const ai = order.indexOf(a[0]);
    const bi = order.indexOf(b[0]);
    if (ai >= 0 && bi >= 0) return ai - bi;
    if (ai >= 0) return -1;
    if (bi >= 0) return 1;
    return a[0].localeCompare(b[0]);
  });
  typeMix.innerHTML = items
    .map(([type, count]) => `<div class="mix-pill"><span>${escapeHtml(type)}</span><strong>${count}</strong></div>`)
    .join('');
}

function isTemporalThemeLabel(label) {
  const normalized = String(label || '').trim().toLowerCase();
  if (!normalized) return false;
  const tokens = normalized.match(/[a-z0-9:]+/g) || [];
  if (!tokens.length) return false;
  const temporalToken = /^(?:\d{1,4}|\d+[smhdwy]|\d{1,2}:\d{2}(?:[ap]m)?|\d+(?:sec(?:ond)?s?|min(?:ute)?s?|hr(?:s)?|hour(?:s)?|day(?:s)?|week(?:s)?|month(?:s)?|year(?:s)?)|today|yesterday|tomorrow|tonight|now|recent(?:ly)?|current(?:ly)?|latest|jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|sept|september|oct|october|nov|november|dec|december)$/i;
  return tokens.every((token) => temporalToken.test(token));
}

function renderThemeMix(posts) {
  const counts = new Map();
  for (const post of posts) {
    const label = String(post.theme_label || '').trim();
    if (!label) continue;
    if (isTemporalThemeLabel(label)) continue;
    counts.set(label, (counts.get(label) || 0) + 1);
  }
  const sorted = Array.from(counts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  if (!sorted.length) {
    themeMix.innerHTML = '';
    themeMixEmpty.classList.remove('hidden');
    return;
  }
  themeMixEmpty.classList.add('hidden');
  themeMix.innerHTML = sorted
    .slice(0, 8)
    .map(([label, count]) => `<div class="mix-pill"><span>${escapeHtml(label)}</span><strong>${count}</strong></div>`)
    .join('');
}

function loadLeaflet() {
  if (window.L) return Promise.resolve(window.L);
  if (locationMapLibraryPromise) return locationMapLibraryPromise;

  locationMapLibraryPromise = new Promise((resolve, reject) => {
    const cssHref = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    const jsSrc = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    if (!document.querySelector(`link[href="${cssHref}"]`)) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = cssHref;
      document.head.appendChild(link);
    }
    if (window.L) {
      resolve(window.L);
      return;
    }
    const script = document.createElement('script');
    script.src = jsSrc;
    script.async = true;
    script.onload = () => resolve(window.L);
    script.onerror = () => reject(new Error('leaflet_load_failed'));
    document.head.appendChild(script);
  });
  return locationMapLibraryPromise;
}

function ensureLocationMapInstance() {
  if (!locationMap) return Promise.resolve(null);
  return loadLeaflet().then((L) => {
    if (!L) return null;
    if (!locationMapInstance) {
      locationMap.innerHTML = '';
      locationMapInstance = L.map(locationMap, {
        zoomControl: false,
        attributionControl: false,
        worldCopyJump: true,
      }).setView([20, 0], 2);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 6,
      }).addTo(locationMapInstance);
      locationMapLayer = L.layerGroup().addTo(locationMapInstance);
    }
    return L;
  });
}

function renderLocationMap(posts) {
  if (!locationMap || !locationMapEmpty || !locationMapTotal) return;

  const mentions = new Map();
  const locationPairs = Object.entries(LOCATION_COORDS_BY_TAG).map(([tag, details]) => ({ tag, ...details }));
  const locationPairsByName = locationPairs
    .slice()
    .sort((a, b) => b.name.length - a.name.length);
  for (const post of posts) {
    const addMention = (name, lat, lon) => {
      const key = `${name}|${lat.toFixed(4)}|${lon.toFixed(4)}`;
      const existing = mentions.get(key);
      if (existing) {
        existing.count += 1;
      } else {
        mentions.set(key, { name, lat, lon, count: 1 });
      }
    };

    const entities = Array.isArray(post.entities) ? post.entities : [];
    for (const entity of entities) {
      if (!entity || entity.type !== 'location') continue;
      const name = String(entity.text || '').trim();
      const lat = Number(entity.lat);
      const lon = Number(entity.lon);
      if (!name || Number.isNaN(lat) || Number.isNaN(lon)) continue;
      addMention(name, lat, lon);
    }
    const tags = Array.isArray(post.tags) ? post.tags : [];
    for (const tag of tags) {
      const keyTag = String(tag || '').trim().toLowerCase();
      if (!keyTag.startsWith('loc:')) continue;
      const mapped = LOCATION_COORDS_BY_TAG[keyTag];
      if (!mapped) continue;
      addMention(mapped.name, mapped.lat, mapped.lon);
    }

    // Fallback path for older data where entities/tags were not persisted.
    const content = String(post.content || '').toLowerCase();
    for (const location of locationPairsByName) {
      const escaped = location.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const pattern = new RegExp(`(^|[^a-z0-9])${escaped.toLowerCase()}([^a-z0-9]|$)`, 'i');
      if (!pattern.test(content)) continue;
      addMention(location.name, location.lat, location.lon);
    }
  }

  const points = Array.from(mentions.values()).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
  const totalMentions = points.reduce((sum, point) => sum + point.count, 0);
  locationMapTotal.textContent = `${totalMentions} mention${totalMentions === 1 ? '' : 's'}`;
  locationMapEmpty.classList.toggle('hidden', points.length > 0);

  ensureLocationMapInstance()
    .then((L) => {
      if (!L || !locationMapLayer || !locationMapInstance) return;
      locationMapLayer.clearLayers();
      if (!points.length) {
        locationMapInstance.setView([20, 0], 2);
        return;
      }
      const maxCount = Math.max(...points.map((point) => point.count), 1);
      const bounds = [];
      for (const point of points.slice(0, 60)) {
        const radius = 4 + (point.count / maxCount) * 7;
        const marker = L.circleMarker([point.lat, point.lon], {
          radius,
          color: '#fde68a',
          weight: 1.2,
          fillColor: '#f59e0b',
          fillOpacity: 0.78,
        }).bindTooltip(`${point.name}: ${point.count} mention${point.count === 1 ? '' : 's'}`);
        marker.addTo(locationMapLayer);
        bounds.push([point.lat, point.lon]);
      }
      if (bounds.length === 1) {
        locationMapInstance.setView(bounds[0], 4);
      } else {
        locationMapInstance.fitBounds(bounds, { padding: [20, 20], maxZoom: 4 });
      }
    })
    .catch(() => {
      // Fallback if map library fails to load.
      locationMap.textContent = points.length
        ? points.slice(0, 8).map((item) => `${item.name} (${item.count})`).join(' • ')
        : 'Map unavailable';
    });
}

function renderEntityMix(posts) {
  if (!entityMix || !entityMixEmpty) return;

  const groupedCounts = {
    person: new Map(),
    org: new Map(),
    location: new Map(),
    other: new Map(),
  };
  for (const post of posts) {
    const entities = Array.isArray(post.entities) ? post.entities : [];
    for (const entity of entities) {
      const type = String(entity?.type || '').trim().toLowerCase();
      const text = String(entity?.text || '').trim();
      if (!type || !text) continue;
      const bucket = groupedCounts[type] || groupedCounts.other;
      const key = text.toLowerCase();
      const current = bucket.get(key);
      if (current) {
        current.count += 1;
      } else {
        bucket.set(key, { type, text, count: 1 });
      }
    }
  }

  const sections = ['location', 'person', 'org', 'other']
    .map((type) => {
      const values = Array.from(groupedCounts[type].values())
        .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text))
        .slice(0, 5);
      if (!values.length) return '';
      const label = type === 'org' ? 'Organizations' : `${type.charAt(0).toUpperCase()}${type.slice(1)}s`;
      return `
        <div class="entity-section">
          <p class="entity-section-title">${escapeHtml(label)}</p>
          <div class="entity-section-list">
            ${values
              .map(
                (item) => {
                  const slug = String(item.text || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
                  const prefix = type === 'location' ? 'loc' : type === 'person' ? 'person' : type === 'org' ? 'org' : 'ner';
                  const entityTag = `${prefix}:${slug || 'unknown'}`;
                  const activeClass = activeEntityFilters.has(entityTag) ? ' is-active' : '';
                  return `<button type="button" class="mix-pill entity-pill entity-filter-pill entity-${escapeHtml(type)}${activeClass}" data-entity-tag="${escapeHtml(entityTag)}"><span>${escapeHtml(item.text)}</span><strong>${item.count}</strong></button>`;
                },
              )
              .join('')}
          </div>
        </div>
      `;
    })
    .filter(Boolean);

  if (!sections.length) {
    entityMix.innerHTML = '';
    entityMixEmpty.classList.remove('hidden');
    return;
  }
  entityMixEmpty.classList.add('hidden');
  entityMix.innerHTML = sections.join('');
}

function _buildSignalRows(posts, fieldName, cssClass) {
  const counts = new Map();
  for (let i = 0; i < posts.length; i += 1) {
    const post = posts[i];
    const values = Array.isArray(post?.[fieldName]) ? post[fieldName] : [];
    for (const value of values) {
      const text = String(value || '').trim();
      if (!text) continue;
      const key = text.toLowerCase();
      const current = counts.get(key);
      if (current) {
        current.count += 1;
      } else {
        counts.set(key, { text, count: 1, firstIndex: i });
      }
    }
  }
  const items = Array.from(counts.values())
    .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text))
    .slice(0, 12);
  return items
    .map(
      (item) =>
        `<button type="button" class="signal-row ${cssClass}" data-post-index="${item.firstIndex}"><span>${escapeHtml(item.text)}</span><strong>${item.count}</strong></button>`,
    )
    .join('');
}

function renderThreatMix(posts) {
  if (!threatMix || !threatMixEmpty) return;
  const grouped = new Map();
  for (let i = 0; i < posts.length; i += 1) {
    const categories = Array.isArray(posts[i]?.threat_categories) ? posts[i].threat_categories : [];
    for (const category of categories) {
      const label = String(category || '').trim();
      if (!label) continue;
      const key = label.toLowerCase();
      const current = grouped.get(key);
      if (current) {
        current.count += 1;
      } else {
        grouped.set(key, { text: label, count: 1, firstIndex: i });
      }
    }
  }
  const markup = Array.from(grouped.values())
    .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text))
    .slice(0, 8)
    .map(
      (item) =>
        `<button type="button" class="signal-row signal-threat-row" data-post-index="${item.firstIndex}"><span>${escapeHtml(item.text)}</span><strong>${item.count}</strong></button>`,
    )
    .join('');
  if (!markup) {
    threatMix.innerHTML = '';
    threatMixEmpty.classList.remove('hidden');
    return;
  }
  threatMixEmpty.classList.add('hidden');
  threatMix.innerHTML = markup;
}

function renderSelectorMix(posts) {
  if (!selectorMix || !selectorMixEmpty) return;
  const markup = _buildSignalRows(posts, 'selector_matches', 'signal-selector-row');
  if (!markup) {
    selectorMix.innerHTML = '';
    selectorMixEmpty.classList.remove('hidden');
    return;
  }
  selectorMixEmpty.classList.add('hidden');
  selectorMix.innerHTML = markup;
}

function renderThreatSignalMix(posts) {
  if (!threatSignalMix || !threatSignalMixEmpty) return;
  const markup = _buildSignalRows(posts, 'threat_matches', 'signal-threat-row');
  if (!markup) {
    threatSignalMix.innerHTML = '';
    threatSignalMixEmpty.classList.remove('hidden');
    return;
  }
  threatSignalMixEmpty.classList.add('hidden');
  threatSignalMix.innerHTML = markup;
}

function renderVisuals(posts) {
  renderTimeline(posts);
  renderKeywordChart(posts);
  renderThemeMix(posts);
  renderLocationMap(posts);
  renderEntityMix(posts);
  renderThreatMix(posts);
  renderThreatSignalMix(posts);
  renderSelectorMix(posts);
  renderTypeMix(posts);
}

async function refreshPosts() {
  if (controller) controller.abort();
  controller = new AbortController();

  const query = searchInput.value.trim();
  const sort = sortSelect.value;
  const params = new URLSearchParams({ query, sort });
  const tags = selectedTags();
  if (activeStartDate) params.set('start_date', activeStartDate);
  if (activeEndDate) params.set('end_date', activeEndDate);
  if (tags.include.length) params.set('include_tags', tags.include.join(','));

  statusEl.textContent = 'Refreshing results...';

  try {
    const response = await fetch(`/api/posts?${params.toString()}`, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const filteredPosts = applySignalTypeFilter(data.posts || []);
    renderPosts(filteredPosts);
    const count = filteredPosts.length;
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

function setModalOpen(isOpen) {
  setupModal.classList.toggle('hidden', !isOpen);
  document.body.classList.toggle('modal-active', isOpen);
}

function setSetupFormBusy(isBusy) {
  collectBtn.disabled = isBusy;
  closeSetupBtn.disabled = isBusy;
  addTargetBtn.disabled = isBusy;
  autofillTargetsBtn.disabled = isBusy;
  startDateInput.disabled = isBusy;
  endDateInput.disabled = isBusy;
  for (const row of targetsList.querySelectorAll('.target-row')) {
    for (const control of row.querySelectorAll('input, select, button')) {
      control.disabled = isBusy;
    }
  }
}

function autofillTargetUsernames() {
  const usernameInputs = Array.from(targetsList.querySelectorAll('.target-username'));
  if (!usernameInputs.length) return;

  const firstValue = (usernameInputs[0].value || '').trim();
  if (!firstValue) {
    setupStatus.textContent = 'Enter the first username, then use Autofill Usernames.';
    return;
  }

  for (let i = 1; i < usernameInputs.length; i += 1) {
    usernameInputs[i].value = firstValue;
  }
  setupStatus.textContent = 'Filled all target usernames from the first row.';
}

function formatTargetLabel(target) {
  return `${target.platform}/${target.username}`;
}

function summarizeErrors(errors) {
  if (!Array.isArray(errors) || !errors.length) return '';
  const labels = errors.map((item) => formatTargetLabel(item));
  return labels.join(', ');
}

async function parseErrorResponse(response) {
  let payload = null;
  try {
    payload = await response.json();
  } catch (_error) {
    payload = null;
  }

  const errorData = payload?.error || {};
  if (errorData.code === 'username_not_found') {
    const platform = errorData.platform || 'source';
    const username = errorData.username || 'unknown';
    return `${platform} username "${username}" was not found.`;
  }
  if (errorData.message) return errorData.message;
  return `HTTP ${response.status}`;
}

async function collectAndOpen(event) {
  event.preventDefault();
  const targets = getTargetsFromForm();
  const startDate = startDateInput.value;
  const endDate = endDateInput.value;

  if (!targets.length || !startDate || !endDate) {
    setupStatus.textContent = 'At least one target and date range are required.';
    return;
  }
  if (endDate < startDate) {
    setupStatus.textContent = 'End date must be on or after start date.';
    return;
  }

  setSetupFormBusy(true);
  setupStatus.textContent = 'Collecting posts...';

  try {
    const response = await fetch('/api/collect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        targets,
        start_date: startDate,
        end_date: endDate,
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const data = await response.json();

    activeTargets = targets;
    activeUsername = targets.length === 1 ? targets[0].username : '';
    activeStartDate = startDate;
    activeEndDate = endDate;
    searchInput.value = '';

    const filteredPosts = applySignalTypeFilter(data.posts || []);
    renderPosts(filteredPosts);
    const themeStatus = data.theme_tagging?.status === 'ok' ? 'themes tagged' : 'theme tagging skipped';
    const errorSummary = summarizeErrors(data.errors);
    statusEl.textContent = `${filteredPosts.length || 0} result${(filteredPosts.length || 0) === 1 ? '' : 's'} • ${data.inserted || 0} new rows • ${themeStatus}${errorSummary ? ` • warnings: ${errorSummary}` : ''}`;
    setupStatus.textContent = errorSummary
      ? `Collected ${data.collected || 0}, inserted ${data.inserted || 0}. Skipped: ${errorSummary}`
      : `Collected ${data.collected || 0}, inserted ${data.inserted || 0}.`;
    setModalOpen(false);
  } catch (error) {
    console.error(error);
    setupStatus.textContent = `Collection failed: ${error.message || 'unknown error'}`;
  } finally {
    setSetupFormBusy(false);
  }
}

searchInput.addEventListener('input', queueRefresh);
sortSelect.addEventListener('change', queueRefresh);
setupForm.addEventListener('submit', collectAndOpen);
for (const el of [filterTwitter, filterReddit, filterTiktok, filterBluesky, filterYoutube, filterPost, filterRepost, filterReply, filterQuote, filterComment, filterSelectors, filterIdeologicalIndicators, filterThreatSignals]) {
  el.addEventListener('change', queueRefresh);
}
entityMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const pill = target.closest('[data-entity-tag]');
  if (!(pill instanceof HTMLElement)) return;
  const tag = String(pill.getAttribute('data-entity-tag') || '').trim().toLowerCase();
  if (!tag) return;
  if (activeEntityFilters.has(tag)) {
    activeEntityFilters.delete(tag);
  } else {
    activeEntityFilters.add(tag);
  }
  renderEntityMix(latestPosts);
  queueRefresh();
});
threatMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const row = target.closest('[data-post-index]');
  if (!(row instanceof HTMLElement)) return;
  const index = Number(row.getAttribute('data-post-index'));
  if (Number.isNaN(index)) return;
  scrollToPost(index);
});
selectorMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const row = target.closest('[data-post-index]');
  if (!(row instanceof HTMLElement)) return;
  const index = Number(row.getAttribute('data-post-index'));
  if (Number.isNaN(index)) return;
  scrollToPost(index);
});
threatSignalMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const row = target.closest('[data-post-index]');
  if (!(row instanceof HTMLElement)) return;
  const index = Number(row.getAttribute('data-post-index'));
  if (Number.isNaN(index)) return;
  scrollToPost(index);
});
filterToggleBtn.addEventListener('click', () => {
  const isHidden = filterPanel.classList.toggle('hidden');
  filterToggleBtn.setAttribute('aria-expanded', String(!isHidden));
});
document.addEventListener('click', (event) => {
  if (!(event.target instanceof Node)) return;
  if (filterPanel.classList.contains('hidden')) return;
  if (filterPanel.contains(event.target) || filterToggleBtn.contains(event.target)) return;
  filterPanel.classList.add('hidden');
  filterToggleBtn.setAttribute('aria-expanded', 'false');
});
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  if (filterPanel.classList.contains('hidden')) return;
  filterPanel.classList.add('hidden');
  filterToggleBtn.setAttribute('aria-expanded', 'false');
});
newCollectionBtn.addEventListener('click', () => {
  setupStatus.textContent = '';
  targetsList.innerHTML = '';
  if (activeTargets.length) {
    for (const target of activeTargets) addTargetRow(target.platform, target.username);
  } else if (activeUsername) {
    addTargetRow('twitter', `@${activeUsername}`);
  } else {
    addTargetRow('twitter', '@johnsmith');
  }
  setModalOpen(true);
});
addTargetBtn.addEventListener('click', () => addTargetRow('twitter', ''));
autofillTargetsBtn.addEventListener('click', autofillTargetUsernames);
closeSetupBtn.addEventListener('click', () => setModalOpen(false));
targetsList.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement) || !target.classList.contains('target-remove')) return;
  const row = target.closest('.target-row');
  if (!row) return;
  row.remove();
  if (!targetsList.querySelector('.target-row')) addTargetRow('twitter', '');
});
retagThemesBtn.addEventListener('click', async () => {
  retagThemesBtn.disabled = true;
  const original = retagThemesBtn.textContent;
  retagThemesBtn.textContent = 'Tagging...';
  try {
    const response = await fetch('/api/themes/tag', { method: 'POST' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    statusEl.textContent = data.status === 'ok'
      ? `Theme tagging complete: ${data.tagged || 0} posts, ${data.topics || 0} topics`
      : `Theme tagging skipped: ${data.reason || 'unknown'}`;
    await refreshPosts();
  } catch (error) {
    console.error(error);
    statusEl.textContent = 'Theme tagging failed.';
  } finally {
    retagThemesBtn.disabled = false;
    retagThemesBtn.textContent = original || 'Tag Themes';
  }
});
quitBtn.addEventListener('click', async () => {
  const ok = window.confirm('Quit PANOPTO and wipe collected session data?');
  if (!ok) return;
  quitBtn.disabled = true;
  quitBtn.textContent = 'Quitting...';
  try {
    await fetch('/api/session/end', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ shutdown: true }),
      keepalive: true,
    });
    statusEl.textContent = 'Session ended. Database wiped.';
    resultsEl.innerHTML = '<div class="empty">PANOPTO session ended. Restart server to collect again.</div>';
  } catch (error) {
    console.error(error);
    statusEl.textContent = 'Failed to end session cleanly.';
  }
});
initializeDateInputs();
addTargetRow('twitter', '@johnsmith');
setModalOpen(true);
