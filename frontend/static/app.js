const searchInput = document.getElementById('searchInput');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const sortSelect = document.getElementById('sortSelect');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const collectionContext = document.getElementById('collectionContext');
const contextTargets = document.getElementById('contextTargets');
const contextRange = document.getElementById('contextRange');
const setupModal = document.getElementById('setupModal');
const setupForm = document.getElementById('setupForm');
const setupStatus = document.getElementById('setupStatus');
const setupTitle = document.getElementById('setupTitle');
const setupSubtitle = document.getElementById('setupSubtitle');
const modeChooser = document.getElementById('modeChooser');
const modeReconBtn = document.getElementById('modeReconBtn');
const modeCollectionBtn = document.getElementById('modeCollectionBtn');
const reconForm = document.getElementById('reconForm');
const reconUsernameInput = document.getElementById('reconUsernameInput');
const reconBtn = document.getElementById('reconBtn');
const reconResults = document.getElementById('reconResults');
const reconStatus = document.getElementById('reconStatus');
const useReconTargetsBtn = document.getElementById('useReconTargetsBtn');
const closeSetupBtn = document.getElementById('closeSetupBtn');
const targetsList = document.getElementById('targetsList');
const addTargetBtn = document.getElementById('addTargetBtn');
const autofillTargetsBtn = document.getElementById('autofillTargetsBtn');
const startDateInput = document.getElementById('startDateInput');
const endDateInput = document.getElementById('endDateInput');
const collectBtn = document.getElementById('collectBtn');
const newCollectionBtn = document.getElementById('newCollectionBtn');
const quitBtn = document.getElementById('quitBtn');
const filterToggleBtn = document.getElementById('filterToggleBtn');
const filterPanel = document.getElementById('filterPanel');
const filterTwitter = document.getElementById('filterTwitter');
const filterReddit = document.getElementById('filterReddit');
const filterTiktok = document.getElementById('filterTiktok');
const filterBluesky = document.getElementById('filterBluesky');
const filterInstagram = document.getElementById('filterInstagram');
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
const leadsList = document.getElementById('leadsList');
const leadsEmpty = document.getElementById('leadsEmpty');
const insightsTabOps = document.getElementById('insightsTabOps');
const insightsTabGeo = document.getElementById('insightsTabGeo');
const insightsTabSignals = document.getElementById('insightsTabSignals');
const insightsPanelOps = document.getElementById('insightsPanelOps');
const insightsPanelGeo = document.getElementById('insightsPanelGeo');
const insightsPanelSignals = document.getElementById('insightsPanelSignals');
const collectionStreams = document.getElementById('collectionStreams');
const collectionStreamsSummary = document.getElementById('collectionStreamsSummary');
const collectionStreamsEmpty = document.getElementById('collectionStreamsEmpty');
const refreshStreamsBtn = document.getElementById('refreshStreamsBtn');
const rerunFailedBtn = document.getElementById('rerunFailedBtn');
const notificationsEl = document.getElementById('notifications');

let requestTimer;
let controller;
let activeStartDate = '';
let activeEndDate = '';
let activeUsername = '';
let activeTargets = [];
let latestPosts = [];
let reconTargets = [];
let reconLeads = [];
let modalMode = 'chooser';
let activeInsightsTab = 'ops';
const activeEntityFilters = new Set();
const activeMixFilters = new Set();
let activeCollectionJobId = '';
let collectionPollTimer = null;
let collectionLoadedAnyData = false;
let lockModalUntilCollectionData = false;
let lastCollectionPhase = '';
let collectionPollNonce = 0;
let lastCollectionUpdatedAt = '';
let dashboardBaseStatus = '';
let collectionProgressStatus = '';
let collectionAppendMode = false;
const collectionSourceState = new Map();
const collectionNoticeKeys = new Set();
const collectionIssueKeys = new Set();
const TARGET_PLATFORM_OPTIONS = [
  { value: 'twitter', label: 'Twitter/X' },
  { value: 'reddit', label: 'Reddit' },
  { value: 'tiktok', label: 'TikTok' },
  { value: 'bluesky', label: 'Bluesky' },
  { value: 'instagram', label: 'Instagram' },
  { value: 'youtube', label: 'YouTube' },
];
const TARGET_PLACEHOLDER_BY_PLATFORM = {
  twitter: '@johnsmith',
  reddit: 'u/johnsmith',
  tiktok: '@johnsmith',
  bluesky: '@johnsmith.bsky.social',
  instagram: '@johnsmith',
  youtube: '@johnsmith',
};
const SOURCE_ORDER = ['twitter', 'reddit', 'tiktok', 'bluesky', 'instagram', 'youtube'];
let locationMapLibraryPromise;
let locationMapInstance;
let locationMapLayer;
let latestLocationMapPoints = [];
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

function ensureTargetPlatformOptions(selectEl) {
  if (!(selectEl instanceof HTMLSelectElement)) return;
  const existingValues = new Set(Array.from(selectEl.options).map((option) => option.value));
  for (const item of TARGET_PLATFORM_OPTIONS) {
    if (existingValues.has(item.value)) continue;
    const option = document.createElement('option');
    option.value = item.value;
    option.textContent = item.label;
    selectEl.appendChild(option);
  }
}

function addTargetRow(platform = 'twitter', username = '') {
  const normalizedPlatform = String(platform || '').trim().toLowerCase();
  const supportedValues = new Set(TARGET_PLATFORM_OPTIONS.map((item) => item.value));
  const selectedPlatform = supportedValues.has(normalizedPlatform) ? normalizedPlatform : 'twitter';
  const row = document.createElement('div');
  row.className = 'target-row';
  row.innerHTML = `
    <select class="target-platform" aria-label="Target platform">
      ${TARGET_PLATFORM_OPTIONS.map((item) => `<option value="${item.value}">${item.label}</option>`).join('')}
    </select>
    <input class="target-username" type="text" autocomplete="off" />
    <button class="icon-btn target-remove" type="button" title="Remove target">×</button>
  `;
  targetsList.appendChild(row);
  const platformEl = row.querySelector('.target-platform');
  ensureTargetPlatformOptions(platformEl);
  platformEl.value = selectedPlatform;
  if (platformEl.value !== selectedPlatform) {
    // Defensive fallback for unexpected platform values from recon payloads.
    const fallbackOption = document.createElement('option');
    fallbackOption.value = selectedPlatform;
    fallbackOption.textContent = selectedPlatform.charAt(0).toUpperCase() + selectedPlatform.slice(1);
    platformEl.appendChild(fallbackOption);
    platformEl.value = selectedPlatform;
  }
  const usernameEl = row.querySelector('.target-username');
  usernameEl.value = username;
  usernameEl.placeholder = TARGET_PLACEHOLDER_BY_PLATFORM[selectedPlatform] || 'username';
  platformEl.addEventListener('change', () => {
    const nextPlatform = String(platformEl.value || '').trim().toLowerCase();
    usernameEl.placeholder = TARGET_PLACEHOLDER_BY_PLATFORM[nextPlatform] || 'username';
  });
}

function normalizeTargetUsername(platform, rawUsername) {
  let username = String(rawUsername || '').trim();
  if (!username) return '';
  if (platform === 'twitter') {
    const match = username.match(/^https?:\/\/(?:www\.)?(?:x|twitter)\.com\/([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
  }
  if (platform === 'reddit') {
    const match = username.match(/^https?:\/\/(?:www\.)?reddit\.com\/(?:user|u)\/([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
  }
  if (platform === 'tiktok') {
    const match = username.match(/^https?:\/\/(?:www\.)?tiktok\.com\/@([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
  }
  if (platform === 'bluesky') {
    const match = username.match(/^https?:\/\/(?:www\.)?bsky\.app\/profile\/([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
    username = username.replace(/\.bsky\.social$/i, '');
  }
  if (platform === 'youtube') {
    const match = username.match(/^https?:\/\/(?:www\.)?youtube\.com\/@([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
  }
  if (platform === 'instagram') {
    const match = username.match(/^https?:\/\/(?:www\.)?instagram\.com\/([^/?#]+)/i);
    if (match) username = decodeURIComponent(match[1] || '').trim();
  }
  username = username.split('/')[0];
  username = username.replace(/^@+/, '').replace(/^u\//i, '');
  return username.trim();
}

function adjustTargetUsernameForCollection(platform, normalizedUsername) {
  const username = String(normalizedUsername || '').trim();
  if (!username) return '';
  if (platform === 'reddit') {
    return username.toLowerCase().startsWith('u/') ? username : `u/${username}`;
  }
  if (platform === 'bluesky') {
    if (username.toLowerCase().startsWith('did:')) return username;
    return username.includes('.') ? username : `${username}.bsky.social`;
  }
  if (platform === 'twitter' || platform === 'tiktok' || platform === 'instagram' || platform === 'youtube') {
    return username.startsWith('@') ? username : `@${username}`;
  }
  return username;
}

function getTargetsFromForm() {
  const targets = [];
  for (const row of targetsList.querySelectorAll('.target-row')) {
    const platformEl = row.querySelector('.target-platform');
    const usernameEl = row.querySelector('.target-username');
    if (!platformEl || !usernameEl) continue;
    const platform = platformEl.value.trim().toLowerCase();
    const normalizedUsername = normalizeTargetUsername(platform, usernameEl.value);
    if (!normalizedUsername) continue;
    const adjustedUsername = adjustTargetUsernameForCollection(platform, normalizedUsername);
    targets.push({ platform, username: adjustedUsername });
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
  if (filterInstagram.checked) include.push('instagram');
  if (filterYoutube.checked) include.push('youtube');
  if (filterPost.checked) include.push('post');
  if (filterRepost.checked) include.push('repost');
  if (filterReply.checked) include.push('reply');
  if (filterQuote.checked) include.push('quote');
  if (filterComment.checked) include.push('comment');
  for (const tag of activeEntityFilters) include.push(tag);

  return { include };
}

function postHasPhoto(post) {
  const media = Array.isArray(post?.metadata?.media) ? post.metadata.media : [];
  if (media.some((item) => String(item?.type || '').toLowerCase() === 'image')) return true;
  const urls = Array.isArray(post?.metadata?.image_urls) ? post.metadata.image_urls : [];
  return urls.length > 0;
}

function postHasVideo(post) {
  const media = Array.isArray(post?.metadata?.media) ? post.metadata.media : [];
  if (media.some((item) => String(item?.type || '').toLowerCase() === 'video')) return true;
  return Boolean(String(post?.metadata?.video_url || '').trim());
}

function applySignalTypeFilter(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  const selectorsOn = Boolean(filterSelectors?.checked);
  const ideologicalOn = Boolean(filterIdeologicalIndicators?.checked);
  const threatOn = Boolean(filterThreatSignals?.checked);
  if (!selectorsOn && !ideologicalOn && !threatOn) return rows;
  return rows.filter((post) => {
    const hasSelectors = Array.isArray(post?.selector_matches) && post.selector_matches.length > 0;
    const ideologicalCategories = Array.isArray(post?.threat_categories) ? post.threat_categories : [];
    const threatSignalCategories = Array.isArray(post?.threat_signal_categories) ? post.threat_signal_categories : [];
    const hasIdeologicalIndicators = ideologicalCategories.length > 0;
    const hasThreatSignals = threatSignalCategories.length > 0 || (Array.isArray(post?.threat_matches) && post.threat_matches.length > 0);
    return (
      (selectorsOn && hasSelectors)
      || (ideologicalOn && hasIdeologicalIndicators)
      || (threatOn && hasThreatSignals)
    );
  });
}

function applyMixFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activeMixFilters.size) return rows;
  return rows.filter((post) => {
    for (const filter of activeMixFilters) {
      if (filter.startsWith('type:')) {
        const expected = filter.slice(5);
        const actual = String(post?.post_type || 'post').toLowerCase();
        if (actual !== expected) return false;
        continue;
      }
      if (filter === 'media:photo' && !postHasPhoto(post)) return false;
      if (filter === 'media:video' && !postHasVideo(post)) return false;
    }
    return true;
  });
}

function applyDashboardFilters(posts) {
  return applyMixFilters(applySignalTypeFilter(posts));
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
  if (!keywordChart || !keywordEmpty) return;
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
    counts.set(`type:${type}`, (counts.get(`type:${type}`) || 0) + 1);
    if (postHasPhoto(post)) counts.set('media:photo', (counts.get('media:photo') || 0) + 1);
    if (postHasVideo(post)) counts.set('media:video', (counts.get('media:video') || 0) + 1);
  }
  const order = ['type:post', 'type:comment', 'type:reply', 'type:quote', 'type:repost', 'media:photo', 'media:video'];
  const items = Array.from(counts.entries()).sort((a, b) => {
    const ai = order.indexOf(a[0]);
    const bi = order.indexOf(b[0]);
    if (ai >= 0 && bi >= 0) return ai - bi;
    if (ai >= 0) return -1;
    if (bi >= 0) return 1;
    return a[0].localeCompare(b[0]);
  });
  typeMix.innerHTML = items
    .map(([tag, count]) => {
      const label = tag.startsWith('type:') ? tag.slice(5) : tag.replace('media:', '');
      const activeClass = activeMixFilters.has(tag) ? ' is-active' : '';
      return `<button type="button" class="mix-pill mix-filter-pill${activeClass}" data-mix-filter="${escapeHtml(tag)}"><span>${escapeHtml(label)}</span><strong>${count}</strong></button>`;
    })
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

function updateLocationMapViewport(points) {
  if (!locationMapInstance) return;
  const rows = Array.isArray(points) ? points : [];
  if (!rows.length) {
    locationMapInstance.setView([20, 0], 2);
    return;
  }
  const bounds = rows.slice(0, 60).map((point) => [point.lat, point.lon]);
  if (bounds.length === 1) {
    locationMapInstance.setView(bounds[0], 4);
  } else {
    locationMapInstance.fitBounds(bounds, { padding: [20, 20], maxZoom: 4 });
  }
}

function refreshMapLayout() {
  if (!locationMapInstance) return;
  window.requestAnimationFrame(() => {
    locationMapInstance.invalidateSize();
    updateLocationMapViewport(latestLocationMapPoints);
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
  latestLocationMapPoints = points;
  const totalMentions = points.reduce((sum, point) => sum + point.count, 0);
  locationMapTotal.textContent = `${totalMentions} mention${totalMentions === 1 ? '' : 's'}`;
  locationMapEmpty.classList.toggle('hidden', points.length > 0);

  ensureLocationMapInstance()
    .then((L) => {
      if (!L || !locationMapLayer || !locationMapInstance) return;
      locationMapLayer.clearLayers();
      if (!points.length) {
        updateLocationMapViewport(points);
        return;
      }
      const maxCount = Math.max(...points.map((point) => point.count), 1);
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
      }
      updateLocationMapViewport(points);
      if (activeInsightsTab === 'geo') refreshMapLayout();
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
  const grouped = new Map();
  for (let i = 0; i < posts.length; i += 1) {
    const categories = Array.isArray(posts[i]?.threat_signal_categories) ? posts[i].threat_signal_categories : [];
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

  dashboardBaseStatus = '';
  updateStatusLine();

  try {
    const response = await fetch(`/api/posts?${params.toString()}`, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const filteredPosts = applyDashboardFilters(data.posts || []);
    renderPosts(filteredPosts);
    dashboardBaseStatus = '';
    updateStatusLine();
  } catch (error) {
    if (error.name === 'AbortError') return;
    console.error(error);
    dashboardBaseStatus = 'Failed to load posts.';
    updateStatusLine();
    resultsEl.innerHTML = '<div class="empty">Could not load data from /api/posts.</div>';
  }
}

function queueRefresh() {
  clearTimeout(requestTimer);
  requestTimer = setTimeout(refreshPosts, 250);
}

function setModalOpen(isOpen) {
  if (!isOpen && lockModalUntilCollectionData && !collectionLoadedAnyData) {
    setupStatus.textContent = 'Please wait. Dashboard opens after first result arrives.';
    showNotificationOnce('wait_first_results', 'Waiting for first results', 'warn');
    return;
  }
  setupModal.classList.toggle('hidden', !isOpen);
  document.body.classList.toggle('modal-active', isOpen);
}

function setModalMode(mode) {
  modalMode = mode;
  const chooser = mode === 'chooser';
  const recon = mode === 'recon';
  const collection = mode === 'collection';
  modeChooser.classList.toggle('hidden', !chooser);
  reconForm.classList.toggle('hidden', !recon);
  setupForm.classList.toggle('hidden', !collection);
  if (chooser) {
    setupTitle.textContent = 'Start Session';
    setupSubtitle.textContent = 'Choose reconnaissance or go straight to collection.';
  } else if (recon) {
    setupTitle.textContent = 'Reconnaissance';
    setupSubtitle.textContent = 'Scan social platforms for active profiles from one @username handle.';
  } else {
    setupTitle.textContent = 'Start Collection';
    setupSubtitle.textContent = 'Set targets and date range to fetch and visualize.';
  }
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

function setReconBusy(isBusy) {
  reconBtn.disabled = isBusy;
  closeSetupBtn.disabled = isBusy;
  reconUsernameInput.disabled = isBusy;
  useReconTargetsBtn.disabled = isBusy || !reconTargets.length;
}

function getDefaultFaviconDomain(site) {
  const normalized = normalizePlatformName(site);
  if (normalized === 'twitter') return 'x.com';
  if (normalized === 'reddit') return 'reddit.com';
  if (normalized === 'tiktok') return 'tiktok.com';
  if (normalized === 'bluesky') return 'bsky.app';
  if (normalized === 'instagram') return 'instagram.com';
  if (normalized === 'youtube') return 'youtube.com';
  if (normalized === 'github') return 'github.com';
  if (normalized === 'facebook') return 'facebook.com';
  if (normalized === 'linkedin') return 'linkedin.com';
  return '';
}

function profileDomain(url) {
  const value = String(url || '').trim();
  if (!value) return '';
  try {
    const parsed = new URL(value);
    return String(parsed.hostname || '').replace(/^www\./i, '').toLowerCase();
  } catch (error) {
    return '';
  }
}

function faviconUrl(site, profileUrl) {
  const domain = profileDomain(profileUrl) || getDefaultFaviconDomain(site);
  if (!domain) return '';
  return `https://www.google.com/s2/favicons?domain=${encodeURIComponent(domain)}&sz=32`;
}

function faviconMarkup(site, profileUrl) {
  const iconUrl = faviconUrl(site, profileUrl);
  if (!iconUrl) return '';
  return `<img class="site-favicon" src="${escapeHtml(iconUrl)}" alt="" aria-hidden="true" loading="lazy" referrerpolicy="no-referrer" />`;
}

function toReconBadge(row, clsName = 'lead') {
  const label = String(row.site || 'unknown');
  const url = String(row.profile_url || '').trim();
  const icon = faviconMarkup(label, url);
  const content = `<span class="recon-label">${icon}<span>${escapeHtml(label)}</span></span>`;
  if (!url) return `<span class="recon-pill ${escapeHtml(clsName)}">${content}</span>`;
  return `<a class="recon-pill ${escapeHtml(clsName)} lead-link" target="_blank" rel="noopener noreferrer" href="${escapeHtml(url)}">${content}</a>`;
}

function renderReconResults(payload) {
  const results = Array.isArray(payload?.results) ? payload.results : [];
  const supportedPresent = results.filter((row) => row.status === 'present' && row.supported_for_collection);
  const leadPresent = results.filter((row) => row.status === 'present' && !row.supported_for_collection);
  const unknown = results.filter((row) => row.status === 'unknown');

  reconResults.classList.remove('hidden');
  reconResults.innerHTML = `
    <div class="recon-summary">
      Checked ${results.length} sites • ${supportedPresent.length} collection-ready • ${leadPresent.length} leads • ${unknown.length} unknown
    </div>
    <div class="recon-group">
      <p>Collection-ready profiles</p>
      <div class="recon-pills">
        ${supportedPresent.length
    ? supportedPresent.map((row) => toReconBadge(row, 'success')).join('')
    : '<span class="recon-pill">No supported active profiles detected</span>'}
      </div>
    </div>
    <div class="recon-group">
      <p>Unsupported leads</p>
      <div class="recon-pills">
        ${leadPresent.length ? leadPresent.map((row) => toReconBadge(row)).join('') : '<span class="recon-pill">No lead profiles detected</span>'}
      </div>
    </div>
  `;
}

function renderLeadsList() {
  if (!leadsList || !leadsEmpty) return;
  if (!reconLeads.length) {
    leadsList.innerHTML = '';
    leadsEmpty.classList.remove('hidden');
    return;
  }
  leadsEmpty.classList.add('hidden');
  leadsList.innerHTML = reconLeads
    .map((lead) => {
      const label = String(lead.site || '').trim() || 'lead';
      const url = String(lead.profile_url || '').trim();
      const icon = faviconMarkup(label, url);
      const content = `<span class="row-label">${icon}<span class="row-label-text">${escapeHtml(label)}</span></span>`;
      if (url) {
        return `<a class="signal-row lead-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${content}<strong>open</strong></a>`;
      }
      return `<div class="signal-row">${content}<strong>lead</strong></div>`;
    })
    .join('');
}

function fillTargetsFromRecon(targets) {
  const rows = Array.isArray(targets) ? targets : [];
  targetsList.innerHTML = '';
  const displayUsernameForPlatform = (platform, username) => {
    const value = String(username || '').trim();
    if (!value) return '';
    if (platform === 'reddit') {
      return value.toLowerCase().startsWith('u/') ? value : `u/${value.replace(/^u\//i, '')}`;
    }
    if (platform === 'twitter' || platform === 'tiktok' || platform === 'bluesky' || platform === 'instagram' || platform === 'youtube') {
      return value.startsWith('@') ? value : `@${value}`;
    }
    return value;
  };
  if (!rows.length) {
    addTargetRow('twitter', '');
    return;
  }
  for (const target of rows) {
    const platform = String(target.platform || '').trim().toLowerCase();
    const username = displayUsernameForPlatform(platform, target.username);
    addTargetRow(platform || 'twitter', username);
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

function normalizePlatformName(value) {
  const platform = String(value || '').trim().toLowerCase();
  if (!platform) return '';
  if (platform === 'x' || platform === 'twitter/x' || platform === 'x.com') return 'twitter';
  return platform;
}

function platformDisplayName(platform) {
  const normalized = normalizePlatformName(platform);
  if (normalized === 'twitter') return 'Twitter/X';
  if (normalized === 'reddit') return 'Reddit';
  if (normalized === 'tiktok') return 'TikTok';
  if (normalized === 'bluesky') return 'Bluesky';
  if (normalized === 'instagram') return 'Instagram';
  if (normalized === 'youtube') return 'YouTube';
  return normalized || 'Unknown';
}

function targetStateKey(platform, username) {
  const normalizedPlatform = normalizePlatformName(platform);
  let normalizedUsername = String(username || '').trim().toLowerCase();
  if (normalizedPlatform === 'twitter' || normalizedPlatform === 'tiktok' || normalizedPlatform === 'instagram' || normalizedPlatform === 'youtube') {
    normalizedUsername = normalizedUsername.replace(/^@+/, '');
  } else if (normalizedPlatform === 'reddit') {
    normalizedUsername = normalizedUsername.replace(/^u\//, '');
  }
  return `${normalizedPlatform}|${normalizedUsername}`;
}

function showNotification(message, type = 'info') {
  if (!notificationsEl) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = String(message || '').trim();
  notificationsEl.appendChild(toast);
  window.setTimeout(() => {
    toast.classList.add('fade-out');
    window.setTimeout(() => toast.remove(), 220);
  }, 4200);
}

function showNotificationOnce(key, message, type = 'info') {
  const normalizedKey = String(key || '').trim().toLowerCase();
  if (!normalizedKey) {
    showNotification(message, type);
    return;
  }
  if (collectionNoticeKeys.has(normalizedKey)) return;
  collectionNoticeKeys.add(normalizedKey);
  showNotification(message, type);
}

function updateStatusLine() {
  const base = String(dashboardBaseStatus || '').trim();
  const progress = String(collectionProgressStatus || '').trim();
  if (base && progress) {
    statusEl.textContent = `${base} • ${progress}`;
    return;
  }
  statusEl.textContent = base || progress || '';
}

function renderCollectionContext() {
  if (!collectionContext || !contextTargets || !contextRange) return;
  const targetCount = Array.isArray(activeTargets) ? activeTargets.length : 0;
  if (!targetCount || !activeStartDate || !activeEndDate) {
    collectionContext.classList.add('hidden');
    contextTargets.textContent = 'No active targets';
    contextRange.textContent = 'Date range unset';
    return;
  }
  const grouped = new Map();
  for (const target of activeTargets) {
    const platform = normalizePlatformName(target?.platform);
    if (!platform) continue;
    grouped.set(platform, (grouped.get(platform) || 0) + 1);
  }
  const platformBits = Array.from(grouped.entries())
    .map(([platform, count]) => `${platformDisplayName(platform)} ${count}`)
    .join(' • ');
  contextTargets.textContent = `${targetCount} target${targetCount === 1 ? '' : 's'}${platformBits ? ` • ${platformBits}` : ''}`;
  contextRange.textContent = `${activeStartDate} to ${activeEndDate}`;
  collectionContext.classList.remove('hidden');
}

function updateFilterToggleLabel() {
  if (!filterToggleBtn) return;
  let activeCount = 0;
  for (const el of [filterTwitter, filterReddit, filterTiktok, filterBluesky, filterInstagram, filterYoutube]) {
    if (!el?.checked) activeCount += 1;
  }
  for (const el of [filterPost, filterRepost, filterReply, filterQuote, filterComment]) {
    if (!el?.checked) activeCount += 1;
  }
  for (const el of [filterSelectors, filterIdeologicalIndicators, filterThreatSignals]) {
    if (el?.checked) activeCount += 1;
  }
  activeCount += activeEntityFilters.size;
  activeCount += activeMixFilters.size;
  filterToggleBtn.textContent = activeCount > 0 ? `Filters (${activeCount})` : 'Filters';
}

function setInsightsTab(tabName) {
  const next = String(tabName || '').trim().toLowerCase();
  if (!next) return;
  activeInsightsTab = next;
  const tabs = [
    { name: 'ops', btn: insightsTabOps, panel: insightsPanelOps },
    { name: 'geo', btn: insightsTabGeo, panel: insightsPanelGeo },
    { name: 'signals', btn: insightsTabSignals, panel: insightsPanelSignals },
  ];
  for (const item of tabs) {
    const active = item.name === next;
    item.btn?.classList.toggle('is-active', active);
    item.btn?.setAttribute('aria-selected', String(active));
    item.panel?.classList.toggle('hidden', !active);
  }
  if (next === 'geo') {
    refreshMapLayout();
    window.setTimeout(refreshMapLayout, 80);
  }
}

function getFailedTargetsFromStreamState() {
  const failed = [];
  for (const row of collectionSourceState.values()) {
    if (!row) continue;
    const status = String(row.status || '').trim().toLowerCase();
    if (status !== 'error' && status !== 'username_not_found' && status !== 'empty' && status !== 'blocked') continue;
    const platform = normalizePlatformName(row.platform);
    const username = String(row.username || '').trim();
    if (!platform || !username) continue;
    failed.push({ platform, username });
  }
  return failed;
}

function updateStreamActionButtons() {
  if (refreshStreamsBtn) {
    const canRefresh = Boolean(activeCollectionJobId);
    refreshStreamsBtn.disabled = !canRefresh;
    refreshStreamsBtn.title = canRefresh ? 'Fetch latest job status now' : 'No active collection job';
  }
  if (rerunFailedBtn) {
    const failedTargets = getFailedTargetsFromStreamState();
    const canRerun = !activeCollectionJobId && failedTargets.length > 0 && Boolean(activeStartDate && activeEndDate);
    rerunFailedBtn.disabled = !canRerun;
    rerunFailedBtn.title = canRerun ? 'Start a new collection for failed targets' : 'No failed targets to rerun';
  }
}

function buildProfileUrl(platform, username) {
  const normalizedPlatform = String(platform || '').trim().toLowerCase();
  const raw = String(username || '').trim();
  const user = raw.replace(/^@+/, '').replace(/^u\//i, '');
  if (!user) return '';
  if (normalizedPlatform === 'twitter') return `https://x.com/${user}`;
  if (normalizedPlatform === 'reddit') return `https://www.reddit.com/user/${user}`;
  if (normalizedPlatform === 'tiktok') return `https://www.tiktok.com/@${user}`;
  if (normalizedPlatform === 'bluesky') return `https://bsky.app/profile/${user}`;
  if (normalizedPlatform === 'instagram') return `https://www.instagram.com/${user}/`;
  if (normalizedPlatform === 'youtube') return `https://www.youtube.com/@${user}`;
  return '';
}

function addLeadEntry(site, profileUrl) {
  const cleanSite = String(site || '').trim();
  const cleanUrl = String(profileUrl || '').trim();
  if (!cleanSite && !cleanUrl) return;
  const key = `${cleanSite.toLowerCase()}|${cleanUrl.toLowerCase()}`;
  const existing = new Set(reconLeads.map((lead) => `${String(lead.site || '').toLowerCase()}|${String(lead.profile_url || '').toLowerCase()}`));
  if (existing.has(key)) return;
  reconLeads.push({ site: cleanSite || 'lead', profile_url: cleanUrl });
  renderLeadsList();
}

function resetCollectionSourceState() {
  collectionSourceState.clear();
  renderCollectionStreams();
}

function seedCollectionSourceState(targets) {
  const rows = Array.isArray(targets) ? targets : [];
  for (const target of rows) {
    const platform = normalizePlatformName(target?.platform);
    const username = String(target?.username || '').trim();
    if (!platform || !username) continue;
    const key = targetStateKey(platform, username);
    if (!collectionSourceState.has(key)) {
      collectionSourceState.set(key, {
        platform,
        username,
        status: 'pending',
        collected: 0,
      });
    }
  }
  renderCollectionStreams();
}

function applyCollectionPerTarget(perTargetRows) {
  const rows = Array.isArray(perTargetRows) ? perTargetRows : [];
  if (!rows.length) return;
  for (const row of rows) {
    const platform = normalizePlatformName(row?.platform);
    const username = String(row?.username || '').trim();
    if (!platform || !username) continue;
    const key = targetStateKey(platform, username);
    const previous = collectionSourceState.get(key) || {
      platform,
      username,
      status: 'pending',
      collected: 0,
    };
    const rawStatus = String(row?.status || previous.status || 'pending').trim().toLowerCase();
    const nextCollected = Number.isFinite(Number(row?.collected)) ? Number(row.collected) : previous.collected;
    const nextStatus = rawStatus === 'ok' && Math.max(0, nextCollected) === 0 ? 'empty' : rawStatus;
    collectionSourceState.set(key, {
      ...previous,
      status: nextStatus,
      collected: Math.max(0, nextCollected),
    });
    if (nextStatus === 'ok') {
      showNotificationOnce(`target_ok|${key}`, `${platformDisplayName(platform)} ${username} loaded (${Math.max(0, nextCollected)} posts).`, 'success');
    } else if (nextStatus === 'empty') {
      showNotificationOnce(`target_empty|${key}`, `${platformDisplayName(platform)} ${username} returned no posts.`, 'warn');
    } else if (nextStatus === 'blocked') {
      showNotificationOnce(`target_blocked|${key}`, `${platformDisplayName(platform)} ${username} blocked by source protection.`, 'warn');
    } else if (nextStatus === 'username_not_found') {
      showNotificationOnce(`target_nf|${key}`, `${platformDisplayName(platform)} ${username} not found.`, 'warn');
    } else if (nextStatus === 'error') {
      showNotificationOnce(`target_err|${key}`, `${platformDisplayName(platform)} ${username} failed.`, 'error');
    }
  }
  renderCollectionStreams();
}

function finalizePendingTargets(targets, finalStatus = 'ok') {
  const rows = Array.isArray(targets) ? targets : [];
  for (const target of rows) {
    const platform = normalizePlatformName(target?.platform);
    const username = String(target?.username || '').trim();
    if (!platform || !username) continue;
    const key = targetStateKey(platform, username);
    const current = collectionSourceState.get(key);
    if (!current) continue;
    const status = String(current.status || '').trim().toLowerCase();
    if (status !== 'pending') continue;
    collectionSourceState.set(key, { ...current, status: finalStatus });
  }
  renderCollectionStreams();
}

function renderCollectionStreams() {
  if (!collectionStreams || !collectionStreamsSummary || !collectionStreamsEmpty) return;
  const rows = Array.from(collectionSourceState.values());
  if (!rows.length) {
    collectionStreams.innerHTML = '';
    collectionStreamsEmpty.classList.remove('hidden');
    collectionStreamsSummary.textContent = 'Idle';
    updateStreamActionButtons();
    return;
  }

  collectionStreamsEmpty.classList.add('hidden');
  const grouped = new Map();
  for (const row of rows) {
    const platform = normalizePlatformName(row.platform);
    const current = grouped.get(platform) || { platform, targets: 0, collected: 0, ok: 0, pending: 0, issues: 0 };
    current.targets += 1;
    current.collected += Math.max(0, Number(row.collected || 0));
    if (row.status === 'ok') current.ok += 1;
    else if (row.status === 'username_not_found' || row.status === 'error' || row.status === 'empty' || row.status === 'blocked') current.issues += 1;
    else current.pending += 1;
    grouped.set(platform, current);
  }

  const ordered = Array.from(grouped.values()).sort((a, b) => {
    const ai = SOURCE_ORDER.indexOf(a.platform);
    const bi = SOURCE_ORDER.indexOf(b.platform);
    if (ai >= 0 && bi >= 0) return ai - bi;
    if (ai >= 0) return -1;
    if (bi >= 0) return 1;
    return a.platform.localeCompare(b.platform);
  });
  const totalPosts = ordered.reduce((sum, item) => sum + item.collected, 0);
  const totalTargets = ordered.reduce((sum, item) => sum + item.targets, 0);
  const totalPending = ordered.reduce((sum, item) => sum + item.pending, 0);
  const totalIssues = ordered.reduce((sum, item) => sum + item.issues, 0);
  collectionStreamsSummary.textContent = `${totalPosts} posts • ${totalTargets} targets`;

  collectionStreams.innerHTML = ordered.map((item) => {
    const statusClass = item.issues ? 'error' : item.pending ? 'running' : (item.ok ? 'ok' : 'warn');
    const metaBits = [
      `${item.targets} target${item.targets === 1 ? '' : 's'}`,
      item.pending ? `${item.pending} pending` : '',
      item.issues ? `${item.issues} issue${item.issues === 1 ? '' : 's'}` : '',
    ].filter(Boolean);
    return `
      <div class="stream-row">
        <div class="stream-row-head">
          <span class="stream-label">
            <span class="stream-dot ${statusClass}" aria-hidden="true"></span>
            <span class="stream-name">${escapeHtml(platformDisplayName(item.platform))}</span>
          </span>
          <span class="stream-count">${item.collected}</span>
        </div>
        <div class="stream-meta">${escapeHtml(metaBits.join(' • ') || 'awaiting update')}</div>
      </div>
    `;
  }).join('');

  if (!totalPending && totalIssues) {
    showNotificationOnce('stream_summary_issue', `${totalIssues} target${totalIssues === 1 ? '' : 's'} reported issues.`, 'warn');
  }
  updateStreamActionButtons();
}

function processCollectionErrors(errors) {
  if (!Array.isArray(errors)) return;
  for (const row of errors) {
    const platform = normalizePlatformName(row?.platform);
    const username = String(row?.username || '').trim();
    const code = String(row?.code || 'collection_error').trim().toLowerCase();
    const key = `${platform}|${username.toLowerCase()}|${code}`;
    if (collectionIssueKeys.has(key)) continue;
    collectionIssueKeys.add(key);
    if (platform && username) {
      const stateKey = targetStateKey(platform, username);
      const current = collectionSourceState.get(stateKey) || { platform, username, status: 'pending', collected: 0 };
      const mappedStatus = code === 'username_not_found' ? 'username_not_found' : (code === 'blocked_by_protection' ? 'blocked' : 'error');
      collectionSourceState.set(stateKey, { ...current, status: mappedStatus });
    }

    const label = `${platform || 'source'} ${username || 'unknown'}`;
    if (code === 'username_not_found') {
      showNotification(`Not found: ${label}`, 'warn');
    } else if (code === 'blocked_by_protection') {
      showNotification(`Blocked by protection: ${label}`, 'warn');
    } else {
      showNotification(`Collection issue: ${label}`, 'error');
    }
    addLeadEntry(`${platform || 'source'} (${code})`, buildProfileUrl(platform, username));
  }
  renderCollectionStreams();
}

function clearCollectionPolling() {
  collectionPollNonce += 1;
  activeCollectionJobId = '';
  lastCollectionPhase = '';
  lastCollectionUpdatedAt = '';
  collectionProgressStatus = '';
  collectionAppendMode = false;
  if (collectionPollTimer) {
    clearTimeout(collectionPollTimer);
    collectionPollTimer = null;
  }
  updateStatusLine();
  updateStreamActionButtons();
}

function applyCollectionPayload(data) {
  const incomingPosts = Array.isArray(data?.posts) ? data.posts : [];
  const allPosts = collectionAppendMode ? mergePostsForAppend(latestPosts, incomingPosts) : incomingPosts;
  const filteredPosts = applyDashboardFilters(allPosts);
  renderPosts(filteredPosts);
  applyCollectionPerTarget(data?.per_target);
  dashboardBaseStatus = '';
  updateStatusLine();
}

function mergePostsForAppend(existingPosts, incomingPosts) {
  const merged = new Map();
  const rows = [...(Array.isArray(existingPosts) ? existingPosts : []), ...(Array.isArray(incomingPosts) ? incomingPosts : [])];
  for (const post of rows) {
    const source = String(post?.source_url || '').trim().toLowerCase();
    const key = source || [
      String(post?.platform || '').trim().toLowerCase(),
      String(post?.username || '').trim().toLowerCase(),
      String(post?.timestamp || '').trim(),
      String(post?.content || '').trim().toLowerCase(),
    ].join('|');
    if (!key) continue;
    const current = merged.get(key);
    if (!current) {
      merged.set(key, post);
      continue;
    }
    const currentSize = JSON.stringify(current || {}).length;
    const nextSize = JSON.stringify(post || {}).length;
    if (nextSize >= currentSize) {
      merged.set(key, post);
    }
  }
  return Array.from(merged.values());
}

function scheduleCollectionPoll(delayMs = 1000, nonce = collectionPollNonce) {
  if (!activeCollectionJobId) return;
  if (nonce !== collectionPollNonce) return;
  if (collectionPollTimer) clearTimeout(collectionPollTimer);
  collectionPollTimer = setTimeout(() => pollCollectionJob(nonce), delayMs);
}

async function pollCollectionJob(nonce = collectionPollNonce) {
  if (!activeCollectionJobId) return;
  if (nonce !== collectionPollNonce) return;
  try {
    const response = await fetch(`/api/collect/status?job_id=${encodeURIComponent(activeCollectionJobId)}`);
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const data = await response.json();
    if (nonce !== collectionPollNonce) return;
    seedCollectionSourceState(data.targets);
    const updatedAt = String(data.updated_at || '').trim();
    const hasJobChange = Boolean(updatedAt && updatedAt !== lastCollectionUpdatedAt);
    if (hasJobChange) {
      lastCollectionUpdatedAt = updatedAt;
    }
    const snapshot = data.snapshot;
    if (hasJobChange && snapshot && Array.isArray(snapshot.posts)) {
      applyCollectionPayload(snapshot);
      processCollectionErrors(snapshot.errors);
      if (snapshot.posts.length > 0 && !collectionLoadedAnyData) {
        collectionLoadedAnyData = true;
        lockModalUntilCollectionData = false;
        setModalOpen(false);
        showNotification('Initial results loaded', 'success');
      }
    }

    if (data.status === 'completed') {
      if (data.result && Array.isArray(data.result.posts)) {
        applyCollectionPayload(data.result);
        processCollectionErrors(data.result.errors);
        if (data.result.posts.length > 0 && !collectionLoadedAnyData) {
          collectionLoadedAnyData = true;
          lockModalUntilCollectionData = false;
          setModalOpen(false);
        }
      }
      finalizePendingTargets(data.targets, 'ok');
      lockModalUntilCollectionData = false;
      collectionProgressStatus = 'collection complete';
      updateStatusLine();
      showNotification('Collection complete', 'success');
      if (!collectionLoadedAnyData) {
        setupStatus.textContent = 'Collection completed with no posts found. Review targets/date range.';
      }
      clearCollectionPolling();
      return;
    }
    if (data.status === 'failed') {
      const message = data?.error?.message || 'background collection failed';
      collectionProgressStatus = `collection failed: ${message}`;
      updateStatusLine();
      finalizePendingTargets(data.targets, 'error');
      lockModalUntilCollectionData = false;
      addLeadEntry('collection failed', '');
      showNotification(`Collection failed: ${message}`, 'error');
      clearCollectionPolling();
      return;
    }

    const phase = String(data.phase || 'running').replace(/_/g, ' ');
    const stage = Number(data.current_stage || 0);
    const totalStages = Number(data.total_stages || 0);
    collectionProgressStatus = `collecting ${phase}${totalStages ? ` (${stage}/${totalStages})` : ''}`;
    updateStatusLine();
    if (lastCollectionPhase !== phase) {
      lastCollectionPhase = phase;
      showNotification(`Collection progress: ${phase}`, 'info');
    }
    if (lockModalUntilCollectionData) {
      setupStatus.textContent = `Collecting ${phase}${totalStages ? ` (${stage}/${totalStages})` : ''}... waiting for first results.`;
    }
    scheduleCollectionPoll(1200, nonce);
  } catch (error) {
    console.error(error);
    collectionProgressStatus = `collection status retrying: ${error.message || 'unknown error'}`;
    updateStatusLine();
    scheduleCollectionPoll(1600, nonce);
  }
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

async function runRecon(event) {
  event.preventDefault();
  const raw = String(reconUsernameInput.value || '').trim();
  if (!raw) {
    reconStatus.textContent = 'Username is required. Use @johnsmith format.';
    return;
  }
  if (!raw.startsWith('@')) {
    reconStatus.textContent = 'Enter username in @johnsmith format.';
    return;
  }

  setReconBusy(true);
  reconStatus.textContent = 'Running reconnaissance...';
  reconResults.classList.add('hidden');
  useReconTargetsBtn.classList.add('hidden');
  useReconTargetsBtn.disabled = true;
  reconTargets = [];

  try {
    const response = await fetch('/api/recon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: raw }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const payload = await response.json();
    reconTargets = Array.isArray(payload.collection_targets) ? payload.collection_targets : [];
    reconLeads = Array.isArray(payload.leads) ? payload.leads : [];
    renderReconResults(payload);
    renderLeadsList();
    if (reconTargets.length > 0) {
      useReconTargetsBtn.classList.remove('hidden');
      useReconTargetsBtn.disabled = false;
    } else {
      useReconTargetsBtn.classList.add('hidden');
      useReconTargetsBtn.disabled = true;
    }
    reconStatus.textContent = `Recon complete: ${payload.present_count || 0} profile(s) found.`;
  } catch (error) {
    console.error(error);
    useReconTargetsBtn.classList.add('hidden');
    useReconTargetsBtn.disabled = true;
    reconStatus.textContent = `Recon failed: ${error.message || 'unknown error'}`;
  } finally {
    setReconBusy(false);
  }
}

async function startBackgroundCollection(targets, startDate, endDate, options = {}) {
  const {
    lockModal = false,
    showStartNotification = true,
    setupMessage = 'Collection started.',
    statusPrefix = 'Collection',
    appendResults = false,
    resetStreamState = true,
  } = options;
  collectionLoadedAnyData = false;
  lockModalUntilCollectionData = Boolean(lockModal);
  lastCollectionPhase = '';
  lastCollectionUpdatedAt = '';
  collectionNoticeKeys.clear();
  collectionIssueKeys.clear();
  if (resetStreamState) {
    resetCollectionSourceState();
  }
  seedCollectionSourceState(targets);
  collectionProgressStatus = 'collection queued';
  updateStatusLine();

  try {
    const response = await fetch('/api/collect/start', {
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
    renderCollectionContext();
    searchInput.value = '';
    clearCollectionPolling();
    collectionAppendMode = Boolean(appendResults);
    activeCollectionJobId = String(data.job_id || '').trim();
    collectionPollNonce += 1;

    setupStatus.textContent = setupMessage;
    collectionProgressStatus = 'collection queued';
    updateStatusLine();
    if (showStartNotification) {
      showNotification(`${statusPrefix} started`, 'info');
    }
    setModalOpen(Boolean(lockModal));
    if (activeCollectionJobId) {
      scheduleCollectionPoll(150, collectionPollNonce);
    } else {
      collectionProgressStatus = 'collection failed: missing job id';
      updateStatusLine();
      showNotification(`${statusPrefix} failed: missing job id`, 'error');
    }
    updateStreamActionButtons();
    return true;
  } catch (error) {
    console.error(error);
    setupStatus.textContent = `${statusPrefix} failed: ${error.message || 'unknown error'}`;
    collectionProgressStatus = `collection failed: ${error.message || 'unknown error'}`;
    updateStatusLine();
    showNotification(`${statusPrefix} failed: ${error.message || 'unknown error'}`, 'error');
    updateStreamActionButtons();
    return false;
  }
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
  setupStatus.textContent = 'Starting background collection...';
  await startBackgroundCollection(targets, startDate, endDate, {
    lockModal: true,
    setupMessage: 'Collection started. Waiting for first results before opening dashboard.',
    statusPrefix: 'Collection',
    showStartNotification: true,
    appendResults: false,
    resetStreamState: true,
  });
  setSetupFormBusy(false);
}

searchInput.addEventListener('input', queueRefresh);
clearSearchBtn?.addEventListener('click', () => {
  if (!searchInput.value) return;
  searchInput.value = '';
  queueRefresh();
  searchInput.focus();
});
sortSelect.addEventListener('change', queueRefresh);
setupForm.addEventListener('submit', collectAndOpen);
reconForm.addEventListener('submit', runRecon);
for (const el of [filterTwitter, filterReddit, filterTiktok, filterBluesky, filterInstagram, filterYoutube, filterPost, filterRepost, filterReply, filterQuote, filterComment, filterSelectors, filterIdeologicalIndicators, filterThreatSignals]) {
  el.addEventListener('change', () => {
    updateFilterToggleLabel();
    queueRefresh();
  });
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
  updateFilterToggleLabel();
  queueRefresh();
});
typeMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const pill = target.closest('[data-mix-filter]');
  if (!(pill instanceof HTMLElement)) return;
  const tag = String(pill.getAttribute('data-mix-filter') || '').trim().toLowerCase();
  if (!tag) return;
  if (activeMixFilters.has(tag)) {
    activeMixFilters.delete(tag);
  } else {
    activeMixFilters.add(tag);
  }
  renderTypeMix(latestPosts);
  updateFilterToggleLabel();
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
  if (event.key === '/' && event.target instanceof Element && !event.target.closest('input, textarea, [contenteditable="true"]')) {
    event.preventDefault();
    searchInput.focus();
    return;
  }
  if (event.key !== 'Escape') return;
  if (filterPanel.classList.contains('hidden')) return;
  filterPanel.classList.add('hidden');
  filterToggleBtn.setAttribute('aria-expanded', 'false');
});
window.addEventListener('resize', () => {
  if (activeInsightsTab !== 'geo') return;
  refreshMapLayout();
});
insightsTabOps?.addEventListener('click', () => setInsightsTab('ops'));
insightsTabGeo?.addEventListener('click', () => setInsightsTab('geo'));
insightsTabSignals?.addEventListener('click', () => setInsightsTab('signals'));
refreshStreamsBtn?.addEventListener('click', () => {
  if (!activeCollectionJobId) return;
  showNotification('Refreshing collection status…', 'info');
  scheduleCollectionPoll(25, collectionPollNonce);
});
rerunFailedBtn?.addEventListener('click', async () => {
  if (activeCollectionJobId) return;
  const failedTargets = getFailedTargetsFromStreamState();
  if (!failedTargets.length) {
    showNotification('No failed targets to rerun.', 'warn');
    return;
  }
  const startDate = activeStartDate || startDateInput.value;
  const endDate = activeEndDate || endDateInput.value;
  if (!startDate || !endDate) {
    showNotification('Set a date range before rerunning failed targets.', 'warn');
    return;
  }
  rerunFailedBtn.disabled = true;
  if (refreshStreamsBtn) refreshStreamsBtn.disabled = true;
  await startBackgroundCollection(failedTargets, startDate, endDate, {
    lockModal: false,
    setupMessage: 'Rerunning failed collection targets in background.',
    statusPrefix: 'Failed-target rerun',
    showStartNotification: true,
    appendResults: true,
    resetStreamState: false,
  });
  updateStreamActionButtons();
});
newCollectionBtn.addEventListener('click', () => {
  setupStatus.textContent = '';
  reconStatus.textContent = '';
  reconResults.classList.add('hidden');
  setModalMode('collection');
  targetsList.innerHTML = '';
  resetCollectionSourceState();
  if (activeTargets.length) {
    for (const target of activeTargets) addTargetRow(target.platform, target.username);
  } else if (activeUsername) {
    addTargetRow('twitter', `@${activeUsername}`);
  } else {
    addTargetRow('twitter', '');
  }
  setModalOpen(true);
});
addTargetBtn.addEventListener('click', () => addTargetRow('twitter', ''));
autofillTargetsBtn.addEventListener('click', autofillTargetUsernames);
closeSetupBtn.addEventListener('click', () => setModalOpen(false));
modeReconBtn.addEventListener('click', () => {
  reconStatus.textContent = '';
  setModalMode('recon');
  reconUsernameInput.focus();
});
modeCollectionBtn.addEventListener('click', () => {
  setupStatus.textContent = '';
  setModalMode('collection');
  if (!targetsList.querySelector('.target-row')) addTargetRow('twitter', '');
});
useReconTargetsBtn.addEventListener('click', () => {
  if (!reconTargets.length) return;
  fillTargetsFromRecon(reconTargets);
  setupStatus.textContent = 'Loaded active recon profiles into collection targets.';
  setModalMode('collection');
});
targetsList.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement) || !target.classList.contains('target-remove')) return;
  const row = target.closest('.target-row');
  if (!row) return;
  row.remove();
  if (!targetsList.querySelector('.target-row')) addTargetRow('twitter', '');
});
quitBtn.addEventListener('click', async () => {
  const ok = window.confirm('Quit PANOPTO and wipe collected session data?');
  if (!ok) return;
  quitBtn.disabled = true;
  quitBtn.textContent = 'Quitting...';
  try {
    clearCollectionPolling();
    resetCollectionSourceState();
    activeTargets = [];
    activeStartDate = '';
    activeEndDate = '';
    renderCollectionContext();
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
addTargetRow('twitter', '');
renderLeadsList();
renderCollectionStreams();
setInsightsTab(activeInsightsTab);
updateStreamActionButtons();
updateFilterToggleLabel();
renderCollectionContext();
setModalMode('chooser');
setModalOpen(true);
