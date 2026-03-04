const searchInput = document.getElementById('searchInput');
const caseWorkspace = document.getElementById('caseWorkspace');
const caseTiles = document.getElementById('caseTiles');
const caseTilesEmpty = document.getElementById('caseTilesEmpty');
const caseSearchInput = document.getElementById('caseSearchInput');
const caseStatusFilter = document.getElementById('caseStatusFilter');
const caseThreatFilter = document.getElementById('caseThreatFilter');
const caseSortSelect = document.getElementById('caseSortSelect');
const openNewCaseBtn = document.getElementById('openNewCaseBtn');
const openConfigBtn = document.getElementById('openConfigBtn');
const generateDemoCaseBtn = document.getElementById('generateDemoCaseBtn');
const quitSessionCaseBtn = document.getElementById('quitSessionCaseBtn');
const quitSaveSessionCaseBtn = document.getElementById('quitSaveSessionCaseBtn');
const configModal = document.getElementById('configModal');
const configForm = document.getElementById('configForm');
const configPdlApiKeyInput = document.getElementById('configPdlApiKeyInput');
const configPdlApiKeyHint = document.getElementById('configPdlApiKeyHint');
const configOsintIndustriesApiKeyInput = document.getElementById('configOsintIndustriesApiKeyInput');
const configOsintIndustriesApiKeyHint = document.getElementById('configOsintIndustriesApiKeyHint');
const configOsintIndustriesPremiumInput = document.getElementById('configOsintIndustriesPremiumInput');
const configNumverifyApiKeyInput = document.getElementById('configNumverifyApiKeyInput');
const configNumverifyApiKeyHint = document.getElementById('configNumverifyApiKeyHint');
const configOpenAiApiKeyInput = document.getElementById('configOpenAiApiKeyInput');
const configOpenAiApiKeyHint = document.getElementById('configOpenAiApiKeyHint');
const configCustomKeywordInput = document.getElementById('configCustomKeywordInput');
const configCustomKeywordPills = document.getElementById('configCustomKeywordPills');
const configSaveBtn = document.getElementById('configSaveBtn');
const configCloseBtn = document.getElementById('configCloseBtn');
const configCancelBtn = document.getElementById('configCancelBtn');
const configStatus = document.getElementById('configStatus');
const configSecretStateSummary = document.getElementById('configSecretStateSummary');
const caseEditModal = document.getElementById('caseEditModal');
const caseEditForm = document.getElementById('caseEditForm');
const caseEditStatusSelect = document.getElementById('caseEditStatusSelect');
const caseEditCadenceField = document.getElementById('caseEditCadenceField');
const caseEditCadenceSelect = document.getElementById('caseEditCadenceSelect');
const caseEditThreatSelect = document.getElementById('caseEditThreatSelect');
const caseEditLocationSelect = document.getElementById('caseEditLocationSelect');
const caseEditCancelBtn = document.getElementById('caseEditCancelBtn');
const caseEditCloseBtn = document.getElementById('caseEditCloseBtn');
const caseEditSaveBtn = document.getElementById('caseEditSaveBtn');
const caseSaveModal = document.getElementById('caseSaveModal');
const caseSaveForm = document.getElementById('caseSaveForm');
const caseSaveTitleInput = document.getElementById('caseSaveTitleInput');
const caseSaveStatusSelect = document.getElementById('caseSaveStatusSelect');
const caseSaveCadenceField = document.getElementById('caseSaveCadenceField');
const caseSaveCadenceSelect = document.getElementById('caseSaveCadenceSelect');
const caseSaveThreatSelect = document.getElementById('caseSaveThreatSelect');
const caseSaveLocationInput = document.getElementById('caseSaveLocationInput');
const caseSaveImageOptions = document.getElementById('caseSaveImageOptions');
const caseSaveSubmitBtn = document.getElementById('caseSaveSubmitBtn');
const caseSaveCancelBtn = document.getElementById('caseSaveCancelBtn');
const caseSaveCloseBtn = document.getElementById('caseSaveCloseBtn');
const caseNotesModal = document.getElementById('caseNotesModal');
const caseNotesForm = document.getElementById('caseNotesForm');
const caseNotesNameInput = document.getElementById('caseNotesNameInput');
const caseNotesLocationInput = document.getElementById('caseNotesLocationInput');
const caseNotesAgeInput = document.getElementById('caseNotesAgeInput');
const caseNotesAkasInput = document.getElementById('caseNotesAkasInput');
const caseNotesSubjectImage = document.getElementById('caseNotesSubjectImage');
const caseNotesSubjectImageSelect = document.getElementById('caseNotesSubjectImageSelect');
const caseNotesSubjectUploadBtn = document.getElementById('caseNotesSubjectUploadBtn');
const caseNotesSubjectUploadInput = document.getElementById('caseNotesSubjectUploadInput');
const caseNotesContextInput = document.getElementById('caseNotesContextInput');
const caseNotesThreatInput = document.getElementById('caseNotesThreatInput');
const caseNotesPersonalInput = document.getElementById('caseNotesPersonalInput');
const caseNotesProfilesList = document.getElementById('caseNotesProfilesList');
const caseNotesAddProfileBtn = document.getElementById('caseNotesAddProfileBtn');
const caseNotesExportPdfBtn = document.getElementById('caseNotesExportPdfBtn');
const caseNotesSaveBtn = document.getElementById('caseNotesSaveBtn');
const caseNotesCloseBtn = document.getElementById('caseNotesCloseBtn');
const caseNotesCancelBtn = document.getElementById('caseNotesCancelBtn');
const dashboardPanel = document.getElementById('dashboardPanel');
const dashboardContent = document.getElementById('dashboardContent');
const openCaseNotesTopBtn = document.getElementById('openCaseNotesTopBtn');
const backToCasesBtn = document.getElementById('backToCasesBtn');
const saveQuitCaseBtn = document.getElementById('saveQuitCaseBtn');
const clearSearchBtn = document.getElementById('clearSearchBtn');
const sortSelect = document.getElementById('sortSelect');
const viewPostsBtn = document.getElementById('viewPostsBtn');
const viewMediaBtn = document.getElementById('viewMediaBtn');
const viewFootprintBtn = document.getElementById('viewFootprintBtn');
const viewPatternLifeBtn = document.getElementById('viewPatternLifeBtn');
const filterMenu = document.getElementById('filterMenu');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const footprintView = document.getElementById('footprintView');
const patternLifeView = document.getElementById('patternLifeView');
const footprintReconForm = document.getElementById('footprintReconForm');
const footprintSelectorsList = document.getElementById('footprintSelectorsList');
const addFootprintSelectorBtn = document.getElementById('addFootprintSelectorBtn');
const footprintReconBtn = document.getElementById('footprintReconBtn');
const footprintUseTargetsBtn = document.getElementById('footprintUseTargetsBtn');
const footprintReconResults = document.getElementById('footprintReconResults');
const footprintReconStatus = document.getElementById('footprintReconStatus');
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
const reconSelectorsList = document.getElementById('reconSelectorsList');
const addReconSelectorBtn = document.getElementById('addReconSelectorBtn');
const reconBtn = document.getElementById('reconBtn');
const reconResults = document.getElementById('reconResults');
const reconStatus = document.getElementById('reconStatus');
const useReconTargetsBtn = document.getElementById('useReconTargetsBtn');
const goReconAssessmentBtn = document.getElementById('goReconAssessmentBtn');
const closeSetupBtn = document.getElementById('closeSetupBtn');
const targetsList = document.getElementById('targetsList');
const addTargetBtn = document.getElementById('addTargetBtn');
const autofillTargetsBtn = document.getElementById('autofillTargetsBtn');
const startDateInput = document.getElementById('startDateInput');
const endDateInput = document.getElementById('endDateInput');
const collectBtn = document.getElementById('collectBtn');
const newCollectionBtn = document.getElementById('newCollectionBtn');
const quitBtn = document.getElementById('quitBtn');
const quitSaveBtn = document.getElementById('quitSaveBtn');
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
const filterLLMPrimary = document.getElementById('filterLLMPrimary');
const filterLLMSecondary = document.getElementById('filterLLMSecondary');
const runFaceRecognitionBtn = document.getElementById('runFaceRecognitionBtn');
const faceConfidenceRange = document.getElementById('faceConfidenceRange');
const faceConfidenceValue = document.getElementById('faceConfidenceValue');
const faceRecognitionStatus = document.getElementById('faceRecognitionStatus');
const faceRecognitionFilterList = document.getElementById('faceRecognitionFilterList');
const faceRecognitionFilterEmpty = document.getElementById('faceRecognitionFilterEmpty');
const timelineChart = document.getElementById('timelineChart');
const timelineEmpty = document.getElementById('timelineEmpty');
const timelineTotal = document.getElementById('timelineTotal');
const postingTimezoneMap = document.getElementById('postingTimezoneMap');
const postingTimezoneInference = document.getElementById('postingTimezoneInference');
const postingRhythmSummary = document.getElementById('postingRhythmSummary');
const postingHourChart = document.getElementById('postingHourChart');
const postingSourceMix = document.getElementById('postingSourceMix');
const postingRhythmEmpty = document.getElementById('postingRhythmEmpty');
const patternLifeTimezoneInference = document.getElementById('patternLifeTimezoneInference');
const patternLifeRhythmSummary = document.getElementById('patternLifeRhythmSummary');
const patternLifeHourChart = document.getElementById('patternLifeHourChart');
const patternLifeSourceMix = document.getElementById('patternLifeSourceMix');
const patternLifeRhythmEmpty = document.getElementById('patternLifeRhythmEmpty');
const keywordChart = document.getElementById('keywordChart');
const keywordEmpty = document.getElementById('keywordEmpty');
const typeMix = document.getElementById('typeMix');
const locationMap = document.getElementById('locationMap');
const locationMapEmpty = document.getElementById('locationMapEmpty');
const locationMapTotal = document.getElementById('locationMapTotal');
const patternLifeMap = document.getElementById('patternLifeMap');
const patternLifeMapEmpty = document.getElementById('patternLifeMapEmpty');
const patternLifeLocationMapTotal = document.getElementById('patternLifeLocationMapTotal');
const entityMix = document.getElementById('entityMix');
const entityMixEmpty = document.getElementById('entityMixEmpty');
const threatMix = document.getElementById('threatMix');
const threatMixEmpty = document.getElementById('threatMixEmpty');
const threatSignalMix = document.getElementById('threatSignalMix');
const threatSignalMixEmpty = document.getElementById('threatSignalMixEmpty');
const selectorMix = document.getElementById('selectorMix');
const selectorMixEmpty = document.getElementById('selectorMixEmpty');
const customKeywordMix = document.getElementById('customKeywordMix');
const customKeywordMixEmpty = document.getElementById('customKeywordMixEmpty');
const llmPrimaryRadar = document.getElementById('llmPrimaryRadar');
const llmPrimaryMix = document.getElementById('llmPrimaryMix');
const llmPrimaryMixEmpty = document.getElementById('llmPrimaryMixEmpty');
const llmSecondaryRadar = document.getElementById('llmSecondaryRadar');
const llmSecondaryMix = document.getElementById('llmSecondaryMix');
const llmSecondaryMixEmpty = document.getElementById('llmSecondaryMixEmpty');
const llmThemeMix = document.getElementById('llmThemeMix');
const llmThemeMixEmpty = document.getElementById('llmThemeMixEmpty');
const llmCoverageCard = document.getElementById('llmCoverageCard');
const llmCoveragePrimary = document.getElementById('llmCoveragePrimary');
const llmCoverageSecondary = document.getElementById('llmCoverageSecondary');
const aiThreatAssessmentCard = document.getElementById('aiThreatAssessmentCard');
const runAiThreatAssessmentBtn = document.getElementById('runAiThreatAssessmentBtn');
const aiThreatAssessmentStatus = document.getElementById('aiThreatAssessmentStatus');
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
const openManualInsertBtn = document.getElementById('openManualInsertBtn');
const manualInsertModal = document.getElementById('manualInsertModal');
const manualInsertForm = document.getElementById('manualInsertForm');
const manualInsertTextInput = document.getElementById('manualInsertTextInput');
const manualInsertFileInput = document.getElementById('manualInsertFileInput');
const manualInsertAuthorInput = document.getElementById('manualInsertAuthorInput');
const manualInsertUrlInput = document.getElementById('manualInsertUrlInput');
const manualInsertSourceInput = document.getElementById('manualInsertSourceInput');
const manualInsertSaveBtn = document.getElementById('manualInsertSaveBtn');
const manualInsertCloseBtn = document.getElementById('manualInsertCloseBtn');
const manualInsertCancelBtn = document.getElementById('manualInsertCancelBtn');
const manualInsertStatus = document.getElementById('manualInsertStatus');
const postModal = document.getElementById('postModal');
const postModalTitle = document.getElementById('postModalTitle');
const postModalBody = document.getElementById('postModalBody');
const postModalCloseBtn = document.getElementById('postModalCloseBtn');
const notificationsEl = document.getElementById('notifications');

let requestTimer;
let controller;
let caseList = [];
let activeCaseId = '';
let activeCase = null;
let activeCaseExplicitlySaved = false;
let editingCaseId = '';
const caseWatchlistCadenceById = new Map();
let caseSaveSelectedImageUrl = '';
let caseSaveImageChoices = [];
let caseNotesImageChoices = [];
let caseNotesKnownProfiles = [];
let activeStartDate = '';
let activeEndDate = '';
let activeUsername = '';
let activeTargets = [];
let latestPosts = [];
let latestRenderedPosts = [];
let activeResultsView = 'posts';
let reconTargets = [];
let reconLeads = [];
let reconProfiles = [];
let reconPersonDataProfile = {};
let reconPersonDataProfiles = [];
let reconOsintProfiles = [];
let reconNumverifyProfiles = [];
let modalMode = 'chooser';
let activeInsightsTab = 'ops';
const activeEntityFilters = new Set();
const activeMixFilters = new Set();
const activeSignalFilters = new Set();
const activeCustomKeywordFilters = new Set();
const activeFaceFilters = new Set();
let latestFaceClusters = [];
let latestFaceRecognition = { available: false, reason: 'not_run' };
let activeFaceMinConfidence = 0.8;
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
let activeThreatAssessmentEditorPostIndex = null;
const threatAssessmentSaveInFlight = new Set();
const collectionSourceState = new Map();
const collectionNoticeKeys = new Set();
const collectionIssueKeys = new Set();
let reconPreviewTooltipEl = null;
let activeReconPreviewAnchor = null;
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
let postingTimezoneMapInstance;
let postingTimezoneMapLayer;
let latestLocationMapPoints = [];
let patternLifeMapInstance;
let patternLifeMapLayer;
let latestPatternLifeMapPoints = [];
let configCustomKeywordList = [];
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

const THREAT_ORDER = {
  'Low Threat': 1,
  'Moderate Threat': 2,
  'Substantial Threat': 3,
  'High Threat': 4,
  'Very High Threat': 5,
};

function formatIsoDateTime(value) {
  const text = String(value || '').trim();
  if (!text) return 'Unknown';
  const date = new Date(text);
  if (Number.isNaN(date.getTime())) return 'Unknown';
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll('`', '&#96;');
}

function slugifyToken(value) {
  return String(value || '').trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

const USER_PLACEHOLDER_AVATAR_URL = `data:image/svg+xml,${encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="32" fill="#0f172a"/><circle cx="32" cy="24" r="12" fill="#94a3b8"/><path d="M13 54c2-11 9-17 19-17s17 6 19 17" fill="#94a3b8"/></svg>`,
)}`;

function normalizeProfileImageUrl(value) {
  const url = String(value || '').trim();
  if (isHttpUrl(url) || url.startsWith('data:image/')) return url;
  return '';
}

function profileImageFromMetadata(metadata) {
  if (!metadata || typeof metadata !== 'object') return '';
  const candidates = [
    metadata.profile_image_url,
    metadata.profile_image,
    metadata.avatar_url,
    metadata.avatar,
    metadata.author_avatar,
    metadata.user_avatar,
  ];
  for (const candidate of candidates) {
    const url = normalizeProfileImageUrl(candidate);
    if (url) return url;
  }
  return '';
}

function postProfileImageUrl(post) {
  return profileImageFromMetadata(post?.metadata || {});
}

function caseProfileImageUrl(row) {
  const url = normalizeProfileImageUrl(row?.poi_image_url);
  return url || USER_PLACEHOLDER_AVATAR_URL;
}

function showCaseWorkspace() {
  caseWorkspace?.classList.remove('hidden');
  dashboardPanel?.classList.add('hidden');
  dashboardContent?.classList.add('hidden');
  setModalOpen(false);
}

function showDashboard() {
  caseWorkspace?.classList.add('hidden');
  dashboardPanel?.classList.remove('hidden');
  dashboardContent?.classList.remove('hidden');
}

function caseRowMarkup(row) {
  const caseId = String(row?.case_id || '').trim();
  const caseName = String(row?.case_name || 'Untitled Case').trim() || 'Untitled Case';
  const status = String(row?.status || 'Open').trim() || 'Open';
  const threatLevel = String(row?.threat_level || 'Low Threat').trim() || 'Low Threat';
  const knownLocation = String(row?.known_location || '').trim() || 'Unknown';
  const openedAt = formatIsoDateTime(row?.opened_at);
  const editedAt = formatIsoDateTime(row?.last_edited_at);
  const postCount = Number(row?.post_count || 0);
  const statusCls = `status-${slugifyToken(status)}`;
  let threatCls = 'threat-low';
  if (threatLevel === 'Moderate Threat') threatCls = 'threat-moderate';
  else if (threatLevel === 'Substantial Threat') threatCls = 'threat-substantial';
  else if (threatLevel === 'High Threat') threatCls = 'threat-high';
  else if (threatLevel === 'Very High Threat') threatCls = 'threat-very-high';
  const poiImageUrl = caseProfileImageUrl(row);
  const poiImageAlt = `${caseName} profile image`;
  return `
    <article class="case-tile" data-case-id="${escapeAttr(caseId)}">
      <div class="case-tile-head">
        <div class="case-poi-avatar-wrap">
          <img class="case-poi-avatar" src="${escapeAttr(poiImageUrl)}" alt="${escapeAttr(poiImageAlt)}" loading="lazy" />
        </div>
        <div class="case-title-group">
          <h3>${escapeHtml(caseName)}</h3>
          <div class="case-tags">
            <span class="case-chip case-badge case-status ${escapeAttr(statusCls)}">${escapeHtml(status)}</span>
            <span class="case-chip case-badge threat ${escapeAttr(threatCls)}">${escapeHtml(threatLevel)}</span>
            <span class="case-chip case-tag case-tag-location">${escapeHtml(knownLocation)}</span>
            <span class="case-chip case-tag case-tag-collected">${postCount} Posts Collected</span>
          </div>
          <div class="case-submeta">
            <span>Opened ${escapeHtml(openedAt)}</span>
            <span>Edited ${escapeHtml(editedAt)}</span>
          </div>
        </div>
        <div class="case-icon-actions">
          <button class="icon-btn case-icon-btn case-open-icon" type="button" title="Open case" aria-label="Open case" data-case-open="${escapeAttr(caseId)}">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 4h8l4 4v12H6z"></path><path d="M14 4v4h4"></path></svg>
          </button>
          <button class="icon-btn case-icon-btn case-edit-icon" type="button" title="Edit case details" aria-label="Edit case details" data-case-edit="${escapeAttr(caseId)}">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 20l4.5-1 9.5-9.5-3.5-3.5L5 15.5z"></path><path d="M13.5 6l3.5 3.5"></path></svg>
          </button>
          <button class="icon-btn case-icon-btn case-delete-icon" type="button" title="Delete case" aria-label="Delete case" data-case-delete="${escapeAttr(caseId)}">
            <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16"></path><path d="M9 7V5h6v2"></path><path d="M8 10v8"></path><path d="M12 10v8"></path><path d="M16 10v8"></path></svg>
          </button>
        </div>
      </div>
    </article>
  `;
}

function filteredSortedCases() {
  const query = String(caseSearchInput?.value || '').trim().toLowerCase();
  const statusFilter = String(caseStatusFilter?.value || '').trim();
  const threatFilter = String(caseThreatFilter?.value || '').trim();
  const sortBy = String(caseSortSelect?.value || 'last_edited_desc').trim();
  const rows = caseList
    .filter((row) => {
      const name = String(row?.case_name || '').toLowerCase();
      const location = String(row?.known_location || '').toLowerCase();
      const tags = Array.isArray(row?.metadata_tags) ? row.metadata_tags.map((item) => String(item || '').toLowerCase()) : [];
      const tagHit = tags.some((tag) => tag.includes(query));
      if (query && !name.includes(query) && !location.includes(query) && !tagHit) return false;
      if (statusFilter && String(row?.status || '') !== statusFilter) return false;
      if (threatFilter && String(row?.threat_level || '') !== threatFilter) return false;
      return true;
    });

  rows.sort((a, b) => {
    if (sortBy === 'name_asc') {
      return String(a?.case_name || '').localeCompare(String(b?.case_name || ''));
    }
    if (sortBy === 'opened_desc') {
      return String(b?.opened_at || '').localeCompare(String(a?.opened_at || ''));
    }
    if (sortBy === 'threat_desc') {
      const threatDiff = (THREAT_ORDER[String(b?.threat_level || '')] || 0) - (THREAT_ORDER[String(a?.threat_level || '')] || 0);
      if (threatDiff !== 0) return threatDiff;
      return String(b?.last_edited_at || '').localeCompare(String(a?.last_edited_at || ''));
    }
    return String(b?.last_edited_at || '').localeCompare(String(a?.last_edited_at || ''));
  });

  return rows;
}

function renderCases() {
  if (!caseTiles || !caseTilesEmpty) return;
  const rows = filteredSortedCases();
  if (!rows.length) {
    caseTiles.innerHTML = '';
    caseTilesEmpty.classList.remove('hidden');
    return;
  }
  caseTilesEmpty.classList.add('hidden');
  caseTiles.innerHTML = rows.map(caseRowMarkup).join('');
}

function syncActiveCaseFromList() {
  if (!activeCaseId) return;
  const found = caseList.find((row) => String(row?.case_id || '') === activeCaseId) || null;
  activeCase = found;
  if (found) {
    dashboardBaseStatus = `Active case: ${found.case_name}`;
    updateStatusLine();
  }
}

function setCaseEditModalOpen(isOpen) {
  if (!caseEditModal) return;
  caseEditModal.classList.toggle('hidden', !isOpen);
  syncModalActiveState();
}

function setCaseSaveModalOpen(isOpen) {
  if (!caseSaveModal) return;
  caseSaveModal.classList.toggle('hidden', !isOpen);
  syncModalActiveState();
}

async function loadCases() {
  try {
    const response = await fetch('/api/cases');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    caseList = Array.isArray(payload?.cases) ? payload.cases : [];
    syncActiveCaseFromList();
    renderCases();
  } catch (error) {
    console.error(error);
    caseList = [];
    renderCases();
  }
}

async function deleteCaseAndContents(caseId) {
  const id = String(caseId || '').trim();
  if (!id) return;
  const ok = window.confirm('Delete this case and all collected posts?');
  if (!ok) return;
  try {
    const response = await fetch(`/api/cases/${encodeURIComponent(id)}`, { method: 'DELETE' });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    if (activeCaseId === id) {
      activeCaseId = '';
      activeCase = null;
      activeCaseExplicitlySaved = false;
      activeTargets = [];
      activeStartDate = '';
      activeEndDate = '';
      renderCollectionContext();
      showCaseWorkspace();
    }
    await loadCases();
    showNotification('Case deleted', 'success');
  } catch (error) {
    console.error(error);
    showNotification(`Delete failed: ${error.message || 'unknown error'}`, 'error');
  }
}

async function discardUnsavedActiveCase() {
  const id = String(activeCaseId || '').trim();
  if (!id || activeCaseExplicitlySaved) return false;
  try {
    const response = await fetch(`/api/cases/${encodeURIComponent(id)}`, { method: 'DELETE' });
    if (!response.ok) return false;
    activeCaseId = '';
    activeCase = null;
    activeCaseExplicitlySaved = false;
    activeCaseExplicitlySaved = false;
    activeTargets = [];
    activeStartDate = '';
    activeEndDate = '';
    renderCollectionContext();
    return true;
  } catch (_error) {
    return false;
  }
}

function confirmUnsavedCaseExit(actionLabel = 'exit') {
  const hasDraft = Boolean(String(activeCaseId || '').trim()) && !activeCaseExplicitlySaved;
  if (!hasDraft) return true;
  const label = String(actionLabel || 'exit').trim();
  return window.confirm(
    `This case has not been saved. If you ${label}, the draft case will be discarded.\n\nContinue?`,
  );
}

function watchlistCadenceForCase(caseId, fallback = '') {
  const key = String(caseId || '').trim();
  if (key && caseWatchlistCadenceById.has(key)) return String(caseWatchlistCadenceById.get(key) || '').trim();
  return String(fallback || '').trim();
}

function storeWatchlistCadence(caseId, status, cadence) {
  const key = String(caseId || '').trim();
  if (!key) return;
  if (String(status || '').trim() !== 'Watchlist') {
    caseWatchlistCadenceById.delete(key);
    return;
  }
  const value = String(cadence || '').trim();
  if (value) caseWatchlistCadenceById.set(key, value);
}

function setWatchlistCadenceVisibility(statusSelect, cadenceField, cadenceSelect, defaultCadence = '') {
  if (!statusSelect || !cadenceField || !cadenceSelect) return;
  const isWatchlist = String(statusSelect.value || '').trim() === 'Watchlist';
  cadenceField.classList.toggle('hidden', !isWatchlist);
  cadenceSelect.disabled = !isWatchlist;
  cadenceSelect.required = isWatchlist;
  if (!isWatchlist) {
    cadenceSelect.value = '';
    return;
  }
  if (!String(cadenceSelect.value || '').trim()) {
    cadenceSelect.value = String(defaultCadence || '').trim() || 'Every 15 Minutes';
  }
}

function openCaseEditModal(caseId) {
  const id = String(caseId || '').trim();
  if (!id) return;
  const row = caseList.find((item) => String(item?.case_id || '') === id);
  if (!row) return;
  editingCaseId = id;
  if (caseEditStatusSelect) caseEditStatusSelect.value = String(row.status || 'Open');
  if (caseEditThreatSelect) caseEditThreatSelect.value = String(row.threat_level || 'Low Threat');
  if (caseEditLocationSelect) {
    caseEditLocationSelect.value = String(row.known_location || 'Unknown').trim() || 'Unknown';
  }
  if (caseEditCadenceSelect) {
    caseEditCadenceSelect.value = watchlistCadenceForCase(id, row.monitoring_refresh_cadence);
  }
  setWatchlistCadenceVisibility(caseEditStatusSelect, caseEditCadenceField, caseEditCadenceSelect, watchlistCadenceForCase(id, row.monitoring_refresh_cadence));
  setCaseEditModalOpen(true);
}

function closeCaseEditModal() {
  editingCaseId = '';
  if (caseEditCadenceSelect) caseEditCadenceSelect.value = '';
  setWatchlistCadenceVisibility(caseEditStatusSelect, caseEditCadenceField, caseEditCadenceSelect);
  setCaseEditModalOpen(false);
}

async function submitCaseEdit(event) {
  event.preventDefault();
  const id = String(editingCaseId || '').trim();
  if (!id) return;
  const nextStatus = String(caseEditStatusSelect?.value || '').trim();
  const nextCadence = String(caseEditCadenceSelect?.value || '').trim();
  const nextThreat = String(caseEditThreatSelect?.value || '').trim();
  const nextLocation = String(caseEditLocationSelect?.value || 'Unknown').trim() || 'Unknown';
  if (nextStatus === 'Watchlist' && !nextCadence) {
    showNotification('Monitoring refresh cadence is required for Watchlist.', 'warn');
    caseEditCadenceSelect?.focus();
    return;
  }
  if (caseEditSaveBtn) caseEditSaveBtn.disabled = true;
  try {
    const response = await fetch(`/api/cases/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status: nextStatus,
        threat_level: nextThreat,
        known_location: nextLocation,
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    storeWatchlistCadence(id, nextStatus, nextCadence);
    await loadCases();
    closeCaseEditModal();
    if (nextStatus === 'Watchlist') {
      showNotification(`Case details updated (cadence: ${nextCadence})`, 'success');
    } else {
      showNotification('Case details updated', 'success');
    }
  } catch (error) {
    console.error(error);
    showNotification(`Update failed: ${error.message || 'unknown error'}`, 'error');
  } finally {
    if (caseEditSaveBtn) caseEditSaveBtn.disabled = false;
  }
}

async function openCase(caseId) {
  const id = String(caseId || '').trim();
  if (!id) return;
  const found = caseList.find((row) => String(row?.case_id || '') === id) || null;
  clearCollectionPolling();
  activeCaseId = id;
  activeCase = found;
  activeCaseExplicitlySaved = true;
  activeTargets = [];
  activeStartDate = '';
  activeEndDate = '';
  activeEntityFilters.clear();
  activeMixFilters.clear();
  activeSignalFilters.clear();
  activeCustomKeywordFilters.clear();
  activeFaceFilters.clear();
  latestFaceClusters = [];
  latestFaceRecognition = { available: false, reason: 'not_run' };
  renderFaceRecognitionFilters();
  updateFilterToggleLabel();
  renderCollectionContext();
  dashboardBaseStatus = found ? `Active case: ${found.case_name}` : '';
  updateStatusLine();
  seedReconFromCaseNotes(found);
  showDashboard();
  await refreshPosts();
}

function uniqueProfileImageUrls(posts) {
  const seen = new Set();
  const output = [];
  for (const post of Array.isArray(posts) ? posts : []) {
    const url = postProfileImageUrl(post);
    if (!url || seen.has(url)) continue;
    seen.add(url);
    output.push(url);
  }
  return output;
}

function renderCaseSaveImageOptions() {
  if (!caseSaveImageOptions) return;
  const selected = String(caseSaveSelectedImageUrl || '').trim();
  const imageOptions = [USER_PLACEHOLDER_AVATAR_URL, ...caseSaveImageChoices.filter((url) => url !== USER_PLACEHOLDER_AVATAR_URL)];
  caseSaveImageOptions.innerHTML = imageOptions
    .map((url, index) => {
      const checked = (selected ? selected === url : index === 0) ? ' checked' : '';
      const label = index === 0 ? 'No image (placeholder)' : `Profile ${index}`;
      return `
        <label class="case-save-image-option">
          <input type="radio" name="caseSavePoiImage" value="${escapeAttr(url)}"${checked} />
          <img src="${escapeAttr(url)}" alt="${escapeAttr(label)}" loading="lazy" />
          <span>${escapeHtml(label)}</span>
        </label>
      `;
    })
    .join('');
}

async function fetchCasePosts(caseId) {
  const id = String(caseId || '').trim();
  if (!id) return [];
  try {
    const params = new URLSearchParams({
      query: '',
      sort: 'newest',
      case_id: id,
    });
    const response = await fetch(`/api/posts?${params.toString()}`);
    if (!response.ok) return [];
    const payload = await response.json();
    return Array.isArray(payload?.posts) ? payload.posts : [];
  } catch (_error) {
    return [];
  }
}

async function openCaseSaveModal() {
  if (!activeCaseId) {
    showCaseWorkspace();
    return;
  }
  const currentName = String(activeCase?.case_name || '').trim() || 'Untitled Case';
  const currentStatus = String(activeCase?.status || 'Open').trim() || 'Open';
  const currentCadence = watchlistCadenceForCase(activeCaseId, activeCase?.monitoring_refresh_cadence);
  const currentThreat = String(activeCase?.threat_level || 'Low Threat').trim() || 'Low Threat';
  const currentLocation = String(activeCase?.known_location || 'Unknown').trim() || 'Unknown';
  const currentPoiImage = normalizeProfileImageUrl(activeCase?.poi_image_url);
  if (caseSaveTitleInput) caseSaveTitleInput.value = currentName;
  if (caseSaveStatusSelect) caseSaveStatusSelect.value = currentStatus;
  if (caseSaveCadenceSelect) caseSaveCadenceSelect.value = currentCadence;
  if (caseSaveThreatSelect) caseSaveThreatSelect.value = currentThreat;
  if (caseSaveLocationInput) caseSaveLocationInput.value = currentLocation;
  const posts = await fetchCasePosts(activeCaseId);
  const associatedImages = uniqueProfileImageUrls(posts);
  if (currentPoiImage && !associatedImages.includes(currentPoiImage)) {
    associatedImages.unshift(currentPoiImage);
  }
  caseSaveImageChoices = associatedImages;
  caseSaveSelectedImageUrl = currentPoiImage || USER_PLACEHOLDER_AVATAR_URL;
  renderCaseSaveImageOptions();
  setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect, currentCadence);
  setCaseSaveModalOpen(true);
}

function closeCaseSaveModal() {
  caseSaveSelectedImageUrl = '';
  caseSaveImageChoices = [];
  if (caseSaveCadenceSelect) caseSaveCadenceSelect.value = '';
  setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect);
  setCaseSaveModalOpen(false);
}

function normalizeCaseNotesObject(raw) {
  if (!raw || typeof raw !== 'object') return {};
  return raw;
}

function normalizeKnownProfiles(rawProfiles) {
  const rows = Array.isArray(rawProfiles) ? rawProfiles : [];
  const output = [];
  for (const item of rows) {
    if (!item || typeof item !== 'object') continue;
    output.push({
      site: String(item.site || '').trim(),
      url: String(item.url || '').trim(),
      image_url: normalizeProfileImageUrl(item.image_url),
      screenshot_url: String(item.screenshot_url || '').trim(),
    });
  }
  return output;
}

const COLLECTION_READY_SITE_KEYS = new Set(['twitter', 'reddit', 'tiktok', 'bluesky', 'instagram', 'youtube']);

function _siteKeyFromKnownProfile(profile) {
  const rawSite = String(profile?.site || '').trim();
  const normalized = normalizePlatformName(rawSite) || inferPlatformFromProfileUrl(profile?.url);
  if (normalized) return normalized;
  const compact = rawSite.toLowerCase();
  if (compact.includes('twitter') || compact.includes('x.com') || compact.includes('x /')) return 'twitter';
  if (compact.includes('reddit')) return 'reddit';
  if (compact.includes('tiktok')) return 'tiktok';
  if (compact.includes('bluesky') || compact.includes('bsky')) return 'bluesky';
  if (compact.includes('instagram')) return 'instagram';
  if (compact.includes('youtube')) return 'youtube';
  if (compact.includes('github')) return 'github';
  if (compact.includes('linkedin')) return 'linkedin';
  if (compact.includes('threads')) return 'threads';
  return '';
}

function _collectionTargetFromKnownProfile(profile, siteKey) {
  if (!COLLECTION_READY_SITE_KEYS.has(siteKey)) return null;
  const handle = extractHandleFromProfileUrl(profile?.url);
  if (!handle) return null;
  return {
    platform: siteKey,
    username: adjustTargetUsernameForCollection(siteKey, handle),
  };
}

function seedReconFromCaseNotes(caseRow) {
  const notes = normalizeCaseNotesObject(caseRow?.case_notes || {});
  const knownProfiles = normalizeKnownProfiles(notes.known_profiles);
  if (!knownProfiles.length) {
    reconProfiles = [];
    reconTargets = [];
    reconLeads = [];
    reconPersonDataProfile = {};
    reconPersonDataProfiles = [];
    reconOsintProfiles = [];
    reconNumverifyProfiles = [];
    renderLeadsList();
    renderReconResults({ results: [], checked: 0, present_count: 0 }, reconResults);
    renderReconResults({ results: [], checked: 0, present_count: 0 }, footprintReconResults);
    renderPatternOfLife(latestPosts);
    if (footprintReconStatus) footprintReconStatus.textContent = 'No seeded digital footprint profiles found in case notes.';
    return;
  }

  const results = knownProfiles.map((profile) => {
    const siteKey = _siteKeyFromKnownProfile(profile);
    return {
      site: siteKey || String(profile.site || '').trim() || 'unknown',
      status: 'present',
      profile_url: String(profile.url || '').trim(),
      profile_image_url: normalizeProfileImageUrl(profile.image_url),
      screenshot_url: String(profile.screenshot_url || '').trim(),
      source: 'seed',
      supported_for_collection: COLLECTION_READY_SITE_KEYS.has(siteKey),
      reason: '',
    };
  });

  const collectionReadyProfiles = results.filter((row) => row.supported_for_collection && String(row.profile_url || '').trim());
  const unsupportedProfilesWithUrl = results.filter((row) => !row.supported_for_collection && String(row.profile_url || '').trim());
  const knownPresentWithoutUrl = results.filter((row) => !String(row.profile_url || '').trim());

  const targetMap = new Map();
  for (const profile of knownProfiles) {
    const siteKey = _siteKeyFromKnownProfile(profile);
    const target = _collectionTargetFromKnownProfile(profile, siteKey);
    if (!target) continue;
    const key = `${target.platform}|${String(target.username || '').toLowerCase()}`;
    if (targetMap.has(key)) continue;
    targetMap.set(key, target);
  }

  reconProfiles = results;
  reconTargets = Array.from(targetMap.values());
  reconLeads = unsupportedProfilesWithUrl.map((row) => ({
    site: row.site,
    profile_url: row.profile_url,
    screenshot_url: row.screenshot_url,
    source: 'seed',
  }));
  reconPersonDataProfile = {};
  reconPersonDataProfiles = [];
  reconOsintProfiles = [];
  reconNumverifyProfiles = [];
  renderLeadsList();

  const payload = {
    results,
    checked: results.length,
    present_count: results.length,
    collection_ready_profiles: collectionReadyProfiles,
    unsupported_profiles_with_url: unsupportedProfilesWithUrl,
    known_present_without_url: knownPresentWithoutUrl,
    osint_profiles: [],
    numverify_profiles: [],
    person_data_profile: {},
    person_data_profiles: [],
  };
  renderReconResults(payload, reconResults);
  renderReconResults(payload, footprintReconResults);
  renderPatternOfLife(latestPosts);
  if (footprintReconStatus) {
    footprintReconStatus.textContent = `Loaded ${results.length} seeded profile hit(s) from case notes.`;
  }
}

function defaultKnownProfilesFromRecon() {
  if (!Array.isArray(reconProfiles) || !reconProfiles.length) return [];
  return reconProfiles.map((profile) => ({
    site: discoveredProfileLabel(String(profile?.site || '').trim(), String(profile?.profile_url || '').trim()),
    url: String(profile?.profile_url || '').trim(),
    image_url: normalizeProfileImageUrl(profile?.profile_image_url) || normalizeProfileImageUrl(profile?.image_url),
    screenshot_url: String(profile?.screenshot_url || '').trim(),
  }));
}

function normalizeProfileKey(site, url) {
  const platform = normalizePlatformName(site || inferPlatformFromProfileUrl(url));
  const handle = extractHandleFromProfileUrl(url).toLowerCase();
  if (platform && handle) return `${platform}|${handle}`;
  return `${platform}|${String(url || '').trim().toLowerCase()}`;
}

function extractHandleFromProfileUrl(url) {
  const value = String(url || '').trim();
  if (!value) return '';
  try {
    const parsed = new URL(value);
    const host = String(parsed.hostname || '').replace(/^www\./i, '').toLowerCase();
    const parts = String(parsed.pathname || '').split('/').filter(Boolean);
    if (!parts.length) return '';
    if (host.includes('x.com') || host.includes('twitter.com')) return parts[0].replace(/^@+/, '');
    if (host.includes('reddit.com')) {
      const idx = parts.findIndex((item) => item.toLowerCase() === 'user' || item.toLowerCase() === 'u');
      if (idx >= 0 && parts[idx + 1]) return parts[idx + 1];
    }
    if (host.includes('tiktok.com')) return parts[0].replace(/^@+/, '');
    if (host.includes('bsky.app') && parts[0].toLowerCase() === 'profile' && parts[1]) return parts[1].replace(/\.bsky\.social$/i, '');
    if (host.includes('instagram.com')) return parts[0].replace(/^@+/, '');
    if (host.includes('youtube.com') && parts[0].startsWith('@')) return parts[0].replace(/^@+/, '');
  } catch (_error) {
    return '';
  }
  return '';
}

function discoveredProfileLabel(site, url) {
  const platform = platformDisplayName(site || inferPlatformFromProfileUrl(url));
  const handle = extractHandleFromProfileUrl(url);
  if (handle) return `${platform} / @${handle}`;
  return platform;
}

function inferPlatformFromProfileUrl(url) {
  const host = profileDomain(url);
  if (!host) return '';
  if (host === 'x.com' || host === 'twitter.com' || host.endsWith('.x.com') || host.endsWith('.twitter.com')) return 'twitter';
  if (host.includes('reddit.com')) return 'reddit';
  if (host.includes('tiktok.com') || host.includes('tikvib.com')) return 'tiktok';
  if (host.includes('bsky.app') || host.includes('bsky.social')) return 'bluesky';
  if (host.includes('instagram.com') || host.includes('byviewer.com')) return 'instagram';
  if (host.includes('youtube.com') || host.includes('youtu.be')) return 'youtube';
  if (host.includes('facebook.com')) return 'facebook';
  return '';
}

function collectProfileImagesByPlatform(posts) {
  const byPlatform = new Map();
  for (const post of Array.isArray(posts) ? posts : []) {
    const platform = normalizePlatformName(post?.platform);
    const image = postProfileImageUrl(post);
    if (!platform || !image || byPlatform.has(platform)) continue;
    byPlatform.set(platform, image);
  }
  return byPlatform;
}

function enrichKnownProfilesWithExtractedImages(profiles, posts) {
  const byPlatform = collectProfileImagesByPlatform(posts);
  return normalizeKnownProfiles(profiles).map((profile) => {
    if (normalizeProfileImageUrl(profile.image_url)) return profile;
    const inferredPlatform = normalizePlatformName(profile.site) || inferPlatformFromProfileUrl(profile.url);
    const inferredImage = inferredPlatform ? String(byPlatform.get(inferredPlatform) || '').trim() : '';
    return {
      ...profile,
      image_url: normalizeProfileImageUrl(inferredImage),
    };
  });
}

function discoverKnownProfilesFromPosts(posts) {
  const grouped = new Map();
  for (const post of Array.isArray(posts) ? posts : []) {
    const platform = normalizePlatformName(post?.platform);
    const username = String(post?.username || '').trim();
    const profileUrl = buildProfileUrl(platform, username);
    if (!platform || !profileUrl) continue;
    const key = normalizeProfileKey(platform, profileUrl);
    const current = grouped.get(key) || {
      site: discoveredProfileLabel(platform, profileUrl),
      url: profileUrl,
      image_url: '',
      screenshot_url: '',
    };
    if (!current.image_url) current.image_url = postProfileImageUrl(post);
    grouped.set(key, current);
  }
  return Array.from(grouped.values());
}

function mergeDiscoveredKnownProfiles(baseProfiles, discoveredProfiles) {
  const merged = new Map();
  for (const item of normalizeKnownProfiles(discoveredProfiles)) {
    const key = normalizeProfileKey(item.site, item.url);
    merged.set(key, { ...item });
  }
  for (const item of normalizeKnownProfiles(baseProfiles)) {
    const key = normalizeProfileKey(item.site, item.url);
    if (!merged.has(key)) {
      merged.set(key, { ...item });
      continue;
    }
    const current = merged.get(key) || {};
    merged.set(key, {
      site: String(item.site || current.site || '').trim(),
      url: String(item.url || current.url || '').trim(),
      image_url: normalizeProfileImageUrl(item.image_url) || normalizeProfileImageUrl(current.image_url),
      screenshot_url: String(item.screenshot_url || current.screenshot_url || '').trim(),
    });
  }
  return Array.from(merged.values());
}

function firstProfileNameCandidate(posts, profiles) {
  for (const post of Array.isArray(posts) ? posts : []) {
    const displayName = String(post?.display_name || '').trim();
    if (displayName) return displayName;
  }
  for (const post of Array.isArray(posts) ? posts : []) {
    const username = String(post?.username || '').trim().replace(/^@+/, '');
    if (username) return username;
  }
  for (const profile of normalizeKnownProfiles(profiles)) {
    const handle = extractHandleFromProfileUrl(profile.url);
    if (handle) return handle;
  }
  return '';
}

function readImageAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    if (!(file instanceof File)) {
      reject(new Error('invalid_file'));
      return;
    }
    if (!String(file.type || '').toLowerCase().startsWith('image/')) {
      reject(new Error('file_not_image'));
      return;
    }
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || '').trim());
    reader.onerror = () => reject(new Error('read_failed'));
    reader.readAsDataURL(file);
  });
}

function caseNotesImageLabel(url, index) {
  if (url === USER_PLACEHOLDER_AVATAR_URL) return 'Placeholder';
  return `Profile ${index}`;
}

function renderCaseNotesSubjectImageOptions(selectedUrl) {
  if (!(caseNotesSubjectImageSelect instanceof HTMLSelectElement)) return;
  const selected = String(selectedUrl || '').trim() || USER_PLACEHOLDER_AVATAR_URL;
  const options = [USER_PLACEHOLDER_AVATAR_URL, ...caseNotesImageChoices.filter((url) => url !== USER_PLACEHOLDER_AVATAR_URL)];
  caseNotesSubjectImageSelect.innerHTML = options
    .map((url, index) => `<option value="${escapeAttr(url)}"${selected === url ? ' selected' : ''}>${escapeHtml(caseNotesImageLabel(url, index))}</option>`)
    .join('');
  caseNotesSubjectImageSelect.value = selected;
}

function renderCaseNotesSubjectImagePreview(url) {
  if (!(caseNotesSubjectImage instanceof HTMLImageElement)) return;
  const selected = normalizeProfileImageUrl(url) || USER_PLACEHOLDER_AVATAR_URL;
  caseNotesSubjectImage.src = selected;
}

function caseNotesProfileCardMarkup(profile, index) {
  const safe = profile || {};
  const site = String(safe.site || '').trim();
  const url = String(safe.url || '').trim();
  const imageUrl = normalizeProfileImageUrl(safe.image_url) || USER_PLACEHOLDER_AVATAR_URL;
  const screenshotUrl = String(safe.screenshot_url || '').trim();
  const imageOptions = [USER_PLACEHOLDER_AVATAR_URL, ...caseNotesImageChoices.filter((item) => item !== USER_PLACEHOLDER_AVATAR_URL)];
  return `
    <article class="case-notes-profile-card" data-profile-index="${index}" data-screenshot-url="${escapeAttr(screenshotUrl)}">
      <div class="case-notes-profile-top">
        <img class="case-notes-profile-avatar" src="${escapeAttr(imageUrl)}" alt="Profile image" loading="lazy" />
        <div class="case-notes-profile-fields">
          <div class="case-notes-profile-grid">
            <label class="field">
              <span>Name</span>
              <input class="case-notes-profile-site" type="text" value="${escapeAttr(site)}" placeholder="Platform or profile name" />
            </label>
            <label class="field">
              <span>Profile Picture</span>
              <select class="case-notes-profile-image-select">
                ${imageOptions.map((imgUrl, imgIndex) => `<option value="${escapeAttr(imgUrl)}"${imgUrl === imageUrl ? ' selected' : ''}>${escapeHtml(caseNotesImageLabel(imgUrl, imgIndex))}</option>`).join('')}
              </select>
            </label>
          </div>
          <div class="case-notes-profile-actions">
            <button class="secondary-btn case-notes-profile-upload-image-btn" type="button">Upload Profile Picture</button>
            <input class="case-notes-profile-upload-image-input hidden" type="file" accept="image/*" />
            <button class="secondary-btn case-notes-profile-upload-shot-btn" type="button">Upload Screenshot</button>
            <input class="case-notes-profile-upload-shot-input hidden" type="file" accept="image/*" />
          </div>
          <label class="field">
            <span>URL</span>
            <input class="case-notes-profile-url" type="text" value="${escapeAttr(url)}" placeholder="https://..." />
          </label>
        </div>
      </div>
      <div class="case-notes-profile-shot">
        ${screenshotUrl
    ? `<img src="${escapeAttr(screenshotUrl)}" alt="${escapeAttr(site || 'Profile')} screenshot" loading="lazy" />`
    : '<p class="case-notes-profile-shot-empty">No screenshot available.</p>'}
      </div>
      <div class="case-notes-profile-actions case-notes-profile-actions-end">
        <button class="secondary-btn case-notes-remove-profile-btn" type="button">Delete</button>
      </div>
    </article>
  `;
}

function renderCaseNotesProfiles() {
  if (!caseNotesProfilesList) return;
  if (!caseNotesKnownProfiles.length) {
    caseNotesProfilesList.innerHTML = '<div class="empty">No known profiles yet. Add a profile or run recon.</div>';
    return;
  }
  caseNotesProfilesList.innerHTML = caseNotesKnownProfiles.map((profile, index) => caseNotesProfileCardMarkup(profile, index)).join('');
}

function setCaseNotesModalOpen(isOpen) {
  if (!caseNotesModal) return;
  caseNotesModal.classList.toggle('hidden', !isOpen);
  syncModalActiveState();
}

function closeCaseNotesModal() {
  setCaseNotesModalOpen(false);
  if (activeInsightsTab === 'notes') {
    setInsightsTab('ops');
  }
}

function syncKnownProfilesFromForm() {
  if (!caseNotesProfilesList) return;
  const rows = Array.from(caseNotesProfilesList.querySelectorAll('.case-notes-profile-card'));
  caseNotesKnownProfiles = rows.map((row) => {
    const site = row.querySelector('.case-notes-profile-site');
    const url = row.querySelector('.case-notes-profile-url');
    const imageSelect = row.querySelector('.case-notes-profile-image-select');
    const selectedImage = imageSelect instanceof HTMLSelectElement ? String(imageSelect.value || '').trim() : '';
    const screenshot = String(row.getAttribute('data-screenshot-url') || '').trim();
    return {
      site: site instanceof HTMLInputElement ? String(site.value || '').trim() : '',
      url: url instanceof HTMLInputElement ? String(url.value || '').trim() : '',
      image_url: selectedImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(selectedImage),
      screenshot_url: screenshot,
    };
  });
}

async function openCaseNotesModal() {
  if (!activeCaseId || !activeCase) {
    showNotification('Open a case first.', 'warn');
    return;
  }
  const notes = normalizeCaseNotesObject(activeCase.case_notes || {});
  const posts = await fetchCasePosts(activeCaseId);
  const associatedImages = uniqueProfileImageUrls(posts);
  const casePoiImage = normalizeProfileImageUrl(activeCase?.poi_image_url);
  const notesSubjectImage = normalizeProfileImageUrl(notes.subject_image_url);
  const notesKnownProfiles = normalizeKnownProfiles(notes.known_profiles);
  const discoveredFromRecon = defaultKnownProfilesFromRecon();
  const discoveredFromPosts = discoverKnownProfilesFromPosts(posts);
  const discoveredKnownProfiles = mergeDiscoveredKnownProfiles(discoveredFromRecon, discoveredFromPosts);
  const knownProfiles = notesKnownProfiles.length ? mergeDiscoveredKnownProfiles(notesKnownProfiles, discoveredKnownProfiles) : discoveredKnownProfiles;
  caseNotesKnownProfiles = enrichKnownProfilesWithExtractedImages(knownProfiles, posts);
  const knownProfileImages = caseNotesKnownProfiles.map((item) => normalizeProfileImageUrl(item.image_url)).filter(Boolean);
  caseNotesImageChoices = [...new Set([USER_PLACEHOLDER_AVATAR_URL, casePoiImage, notesSubjectImage, ...associatedImages, ...knownProfileImages].filter(Boolean))];

  const discoveredName = firstProfileNameCandidate(posts, caseNotesKnownProfiles);
  if (caseNotesNameInput) caseNotesNameInput.value = String(notes.name || discoveredName || activeCase.case_name || '').trim();
  if (caseNotesLocationInput) caseNotesLocationInput.value = String(notes.location || activeCase.known_location || '').trim();
  if (caseNotesAgeInput) caseNotesAgeInput.value = String(notes.age || '').trim();
  if (caseNotesAkasInput) caseNotesAkasInput.value = String(notes.akas || '').trim();
  if (caseNotesContextInput) caseNotesContextInput.value = String(notes.context || '').trim();
  if (caseNotesThreatInput) caseNotesThreatInput.value = String(notes.threat_risk_assessment || '').trim();
  if (caseNotesPersonalInput) caseNotesPersonalInput.value = String(notes.personal_details || '').trim();

  const selectedSubject = notesSubjectImage || casePoiImage || knownProfileImages[0] || associatedImages[0] || USER_PLACEHOLDER_AVATAR_URL;
  renderCaseNotesSubjectImageOptions(selectedSubject);
  renderCaseNotesSubjectImagePreview(selectedSubject);
  renderCaseNotesProfiles();
  setCaseNotesModalOpen(true);
}

async function submitCaseNotes(event) {
  event.preventDefault();
  if (!activeCaseId) return;
  syncKnownProfilesFromForm();
  const name = String(caseNotesNameInput?.value || '').trim() || String(activeCase?.case_name || 'Untitled Case');
  const location = String(caseNotesLocationInput?.value || '').trim();
  const age = String(caseNotesAgeInput?.value || '').trim();
  const akas = String(caseNotesAkasInput?.value || '').trim();
  const context = String(caseNotesContextInput?.value || '').trim();
  const threatRisk = String(caseNotesThreatInput?.value || '').trim();
  const personal = String(caseNotesPersonalInput?.value || '').trim();
  const subjectImage = String(caseNotesSubjectImageSelect?.value || '').trim();
  const normalizedSubjectImage = subjectImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(subjectImage);
  const sanitizedProfiles = caseNotesKnownProfiles
    .map((profile) => ({
      site: String(profile.site || '').trim(),
      url: String(profile.url || '').trim(),
      image_url: normalizeProfileImageUrl(profile.image_url),
      screenshot_url: String(profile.screenshot_url || '').trim(),
    }))
    .filter((profile) => profile.site || profile.url || profile.image_url || profile.screenshot_url);
  const notes = {
    name,
    location,
    age,
    akas,
    subject_image_url: normalizedSubjectImage,
    context,
    threat_risk_assessment: threatRisk,
    personal_details: personal,
    known_profiles: sanitizedProfiles,
  };
  if (caseNotesSaveBtn) caseNotesSaveBtn.disabled = true;
  try {
    const response = await fetch(`/api/cases/${encodeURIComponent(activeCaseId)}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_name: name,
        known_location: location,
        poi_image_url: normalizedSubjectImage,
        case_notes: notes,
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    await loadCases();
    closeCaseNotesModal();
    showNotification('Case notes saved', 'success');
  } catch (error) {
    console.error(error);
    showNotification(`Case notes save failed: ${error.message || 'unknown error'}`, 'error');
  } finally {
    if (caseNotesSaveBtn) caseNotesSaveBtn.disabled = false;
  }
}

function exportCaseNotesPdf() {
  if (!activeCaseId) {
    showNotification('Open a case first.', 'warn');
    return;
  }
  if (caseNotesExportPdfBtn) caseNotesExportPdfBtn.disabled = true;
  fetch(`/api/cases/${encodeURIComponent(activeCaseId)}/notes.pdf`)
    .then(async (response) => {
      if (!response.ok) {
        const message = await parseErrorResponse(response);
        throw new Error(message);
      }
      return response.blob();
    })
    .then((blob) => {
      const objectUrl = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      const fallbackName = `${String(activeCase?.case_name || 'case-notes').trim().replace(/[^a-z0-9]+/gi, '-').toLowerCase() || 'case-notes'}-report.pdf`;
      anchor.href = objectUrl;
      anchor.download = fallbackName;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1200);
      showNotification('PDF downloaded', 'success');
    })
    .catch((error) => {
      console.error(error);
      showNotification(`PDF export failed: ${error.message || 'unknown error'}`, 'error');
    })
    .finally(() => {
      if (caseNotesExportPdfBtn) caseNotesExportPdfBtn.disabled = false;
    });
}

async function submitCaseSave(event) {
  event.preventDefault();
  const id = String(activeCaseId || '').trim();
  if (!id) return;
  const nextName = String(caseSaveTitleInput?.value || '').trim();
  const nextStatus = String(caseSaveStatusSelect?.value || '').trim();
  const nextCadence = String(caseSaveCadenceSelect?.value || '').trim();
  const nextThreat = String(caseSaveThreatSelect?.value || '').trim();
  const nextLocation = String(caseSaveLocationInput?.value || 'Unknown').trim() || 'Unknown';
  const selectedInput = caseSaveForm?.querySelector('input[name="caseSavePoiImage"]:checked');
  const selectedImage = selectedInput instanceof HTMLInputElement ? String(selectedInput.value || '').trim() : '';
  const nextPoiImage = selectedImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(selectedImage);
  if (!nextName) {
    showNotification('Case title is required.', 'warn');
    return;
  }
  if (nextStatus === 'Watchlist' && !nextCadence) {
    showNotification('Monitoring refresh cadence is required for Watchlist.', 'warn');
    caseSaveCadenceSelect?.focus();
    return;
  }
  if (caseSaveSubmitBtn) caseSaveSubmitBtn.disabled = true;
  try {
    const response = await fetch(`/api/cases/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_name: nextName,
        status: nextStatus,
        threat_level: nextThreat,
        known_location: nextLocation,
        poi_image_url: nextPoiImage,
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    storeWatchlistCadence(id, nextStatus, nextCadence);
    activeCaseExplicitlySaved = true;
    clearCollectionPolling();
    await loadCases();
    closeCaseSaveModal();
    showCaseWorkspace();
    if (nextStatus === 'Watchlist') {
      showNotification(`Case saved and closed (cadence: ${nextCadence})`, 'success');
    } else {
      showNotification('Case saved and closed', 'success');
    }
  } catch (error) {
    console.error(error);
    showNotification(`Save failed: ${error.message || 'unknown error'}`, 'error');
  } finally {
    if (caseSaveSubmitBtn) caseSaveSubmitBtn.disabled = false;
  }
}

async function generateDemoCase() {
  try {
    const response = await fetch('/api/cases/demo', { method: 'POST' });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    await loadCases();
    showNotification('Demo case generated', 'success');
  } catch (error) {
    console.error(error);
    showNotification(`Demo case failed: ${error.message || 'unknown error'}`, 'error');
  }
}

async function createNewCaseAndLaunch() {
  const now = new Date();
  const stamp = now.toLocaleString(undefined, { year: 'numeric', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit' });
  try {
    const response = await fetch('/api/cases', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_name: `Case ${stamp}`,
        status: 'Open',
        threat_level: 'Low Threat',
        known_location: '',
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const created = await response.json();
    clearCollectionPolling();
    activeCaseId = String(created?.case_id || '').trim();
    activeCase = created;
    activeCaseExplicitlySaved = false;
    dashboardBaseStatus = `Active case: ${String(created?.case_name || 'Untitled Case')}`;
    updateStatusLine();
    await loadCases();
    showDashboard();
    setupStatus.textContent = '';
    reconStatus.textContent = '';
    reconResults.classList.add('hidden');
    setModalMode('chooser');
    targetsList.innerHTML = '';
    addTargetRow('twitter', '');
    setModalOpen(true);
  } catch (error) {
    console.error(error);
    showNotification(`Could not create case: ${error.message || 'unknown error'}`, 'error');
  }
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

function llmAssessmentFromPost(post) {
  if (post?.llm_assessment && typeof post.llm_assessment === 'object') return post.llm_assessment;
  if (post?.metadata?.llm_assessment && typeof post.metadata.llm_assessment === 'object') return post.metadata.llm_assessment;
  return null;
}

const LLM_INDICATOR_DESCRIPTORS = {
  pathway: 'Observable preparation for attack activity such as planning, target selection, or testing response.',
  fixation: 'Intense, obsessive preoccupation that dominates thinking and impairs normal functioning.',
  leakage: 'Indirect or veiled communication suggesting attack intent to third parties.',
  'directly communicated threat': 'Explicitly stated threat or declared intent to attack a target.',
  'last resort': 'Language presenting violent action as urgent, necessary, or the only option left.',
  'violent identification': 'Adoption of a warrior identity, martyr framing, or idolization of attackers.',
  'testing violence': 'References to recent offline violence used to test capability or barriers.',
  'testing violence (novel aggression)': 'References to recent offline violence used to test capability or barriers.',
  'sudden behaviour change': 'Major break from baseline behavior such as withdrawal, relocation, or settling affairs.',
  'personal grievance': 'Strong anger, resentment, humiliation, or victimhood directed at a person/group/society.',
  stressor: 'Significant destabilizing stressors such as loss, conflict, legal/financial pressure, or failure.',
  'concerning history': 'History of problematic or violent behavior that elevates future violence risk.',
  'negative emotional state': 'Pervasive hopelessness, despair, isolation, nihilism, or worthlessness.',
  'suicidal ideation': 'Suicidal thoughts/fantasies/attempts, especially when intertwined with violence.',
  'mental health risk': 'Indicators of severe psychological distress like paranoia, delusions, or disorganization.',
  'violent ideation': 'Communicated violent fantasies/threats indicating propensity for aggressive action.',
  'violent fascination': 'Unusual interest in violent extremist content, gore, weapons, or mass violence.',
  'violent justification': 'Attempts to justify, excuse, or legitimize the use of violence.',
  grandiosity: 'Inflated beliefs of personal importance or heroic/existential significance.',
  'hostile worldview': 'Us-vs-them framing with dehumanizing hostility toward perceived outgroups.',
  incitement: 'Attempts to recruit, mobilize, or encourage others toward violence.',
  'extremist beliefs': 'Uncompromising extremist ideology, especially with violence advocacy.',
  fame: 'Desire for notoriety through extreme or violent acts.',
  networks: 'Claimed links or participation in extremist networks or communities.',
  'capability (knowledge)': 'Skills/training/knowledge relevant to planning or executing violence.',
  'capability (resources)': 'Access to tools or materials that could enable an attack.',
  'capability (access)': 'Proximity/insider access or specific target-location knowledge that enables attack.',
  'protective factor': 'Mitigating conditions (support, coping, opportunities, anti-violence stance) that reduce risk.',
};

const LLM_PRIMARY_BEHAVIOUR_KEYS = new Set([
  'pathway',
  'fixation',
  'leakage',
  'directly communicated threat',
  'last resort',
  'violent identification',
  'testing violence (novel aggression)',
  'sudden behaviour change',
]);

const LLM_SECONDARY_BEHAVIOUR_KEYS = new Set([
  'personal grievance',
  'stressor',
  'concerning history',
  'negative emotional state',
  'suicidal ideation',
  'mental health risk',
  'violent ideation',
  'violent fascination',
  'violent justification',
  'grandiosity',
  'hostile worldview',
  'incitement',
  'extremist beliefs',
  'fame',
  'networks',
  'capability (knowledge)',
  'capability (resources)',
  'capability (access)',
]);

function normalizeLlmIndicatorKey(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ');
}

function normalizeLlmCoverageIndicatorKey(value) {
  const key = normalizeLlmIndicatorKey(value);
  if (key === 'testing violence') return 'testing violence (novel aggression)';
  return key;
}

function llmIndicatorDescriptor(indicator) {
  const key = normalizeLlmIndicatorKey(indicator);
  return LLM_INDICATOR_DESCRIPTORS[key] || 'Indicator from the behavioural threat assessment guide.';
}

function llmAssessmentPrimary(assessment) {
  if (!assessment || typeof assessment !== 'object') return [];
  if (Array.isArray(assessment.tagged_primary)) return assessment.tagged_primary;
  if (Array.isArray(assessment.primary_warning_behaviours)) return assessment.primary_warning_behaviours;
  return [];
}

function llmAssessmentSecondary(assessment) {
  if (!assessment || typeof assessment !== 'object') return [];
  if (Array.isArray(assessment.tagged_secondary)) return assessment.tagged_secondary;
  if (Array.isArray(assessment.secondary_risk_factors)) return assessment.secondary_risk_factors;
  return [];
}

function llmAssessmentHasIndicators(assessment) {
  if (!assessment || typeof assessment !== 'object') return false;
  const primary = llmAssessmentPrimary(assessment);
  const secondary = llmAssessmentSecondary(assessment);
  const theme = String(assessment.underlying_theme || '').trim();
  return primary.length > 0 || secondary.length > 0 || Boolean(theme);
}

function _normalizeAssessmentList(values) {
  if (!Array.isArray(values)) return [];
  const output = [];
  const seen = new Set();
  for (const item of values) {
    const clean = String(item || '').trim().replace(/\s+/g, ' ');
    if (!clean) continue;
    const key = clean.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    output.push(clean);
  }
  return output;
}

function normalizeEditableLlmAssessment(assessment) {
  const source = assessment && typeof assessment === 'object' ? assessment : {};
  return {
    tagged_primary: _normalizeAssessmentList(llmAssessmentPrimary(source)),
    tagged_secondary: _normalizeAssessmentList(llmAssessmentSecondary(source)),
    underlying_theme: String(source.underlying_theme || '').trim(),
    rationale: String(source.rationale || '').trim(),
  };
}

function buildPersistedLlmAssessment(assessment, fallbackAssessment = {}) {
  const normalized = normalizeEditableLlmAssessment(assessment);
  const fallback = fallbackAssessment && typeof fallbackAssessment === 'object' ? fallbackAssessment : {};
  const rationale = normalized.rationale || String(fallback.rationale || '').trim();
  const underlyingTheme = normalized.tagged_primary.length || normalized.tagged_secondary.length
    ? normalized.underlying_theme
    : '';
  return {
    tagged_primary: normalized.tagged_primary,
    tagged_secondary: normalized.tagged_secondary,
    primary_warning_behaviours: normalized.tagged_primary,
    secondary_risk_factors: normalized.tagged_secondary,
    underlying_theme: underlyingTheme,
    rationale,
  };
}

function cloneJsonObject(value) {
  if (!value || typeof value !== 'object') return {};
  try {
    return JSON.parse(JSON.stringify(value));
  } catch (_error) {
    return {};
  }
}

function applyLocalLlmAssessmentUpdate(rowId, nextAssessment) {
  const targetRowId = Number(rowId);
  if (!Number.isFinite(targetRowId)) return;
  const normalized = buildPersistedLlmAssessment(nextAssessment, nextAssessment);
  for (const post of latestPosts) {
    if (!post || Number(post.row_id) !== targetRowId) continue;
    if (!post.metadata || typeof post.metadata !== 'object') post.metadata = {};
    post.metadata.llm_assessment = { ...normalized };
    post.llm_assessment = {
      tagged_primary: [...normalized.tagged_primary],
      tagged_secondary: [...normalized.tagged_secondary],
      underlying_theme: normalized.underlying_theme,
      rationale: normalized.rationale,
    };
    post.llm_primary_warning_behaviours = [...normalized.tagged_primary];
    post.llm_secondary_risk_factors = [...normalized.tagged_secondary];
    post.llm_underlying_theme = normalized.underlying_theme;
    post.llm_rationale = normalized.rationale;
  }
}

async function persistThreatAssessmentUpdate(postIndex, nextAssessment, options = {}) {
  const opts = options && typeof options === 'object' ? options : {};
  const closeEditor = Boolean(opts.closeEditor);
  const index = Number(postIndex);
  const post = latestRenderedPosts[index];
  if (!post || typeof post !== 'object') return false;
  const rowId = Number(post.row_id);
  if (!Number.isFinite(rowId)) {
    showNotification('Threat assessment update failed: post row id missing.', 'error');
    return false;
  }
  if (threatAssessmentSaveInFlight.has(rowId)) return false;
  threatAssessmentSaveInFlight.add(rowId);
  renderPosts(latestPosts);
  try {
    const currentAssessment = normalizeEditableLlmAssessment(llmAssessmentFromPost(post));
    const persistedAssessment = buildPersistedLlmAssessment(nextAssessment, currentAssessment);
    const metadata = cloneJsonObject(post.metadata);
    metadata.llm_assessment = persistedAssessment;
    const response = await fetch('/api/posts/assessment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        row_id: rowId,
        case_id: String(activeCaseId || post.case_id || '').trim(),
        metadata,
      }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    applyLocalLlmAssessmentUpdate(rowId, persistedAssessment);
    if (closeEditor || !persistedAssessment.tagged_primary.length && !persistedAssessment.tagged_secondary.length) {
      activeThreatAssessmentEditorPostIndex = null;
    }
    renderPosts(latestPosts);
    return true;
  } catch (error) {
    console.error(error);
    showNotification(`Threat assessment update failed: ${error.message || 'unknown error'}`, 'error');
    renderPosts(latestPosts);
    return false;
  } finally {
    threatAssessmentSaveInFlight.delete(rowId);
  }
}

function renderLLMCoverage(posts) {
  if (!(llmCoverageCard instanceof HTMLElement) || !llmCoveragePrimary || !llmCoverageSecondary) return;
  const list = Array.isArray(posts) ? posts : [];
  const assessments = list
    .map((post) => llmAssessmentFromPost(post))
    .filter((assessment) => assessment && typeof assessment === 'object');

  const hasAssessment = assessments.length > 0;
  llmCoverageCard.classList.toggle('hidden', !hasAssessment);
  if (!hasAssessment) {
    llmCoveragePrimary.innerHTML = '';
    llmCoverageSecondary.innerHTML = '';
    return;
  }

  const observedPrimary = new Set();
  const observedSecondary = new Set();
  for (const assessment of assessments) {
    for (const indicator of llmAssessmentPrimary(assessment)) {
      const key = normalizeLlmCoverageIndicatorKey(indicator);
      if (LLM_PRIMARY_BEHAVIOUR_KEYS.has(key)) observedPrimary.add(key);
    }
    for (const indicator of llmAssessmentSecondary(assessment)) {
      const key = normalizeLlmCoverageIndicatorKey(indicator);
      if (LLM_SECONDARY_BEHAVIOUR_KEYS.has(key)) observedSecondary.add(key);
    }
  }

  const coverageRow = (label, numerator, denominator) => `
    <span class="llm-coverage-row-label">
      <span class="llm-coverage-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" role="img" focusable="false">
          <path d="M12 3l9 16H3z"></path>
          <path d="M12 9v5"></path>
          <circle cx="12" cy="17.2" r="1"></circle>
        </svg>
      </span>
      <span>${escapeHtml(label)}</span>
    </span>
    <strong class="llm-coverage-ratio">${numerator}/${denominator}</strong>
  `;

  llmCoveragePrimary.innerHTML = coverageRow('Primary Warning Behaviours', observedPrimary.size, LLM_PRIMARY_BEHAVIOUR_KEYS.size);
  llmCoverageSecondary.innerHTML = coverageRow('Secondary Warning Behaviours', observedSecondary.size, LLM_SECONDARY_BEHAVIOUR_KEYS.size);
}

function renderLLMAssessmentDetail(post, index, options = {}) {
  if (activeInsightsTab !== 'signals') return '';
  const assessment = llmAssessmentFromPost(post);
  if (!llmAssessmentHasIndicators(assessment)) return '';
  const editable = options.assessmentEditable !== false;
  const normalized = normalizeEditableLlmAssessment(assessment);
  const primary = normalized.tagged_primary;
  const secondary = normalized.tagged_secondary;
  const theme = normalized.underlying_theme;
  const isEditing = editable && activeThreatAssessmentEditorPostIndex === Number(index);
  const isSaving = threatAssessmentSaveInFlight.has(Number(post?.row_id));
  const allTags = [
    ...primary.map((item) => ({ label: String(item || '').trim(), kind: 'primary' })),
    ...secondary.map((item) => ({ label: String(item || '').trim(), kind: 'secondary' })),
  ].filter((item) => item.label);
  const editablePills = allTags.length
    ? allTags.map((item) => `
      <button
        type="button"
        class="llm-pill llm-pill-editable ${item.kind}"
        data-assessment-remove-tag
        data-assessment-tag-kind="${escapeAttr(item.kind)}"
        data-assessment-tag-label="${escapeAttr(item.label)}"
        title="Remove ${escapeAttr(item.label)}"
        ${isSaving ? 'disabled' : ''}
      >
        <span>${escapeHtml(item.label)}</span>
        <span aria-hidden="true">×</span>
      </button>
    `).join('')
    : '<p class="llm-assessment-editor-hint">No tags yet. Add one below.</p>';
  return `
    <section class="llm-assessment" data-post-index="${Number(index)}">
      <div class="llm-assessment-head">
        ${theme ? `<p class="llm-theme-line">Assessment: Possible ${escapeHtml(theme)}</p>` : '<p class="llm-theme-line llm-theme-empty">Assessment theme not set.</p>'}
        ${editable ? `<button type="button" class="llm-assessment-toggle" data-assessment-toggle ${isSaving ? 'disabled' : ''}>${isEditing ? 'Done' : 'Edit'}</button>` : ''}
      </div>
      ${allTags.length ? `<div class="llm-pill-row">${allTags.map((item) => `<span class="llm-pill ${item.kind}" title="${escapeAttr(llmIndicatorDescriptor(item.label))}">${escapeHtml(item.label)}</span>`).join('')}</div>` : ''}
      ${editable ? `
        <div class="llm-assessment-editor${isEditing ? '' : ' hidden'}">
          <label class="llm-assessment-theme-field">
            <span>Theme Comment</span>
            <input type="text" data-assessment-theme-input value="${escapeAttr(theme)}" placeholder="Add theme comment" ${isSaving ? 'disabled' : ''} />
          </label>
          <div class="llm-assessment-editor-actions">
            <button type="button" class="llm-assessment-action-btn" data-assessment-theme-save ${isSaving ? 'disabled' : ''}>Save Theme</button>
            <button type="button" class="llm-assessment-action-btn subtle" data-assessment-theme-remove ${isSaving ? 'disabled' : ''}>Remove Theme</button>
          </div>
          <div class="llm-assessment-tag-editor">
            <input type="text" data-assessment-tag-input placeholder="Add tag (comma-separated supported)" ${isSaving ? 'disabled' : ''} />
            <select data-assessment-tag-kind ${isSaving ? 'disabled' : ''}>
              <option value="primary">Primary Warning</option>
              <option value="secondary">Secondary Risk</option>
            </select>
            <button type="button" class="llm-assessment-action-btn" data-assessment-tag-add ${isSaving ? 'disabled' : ''}>Add</button>
          </div>
          <p class="llm-assessment-editor-hint">Click a tag below to remove it.</p>
          <div class="llm-pill-row llm-pill-row-edit">${editablePills}</div>
        </div>
      ` : ''}
    </section>
  `;
}

function renderPosts(posts) {
  latestPosts = Array.isArray(posts) ? posts : [];
  latestRenderedPosts = activeInsightsTab === 'signals'
    ? latestPosts.filter((post) => llmAssessmentHasIndicators(llmAssessmentFromPost(post)))
    : latestPosts;
  if (!latestRenderedPosts.length) {
    const message = activeInsightsTab === 'signals'
      ? 'No posts with primary/secondary threat indicators are available.'
      : 'No posts matched your query.';
    resultsEl.innerHTML = `<div class="empty">${escapeHtml(message)}</div>`;
    renderVisuals(latestRenderedPosts);
    return;
  }

  resultsEl.innerHTML = activeResultsView === 'media'
    ? renderMediaGrid(latestRenderedPosts)
    : latestRenderedPosts.map((post, index) => renderPostCard(post, index)).join('');
  renderVisuals(latestRenderedPosts);
}

function renderPostCard(post, index, options = {}) {
  const includeCardId = options.includeCardId !== false;
  const fullContent = options.fullContent === true;
  const assessmentEditable = options.assessmentEditable !== false;
  const profileImageUrl = postProfileImageUrl(post) || USER_PLACEHOLDER_AVATAR_URL;
  return `
    <article ${includeCardId ? `id="post-card-${index}" ` : ''}class="card" data-post-index="${index}">
      <div class="meta">
        <div class="account-line">
          <img class="account-avatar" src="${escapeAttr(profileImageUrl)}" alt="${escapeAttr(accountTag(post))} profile image" loading="lazy" />
          <span class="account-tag">${escapeHtml(accountTag(post))}</span>
          <span class="source-tag">${escapeHtml((post.platform || 'Unknown').toUpperCase())}</span>
          <span class="type-tag">${escapeHtml((post.post_type || 'post').toUpperCase())}</span>
        </div>
        <div class="meta-right">
          <time class="recency">${escapeHtml(formatRecency(post.timestamp))}</time>
          ${post.source_url ? `<a class="url-icon" href="${escapeHtml(post.source_url)}" target="_blank" rel="noopener noreferrer" title="Open source post">🔗</a>` : ''}
        </div>
      </div>
      <div class="content">${postContentMarkup(post, index, { fullContent })}</div>
      ${renderLLMAssessmentDetail(post, index, { assessmentEditable })}
      ${renderQuoteNest(post)}
      ${renderPostMedia(post)}
    </article>
  `;
}

function collectMediaItems(posts) {
  const items = [];
  const profileTileByUrl = new Map();
  const mergeFaceDetections = (existing, incoming) => {
    const seen = new Set((Array.isArray(existing) ? existing : []).map((row) => {
      const b = row?.bbox || {};
      return [
        String(row?.personId || '').toLowerCase(),
        Number(b.x || 0).toFixed(4),
        Number(b.y || 0).toFixed(4),
        Number(b.w || 0).toFixed(4),
        Number(b.h || 0).toFixed(4),
        Number(row?.confidence || 0).toFixed(3),
      ].join('|');
    }));
    const out = Array.isArray(existing) ? existing.slice() : [];
    for (const face of Array.isArray(incoming) ? incoming : []) {
      const b = face?.bbox || {};
      const key = [
        String(face?.personId || '').toLowerCase(),
        Number(b.x || 0).toFixed(4),
        Number(b.y || 0).toFixed(4),
        Number(b.w || 0).toFixed(4),
        Number(b.h || 0).toFixed(4),
        Number(face?.confidence || 0).toFixed(3),
      ].join('|');
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(face);
    }
    return out;
  };
  for (let postIndex = 0; postIndex < posts.length; postIndex += 1) {
    const post = posts[postIndex];
    const profileUrl = postProfileImageUrl(post);
    if (isHttpUrl(profileUrl)) {
      const profileFaces = facesForMedia(post, { url: profileUrl, thumbnail_url: '' }, profileUrl);
      if (profileTileByUrl.has(profileUrl)) {
        const existingItem = items[profileTileByUrl.get(profileUrl)];
        existingItem.faceDetections = mergeFaceDetections(existingItem.faceDetections, profileFaces);
      } else {
        const next = {
          postIndex,
          mediaIndex: -1,
          type: 'image',
          mediaUrl: profileUrl,
          previewUrl: profileUrl,
          posterUrl: '',
          kind: 'profile',
          faceDetections: profileFaces,
        };
        profileTileByUrl.set(profileUrl, items.length);
        items.push(next);
      }
    }
    const media = normalizeMedia(post);
    for (let mediaIndex = 0; mediaIndex < media.length; mediaIndex += 1) {
      const entry = media[mediaIndex];
      const type = String(entry.type || '').toLowerCase() === 'video' ? 'video' : 'image';
      const previewUrl = type === 'video' ? String(entry.thumbnail_url || '').trim() : String(entry.url || '').trim();
      items.push({
        postIndex,
        mediaIndex,
        type,
        mediaUrl: String(entry.url || '').trim(),
        previewUrl,
        posterUrl: String(entry.thumbnail_url || '').trim(),
        kind: 'post',
        faceDetections: facesForMedia(post, entry, previewUrl),
      });
    }
  }
  return items;
}

function facesForMedia(post, mediaEntry, previewUrl = '') {
  const metadata = post?.metadata;
  const rows = Array.isArray(metadata?.face_recognition) ? metadata.face_recognition : [];
  const mediaUrl = String(mediaEntry?.url || '').trim();
  const thumbUrl = String(mediaEntry?.thumbnail_url || '').trim();
  const preview = String(previewUrl || '').trim();
  const out = [];
  for (const row of rows) {
    if (!row || typeof row !== 'object') continue;
    const rowMedia = String(row.media_url || '').trim();
    const rowAnalysis = String(row.analysis_url || '').trim();
    const matches = rowMedia === mediaUrl || rowAnalysis === mediaUrl || rowAnalysis === thumbUrl || rowMedia === thumbUrl || rowAnalysis === preview || rowMedia === preview;
    if (!matches) continue;
    const faces = Array.isArray(row.faces) ? row.faces : [];
    for (const face of faces) {
      if (!face || typeof face !== 'object') continue;
      const bbox = face.bbox && typeof face.bbox === 'object' ? face.bbox : {};
      const x = Number(bbox.x);
      const y = Number(bbox.y);
      const w = Number(bbox.w);
      const h = Number(bbox.h);
      if (![x, y, w, h].every((value) => Number.isFinite(value))) continue;
      out.push({
        personId: String(face.person_id || '').trim().toLowerCase(),
        label: String(face.label || '').trim(),
        color: String(face.color || '').trim() || '#22c55e',
        confidence: Number(face.confidence),
        bbox: {
          x: Math.max(0, Math.min(1, x)),
          y: Math.max(0, Math.min(1, y)),
          w: Math.max(0, Math.min(1, w)),
          h: Math.max(0, Math.min(1, h)),
        },
      });
    }
  }
  return out;
}

function facePassesConfidence(face) {
  const confidence = Number(face?.confidence);
  if (!Number.isFinite(confidence)) return activeFaceMinConfidence <= 0;
  return confidence >= activeFaceMinConfidence;
}

function formatConfidencePercent(value) {
  const num = Number(value);
  if (!Number.isFinite(num) || num <= 0) return '0%';
  return `${Math.round(Math.max(0, Math.min(1, num)) * 100)}%`;
}

function renderFaceOverlays(faceDetections) {
  const activeIds = Array.from(activeFaceFilters);
  if (!activeIds.length) return '';
  const rows = Array.isArray(faceDetections) ? faceDetections : [];
  const matches = rows.filter((item) => activeFaceFilters.has(String(item?.personId || '').toLowerCase()) && facePassesConfidence(item));
  if (!matches.length) return '';
  return `
    <span class="media-face-overlay">
      ${matches
        .map((item) => {
          const box = item.bbox || {};
          const bx = Number(box.x || 0);
          const by = Number(box.y || 0);
          const bw = Number(box.w || 0);
          const bh = Number(box.h || 0);
          const baseSide = Math.max(bw, bh);
          const side = Math.max(0.02, Math.min(1, baseSide * 1.18));
          const cx = bx + (bw / 2);
          const cy = by + (bh / 2);
          let sx = cx - (side / 2);
          let sy = cy - (side / 2);
          sx = Math.max(0, Math.min(1 - side, sx));
          sy = Math.max(0, Math.min(1 - side, sy));
          const x = sx * 100;
          const y = sy * 100;
          const w = side * 100;
          const h = side * 100;
          const color = String(item.color || '').trim() || '#22c55e';
          const label = String(item.label || item.personId || 'Person').trim();
          const conf = formatConfidencePercent(item.confidence);
          return `
            <span class="media-face-box" style="left:${x.toFixed(3)}%;top:${y.toFixed(3)}%;width:${w.toFixed(3)}%;height:${h.toFixed(3)}%;--face-color:${escapeAttr(color)}">
              <span class="media-face-label">${escapeHtml(label)} · ${escapeHtml(conf)}</span>
            </span>
          `;
        })
        .join('')}
    </span>
  `;
}

function renderInlineFaceRecognitionControls() {
  const rows = Array.isArray(latestFaceClusters) ? latestFaceClusters : [];
  const normalizedRows = rows
    .map((row) => {
      const personId = String(row?.person_id || '').trim().toLowerCase();
      const label = String(row?.label || '').trim() || personId;
      const count = Number(row?.count || 0);
      const color = String(row?.color || '').trim() || '#22c55e';
      const avgConfidence = Number(row?.avg_confidence || 0);
      return { personId, label, count, color, avgConfidence };
    })
    .filter((row) => row.personId && row.count > 0 && row.avgConfidence >= activeFaceMinConfidence);
  const stats = latestFaceRecognition && typeof latestFaceRecognition === 'object'
    ? latestFaceRecognition
    : { available: false, reason: 'unknown' };
  const reason = faceRecognitionReasonMessage(stats.reason);
  const imagesAnalyzed = Number(stats.images_analyzed || 0);
  const facesDetected = Number(stats.faces_detected || 0);
  const status = String(stats.reason || '').toLowerCase() === 'ok'
    ? `${reason} Images analyzed: ${imagesAnalyzed}. Faces detected: ${facesDetected}.`
    : reason;
  const chips = normalizedRows.length
    ? normalizedRows
      .map((row) => {
        const activeClass = activeFaceFilters.has(row.personId) ? ' is-active' : '';
        return `<button type="button" class="theme-filter-item face-filter-item${activeClass}" data-face-filter-inline="${escapeAttr(row.personId)}" style="--face-color:${escapeAttr(row.color)}"><span>${escapeHtml(row.label)}</span><em>${row.count} • ${formatConfidencePercent(row.avgConfidence)}</em></button>`;
      })
      .join('')
    : '<span class="theme-filter-empty">No recurring faces detected in current results.</span>';
  return `
    <section class="media-face-controls">
      <div class="media-face-controls-top">
        <button type="button" class="secondary-btn media-face-run-btn" data-face-run-inline>Run Facial Recognition</button>
        <p class="theme-filter-empty media-face-status">${escapeHtml(status)}</p>
      </div>
      <div class="filter-group media-face-threshold">
        <label>
          Min confidence
          <input type="range" min="0" max="1" step="0.05" value="${escapeAttr(String(activeFaceMinConfidence))}" data-face-confidence-inline />
          <span data-face-confidence-inline-value>${escapeHtml(formatConfidencePercent(activeFaceMinConfidence))}</span>
        </label>
      </div>
      <div class="theme-filter-list media-face-chip-list">${chips}</div>
    </section>
  `;
}

function renderMediaGrid(posts) {
  const allItems = collectMediaItems(posts)
    .sort((left, right) => {
      const l = left?.kind === 'profile' ? 0 : 1;
      const r = right?.kind === 'profile' ? 0 : 1;
      if (l !== r) return l - r;
      return 0;
    });
  const items = activeFaceFilters.size
    ? allItems.filter((item) => item.faceDetections.some((face) => activeFaceFilters.has(String(face?.personId || '').toLowerCase()) && facePassesConfidence(face)))
    : allItems;
  if (!items.length) {
    return `
      ${renderInlineFaceRecognitionControls()}
      <div class="empty">No images or videos matched your current filters.</div>
    `;
  }
  return `
    ${renderInlineFaceRecognitionControls()}
    <section class="results-media-grid">
      ${items.map((item) => {
    const post = posts[item.postIndex];
    const source = String(post?.platform || 'unknown').trim().toUpperCase();
    const preview = isHttpUrl(item.previewUrl) ? item.previewUrl : item.mediaUrl;
    const hasMatchedFace = item.faceDetections.some((entry) => activeFaceFilters.has(String(entry?.personId || '').toLowerCase()) && facePassesConfidence(entry));
    const previewMarkup = item.type === 'video'
      ? `<video preload="metadata" muted playsinline ${isHttpUrl(item.posterUrl) ? `poster="${escapeAttr(item.posterUrl)}"` : ''}><source src="${escapeAttr(item.mediaUrl)}" type="video/mp4" /></video>`
      : `<img loading="lazy" src="${escapeAttr(preview)}" alt="Post media preview" />`;
    const kindBadge = item.kind === 'profile' ? '<span class="media-grid-kind media-grid-kind-profile">PROFILE</span>' : '';
    return `
        <button type="button" class="media-grid-tile${hasMatchedFace ? ' has-face-match' : ''}" data-post-index="${item.postIndex}" data-media-index="${item.mediaIndex}">
          <span class="media-grid-preview">${previewMarkup}${renderFaceOverlays(item.faceDetections)}</span>
          <span class="media-grid-meta">
            <span class="media-grid-author">${escapeHtml(accountTag(post))}</span>
            <span class="media-grid-source">${escapeHtml(source)} ${kindBadge}</span>
          </span>
        </button>
      `;
  }).join('')}
    </section>
  `;
}

function postContentMarkup(post, index, options = {}) {
  const fullContent = options.fullContent === true;
  const text = primaryPostText(post);
  if (fullContent) return renderContentWithSignals(text, searchInput.value, post);
  const metadata = post?.metadata || {};
  const isFileInsert = Boolean(metadata?.manual_insert && metadata?.manual_insert_from_file);
  if (!isFileInsert || text.length <= 500) {
    return renderContentWithSignals(text, searchInput.value, post);
  }
  const leading = text.slice(0, 500);
  const trailing = text.slice(500);
  return `
    <span class="content-truncated" data-expanded="false" data-content-head="${escapeAttr(leading)}" data-content-rest="${escapeAttr(trailing)}">${renderContentWithSignals(leading, searchInput.value, post)}<span class="content-ellipsis">...</span></span>
    <button type="button" class="content-more-toggle" data-post-index="${index}" aria-expanded="false">Show more+</button>
  `;
}

function postContentMarkup(post, index) {
  const text = primaryPostText(post);
  const metadata = post?.metadata || {};
  const isFileInsert = Boolean(metadata?.manual_insert && metadata?.manual_insert_from_file);
  if (!isFileInsert || text.length <= 500) {
    return renderContentWithSignals(text, searchInput.value, post);
  }
  const leading = text.slice(0, 500);
  const trailing = text.slice(500);
  return `
    <span class="content-truncated" data-expanded="false" data-content-head="${escapeAttr(leading)}" data-content-rest="${escapeAttr(trailing)}">${renderContentWithSignals(leading, searchInput.value, post)}<span class="content-ellipsis">...</span></span>
    <button type="button" class="content-more-toggle" data-post-index="${index}" aria-expanded="false">Show more+</button>
  `;
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
  if (activeResultsView !== 'posts') {
    setResultsView('posts');
    window.setTimeout(() => scrollToPost(index), 0);
    return;
  }
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
  const loweredText = text.toLowerCase();
  const searchTerms = extractSearchTerms(query);
  const threatTerms = Array.isArray(post?.threat_matches) ? post.threat_matches : [];
  const selectorTerms = Array.isArray(post?.selector_matches) ? post.selector_matches : [];
  const customKeywordTerms = normalizeCustomKeywordList(configCustomKeywordList)
    .filter((term) => loweredText.includes(term.toLowerCase()));
  const llmAssessment = llmAssessmentFromPost(post);
  const llmTerms = [
    ...llmAssessmentPrimary(llmAssessment),
    ...llmAssessmentSecondary(llmAssessment),
  ];

  const ranges = [
    ..._collectRanges(text, searchTerms, 'keyterm-text', 1),
    ..._collectRanges(text, threatTerms, 'signal-threat', 2),
    ..._collectRanges(text, selectorTerms, 'signal-selector', 3),
    ..._collectRanges(text, customKeywordTerms, 'signal-custom-keyword', 4),
    ..._collectRanges(text, llmTerms, 'signal-llm', 5),
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

function normalizeCustomKeywordTerm(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function normalizeCustomKeywordList(raw) {
  const rows = Array.isArray(raw) ? raw : [];
  const output = [];
  const seen = new Set();
  for (const row of rows) {
    const clean = normalizeCustomKeywordTerm(row);
    if (!clean) continue;
    const lowered = clean.toLowerCase();
    if (seen.has(lowered)) continue;
    seen.add(lowered);
    output.push(clean.slice(0, 120));
    if (output.length >= 200) break;
  }
  return output;
}

function renderConfigCustomKeywordPills() {
  if (!(configCustomKeywordPills instanceof HTMLElement)) return;
  if (!configCustomKeywordList.length) {
    configCustomKeywordPills.innerHTML = '<span class="config-keyword-empty">No custom keywords configured.</span>';
    return;
  }
  configCustomKeywordPills.innerHTML = configCustomKeywordList
    .map((term) => `
      <button type="button" class="config-keyword-pill" data-config-keyword-pill="${escapeAttr(term.toLowerCase())}" title="Remove keyword">
        <span>${escapeHtml(term)}</span><strong aria-hidden="true">&times;</strong>
      </button>
    `)
    .join('');
}

function addConfigCustomKeywordTerm(rawTerm) {
  const clean = normalizeCustomKeywordTerm(rawTerm);
  if (!clean) return;
  const lowered = clean.toLowerCase();
  if (configCustomKeywordList.some((item) => item.toLowerCase() === lowered)) return;
  configCustomKeywordList.push(clean.slice(0, 120));
  renderConfigCustomKeywordPills();
}

function removeConfigCustomKeywordTerm(termLower) {
  const lowered = String(termLower || '').trim().toLowerCase();
  if (!lowered) return;
  configCustomKeywordList = configCustomKeywordList.filter((item) => item.toLowerCase() !== lowered);
  if (activeCustomKeywordFilters.has(lowered)) activeCustomKeywordFilters.delete(lowered);
  renderConfigCustomKeywordPills();
  renderCustomKeywordMix(latestPosts);
  updateFilterToggleLabel();
  queueRefresh();
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
  const llmPrimaryOn = Boolean(filterLLMPrimary?.checked);
  const llmSecondaryOn = Boolean(filterLLMSecondary?.checked);
  if (!selectorsOn && !ideologicalOn && !threatOn && !llmPrimaryOn && !llmSecondaryOn) return rows;
  return rows.filter((post) => {
    const hasSelectors = Array.isArray(post?.selector_matches) && post.selector_matches.length > 0;
    const ideologicalCategories = Array.isArray(post?.threat_categories) ? post.threat_categories : [];
    const threatSignalCategories = Array.isArray(post?.threat_signal_categories) ? post.threat_signal_categories : [];
    const hasIdeologicalIndicators = ideologicalCategories.length > 0;
    const hasThreatSignals = threatSignalCategories.length > 0 || (Array.isArray(post?.threat_matches) && post.threat_matches.length > 0);
    const assessment = llmAssessmentFromPost(post);
    const hasLLMPrimary = llmAssessmentPrimary(assessment).length > 0;
    const hasLLMSecondary = llmAssessmentSecondary(assessment).length > 0;
    return (
      (selectorsOn && hasSelectors)
      || (ideologicalOn && hasIdeologicalIndicators)
      || (threatOn && hasThreatSignals)
      || (llmPrimaryOn && hasLLMPrimary)
      || (llmSecondaryOn && hasLLMSecondary)
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

function _signalValuesForField(post, fieldName) {
  if (fieldName === 'llm_primary_warning_behaviours') {
    const assessment = llmAssessmentFromPost(post);
    return llmAssessmentPrimary(assessment);
  }
  if (fieldName === 'llm_secondary_risk_factors') {
    const assessment = llmAssessmentFromPost(post);
    return llmAssessmentSecondary(assessment);
  }
  return Array.isArray(post?.[fieldName]) ? post[fieldName] : [];
}

function postMentionsCustomKeyword(post, keyword) {
  const needle = String(keyword || '').trim().toLowerCase();
  if (!needle) return false;
  const haystack = String(primaryPostText(post) || '').toLowerCase();
  return haystack.includes(needle);
}

function applySignalTagFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activeSignalFilters.size) return rows;
  return rows.filter((post) => {
    for (const entry of activeSignalFilters) {
      const [fieldName, value] = String(entry || '').split('|');
      if (!fieldName || !value) continue;
      const values = _signalValuesForField(post, fieldName).map((item) => String(item || '').trim().toLowerCase()).filter(Boolean);
      if (!values.includes(value)) return false;
    }
    return true;
  });
}

function applyCustomKeywordFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activeCustomKeywordFilters.size) return rows;
  const needles = Array.from(activeCustomKeywordFilters.values());
  return rows.filter((post) => needles.some((keyword) => postMentionsCustomKeyword(post, keyword)));
}

function applyFaceFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activeFaceFilters.size) return rows;
  return rows.filter((post) => {
    const records = Array.isArray(post?.metadata?.face_recognition) ? post.metadata.face_recognition : [];
    for (const media of records) {
      if (!media || typeof media !== 'object') continue;
      const faces = Array.isArray(media.faces) ? media.faces : [];
      for (const face of faces) {
        const personId = String(face?.person_id || '').trim().toLowerCase();
        if (!personId || !activeFaceFilters.has(personId)) continue;
        if (facePassesConfidence(face)) return true;
      }
    }
    return false;
  });
}

function applyDashboardFilters(posts) {
  return applyFaceFilters(applyCustomKeywordFilters(applySignalTagFilters(applyMixFilters(applySignalTypeFilter(posts)))));
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

function formatUtcOffsetLabel(offsetHours) {
  const value = Number(offsetHours);
  if (!Number.isFinite(value)) return 'UTC';
  if (value === 0) return 'UTC+0';
  return value > 0 ? `UTC+${value}` : `UTC${value}`;
}

function hourLabel(hour) {
  const safe = ((Number(hour) % 24) + 24) % 24;
  return `${String(safe).padStart(2, '0')}:00`;
}

function sumHourlyWindow(histogram, startHour, spanHours) {
  const hist = Array.isArray(histogram) ? histogram : [];
  let total = 0;
  const safeStart = ((Number(startHour) % 24) + 24) % 24;
  const safeSpan = Math.max(1, Math.min(24, Math.floor(Number(spanHours) || 1)));
  for (let i = 0; i < safeSpan; i += 1) {
    total += Number(hist[(safeStart + i) % 24] || 0);
  }
  return total;
}

function shiftedHourlyHistogram(utcHistogram, utcOffsetHours) {
  const source = Array.isArray(utcHistogram) ? utcHistogram : Array(24).fill(0);
  const shifted = Array(24).fill(0);
  for (let utcHour = 0; utcHour < 24; utcHour += 1) {
    const localHour = (utcHour + utcOffsetHours + 24 * 2) % 24;
    shifted[localHour] = Number(source[utcHour] || 0);
  }
  return shifted;
}

function findLowestWindow(histogram, spanHours, allowedStarts = null) {
  const starts = Array.isArray(allowedStarts) && allowedStarts.length
    ? allowedStarts
    : Array.from({ length: 24 }, (_, idx) => idx);
  let bestStart = starts[0] || 0;
  let bestValue = Number.POSITIVE_INFINITY;
  for (const start of starts) {
    const value = sumHourlyWindow(histogram, start, spanHours);
    if (value < bestValue) {
      bestValue = value;
      bestStart = start;
    }
  }
  return { start: bestStart, value: Number.isFinite(bestValue) ? bestValue : 0 };
}

function inferTimezoneFromUtcHistogram(utcHistogram, sampleCount) {
  const candidates = [];
  for (let offset = -12; offset <= 14; offset += 1) {
    const local = shiftedHourlyHistogram(utcHistogram, offset);
    const sleepCount = sumHourlyWindow(local, 0, 6);
    const daytimeCount = sumHourlyWindow(local, 8, 10);
    const eveningCount = sumHourlyWindow(local, 18, 5);
    const overnightWindow = findLowestWindow(local, 7);
    const density = sampleCount > 0 ? sampleCount / 24 : 0;
    const score = (
      (daytimeCount / 10) * 1.2 +
      (eveningCount / 5) * 0.9 -
      (sleepCount / 6) * 1.6 -
      (overnightWindow.value / 7) * 0.7 +
      density * 0.12
    );
    candidates.push({ offset, local, score });
  }
  candidates.sort((a, b) => b.score - a.score);
  const best = candidates[0];
  const second = candidates[1];
  const gap = best && second ? (best.score - second.score) : 0;
  let confidence = 'low';
  if (sampleCount >= 36 && gap >= 0.25) confidence = 'high';
  else if (sampleCount >= 18 && gap >= 0.12) confidence = 'medium';
  return {
    offset: best ? best.offset : 0,
    localHistogram: best ? best.local : Array(24).fill(0),
    confidence,
    scoreGap: gap,
  };
}

function summarizePostingRhythm(posts) {
  const utcHistogram = Array(24).fill(0);
  let sampleCount = 0;
  const sourceCounts = new Map();
  for (const post of Array.isArray(posts) ? posts : []) {
    const timestamp = String(post?.timestamp || '').trim();
    if (!timestamp) continue;
    const parsed = new Date(timestamp);
    if (Number.isNaN(parsed.getTime())) continue;
    const utcHour = parsed.getUTCHours();
    utcHistogram[utcHour] += 1;
    sampleCount += 1;
    const source = String(post?.platform || 'unknown').trim() || 'unknown';
    sourceCounts.set(source, (sourceCounts.get(source) || 0) + 1);
  }

  if (sampleCount < 6) {
    return {
      sampleCount,
      insufficient: true,
      offset: 0,
      timezoneLabel: 'Insufficient data',
      summary: 'Need at least 6 timestamped posts to estimate posting rhythm.',
      localHistogram: Array(24).fill(0),
      sources: [],
      sleepWindowStart: 0,
      workWindowStart: 9,
      confidence: 'low',
    };
  }

  const tz = inferTimezoneFromUtcHistogram(utcHistogram, sampleCount);
  const localHistogram = tz.localHistogram;
  const sleepWindow = findLowestWindow(localHistogram, 7);
  const workWindow = findLowestWindow(localHistogram, 4, [8, 9, 10, 11, 12, 13, 14]);
  const sources = Array.from(sourceCounts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 6);

  const timezoneLabel = `${formatUtcOffsetLabel(tz.offset)} (${tz.confidence} confidence)`;
  const summary = `Likely sleep window ${hourLabel(sleepWindow.start)}-${hourLabel((sleepWindow.start + 7) % 24)} local; likely low-posting work window ${hourLabel(workWindow.start)}-${hourLabel((workWindow.start + 4) % 24)} local.`;
  return {
    sampleCount,
    insufficient: false,
    offset: tz.offset,
    timezoneLabel,
    summary,
    localHistogram,
    sources,
    sleepWindowStart: sleepWindow.start,
    workWindowStart: workWindow.start,
    confidence: tz.confidence,
  };
}

function renderPostingTimezoneMap(analysis) {
  if (!postingTimezoneMap) return;
  if (postingTimezoneMapInstance) {
    postingTimezoneMapInstance.remove();
    postingTimezoneMapInstance = null;
    postingTimezoneMapLayer = null;
  }
  const insufficient = Boolean(analysis?.insufficient);
  const offset = Number(analysis?.offset || 0);
  const confidence = String(analysis?.confidence || 'low').toLowerCase();

  if (insufficient) {
    postingTimezoneMap.innerHTML = '<div class="posting-timezone-map-empty">Need at least 6 timestamped posts to highlight likely timezone.</div>';
    return;
  }

  const minOffset = -12;
  const maxOffset = 14;
  const clampedOffset = Math.max(minOffset, Math.min(maxOffset, offset));
  const confidenceClass = confidence === 'high' ? ' is-high' : confidence === 'medium' ? ' is-medium' : ' is-low';
  const centerLongitude = Math.max(-180, Math.min(180, clampedOffset * 15));
  const corridorHalfWidthDegrees = 15;

  postingTimezoneMap.innerHTML = `
    <div class="posting-timezone-map-shell${confidenceClass}">
      <div class="posting-timezone-map-canvas" aria-hidden="true"></div>
      <div class="posting-timezone-map-label">Likely timezone corridor: <strong>${escapeHtml(formatUtcOffsetLabel(clampedOffset))}</strong></div>
    </div>
  `;

  const canvas = postingTimezoneMap.querySelector('.posting-timezone-map-canvas');
  if (!(canvas instanceof HTMLElement)) return;
  loadLeaflet()
    .then((L) => {
      if (!L) throw new Error('leaflet_unavailable');
      postingTimezoneMapInstance = L.map(canvas, {
        zoomControl: false,
        attributionControl: false,
        dragging: false,
        scrollWheelZoom: false,
        doubleClickZoom: false,
        boxZoom: false,
        keyboard: false,
        tap: false,
        touchZoom: false,
        worldCopyJump: true,
      }).setView([20, centerLongitude], 1);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 4,
        minZoom: 1,
      }).addTo(postingTimezoneMapInstance);
      postingTimezoneMapLayer = L.layerGroup().addTo(postingTimezoneMapInstance);

      const west = centerLongitude - corridorHalfWidthDegrees;
      const east = centerLongitude + corridorHalfWidthDegrees;
      const addCorridor = (westBound, eastBound) => {
        L.rectangle([[-85, westBound], [85, eastBound]], {
          color: 'rgba(245, 158, 11, 0.88)',
          weight: 1,
          fillColor: 'rgba(250, 204, 21, 0.24)',
          fillOpacity: 0.6,
          interactive: false,
        }).addTo(postingTimezoneMapLayer);
      };
      if (west < -180) {
        addCorridor(west + 360, 180);
        addCorridor(-180, east);
      } else if (east > 180) {
        addCorridor(west, 180);
        addCorridor(-180, east - 360);
      } else {
        addCorridor(west, east);
      }
      postingTimezoneMapInstance.invalidateSize();
    })
    .catch(() => {
      postingTimezoneMap.innerHTML = '<div class="posting-timezone-map-empty">Timezone map failed to load.</div>';
    });
}

function renderPostingRhythm(posts) {
  if (!postingTimezoneInference || !postingRhythmSummary || !postingHourChart || !postingSourceMix || !postingRhythmEmpty) return;
  const analysis = summarizePostingRhythm(posts);
  postingTimezoneInference.innerHTML = `
    <span class="posting-timezone-kicker">Likely timezone</span>
    <span class="posting-timezone-value">${escapeHtml(analysis.timezoneLabel)}</span>
  `;
  postingRhythmSummary.textContent = `${analysis.summary} ${analysis.sampleCount} timestamped post${analysis.sampleCount === 1 ? '' : 's'} analyzed (UTC timestamps shifted for inference only).`;
  renderPostingTimezoneMap(analysis);

  if (analysis.insufficient) {
    postingHourChart.innerHTML = '';
    postingSourceMix.innerHTML = '';
    postingRhythmEmpty.classList.remove('hidden');
    return;
  }

  postingRhythmEmpty.classList.add('hidden');
  const maxCount = Math.max(...analysis.localHistogram, 1);
  postingHourChart.innerHTML = analysis.localHistogram
    .map((count, hour) => {
      const heightPct = Math.max(5, Math.round((count / maxCount) * 100));
      const sleepClass = ((hour - analysis.sleepWindowStart + 24) % 24) < 7 ? ' is-sleep' : '';
      const workClass = ((hour - analysis.workWindowStart + 24) % 24) < 4 ? ' is-work' : '';
      return `
        <div class="posting-hour-cell${sleepClass}${workClass}">
          <div class="posting-hour-bar-wrap">
            <div class="posting-hour-bar" style="height:${heightPct}%"></div>
          </div>
          <span class="posting-hour-label">${hourLabel(hour).slice(0, 2)}</span>
          <span class="posting-hour-count">${count}</span>
        </div>
      `;
    })
    .join('');

  postingSourceMix.innerHTML = analysis.sources
    .map(([source, count]) => `<span class="mix-pill"><span>${escapeHtml(source)}</span><strong>${count}</strong></span>`)
    .join('');
}

function renderPatternPostingRhythm(posts, providedAnalysis = null) {
  if (
    !patternLifeTimezoneInference
    || !patternLifeRhythmSummary
    || !patternLifeHourChart
    || !patternLifeSourceMix
    || !patternLifeRhythmEmpty
  ) return providedAnalysis || summarizePostingRhythm(posts);
  const analysis = providedAnalysis || summarizePostingRhythm(posts);
  patternLifeTimezoneInference.innerHTML = `
    <span class="posting-timezone-kicker">Likely timezone</span>
    <span class="posting-timezone-value">${escapeHtml(analysis.timezoneLabel)}</span>
  `;
  patternLifeRhythmSummary.textContent = `${analysis.summary} ${analysis.sampleCount} timestamped post${analysis.sampleCount === 1 ? '' : 's'} analyzed (UTC timestamps shifted for inference only).`;

  if (analysis.insufficient) {
    patternLifeHourChart.innerHTML = '';
    patternLifeSourceMix.innerHTML = '';
    patternLifeRhythmEmpty.classList.remove('hidden');
    return analysis;
  }

  patternLifeRhythmEmpty.classList.add('hidden');
  const maxCount = Math.max(...analysis.localHistogram, 1);
  patternLifeHourChart.innerHTML = analysis.localHistogram
    .map((count, hour) => {
      const heightPct = Math.max(5, Math.round((count / maxCount) * 100));
      const sleepClass = ((hour - analysis.sleepWindowStart + 24) % 24) < 7 ? ' is-sleep' : '';
      const workClass = ((hour - analysis.workWindowStart + 24) % 24) < 4 ? ' is-work' : '';
      return `
        <div class="posting-hour-cell${sleepClass}${workClass}">
          <div class="posting-hour-bar-wrap">
            <div class="posting-hour-bar" style="height:${heightPct}%"></div>
          </div>
          <span class="posting-hour-label">${hourLabel(hour).slice(0, 2)}</span>
          <span class="posting-hour-count">${count}</span>
        </div>
      `;
    })
    .join('');
  patternLifeSourceMix.innerHTML = analysis.sources
    .map(([source, count]) => `<span class="mix-pill"><span>${escapeHtml(source)}</span><strong>${count}</strong></span>`)
    .join('');
  return analysis;
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

function faceRecognitionReasonMessage(reason) {
  const normalized = String(reason || '').trim().toLowerCase();
  if (normalized === 'ok') return 'Completed.';
  if (normalized === 'no_posts') return 'No posts available for analysis.';
  if (normalized === 'opencv_not_installed') return 'Face engine unavailable (opencv not installed).';
  if (normalized === 'no_supported_backend') return 'No supported face-recognition backend is available.';
  if (normalized === 'analysis_fetch_failed') return 'Unable to fetch/decode media for analysis.';
  if (normalized === 'not_run') return 'Facial recognition not run yet. Click "Run Facial Recognition".';
  return normalized ? `Face analysis status: ${normalized}.` : 'Facial recognition status unavailable.';
}

function updateFaceRecognitionStatus() {
  if (!(faceRecognitionStatus instanceof HTMLElement)) return;
  const stats = latestFaceRecognition && typeof latestFaceRecognition === 'object'
    ? latestFaceRecognition
    : { available: false, reason: 'unknown' };
  const reasonText = faceRecognitionReasonMessage(stats.reason);
  const backend = String(stats.backend || '').trim();
  const imagesAnalyzed = Number(stats.images_analyzed || 0);
  const facesDetected = Number(stats.faces_detected || 0);
  if (String(stats.reason || '').toLowerCase() === 'ok') {
    const backendSuffix = backend ? ` Backend: ${backend}.` : '';
    faceRecognitionStatus.textContent = `${reasonText} Images analyzed: ${imagesAnalyzed}. Faces detected: ${facesDetected}.${backendSuffix}`;
    return;
  }
  faceRecognitionStatus.textContent = backend ? `${reasonText} Backend: ${backend}.` : reasonText;
}

function updateFaceConfidenceDisplays() {
  if (faceConfidenceRange instanceof HTMLInputElement) {
    faceConfidenceRange.value = String(activeFaceMinConfidence);
  }
  if (faceConfidenceValue instanceof HTMLElement) {
    faceConfidenceValue.textContent = formatConfidencePercent(activeFaceMinConfidence);
  }
}

function renderFaceRecognitionFilters() {
  if (!(faceRecognitionFilterList instanceof HTMLElement) || !(faceRecognitionFilterEmpty instanceof HTMLElement)) return;
  updateFaceRecognitionStatus();
  updateFaceConfidenceDisplays();
  const rows = Array.isArray(latestFaceClusters) ? latestFaceClusters : [];
  const normalizedRows = rows
    .map((row) => {
      const personId = String(row?.person_id || '').trim().toLowerCase();
      const label = String(row?.label || '').trim() || personId;
      const count = Number(row?.count || 0);
      const color = String(row?.color || '').trim() || '#22c55e';
      const avgConfidence = Number(row?.avg_confidence || 0);
      return { personId, label, count, color, avgConfidence };
    })
    .filter((row) => row.personId && row.count > 0 && row.avgConfidence >= activeFaceMinConfidence);
  const knownIds = new Set(normalizedRows.map((row) => row.personId));
  for (const activeId of Array.from(activeFaceFilters)) {
    if (!knownIds.has(activeId)) activeFaceFilters.delete(activeId);
  }
  if (!normalizedRows.length) {
    faceRecognitionFilterList.innerHTML = '';
    const facesDetected = Number((latestFaceRecognition && latestFaceRecognition.faces_detected) || 0);
    if (facesDetected > 0) {
      faceRecognitionFilterEmpty.textContent = activeFaceMinConfidence > 0
        ? 'Faces detected, but no recurring clusters meet the current confidence threshold.'
        : 'Faces detected, but no recurring person clusters were found.';
    } else {
      faceRecognitionFilterEmpty.textContent = 'No recurring faces detected in current results.';
    }
    faceRecognitionFilterEmpty.classList.remove('hidden');
    updateFilterToggleLabel();
    return;
  }
  faceRecognitionFilterEmpty.classList.add('hidden');
  faceRecognitionFilterList.innerHTML = normalizedRows
    .map((row) => {
      const activeClass = activeFaceFilters.has(row.personId) ? ' is-active' : '';
      return `<button type="button" class="theme-filter-item face-filter-item${activeClass}" data-face-filter="${escapeAttr(row.personId)}" style="--face-color:${escapeAttr(row.color)}"><span>${escapeHtml(row.label)}</span><em>${row.count} • ${formatConfidencePercent(row.avgConfidence)}</em></button>`;
    })
    .join('');
  updateFilterToggleLabel();
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
  window.requestAnimationFrame(() => {
    if (locationMapInstance) {
      locationMapInstance.invalidateSize();
      updateLocationMapViewport(latestLocationMapPoints);
    }
    if (patternLifeMapInstance) {
      patternLifeMapInstance.invalidateSize();
      updatePatternLifeMapViewport(latestPatternLifeMapPoints);
    }
    if (postingTimezoneMapInstance) postingTimezoneMapInstance.invalidateSize();
  });
}

function renderLocationMap(posts) {
  if (!locationMap || !locationMapEmpty || !locationMapTotal) return;

  const mentions = new Map();
  const locationPairs = Object.entries(LOCATION_COORDS_BY_TAG).map(([tag, details]) => ({ tag, ...details }));
  const locationPairsByName = locationPairs
    .slice()
    .sort((a, b) => b.name.length - a.name.length);
  const addMention = (name, lat, lon) => {
    const key = `${name}|${lat.toFixed(4)}|${lon.toFixed(4)}`;
    const existing = mentions.get(key);
    if (existing) {
      existing.count += 1;
    } else {
      mentions.set(key, { name, lat, lon, count: 1 });
    }
  };
  for (const post of posts) {
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

  for (const profile of (Array.isArray(reconPersonDataProfiles) ? reconPersonDataProfiles : [])) {
    if (!profile || typeof profile !== 'object') continue;
    const name = String(profile.location_name || '').trim();
    const lat = Number(profile.location_latitude);
    const lon = Number(profile.location_longitude);
    if (name && !Number.isNaN(lat) && !Number.isNaN(lon)) {
      addMention(name, lat, lon);
      continue;
    }
    if (!name) continue;
    const loweredName = name.toLowerCase();
    for (const location of locationPairsByName) {
      if (loweredName.includes(location.name.toLowerCase())) {
        addMention(location.name, location.lat, location.lon);
        break;
      }
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

function _locationPairsByName() {
  return Object.values(LOCATION_COORDS_BY_TAG)
    .slice()
    .sort((a, b) => b.name.length - a.name.length);
}

function _resolvedLocationsFromText(text, pairs) {
  const normalized = String(text || '').trim().toLowerCase();
  if (!normalized) return [];
  const hits = [];
  const seen = new Set();
  for (const location of pairs) {
    const candidate = String(location.name || '').trim();
    if (!candidate) continue;
    const lowered = candidate.toLowerCase();
    if (!lowered || seen.has(lowered)) continue;
    const escaped = lowered.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const pattern = new RegExp(`(^|[^a-z0-9])${escaped}([^a-z0-9]|$)`, 'i');
    if (!pattern.test(normalized)) continue;
    seen.add(lowered);
    hits.push(location);
  }
  return hits;
}

function _primaryLocationLabel(locationName, fallbackLabel = 'Unknown') {
  const clean = String(locationName || '').trim();
  if (!clean) return fallbackLabel;
  return clean;
}

function collectPatternOfLifeLocationPoints(posts) {
  const locationPairsByName = _locationPairsByName();
  const pointsByKey = new Map();
  const kindKey = (kind) => {
    const normalized = String(kind || '').trim().toLowerCase();
    if (normalized === 'post' || normalized === 'post_ner' || normalized === 'post_text') return 'post';
    if (normalized === 'pdl') return 'pdl';
    if (normalized === 'numverify') return 'numverify';
    if (normalized === 'osint_industries') return 'osint_industries';
    return 'other';
  };
  const addPoint = (name, lat, lon, reference = null) => {
    const key = `${name}|${Number(lat).toFixed(4)}|${Number(lon).toFixed(4)}`;
    const existing = pointsByKey.get(key);
    if (existing) {
      existing.count += 1;
      const sourceKind = kindKey(reference?.kind);
      existing.sourceCounts.set(sourceKind, (existing.sourceCounts.get(sourceKind) || 0) + 1);
      if (reference && existing.refKeys.size < 24) {
        const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}`;
        if (!existing.refKeys.has(refKey)) {
          existing.refKeys.add(refKey);
          existing.references.push(reference);
        }
      }
      return;
    }
    const references = [];
    const refKeys = new Set();
    const sourceCounts = new Map();
    const sourceKind = kindKey(reference?.kind);
    sourceCounts.set(sourceKind, 1);
    if (reference) {
      const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}`;
      refKeys.add(refKey);
      references.push(reference);
    }
    pointsByKey.set(key, { name, lat, lon, count: 1, references, refKeys, sourceCounts });
  };

  const rows = Array.isArray(posts) ? posts : [];
  for (let postIndex = 0; postIndex < rows.length; postIndex += 1) {
    const post = rows[postIndex];
    const postLabel = `${accountTag(post)} • ${(String(post?.platform || 'unknown').trim() || 'unknown').toUpperCase()}`;
    const postDetail = primaryPostText(post).slice(0, 180);
    const postNerRef = { kind: 'post_ner', label: postLabel, detail: postDetail, postIndex };
    const postTextRef = { kind: 'post_text', label: postLabel, detail: postDetail, postIndex };
    const entities = Array.isArray(post?.entities) ? post.entities : [];
    for (const entity of entities) {
      if (!entity || String(entity.type || '').trim().toLowerCase() !== 'location') continue;
      const name = String(entity.text || '').trim();
      const lat = Number(entity.lat);
      const lon = Number(entity.lon);
      if (!name || Number.isNaN(lat) || Number.isNaN(lon)) continue;
      addPoint(name, lat, lon, postNerRef);
    }

    const tags = Array.isArray(post?.tags) ? post.tags : [];
    for (const tag of tags) {
      const keyTag = String(tag || '').trim().toLowerCase();
      if (!keyTag.startsWith('loc:')) continue;
      const mapped = LOCATION_COORDS_BY_TAG[keyTag];
      if (!mapped) continue;
      addPoint(mapped.name, mapped.lat, mapped.lon, postNerRef);
    }

    const content = String(post?.content || '');
    for (const location of _resolvedLocationsFromText(content, locationPairsByName)) {
      addPoint(location.name, location.lat, location.lon, postTextRef);
    }
  }

  const addFromTextSource = (rawText, label, detail, kind) => {
    const matches = _resolvedLocationsFromText(rawText, locationPairsByName);
    for (const location of matches) {
      addPoint(location.name, location.lat, location.lon, {
        kind,
        label,
        detail: String(detail || '').trim(),
      });
    }
  };

  const pdlProfiles = [];
  if (reconPersonDataProfile && typeof reconPersonDataProfile === 'object' && Object.keys(reconPersonDataProfile).length) {
    pdlProfiles.push(reconPersonDataProfile);
  }
  for (const profile of (Array.isArray(reconPersonDataProfiles) ? reconPersonDataProfiles : [])) {
    if (!profile || typeof profile !== 'object') continue;
    pdlProfiles.push(profile);
  }
  for (const profile of pdlProfiles) {
    const locName = _primaryLocationLabel(profile?.location_name, '');
    if (!locName) continue;
    const label = `PDL: ${String(profile?.full_name || profile?.query_value || 'profile').trim() || 'profile'}`;
    const detail = `primary location: ${locName}`;
    const lat = Number(profile?.location_latitude);
    const lon = Number(profile?.location_longitude);
    if (!Number.isNaN(lat) && !Number.isNaN(lon)) {
      addPoint(locName, lat, lon, { kind: 'pdl', label, detail });
    } else {
      addFromTextSource(locName, label, detail, 'pdl');
    }
  }

  const osintProfiles = Array.isArray(reconOsintProfiles) ? reconOsintProfiles : [];
  for (const profile of osintProfiles) {
    const title = String(profile?.title || profile?.name || profile?.username || 'profile').trim();
    const location = String(profile?.location || '').trim();
    const bio = String(profile?.bio || '').trim();
    if (location) {
      addFromTextSource(location, `OSINT Industries: ${title}`, `location: ${location}`, 'osint_industries');
    }
    if (bio) {
      addFromTextSource(bio, `OSINT Industries: ${title}`, `bio: ${bio.slice(0, 180)}`, 'osint_industries');
    }
  }

  const numverifyProfiles = Array.isArray(reconNumverifyProfiles) ? reconNumverifyProfiles : [];
  for (const profile of numverifyProfiles) {
    const number = String(profile?.number || profile?.international_format || 'number').trim();
    const location = String(profile?.location || '').trim();
    const country = String(profile?.country_name || '').trim();
    if (location) {
      addFromTextSource(location, `Numverify: ${number}`, `location: ${location}`, 'numverify');
    }
    if (country) {
      addFromTextSource(country, `Numverify: ${number}`, `country: ${country}`, 'numverify');
    }
  }

  const points = Array.from(pointsByKey.values())
    .map((row) => ({
      ...row,
      references: row.references.slice(0, 10),
      sourceCounts: Object.fromEntries(row.sourceCounts.entries()),
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
  for (const point of points) {
    delete point.refKeys;
    const sourceRows = Object.entries(point.sourceCounts || {}).sort((a, b) => Number(b[1]) - Number(a[1]));
    point.dominantKind = String(sourceRows[0]?.[0] || 'other');
  }
  return points;
}

function patternLifeMarkerStyle(point, maxCount) {
  const sizeRatio = maxCount > 0 ? Number(point?.count || 0) / maxCount : 0;
  const radius = 4 + Math.max(0.1, sizeRatio) * 8;
  const kind = String(point?.dominantKind || 'other').toLowerCase();
  if (kind === 'post') {
    return { radius, color: '#86efac', fillColor: '#16a34a', fillOpacity: 0.86 };
  }
  if (kind === 'pdl') {
    return { radius, color: '#bfdbfe', fillColor: '#3b82f6', fillOpacity: 0.84 };
  }
  if (kind === 'osint_industries') {
    return { radius, color: '#e9d5ff', fillColor: '#a855f7', fillOpacity: 0.84 };
  }
  if (kind === 'numverify') {
    return { radius, color: '#fef3c7', fillColor: '#f59e0b', fillOpacity: 0.85 };
  }
  return { radius, color: '#d1d5db', fillColor: '#6b7280', fillOpacity: 0.8 };
}

function patternLifePopupPlacement(mapInstance, point) {
  if (!mapInstance || !point) return 'top';
  const markerPoint = mapInstance.latLngToContainerPoint([point.lat, point.lon]);
  const size = mapInstance.getSize();
  const sideThreshold = Math.max(140, Math.round(size.x * 0.24));
  const topThreshold = Math.max(120, Math.round(size.y * 0.22));
  if (markerPoint.y <= topThreshold) return 'bottom';
  if (markerPoint.x <= sideThreshold) return 'right';
  if (markerPoint.x >= (size.x - sideThreshold)) return 'left';
  return 'top';
}

function patternLifePopupOffset(placement) {
  const normalized = String(placement || '').toLowerCase();
  if (normalized === 'left') return [-22, -8];
  if (normalized === 'right') return [22, -8];
  if (normalized === 'bottom') return [0, 18];
  return [0, -10];
}

function highlightPatternLifeLocation(text, locationName) {
  const source = String(text || '');
  const needle = String(locationName || '').trim();
  if (!source || !needle) return escapeHtml(source);
  const escapedNeedle = needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(escapedNeedle, 'ig');
  let lastIndex = 0;
  let match = pattern.exec(source);
  let output = '';
  let found = false;
  while (match) {
    const start = Number(match.index);
    const value = String(match[0] || '');
    output += escapeHtml(source.slice(lastIndex, start));
    output += `<strong class="pattern-life-hit">${escapeHtml(value)}</strong>`;
    lastIndex = start + value.length;
    found = true;
    match = pattern.exec(source);
  }
  output += escapeHtml(source.slice(lastIndex));
  return found ? output : escapeHtml(source);
}

function patternLifePostPreviewMarkup(post, ref, locationName) {
  const postIndex = Number(ref?.postIndex);
  if (!Number.isFinite(postIndex) || postIndex < 0 || !post || typeof post !== 'object') return '';
  const profileImage = postProfileImageUrl(post) || USER_PLACEHOLDER_AVATAR_URL;
  const account = accountTag(post);
  const platform = String(post?.platform || 'unknown').trim().toUpperCase();
  const postType = String(post?.post_type || 'post').trim().toUpperCase();
  const recency = formatRecency(post?.timestamp);
  const content = primaryPostText(post).slice(0, 220);
  const isNerLinked = String(ref?.kind || '').toLowerCase() === 'post_ner';
  const contentMarkup = isNerLinked
    ? highlightPatternLifeLocation(content, locationName)
    : escapeHtml(content);
  const media = normalizeMedia(post);
  const firstMedia = Array.isArray(media) ? media[0] : null;
  const mediaType = String(firstMedia?.type || '').trim().toLowerCase();
  const mediaPreviewUrl = mediaType === 'video'
    ? String(firstMedia?.thumbnail_url || '').trim()
    : String(firstMedia?.url || '').trim();
  const mediaMarkup = mediaPreviewUrl && isHttpUrl(mediaPreviewUrl)
    ? `<div class="pattern-life-post-media"><img src="${escapeAttr(mediaPreviewUrl)}" alt="Post media preview" loading="lazy" /></div>`
    : '';
  const matchBadge = isNerLinked ? '<span class="pattern-life-match-badge">NER location match</span>' : '';

  return `
    <button type="button" class="pattern-life-post-card" data-pattern-life-post-index="${postIndex}" title="Open linked post">
      <div class="pattern-life-post-head">
        <div class="pattern-life-post-account">
          <img class="pattern-life-post-avatar" src="${escapeAttr(profileImage)}" alt="${escapeAttr(account)} profile image" loading="lazy" />
          <span class="pattern-life-post-handle">${escapeHtml(account)}</span>
        </div>
        <span class="pattern-life-post-recency">${escapeHtml(recency)}</span>
      </div>
      <div class="pattern-life-post-tags">
        <span class="source-tag">${escapeHtml(platform)}</span>
        <span class="type-tag">${escapeHtml(postType)}</span>
        ${matchBadge}
      </div>
      <p class="pattern-life-post-content">${contentMarkup}</p>
      ${mediaMarkup}
    </button>
  `;
}

function ensurePatternLifeMapInstance() {
  if (!patternLifeMap) return Promise.resolve(null);
  return loadLeaflet().then((L) => {
    if (!L) return null;
    if (!patternLifeMapInstance) {
      patternLifeMap.innerHTML = '';
      patternLifeMapInstance = L.map(patternLifeMap, {
        zoomControl: false,
        attributionControl: false,
        worldCopyJump: true,
      }).setView([20, 0], 2);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 6,
      }).addTo(patternLifeMapInstance);
      patternLifeMapLayer = L.layerGroup().addTo(patternLifeMapInstance);
    }
    return L;
  });
}

function updatePatternLifeMapViewport(points) {
  if (!patternLifeMapInstance) return;
  const rows = Array.isArray(points) ? points : [];
  if (!rows.length) {
    patternLifeMapInstance.setView([20, 0], 2);
    return;
  }
  const bounds = rows.slice(0, 80).map((point) => [point.lat, point.lon]);
  if (bounds.length === 1) {
    patternLifeMapInstance.setView(bounds[0], 4);
  } else {
    patternLifeMapInstance.fitBounds(bounds, { padding: [20, 20], maxZoom: 4 });
  }
}

function renderPatternLifeMap(posts, analysis = null) {
  if (!patternLifeMap || !patternLifeMapEmpty || !patternLifeLocationMapTotal) return;
  const rows = Array.isArray(posts) ? posts : [];
  const rhythm = analysis || summarizePostingRhythm(posts);
  const points = collectPatternOfLifeLocationPoints(posts);
  latestPatternLifeMapPoints = points;
  const totalMentions = points.reduce((sum, point) => sum + point.count, 0);
  patternLifeLocationMapTotal.textContent = `${totalMentions} point${totalMentions === 1 ? '' : 's'}`;
  patternLifeMapEmpty.classList.toggle('hidden', points.length > 0);

  ensurePatternLifeMapInstance()
    .then((L) => {
      if (!L || !patternLifeMapLayer || !patternLifeMapInstance) return;
      patternLifeMapLayer.clearLayers();

      if (!rhythm?.insufficient) {
        const minOffset = -12;
        const maxOffset = 14;
        const clampedOffset = Math.max(minOffset, Math.min(maxOffset, Number(rhythm?.offset || 0)));
        const centerLongitude = Math.max(-180, Math.min(180, clampedOffset * 15));
        const west = centerLongitude - 15;
        const east = centerLongitude + 15;
        const addCorridor = (westBound, eastBound) => {
          L.rectangle([[-85, westBound], [85, eastBound]], {
            color: 'rgba(59, 130, 246, 0.82)',
            weight: 1,
            fillColor: 'rgba(59, 130, 246, 0.17)',
            fillOpacity: 0.5,
            interactive: false,
          }).addTo(patternLifeMapLayer);
        };
        if (west < -180) {
          addCorridor(west + 360, 180);
          addCorridor(-180, east);
        } else if (east > 180) {
          addCorridor(west, 180);
          addCorridor(-180, east - 360);
        } else {
          addCorridor(west, east);
        }
      }

      if (!points.length) {
        updatePatternLifeMapViewport(points);
        return;
      }

      const maxCount = Math.max(...points.map((point) => point.count), 1);
      for (const point of points.slice(0, 80)) {
        const markerStyle = patternLifeMarkerStyle(point, maxCount);
        const sourceBreakdown = Object.entries(point.sourceCounts || {})
          .sort((a, b) => Number(b[1]) - Number(a[1]))
          .slice(0, 4)
          .map(([kind, count]) => `${kind.replace(/_/g, ' ')}: ${count}`)
          .join(' • ');
        const hasNerLinkedPosts = point.references.some((ref) => String(ref?.kind || '').toLowerCase() === 'post_ner');
        const hoverRows = point.references
          .slice(0, 3)
          .map((ref) => {
            const label = String(ref?.label || '').trim() || 'source';
            const detail = String(ref?.detail || '').trim();
            return `<div><strong>${escapeHtml(label)}</strong>${detail ? `<div>${escapeHtml(detail)}</div>` : ''}</div>`;
          })
          .join('');
        const popupRows = point.references
          .slice(0, 8)
          .map((ref) => {
            const label = String(ref?.label || '').trim() || 'source';
            const detail = String(ref?.detail || '').trim();
            const postIndex = Number(ref?.postIndex);
            if (Number.isFinite(postIndex) && postIndex >= 0) {
              return patternLifePostPreviewMarkup(rows[postIndex], ref, point.name);
            }
            return `<div class="pattern-life-popup-row"><span>${escapeHtml(label)}</span><small>${escapeHtml(detail || 'location signal')}</small></div>`;
          })
          .join('');
        const marker = L.circleMarker([point.lat, point.lon], {
          radius: markerStyle.radius,
          color: markerStyle.color,
          weight: 1.2,
          fillColor: markerStyle.fillColor,
          fillOpacity: markerStyle.fillOpacity,
        });
        if (!hasNerLinkedPosts) {
          marker.bindTooltip(
            `<div class="pattern-life-tooltip"><strong>${escapeHtml(point.name)}</strong><div>${point.count} signal${point.count === 1 ? '' : 's'}</div>${sourceBreakdown ? `<div>${escapeHtml(sourceBreakdown)}</div>` : ''}${hoverRows}</div>`,
            { sticky: true, direction: 'top', opacity: 0.96 },
          );
        }
        marker
          .bindPopup(
            `<div class="pattern-life-popup"><h4>${escapeHtml(point.name)}</h4><p>${point.count} signal${point.count === 1 ? '' : 's'} mapped</p><div class="pattern-life-popup-list">${popupRows}</div></div>`,
            { maxWidth: 320, autoPan: false },
          );
        let isMarkerHovered = false;
        let isPopupHovered = false;
        let popupCloseTimer = null;
        let popupEl = null;
        let popupEnterHandler = null;
        let popupLeaveHandler = null;
        let popupPlacement = 'top';
        const applyPopupPlacement = () => {
          const nextPlacement = patternLifePopupPlacement(patternLifeMapInstance, point);
          popupPlacement = nextPlacement;
          const popup = marker.getPopup();
          if (!popup) return;
          popup.options.offset = L.point(...patternLifePopupOffset(nextPlacement));
          popup.options.maxWidth = (nextPlacement === 'left' || nextPlacement === 'right') ? 380 : 320;
        };
        const clearPopupCloseTimer = () => {
          if (popupCloseTimer) {
            window.clearTimeout(popupCloseTimer);
            popupCloseTimer = null;
          }
        };
        const schedulePopupClose = () => {
          clearPopupCloseTimer();
          popupCloseTimer = window.setTimeout(() => {
            if (!isMarkerHovered && !isPopupHovered) marker.closePopup();
          }, 120);
        };
        marker.on('mouseover', () => {
          isMarkerHovered = true;
          clearPopupCloseTimer();
          applyPopupPlacement();
          marker.openPopup();
        });
        marker.on('mouseout', () => {
          isMarkerHovered = false;
          schedulePopupClose();
        });
        marker.on('popupopen', (event) => {
          const root = event?.popup?.getElement?.();
          if (!(root instanceof HTMLElement)) return;
          popupEl = root;
          root.classList.remove('pattern-life-popup-top', 'pattern-life-popup-right', 'pattern-life-popup-bottom', 'pattern-life-popup-left');
          root.classList.add(`pattern-life-popup-${popupPlacement}`);
          popupEnterHandler = () => {
            isPopupHovered = true;
            clearPopupCloseTimer();
          };
          popupLeaveHandler = () => {
            isPopupHovered = false;
            schedulePopupClose();
          };
          popupEl.addEventListener('mouseenter', popupEnterHandler);
          popupEl.addEventListener('mouseleave', popupLeaveHandler);
        });
        marker.on('popupclose', () => {
          isPopupHovered = false;
          clearPopupCloseTimer();
          if (popupEl && popupEnterHandler) popupEl.removeEventListener('mouseenter', popupEnterHandler);
          if (popupEl && popupLeaveHandler) popupEl.removeEventListener('mouseleave', popupLeaveHandler);
          popupEl = null;
          popupEnterHandler = null;
          popupLeaveHandler = null;
        });
        marker.addTo(patternLifeMapLayer);
      }
      updatePatternLifeMapViewport(points);
      if (activeResultsView === 'pattern') {
        window.requestAnimationFrame(() => patternLifeMapInstance?.invalidateSize());
      }
    })
    .catch(() => {
      patternLifeMap.textContent = points.length
        ? points.slice(0, 8).map((item) => `${item.name} (${item.count})`).join(' • ')
        : 'Map unavailable';
    });
}

function renderPatternOfLife(posts) {
  const analysis = summarizePostingRhythm(posts);
  renderPatternPostingRhythm(posts, analysis);
  renderPatternLifeMap(posts, analysis);
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

function _buildSignalItems(posts, fieldName, maxItems = 12) {
  const counts = new Map();
  for (let i = 0; i < posts.length; i += 1) {
    const values = _signalValuesForField(posts[i], fieldName);
    for (const value of values) {
      const text = String(value || '').trim();
      if (!text) continue;
      const key = text.toLowerCase();
      const current = counts.get(key);
      if (current) {
        current.count += 1;
      } else {
        counts.set(key, { text, count: 1 });
      }
    }
  }
  return Array.from(counts.values())
    .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text))
    .slice(0, maxItems);
}

function _buildSignalRows(posts, fieldName, cssClass, maxItems = 12) {
  const items = _buildSignalItems(posts, fieldName, maxItems);
  return items
    .map(
      (item) => {
        const value = String(item.text || '').trim().toLowerCase();
        const isActive = activeSignalFilters.has(`${fieldName}|${value}`) ? ' is-active' : '';
        return `<button type="button" class="signal-row ${cssClass}${isActive}" data-signal-field="${escapeAttr(fieldName)}" data-signal-value="${escapeAttr(value)}"><span>${escapeHtml(item.text)}</span><strong>${item.count}</strong></button>`;
      },
    )
    .join('');
}

function renderThreatMix(posts) {
  if (!threatMix || !threatMixEmpty) return;
  const markup = _buildSignalRows(posts, 'threat_categories', 'signal-threat-row', 8);
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
  const markup = _buildSignalRows(posts, 'selector_matches', 'signal-selector-row', 12);
  if (!markup) {
    selectorMix.innerHTML = '';
    selectorMixEmpty.classList.remove('hidden');
    return;
  }
  selectorMixEmpty.classList.add('hidden');
  selectorMix.innerHTML = markup;
}

function renderCustomKeywordMix(posts) {
  if (!customKeywordMix || !customKeywordMixEmpty) return;
  const keywords = normalizeCustomKeywordList(configCustomKeywordList);
  if (!keywords.length) {
    customKeywordMix.innerHTML = '';
    customKeywordMixEmpty.textContent = 'No custom keywords configured. Add keywords in Configuration.';
    customKeywordMixEmpty.classList.remove('hidden');
    return;
  }
  const rows = Array.isArray(posts) ? posts : [];
  const counts = keywords
    .map((term) => {
      let count = 0;
      for (const post of rows) {
        if (postMentionsCustomKeyword(post, term)) count += 1;
      }
      return { term, count, termLower: term.toLowerCase() };
    })
    .filter((row) => row.count > 0)
    .sort((a, b) => b.count - a.count || a.term.localeCompare(b.term))
    .slice(0, 20);
  if (!counts.length) {
    customKeywordMix.innerHTML = '';
    customKeywordMixEmpty.textContent = 'No configured custom keyword mentions in current results.';
    customKeywordMixEmpty.classList.remove('hidden');
    return;
  }
  customKeywordMixEmpty.classList.add('hidden');
  customKeywordMix.innerHTML = counts
    .map((row) => {
      const activeClass = activeCustomKeywordFilters.has(row.termLower) ? ' is-active' : '';
      return `<button type="button" class="signal-row signal-custom-keyword-row${activeClass}" data-custom-keyword="${escapeAttr(row.termLower)}"><span>${escapeHtml(row.term)}</span><strong>${row.count}</strong></button>`;
    })
    .join('');
}

function renderThreatSignalMix(posts) {
  if (!threatSignalMix || !threatSignalMixEmpty) return;
  const markup = _buildSignalRows(posts, 'threat_signal_categories', 'signal-threat-row', 8);
  if (!markup) {
    threatSignalMix.innerHTML = '';
    threatSignalMixEmpty.classList.remove('hidden');
    return;
  }
  threatSignalMixEmpty.classList.add('hidden');
  threatSignalMix.innerHTML = markup;
}

function _renderRadar(target, items) {
  if (!target) return;
  const rows = Array.isArray(items) ? items : [];
  if (!rows.length) {
    target.innerHTML = '';
    return;
  }
  const top = rows.slice(0, 6);
  const size = 320;
  const cx = 160;
  const cy = 120;
  const radius = 84;
  const maxCount = Math.max(...top.map((row) => row.count), 1);
  const levels = [0.25, 0.5, 0.75, 1];
  const angleStep = (Math.PI * 2) / top.length;
  const points = top.map((row, index) => {
    const angle = -Math.PI / 2 + index * angleStep;
    const scaled = (row.count / maxCount) * radius;
    return {
      x: cx + Math.cos(angle) * scaled,
      y: cy + Math.sin(angle) * scaled,
      ax: cx + Math.cos(angle) * (radius + 16),
      ay: cy + Math.sin(angle) * (radius + 16),
      label: row.text,
    };
  });
  const polygon = points.map((point) => `${point.x.toFixed(2)},${point.y.toFixed(2)}`).join(' ');
  const grid = levels
    .map((level) => {
      const ring = top
        .map((_, idx) => {
          const angle = -Math.PI / 2 + idx * angleStep;
          const rr = radius * level;
          return `${(cx + Math.cos(angle) * rr).toFixed(2)},${(cy + Math.sin(angle) * rr).toFixed(2)}`;
        })
        .join(' ');
      return `<polygon class="radar-grid" points="${ring}" />`;
    })
    .join('');
  const spokes = top
    .map((_, idx) => {
      const angle = -Math.PI / 2 + idx * angleStep;
      const x = cx + Math.cos(angle) * radius;
      const y = cy + Math.sin(angle) * radius;
      return `<line class="radar-spoke" x1="${cx}" y1="${cy}" x2="${x.toFixed(2)}" y2="${y.toFixed(2)}"></line>`;
    })
    .join('');
  const labels = points
    .map((point) => `<text class="radar-label" x="${point.ax.toFixed(2)}" y="${point.ay.toFixed(2)}">${escapeHtml(point.label)}</text>`)
    .join('');
  target.innerHTML = `
    ${grid}
    ${spokes}
    <polygon class="radar-shape" points="${polygon}" />
    ${labels}
  `;
}

function renderLLMPrimaryMix(posts) {
  if (!llmPrimaryMix || !llmPrimaryMixEmpty) return;
  const items = _buildSignalItems(posts, 'llm_primary_warning_behaviours', 12);
  const markup = _buildSignalRows(posts, 'llm_primary_warning_behaviours', 'signal-llm-row', 12);
  if (!markup) {
    llmPrimaryMix.innerHTML = '';
    llmPrimaryMixEmpty.classList.remove('hidden');
  } else {
    llmPrimaryMixEmpty.classList.add('hidden');
    llmPrimaryMix.innerHTML = markup;
  }
  _renderRadar(llmPrimaryRadar, items);
}

function renderLLMSecondaryMix(posts) {
  if (!llmSecondaryMix || !llmSecondaryMixEmpty) return;
  const items = _buildSignalItems(posts, 'llm_secondary_risk_factors', 12);
  const markup = _buildSignalRows(posts, 'llm_secondary_risk_factors', 'signal-llm-secondary-row', 12);
  if (!markup) {
    llmSecondaryMix.innerHTML = '';
    llmSecondaryMixEmpty.classList.remove('hidden');
  } else {
    llmSecondaryMixEmpty.classList.add('hidden');
    llmSecondaryMix.innerHTML = markup;
  }
  _renderRadar(llmSecondaryRadar, items);
}

function renderLLMThemeMix(posts) {
  if (!llmThemeMix || !llmThemeMixEmpty) return;
  const counts = new Map();
  const list = Array.isArray(posts) ? posts : [];
  for (let idx = 0; idx < list.length; idx += 1) {
    const post = list[idx];
    const assessment = llmAssessmentFromPost(post);
    const primary = llmAssessmentPrimary(assessment);
    const secondary = llmAssessmentSecondary(assessment);
    if (!primary.length && !secondary.length) continue;
    const theme = String(assessment?.underlying_theme || '').trim();
    if (!theme) continue;
    const existing = counts.get(theme);
    if (existing) {
      existing.count += 1;
    } else {
      counts.set(theme, { text: theme, count: 1, postIndex: idx });
    }
  }
  const rows = Array.from(counts.values())
    .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text))
    .slice(0, 12);
  if (!rows.length) {
    llmThemeMix.innerHTML = '';
    llmThemeMixEmpty.classList.remove('hidden');
    return;
  }
  llmThemeMixEmpty.classList.add('hidden');
  llmThemeMix.innerHTML = rows
    .map((row) => `<button type="button" class="signal-row signal-llm-theme-row" data-post-index="${row.postIndex}" title="Jump to associated post"><span>${escapeHtml(row.text)}</span><strong>${row.count}</strong></button>`)
    .join('');
}

function updateAiThreatAssessmentControls(posts) {
  if (!(runAiThreatAssessmentBtn instanceof HTMLButtonElement)) return;
  const candidates = llmAssessmentCandidatePosts(posts);
  const hasCandidates = candidates.length > 0;
  if (aiThreatAssessmentCard instanceof HTMLElement) {
    aiThreatAssessmentCard.classList.toggle('hidden', !hasCandidates);
  }
  if (!hasCandidates) {
    if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = '';
    return;
  }
  runAiThreatAssessmentBtn.classList.remove('hidden');
}

function renderVisuals(posts) {
  renderTimeline(posts);
  renderPostingRhythm(posts);
  renderKeywordChart(posts);
  renderLocationMap(posts);
  renderEntityMix(posts);
  renderSelectorMix(posts);
  renderCustomKeywordMix(posts);
  renderThreatMix(posts);
  renderThreatSignalMix(posts);
  renderLLMCoverage(posts);
  renderLLMPrimaryMix(posts);
  renderLLMSecondaryMix(posts);
  renderLLMThemeMix(posts);
  updateAiThreatAssessmentControls(posts);
  renderTypeMix(posts);
  renderPatternOfLife(latestPosts);
}

async function refreshPosts(options = {}) {
  const forceFaceRefresh = options && options.forceFaceRefresh === true;
  if (controller) controller.abort();
  controller = new AbortController();

  const query = searchInput.value.trim();
  const sort = sortSelect.value;
  const params = new URLSearchParams({ query, sort });
  if (activeCaseId) params.set('case_id', activeCaseId);
  const tags = selectedTags();
  if (activeStartDate) params.set('start_date', activeStartDate);
  if (activeEndDate) params.set('end_date', activeEndDate);
  if (tags.include.length) params.set('include_tags', tags.include.join(','));
  const includeFaceAnalysis = forceFaceRefresh || activeFaceFilters.size > 0;
  if (includeFaceAnalysis) params.set('include_faces', '1');
  if (forceFaceRefresh) params.set('face_refresh', '1');

  dashboardBaseStatus = '';
  updateStatusLine();

  try {
    const response = await fetch(`/api/posts?${params.toString()}`, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    latestFaceClusters = Array.isArray(data?.face_clusters) ? data.face_clusters : [];
    latestFaceRecognition = data?.face_recognition && typeof data.face_recognition === 'object'
      ? data.face_recognition
      : { available: false, reason: 'unknown' };
    renderFaceRecognitionFilters();
    const filteredPosts = applyDashboardFilters(data.posts || []);
    renderPosts(filteredPosts);
    dashboardBaseStatus = '';
    updateStatusLine();
  } catch (error) {
    if (error.name === 'AbortError') return;
    console.error(error);
    latestFaceClusters = [];
    latestFaceRecognition = { available: false, reason: 'request_failed' };
    renderFaceRecognitionFilters();
    dashboardBaseStatus = 'Failed to load posts.';
    updateStatusLine();
    resultsEl.innerHTML = '<div class="empty">Could not load data from /api/posts.</div>';
  }
}

function queueRefresh() {
  clearTimeout(requestTimer);
  requestTimer = setTimeout(refreshPosts, 250);
}

function applyResultsViewButtonState() {
  const postView = activeResultsView === 'posts';
  const mediaView = activeResultsView === 'media';
  const footprintMode = activeResultsView === 'footprint';
  const patternLifeMode = activeResultsView === 'pattern';
  viewPostsBtn?.classList.toggle('is-active', postView);
  viewMediaBtn?.classList.toggle('is-active', mediaView);
  viewFootprintBtn?.classList.toggle('is-active', footprintMode);
  viewPatternLifeBtn?.classList.toggle('is-active', patternLifeMode);
  viewPostsBtn?.setAttribute('aria-pressed', String(postView));
  viewMediaBtn?.setAttribute('aria-pressed', String(mediaView));
  viewFootprintBtn?.setAttribute('aria-pressed', String(footprintMode));
  viewPatternLifeBtn?.setAttribute('aria-pressed', String(patternLifeMode));
  const hideStandardLayout = footprintMode || patternLifeMode;
  resultsEl?.classList.toggle('hidden', hideStandardLayout);
  dashboardContent?.classList.toggle('media-grid-mode', mediaView);
  const insightsEl = dashboardContent?.querySelector('.insights');
  if (insightsEl instanceof HTMLElement) insightsEl.classList.toggle('hidden', hideStandardLayout || mediaView);
  footprintView?.classList.toggle('hidden', !footprintMode);
  patternLifeView?.classList.toggle('hidden', !patternLifeMode);
  if (filterMenu instanceof HTMLElement) filterMenu.classList.toggle('hidden', hideStandardLayout);
}

function setResultsView(mode) {
  const normalized = String(mode || '').trim().toLowerCase();
  const next = normalized === 'media'
    ? 'media'
    : (normalized === 'footprint' ? 'footprint' : (normalized === 'pattern' ? 'pattern' : 'posts'));
  if (activeResultsView === next) return;
  activeResultsView = next;
  if (activeResultsView === 'footprint') {
    ensureAtLeastOneReconSelectorRow(footprintSelectorsList);
  }
  applyResultsViewButtonState();
  if (activeResultsView === 'pattern') {
    renderPatternOfLife(latestPosts);
    refreshMapLayout();
    window.setTimeout(refreshMapLayout, 80);
  }
  renderPosts(latestPosts);
}

function openPostModal(postIndex) {
  const index = Number(postIndex);
  if (!Number.isFinite(index) || index < 0) return;
  const post = latestRenderedPosts[index];
  if (!post) return;
  if (postModalTitle) {
    const account = accountTag(post);
    postModalTitle.textContent = `${account} • ${(post.platform || 'Unknown').toUpperCase()}`;
  }
  if (postModalBody) {
    postModalBody.innerHTML = renderPostCard(post, index, { includeCardId: false, fullContent: true, assessmentEditable: false });
  }
  postModal?.classList.remove('hidden');
  syncModalActiveState();
}

function closePostModal() {
  postModal?.classList.add('hidden');
  if (postModalBody) postModalBody.innerHTML = '';
  syncModalActiveState();
}

function setModalOpen(isOpen) {
  if (!isOpen && lockModalUntilCollectionData && !collectionLoadedAnyData) {
    setupStatus.textContent = 'Please wait. Dashboard opens after first result arrives.';
    showNotificationOnce('wait_first_results', 'Waiting for first results', 'warn');
    return;
  }
  setupModal.classList.toggle('hidden', !isOpen);
  if (!isOpen) hideReconPreview();
  syncModalActiveState();
}

function openManualInsertModal() {
  if (!activeCaseId) {
    showNotification('Open a case first.', 'warn');
    return;
  }
  if (manualInsertTextInput instanceof HTMLTextAreaElement) manualInsertTextInput.value = '';
  if (manualInsertFileInput instanceof HTMLInputElement) manualInsertFileInput.value = '';
  if (manualInsertAuthorInput instanceof HTMLInputElement) manualInsertAuthorInput.value = '';
  if (manualInsertUrlInput instanceof HTMLInputElement) manualInsertUrlInput.value = '';
  if (manualInsertSourceInput instanceof HTMLInputElement) manualInsertSourceInput.value = '';
  if (manualInsertStatus instanceof HTMLElement) manualInsertStatus.textContent = '';
  manualInsertModal?.classList.remove('hidden');
  syncModalActiveState();
  manualInsertTextInput?.focus();
}

function closeManualInsertModal() {
  manualInsertModal?.classList.add('hidden');
  syncModalActiveState();
}

function syncModalActiveState() {
  const setupOpen = setupModal && !setupModal.classList.contains('hidden');
  const editOpen = caseEditModal && !caseEditModal.classList.contains('hidden');
  const saveOpen = caseSaveModal && !caseSaveModal.classList.contains('hidden');
  const notesOpen = caseNotesModal && !caseNotesModal.classList.contains('hidden');
  const configOpen = configModal && !configModal.classList.contains('hidden');
  const manualInsertOpen = manualInsertModal && !manualInsertModal.classList.contains('hidden');
  const postOpen = postModal && !postModal.classList.contains('hidden');
  document.body.classList.toggle('modal-active', Boolean(setupOpen || editOpen || saveOpen || notesOpen || configOpen || manualInsertOpen || postOpen));
}

function openConfigModal() {
  configModal?.classList.remove('hidden');
  configStatus.textContent = '';
  syncModalActiveState();
  loadConfig();
  configPdlApiKeyInput?.focus();
}

function closeConfigModal() {
  configModal?.classList.add('hidden');
  syncModalActiveState();
}

async function loadConfig() {
  const setConfiguredHint = (inputEl, hintEl, configured, mode) => {
    if (!(inputEl instanceof HTMLInputElement) || !(hintEl instanceof HTMLElement)) return;
    const field = inputEl.closest('.config-secret-field');
    const storage = mode ? ` (${mode})` : '';
    const emptyPlaceholder = String(inputEl.getAttribute('data-empty-placeholder') || inputEl.placeholder || '').trim();
    const configuredPlaceholder = String(inputEl.getAttribute('data-configured-placeholder') || 'Stored key detected. Enter new key to replace.').trim();
    inputEl.value = '';
    if (configured) {
      inputEl.dataset.secretState = 'configured';
      inputEl.placeholder = configuredPlaceholder;
      if (field instanceof HTMLElement) {
        field.dataset.secretState = 'configured';
      }
      hintEl.dataset.secretState = 'configured';
      hintEl.textContent = `Stored key detected${storage}. Leave blank to keep the current key.`;
      return;
    }
    inputEl.dataset.secretState = 'empty';
    inputEl.placeholder = emptyPlaceholder;
    if (field instanceof HTMLElement) {
      field.dataset.secretState = 'empty';
    }
    hintEl.dataset.secretState = 'empty';
    hintEl.textContent = `No stored key found${storage}. Paste a key and click Save.`;
  };
  const summarizeSecretState = (count, total, mode) => {
    if (!(configSecretStateSummary instanceof HTMLElement)) return;
    configSecretStateSummary.dataset.secretState = count > 0 ? 'configured' : 'empty';
    if (!count) {
      configSecretStateSummary.textContent = 'No API keys are loaded from previous sessions. All key fields are currently empty.';
      return;
    }
    const plural = count === 1 ? 'key is' : 'keys are';
    const source = mode ? ` via ${mode}` : '';
    configSecretStateSummary.textContent = `${count} of ${total} API ${plural} already loaded${source}. Leave fields blank to keep existing keys.`;
  };
  try {
    const response = await fetch('/api/config');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const storageMode = String(payload?.secret_storage_mode || '').trim();
    if (configOsintIndustriesPremiumInput instanceof HTMLInputElement) {
      configOsintIndustriesPremiumInput.checked = Boolean(payload?.osint_industries_use_premium);
    }
    if (configCustomKeywordInput instanceof HTMLInputElement) configCustomKeywordInput.value = '';
    configCustomKeywordList = normalizeCustomKeywordList(payload?.custom_keyword_list);
    const validKeywords = new Set(configCustomKeywordList.map((item) => item.toLowerCase()));
    for (const keyword of Array.from(activeCustomKeywordFilters)) {
      if (!validKeywords.has(keyword)) activeCustomKeywordFilters.delete(keyword);
    }
    renderConfigCustomKeywordPills();
    renderCustomKeywordMix(latestPosts);
    updateFilterToggleLabel();
    const secretFlags = [
      Boolean(payload?.pdl_api_key_configured),
      Boolean(payload?.osint_industries_api_key_configured),
      Boolean(payload?.numverify_api_key_configured),
      Boolean(payload?.openai_api_key_configured),
    ];
    summarizeSecretState(secretFlags.filter(Boolean).length, secretFlags.length, storageMode);
    setConfiguredHint(configPdlApiKeyInput, configPdlApiKeyHint, secretFlags[0], storageMode);
    setConfiguredHint(configOsintIndustriesApiKeyInput, configOsintIndustriesApiKeyHint, secretFlags[1], storageMode);
    setConfiguredHint(configNumverifyApiKeyInput, configNumverifyApiKeyHint, secretFlags[2], storageMode);
    setConfiguredHint(configOpenAiApiKeyInput, configOpenAiApiKeyHint, secretFlags[3], storageMode);
  } catch (error) {
    console.error(error);
    if (configStatus) configStatus.textContent = 'Failed to load configuration.';
    if (configSecretStateSummary instanceof HTMLElement) {
      configSecretStateSummary.dataset.secretState = 'error';
      configSecretStateSummary.textContent = 'Unable to determine saved API key status right now.';
    }
  }
}

async function saveConfig(event) {
  event.preventDefault();
  if (
    !configPdlApiKeyInput
    || !configOsintIndustriesApiKeyInput
    || !configNumverifyApiKeyInput
    || !configOpenAiApiKeyInput
    || !(configOsintIndustriesPremiumInput instanceof HTMLInputElement)
  ) return;
  if (configSaveBtn instanceof HTMLButtonElement) configSaveBtn.disabled = true;
  if (configStatus) configStatus.textContent = 'Saving configuration...';
  try {
    if (configCustomKeywordInput instanceof HTMLInputElement) {
      addConfigCustomKeywordTerm(configCustomKeywordInput.value);
      configCustomKeywordInput.value = '';
    }
    const body = {
      osint_industries_use_premium: Boolean(configOsintIndustriesPremiumInput.checked),
      custom_keyword_list: normalizeCustomKeywordList(configCustomKeywordList),
    };
    const pdlKey = String(configPdlApiKeyInput.value || '').trim();
    const osintKey = String(configOsintIndustriesApiKeyInput.value || '').trim();
    const numverifyKey = String(configNumverifyApiKeyInput.value || '').trim();
    const openAiKey = String(configOpenAiApiKeyInput.value || '').trim();
    if (pdlKey) body.pdl_api_key = pdlKey;
    if (osintKey) body.osint_industries_api_key = osintKey;
    if (numverifyKey) body.numverify_api_key = numverifyKey;
    if (openAiKey) body.openai_api_key = openAiKey;
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    await loadConfig();
    if (configStatus) {
      configStatus.textContent = 'Configuration saved. API keys are write-only and never returned by the API.';
    }
  } catch (error) {
    console.error(error);
    if (configStatus) configStatus.textContent = `Failed to save configuration: ${error.message || 'unknown error'}`;
  } finally {
    if (configSaveBtn instanceof HTMLButtonElement) configSaveBtn.disabled = false;
  }
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const raw = String(reader.result || '');
      const splitIndex = raw.indexOf(',');
      if (splitIndex < 0) {
        resolve('');
        return;
      }
      resolve(raw.slice(splitIndex + 1));
    };
    reader.onerror = () => reject(reader.error || new Error('file read failed'));
    reader.readAsDataURL(file);
  });
}

async function submitManualInsert(event) {
  event.preventDefault();
  if (!activeCaseId) {
    if (manualInsertStatus) manualInsertStatus.textContent = 'Open a case before inserting content.';
    return;
  }
  const text = String(manualInsertTextInput?.value || '').trim();
  const file = manualInsertFileInput instanceof HTMLInputElement ? manualInsertFileInput.files?.[0] : null;
  const authorName = String(manualInsertAuthorInput?.value || '').trim();
  const sourceUrl = String(manualInsertUrlInput?.value || '').trim();
  const source = String(manualInsertSourceInput?.value || '').trim();
  if (!text && !file) {
    if (manualInsertStatus) manualInsertStatus.textContent = 'Enter freeform text or choose a file.';
    return;
  }
  if (sourceUrl && !isHttpUrl(sourceUrl)) {
    if (manualInsertStatus) manualInsertStatus.textContent = 'URL must start with http:// or https://';
    return;
  }

  if (manualInsertSaveBtn instanceof HTMLButtonElement) manualInsertSaveBtn.disabled = true;
  if (manualInsertStatus) manualInsertStatus.textContent = 'Saving manual content...';
  try {
    const payload = {
      case_id: activeCaseId,
      text,
      author_name: authorName,
      source_url: sourceUrl,
      source,
    };
    if (file) {
      payload.file_name = String(file.name || '').trim();
      payload.file_mime_type = String(file.type || '').trim();
      payload.file_content_base64 = await readFileAsBase64(file);
    }
    const response = await fetch('/api/posts/manual', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    if (manualInsertStatus) manualInsertStatus.textContent = 'Manual content saved as post.';
    closeManualInsertModal();
    queueRefresh();
    showNotification('Manual content inserted.', 'success');
  } catch (error) {
    console.error(error);
    if (manualInsertStatus) manualInsertStatus.textContent = `Manual insert failed: ${error.message || 'unknown error'}`;
  } finally {
    if (manualInsertSaveBtn instanceof HTMLButtonElement) manualInsertSaveBtn.disabled = false;
  }
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
    setupSubtitle.textContent = 'Scan social platforms and enrichment sources for usernames, emails, phones, names, and wallets.';
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
  if (addReconSelectorBtn instanceof HTMLButtonElement) addReconSelectorBtn.disabled = isBusy;
  if (reconSelectorsList instanceof HTMLElement) {
    const controls = reconSelectorsList.querySelectorAll('select, input, button');
    for (const control of controls) {
      if (control instanceof HTMLSelectElement || control instanceof HTMLInputElement || control instanceof HTMLButtonElement) {
        control.disabled = isBusy;
      }
    }
  }
  useReconTargetsBtn.disabled = isBusy || !reconTargets.length;
  if (goReconAssessmentBtn instanceof HTMLButtonElement) {
    goReconAssessmentBtn.disabled = isBusy;
  }
}

function setFootprintBusy(isBusy) {
  if (footprintReconBtn instanceof HTMLButtonElement) footprintReconBtn.disabled = isBusy;
  if (addFootprintSelectorBtn instanceof HTMLButtonElement) addFootprintSelectorBtn.disabled = isBusy;
  if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = isBusy || !reconTargets.length;
  if (footprintSelectorsList instanceof HTMLElement) {
    const controls = footprintSelectorsList.querySelectorAll('select, input, button');
    for (const control of controls) {
      if (control instanceof HTMLSelectElement || control instanceof HTMLInputElement || control instanceof HTMLButtonElement) {
        control.disabled = isBusy;
      }
    }
  }
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
  const screenshotUrl = String(row.screenshot_url || '').trim();
  const source = String(row.source || '').trim().toLowerCase();
  const icon = faviconMarkup(label, url);
  const content = `<span class="recon-label">${icon}<span>${escapeHtml(label)}</span></span>`;
  const classes = source === 'pdl' ? `${clsName} pdl` : clsName;
  if (!url) return `<span class="recon-pill ${escapeHtml(classes)}">${content}</span>`;
  const previewAttr = screenshotUrl ? ` data-preview-image="${escapeAttr(screenshotUrl)}"` : '';
  const previewLabelAttr = screenshotUrl ? ` data-preview-label="${escapeAttr(label)}"` : '';
  return `<a class="recon-pill ${escapeHtml(classes)} lead-link" target="_blank" rel="noopener noreferrer" href="${escapeHtml(url)}"${previewAttr}${previewLabelAttr}>${content}</a>`;
}

function ensureReconPreviewTooltip() {
  if (reconPreviewTooltipEl instanceof HTMLElement) return reconPreviewTooltipEl;
  const el = document.createElement('div');
  el.className = 'recon-preview-tooltip hidden';
  el.innerHTML = '<img class="recon-preview-image" alt="Recon page preview" loading="lazy" /><div class="recon-preview-label"></div>';
  document.body.appendChild(el);
  reconPreviewTooltipEl = el;
  return el;
}

function positionReconPreviewTooltip(mouseEvent) {
  const tooltip = ensureReconPreviewTooltip();
  const margin = 14;
  const desiredX = mouseEvent.clientX + 16;
  const desiredY = mouseEvent.clientY + 16;
  const rect = tooltip.getBoundingClientRect();
  const maxX = Math.max(margin, window.innerWidth - rect.width - margin);
  const maxY = Math.max(margin, window.innerHeight - rect.height - margin);
  const x = Math.min(desiredX, maxX);
  const y = Math.min(desiredY, maxY);
  tooltip.style.left = `${Math.max(margin, x)}px`;
  tooltip.style.top = `${Math.max(margin, y)}px`;
}

function showReconPreview(anchor, mouseEvent) {
  if (!(anchor instanceof HTMLAnchorElement)) return;
  const src = String(anchor.getAttribute('data-preview-image') || '').trim();
  if (!src) return;
  const label = String(anchor.getAttribute('data-preview-label') || '').trim() || 'Preview';
  const tooltip = ensureReconPreviewTooltip();
  const img = tooltip.querySelector('.recon-preview-image');
  const text = tooltip.querySelector('.recon-preview-label');
  if (!(img instanceof HTMLImageElement) || !(text instanceof HTMLElement)) return;
  img.src = src;
  text.textContent = label;
  tooltip.classList.remove('hidden');
  activeReconPreviewAnchor = anchor;
  positionReconPreviewTooltip(mouseEvent);
}

function hideReconPreview() {
  if (!(reconPreviewTooltipEl instanceof HTMLElement)) return;
  reconPreviewTooltipEl.classList.add('hidden');
  const img = reconPreviewTooltipEl.querySelector('.recon-preview-image');
  if (img instanceof HTMLImageElement) img.src = '';
  activeReconPreviewAnchor = null;
}

function attachReconPreviewHandlers(container) {
  if (!(container instanceof HTMLElement)) return;
  container.addEventListener('mouseover', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    const anchor = target.closest('a[data-preview-image]');
    if (!(anchor instanceof HTMLAnchorElement)) return;
    showReconPreview(anchor, event);
  });
  container.addEventListener('mousemove', (event) => {
    if (!(activeReconPreviewAnchor instanceof HTMLAnchorElement)) return;
    positionReconPreviewTooltip(event);
  });
  container.addEventListener('mouseout', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    const fromAnchor = target.closest('a[data-preview-image]');
    if (!(fromAnchor instanceof HTMLAnchorElement)) return;
    const related = event.relatedTarget;
    if (related instanceof Node && fromAnchor.contains(related)) return;
    hideReconPreview();
  });
}

function personDataProfileMarkup(profile, totalProfiles = 0, pdlProfiles = []) {
  if (!profile || typeof profile !== 'object' || !Object.keys(profile).length) {
    return '';
  }
  const fullName = String(profile.full_name || '').trim();
  const title = String(profile.job_title || '').trim();
  const company = String(profile.job_company_name || '').trim();
  const location = String(profile.location_name || '').trim();
  const queryType = String(profile.query_type || '').trim() || 'unknown';
  const queryValue = String(profile.query_value || '').trim() || 'unknown';
  const proEmail = String(profile.professional_email || profile.work_email || '').trim();
  const personalEmails = Array.isArray(profile.personal_emails) ? profile.personal_emails.filter(Boolean).map((item) => String(item).trim()) : [];
  const mobilePhone = String(profile.mobile_phone || profile.phone || '').trim();
  const personalPhones = Array.isArray(profile.personal_phones) ? profile.personal_phones.filter(Boolean).map((item) => String(item).trim()) : [];
  const professionalPhones = Array.isArray(profile.professional_phones) ? profile.professional_phones.filter(Boolean).map((item) => String(item).trim()) : [];
  const professionalContacts = [];
  const personalContacts = [];
  if (proEmail) professionalContacts.push(proEmail);
  for (const item of professionalPhones) professionalContacts.push(item);
  for (const item of personalEmails) personalContacts.push(item);
  if (mobilePhone) personalContacts.push(mobilePhone);
  for (const item of personalPhones) personalContacts.push(item);
  const uniqueValues = (values) => {
    const output = [];
    const seen = new Set();
    for (const item of values) {
      const clean = String(item || '').trim();
      const key = clean.toLowerCase();
      if (!clean || seen.has(key)) continue;
      seen.add(key);
      output.push(clean);
    }
    return output;
  };
  const professionalValues = uniqueValues(professionalContacts);
  const personalValues = uniqueValues(personalContacts);
  const contactGroupMarkup = (heading, values) => `
    <div class="pdl-contact-group">
      <span class="pdl-contact-heading">${escapeHtml(heading)}</span>
      <div class="recon-pills pdl-contact-pills">
        ${values.length ? values.map((value) => `<span class="recon-pill">${escapeHtml(value)}</span>`).join('') : '<span class="recon-pill">None</span>'}
      </div>
    </div>
  `;
  const normalizePDLProfileUrl = (rawUrl) => {
    const raw = String(rawUrl || '').trim();
    if (!raw) return '';
    if (/^https?:\/\//i.test(raw)) return raw;
    const candidate = raw.replace(/^\/+/, '');
    if (/^(?:www\.)?(?:facebook|linkedin|twitter|x|instagram|reddit|youtube|github|gitlab)\.com\//i.test(candidate)) {
      return `https://${candidate}`;
    }
    if (/^bsky\.app\//i.test(candidate)) {
      return `https://${candidate}`;
    }
    return raw;
  };
  const siteFromUrl = (url) => {
    const value = normalizePDLProfileUrl(url);
    if (!value) return '';
    try {
      const host = String(new URL(value).hostname || '').replace(/^www\./i, '').toLowerCase();
      if (host.includes('linkedin.com')) return 'LinkedIn';
      if (host.includes('facebook.com')) return 'Facebook';
      if (host.includes('x.com') || host.includes('twitter.com')) return 'Twitter/X';
      if (host.includes('reddit.com')) return 'Reddit';
      if (host.includes('instagram.com')) return 'Instagram';
      if (host.includes('youtube.com') || host.includes('youtu.be')) return 'YouTube';
      if (host.includes('github.com')) return 'GitHub';
      if (host.includes('gitlab.com')) return 'GitLab';
      return host || 'profile';
    } catch (error) {
      return 'profile';
    }
  };
  const identificationText = (() => {
    if (queryType === 'profile') {
      const site = siteFromUrl(queryValue) || 'profile';
      return `Identified by ${site} profile found via username.`;
    }
    if (queryType === 'email') {
      return 'Identified by email lookup via People Data Labs.';
    }
    return 'Identified via People Data Labs enrichment.';
  })();
  const fallbackProfileUrls = Array.isArray(profile.profile_urls)
    ? profile.profile_urls
    : ['linkedin_url', 'facebook_url', 'twitter_url', 'github_url']
      .map((key) => String(profile?.[key] || '').trim())
      .filter(Boolean);
  const mergedProfileRows = (() => {
    const rows = [];
    const seen = new Set();
    const addRow = (row) => {
      const url = normalizePDLProfileUrl(row?.profile_url);
      if (!url) return;
      const key = url.toLowerCase();
      if (seen.has(key)) return;
      seen.add(key);
      const derivedSite = siteFromUrl(url);
      const explicitSite = String(row?.site || '').trim();
      const siteLabel = explicitSite && !['profile', 'lead', 'unknown'].includes(explicitSite.toLowerCase())
        ? explicitSite
        : (derivedSite || 'profile');
      rows.push({
        site: siteLabel,
        profile_url: url,
        screenshot_url: String(row?.screenshot_url || '').trim(),
        source: 'pdl',
      });
    };
    for (const row of (Array.isArray(pdlProfiles) ? pdlProfiles : [])) addRow(row);
    for (const url of fallbackProfileUrls) addRow({ profile_url: url, site: siteFromUrl(url) });
    return rows;
  })();
  return `
    <div class="recon-group">
      <p>Person Data Profile${totalProfiles > 1 ? ` (${totalProfiles} matches)` : ''}</p>
      <div class="pdl-poi-profile">
        <div class="pdl-poi-grid">
          <div class="pdl-poi-field">
            <span class="pdl-poi-label">Name</span>
            <strong>${escapeHtml(fullName || 'Unnamed')}</strong>
          </div>
          <div class="pdl-poi-field">
            <span class="pdl-poi-label">Location</span>
            <strong>${escapeHtml(location || 'Unknown')}</strong>
          </div>
          <div class="pdl-poi-field">
            <span class="pdl-poi-label">Job Title</span>
            <strong>${escapeHtml(title || 'Unknown')}</strong>
            ${company ? `<span class="pdl-poi-meta">${escapeHtml(company)}</span>` : ''}
          </div>
        </div>
        <div class="pdl-profiles-block">
          <span class="pdl-contact-heading">Profiles</span>
          <div class="recon-pills">
            ${mergedProfileRows.length
    ? mergedProfileRows.map((row) => toReconBadge(row)).join('')
    : '<span class="recon-pill">No profile URLs returned by People Data Labs.</span>'}
          </div>
        </div>
        <div class="pdl-contact-sections">
          ${contactGroupMarkup('Professional', professionalValues)}
          ${contactGroupMarkup('Personal', personalValues)}
        </div>
        <div class="recon-pills">
          <span class="recon-pill">${escapeHtml(identificationText)}</span>
        </div>
      </div>
    </div>
  `;
}

function osintProfilesMarkup(profiles, rows = []) {
  const items = Array.isArray(profiles) ? profiles : [];
  if (!items.length) return '';
  const screenshotByUrl = new Map();
  for (const row of (Array.isArray(rows) ? rows : [])) {
    if (String(row?.source || '').trim().toLowerCase() !== 'osint_industries') continue;
    const url = String(row?.profile_url || '').trim();
    const shot = String(row?.screenshot_url || '').trim();
    if (!url || !shot || screenshotByUrl.has(url.toLowerCase())) continue;
    screenshotByUrl.set(url.toLowerCase(), shot);
  }
  const linkPill = (label, rawUrl, screenshotLabel) => {
    const url = String(rawUrl || '').trim();
    if (!url) return '';
    const screenshotUrl = screenshotByUrl.get(url.toLowerCase()) || '';
    const previewAttr = screenshotUrl ? ` data-preview-image="${escapeAttr(screenshotUrl)}"` : '';
    const previewLabelAttr = screenshotUrl ? ` data-preview-label="${escapeAttr(screenshotLabel)}"` : '';
    return `<a class="recon-pill lead-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer"${previewAttr}${previewLabelAttr}>${escapeHtml(label)}</a>`;
  };
  const valueItem = (label, value) => {
    const clean = String(value || '').trim();
    if (!clean) return '';
    return `<div class="osint-value"><span class="osint-key">${escapeHtml(label)}</span><strong>${escapeHtml(clean)}</strong></div>`;
  };
  const cards = items.map((profile, index) => {
    const title = String(profile?.title || profile?.name || profile?.username || `Result ${index + 1}`).trim();
    const profileUrl = String(profile?.profile_url || '').trim();
    const website = String(profile?.website || '').trim();
    const profileLink = linkPill('Profile URL', profileUrl, title);
    const websiteLink = website && website !== profileUrl ? linkPill('Website', website, title) : '';
    const imageUrl = String(profile?.picture_url || '').trim();
    return `
      <article class="osint-profile-card">
        <div class="osint-profile-head">
          ${imageUrl ? `<img class="osint-profile-avatar" src="${escapeHtml(imageUrl)}" alt="${escapeAttr(title)}" loading="lazy" referrerpolicy="no-referrer" />` : '<div class="osint-profile-avatar empty">No image</div>'}
          <div>
            <h4>${escapeHtml(title)}</h4>
            <p>${escapeHtml(String(profile?.name || '').trim() || 'Unnamed')}</p>
          </div>
        </div>
        <div class="osint-profile-grid">
          ${valueItem('first_name', profile?.first_name)}
          ${valueItem('last_name', profile?.last_name)}
          ${valueItem('gender', profile?.gender)}
          ${valueItem('age', profile?.age)}
          ${valueItem('location', profile?.location)}
          ${valueItem('username', profile?.username)}
          ${valueItem('email', profile?.email)}
          ${valueItem('phone', profile?.phone)}
          ${valueItem('email_hint', profile?.email_hint)}
          ${valueItem('phone_hint', profile?.phone_hint)}
          ${valueItem('bio', profile?.bio)}
        </div>
        <div class="recon-pills">
          ${profileLink}
          ${websiteLink}
        </div>
      </article>
    `;
  }).join('');
  return `
    <div class="recon-group">
      <p>OSINT Industries Results (${items.length})</p>
      <div class="osint-profiles-list">${cards}</div>
    </div>
  `;
}

function numverifyProfilesMarkup(profiles) {
  const items = Array.isArray(profiles) ? profiles : [];
  if (!items.length) return '';
  const valueItem = (label, value) => {
    const clean = String(value || '').trim();
    if (!clean) return '';
    return `<div class="osint-value"><span class="osint-key">${escapeHtml(label)}</span><strong>${escapeHtml(clean)}</strong></div>`;
  };
  const cards = items.map((profile, index) => {
    const title = String(profile?.title || profile?.number || `Phone Result ${index + 1}`).trim();
    return `
      <article class="osint-profile-card">
        <div class="osint-profile-head">
          <div class="osint-profile-avatar empty">Phone</div>
          <div>
            <h4>${escapeHtml(title)}</h4>
            <p>${profile?.valid ? 'Valid number' : 'Invalid or not recognized'}</p>
          </div>
        </div>
        <div class="osint-profile-grid">
          ${valueItem('number', profile?.number)}
          ${valueItem('international_format', profile?.international_format)}
          ${valueItem('local_format', profile?.local_format)}
          ${valueItem('e164', profile?.e164)}
          ${valueItem('country_name', profile?.country_name)}
          ${valueItem('country_code', profile?.country_code)}
          ${valueItem('country_prefix', profile?.country_prefix)}
          ${valueItem('location', profile?.location)}
          ${valueItem('carrier', profile?.carrier)}
          ${valueItem('line_type', profile?.line_type)}
        </div>
      </article>
    `;
  }).join('');
  return `
    <div class="recon-group">
      <p>Numverify Phone Results (${items.length})</p>
      <div class="osint-profiles-list">${cards}</div>
    </div>
  `;
}

function renderReconResults(payload, targetEl = reconResults) {
  if (!(targetEl instanceof HTMLElement)) return;
  const results = Array.isArray(payload?.results) ? payload.results : [];
  const osintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
  const numverifyProfiles = Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [];
  const personDataProfile = payload?.person_data_profile && typeof payload.person_data_profile === 'object'
    ? payload.person_data_profile
    : {};
  const personDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
  const pdlProfiles = results.filter(
    (row) => row.status === 'present'
      && String(row.source || '').trim().toLowerCase() === 'pdl'
      && String(row.profile_url || '').trim(),
  );
  const supportedPresent = Array.isArray(payload?.collection_ready_profiles)
    ? payload.collection_ready_profiles
    : results.filter((row) => row.status === 'present' && row.supported_for_collection && String(row.profile_url || '').trim());
  const leadPresent = Array.isArray(payload?.unsupported_profiles_with_url)
    ? payload.unsupported_profiles_with_url
    : results.filter((row) => row.status === 'present' && !row.supported_for_collection && String(row.profile_url || '').trim());
  const nonPdlSupportedPresent = supportedPresent.filter((row) => String(row.source || '').trim().toLowerCase() !== 'pdl');
  const nonPdlLeadPresent = leadPresent.filter((row) => String(row.source || '').trim().toLowerCase() !== 'pdl');
  const knownPresentNoUrl = Array.isArray(payload?.known_present_without_url)
    ? payload.known_present_without_url
    : results.filter((row) => row.status === 'present' && !String(row.profile_url || '').trim());
  const unknown = results.filter((row) => row.status === 'unknown');

  targetEl.classList.remove('hidden');
  targetEl.innerHTML = `
    <div class="recon-summary">
      Checked ${results.length} records • ${nonPdlSupportedPresent.length} collection-ready with URL • ${nonPdlLeadPresent.length} unsupported with URL • ${knownPresentNoUrl.length} known without URL • ${unknown.length} unknown
    </div>
    <div class="recon-group">
      <p>Collection-ready with account URL</p>
      <div class="recon-pills">
        ${nonPdlSupportedPresent.length
    ? nonPdlSupportedPresent.map((row) => toReconBadge(row, 'success')).join('')
    : '<span class="recon-pill">No supported profiles with direct URLs</span>'}
      </div>
    </div>
    <div class="recon-group">
      <p>Unsupported with account URL</p>
      <div class="recon-pills">
        ${nonPdlLeadPresent.length ? nonPdlLeadPresent.map((row) => toReconBadge(row)).join('') : '<span class="recon-pill">No unsupported account URLs detected</span>'}
      </div>
    </div>
    <div class="recon-group">
      <p>Known present without direct account URL</p>
      <div class="recon-pills">
        ${knownPresentNoUrl.length ? knownPresentNoUrl.map((row) => toReconBadge(row, 'warn')).join('') : '<span class="recon-pill">No known-present no-URL results</span>'}
      </div>
    </div>
    ${osintProfilesMarkup(osintProfiles, results)}
    ${numverifyProfilesMarkup(numverifyProfiles)}
    ${personDataProfileMarkup(personDataProfile, personDataProfiles.length, pdlProfiles)}
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
      const screenshotUrl = String(lead.screenshot_url || '').trim();
      const source = String(lead.source || '').trim().toLowerCase();
      const leadType = String(lead.lead_type || '').trim().toLowerCase();
      const attribute = String(lead.attribute || '').trim();
      const value = String(lead.value || '').trim();
      if (!url && source === 'pdl' && leadType === 'attribute' && value) {
        return `<div class="signal-row signal-row-simple pdl"><span class="row-label"><span class="row-label-text">${escapeHtml(value)}</span><span class="source-tag pdl-tag">PDL</span></span></div>`;
      }
      const profileName = String(lead.profile_name || '').trim();
      const icon = faviconMarkup(label, url);
      const content = `<span class="row-label">${icon}<span class="row-label-text">${escapeHtml(label)}</span>${source === 'pdl' ? '<span class="source-tag pdl-tag">PDL</span>' : ''}</span>`;
      const detail = leadType === 'attribute'
        ? `<span>${escapeHtml(`${attribute}${profileName ? ` (${profileName})` : ''}: ${value}`)}</span>`
        : '';
      if (url) {
        const previewAttr = screenshotUrl ? ` data-preview-image="${escapeAttr(screenshotUrl)}"` : '';
        const previewLabelAttr = screenshotUrl ? ` data-preview-label="${escapeAttr(label)}"` : '';
        return `<a class="signal-row lead-link${source === 'pdl' ? ' pdl' : ''}" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer"${previewAttr}${previewLabelAttr}>${content}<strong>open</strong></a>`;
      }
      if (detail) {
        return `<div class="signal-row${source === 'pdl' ? ' pdl' : ''}">${content}<strong>intel</strong></div><div class="signal-row signal-row-detail${source === 'pdl' ? ' pdl' : ''}">${detail}</div>`;
      }
      return `<div class="signal-row${source === 'pdl' ? ' pdl' : ''}">${content}<strong>lead</strong></div>`;
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
  if (normalized === 'facebook') return 'Facebook';
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

function notifyReconApiModules(payload) {
  const queried = Array.isArray(payload?.api_modules_queried) ? payload.api_modules_queried : [];
  const notified = new Set();
  for (const item of queried) {
    const moduleKey = String(item?.module || '').trim().toLowerCase();
    if (!moduleKey || notified.has(moduleKey)) continue;
    notified.add(moduleKey);
    const label = String(item?.label || moduleKey.replace(/_/g, ' ')).trim();
    showNotification(`${label} queried successfully.`, 'success');
  }
  if (notified.size) return;

  const hasPdl = Array.isArray(payload?.person_data_profiles) && payload.person_data_profiles.length > 0;
  const hasOsint = Array.isArray(payload?.osint_profiles) && payload.osint_profiles.length > 0;
  const hasNumverify = Array.isArray(payload?.numverify_profiles) && payload.numverify_profiles.length > 0;
  if (hasPdl) showNotification('People Data Labs queried successfully.', 'success');
  if (hasOsint) showNotification('OSINT Industries queried successfully.', 'success');
  if (hasNumverify) showNotification('Numverify queried successfully.', 'success');
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
  for (const el of [filterSelectors, filterIdeologicalIndicators, filterThreatSignals, filterLLMPrimary, filterLLMSecondary]) {
    if (el?.checked) activeCount += 1;
  }
  activeCount += activeEntityFilters.size;
  activeCount += activeMixFilters.size;
  activeCount += activeSignalFilters.size;
  activeCount += activeCustomKeywordFilters.size;
  activeCount += activeFaceFilters.size;
  filterToggleBtn.textContent = activeCount > 0 ? `Filters (${activeCount})` : 'Filters';
}

function setInsightsTab(tabName) {
  const next = String(tabName || '').trim().toLowerCase();
  if (!next) return;
  const previousTab = activeInsightsTab;
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
  if (previousTab === 'signals' && next !== 'signals') {
    for (const el of [filterSelectors, filterIdeologicalIndicators, filterThreatSignals, filterLLMPrimary, filterLLMSecondary]) {
      if (!el) continue;
      el.checked = false;
    }
    activeSignalFilters.clear();
    updateFilterToggleLabel();
    queueRefresh();
    return;
  }
  if (latestPosts.length) {
    renderPosts(latestPosts);
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
  lockModalUntilCollectionData = false;
  collectionLoadedAnyData = false;
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
  latestFaceClusters = [];
  activeFaceFilters.clear();
  latestFaceRecognition = { available: false, reason: 'not_run' };
  renderFaceRecognitionFilters();
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
      await loadCases();
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

function llmAssessmentCandidatePosts(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  const output = [];
  for (const post of rows) {
    if (!post || typeof post !== 'object') continue;
    const rowId = Number(post.row_id);
    if (!Number.isFinite(rowId)) continue;
    const content = String(post.content || '').trim();
    if (!content) continue;
    const metadata = post.metadata && typeof post.metadata === 'object' ? post.metadata : {};
    const existing = metadata.llm_assessment && typeof metadata.llm_assessment === 'object'
      ? metadata.llm_assessment
      : {};
    if (Object.keys(existing).length) continue;
    output.push({
      row_id: rowId,
      post_id: String(post.post_id || '').trim(),
      platform: String(post.platform || '').trim(),
      username: String(post.username || '').trim(),
      content,
      metadata,
    });
  }
  return output;
}

async function runAiThreatAssessment() {
  if (!(runAiThreatAssessmentBtn instanceof HTMLButtonElement)) return;
  const candidates = llmAssessmentCandidatePosts(latestPosts);
  if (!candidates.length) {
    if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = 'No eligible posts found. Posts may already be assessed.';
    return;
  }

  runAiThreatAssessmentBtn.disabled = true;
  if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = 'Estimating OpenAI assessment cost...';

  try {
    const rawExpected = window.prompt(
      'Expected output tokens per post (approximate).',
      '220',
    );
    if (rawExpected === null) {
      if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = 'AI threat assessment canceled.';
      return;
    }
    const expectedOutputTokens = Math.max(1, Number.parseInt(String(rawExpected).trim() || '220', 10) || 220);
    const estimateResponse = await fetch('/api/llm/estimate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        posts: candidates,
        expected_output_tokens_per_post: expectedOutputTokens,
      }),
    });
    if (!estimateResponse.ok) {
      const message = await parseErrorResponse(estimateResponse);
      throw new Error(message);
    }
    const estimatePayload = await estimateResponse.json();
    const estimate = estimatePayload?.estimate || {};
    const candidateCount = Number(estimate?.candidate_posts || 0);
    const totalCost = Number(estimate?.estimated_total_cost_usd || 0);
    const inputTokens = Number(estimate?.estimated_input_tokens || 0);
    const outputTokens = Number(estimate?.estimated_output_tokens || 0);
    const model = String(estimate?.model || 'gpt-4.1-mini');
    const confirmationMessage = [
      `Run AI Threat Assessment on ${candidateCount} post(s)?`,
      `Model: ${model}`,
      `Estimated tokens: input ${inputTokens}, output ${outputTokens}`,
      `Estimated cost: $${totalCost.toFixed(4)} USD`,
      '',
      'Proceed?',
    ].join('\n');
    const shouldRun = window.confirm(confirmationMessage);
    if (!shouldRun) {
      if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = 'AI threat assessment canceled.';
      return;
    }

    if (aiThreatAssessmentStatus) aiThreatAssessmentStatus.textContent = 'Running AI threat assessment...';
    const runResponse = await fetch('/api/llm/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_id: String(activeCaseId || '').trim(),
        posts: candidates,
      }),
    });
    if (!runResponse.ok) {
      const message = await parseErrorResponse(runResponse);
      throw new Error(message);
    }
    const runPayload = await runResponse.json();
    const assessed = Number(runPayload?.assessed || 0);
    const persisted = Number(runPayload?.persisted || 0);
    if (aiThreatAssessmentStatus) {
      aiThreatAssessmentStatus.textContent = `AI threat assessment complete. Assessed ${assessed} post(s), persisted ${persisted}.`;
    }
    await refreshPosts();
  } catch (error) {
    console.error(error);
    if (aiThreatAssessmentStatus) {
      aiThreatAssessmentStatus.textContent = `AI threat assessment failed: ${error.message || 'unknown error'}`;
    }
  } finally {
    runAiThreatAssessmentBtn.disabled = false;
  }
}

function isValidReconEmail(value) {
  return /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(String(value || '').trim());
}

function isValidReconPhone(value) {
  const compact = String(value || '').replace(/[^\d+]/g, '');
  if (!compact.startsWith('+')) return false;
  if ((compact.match(/\+/g) || []).length > 1) return false;
  const digits = compact.replace(/\D/g, '');
  return digits.length >= 7 && digits.length <= 15;
}

const RECON_SELECTOR_TYPES = ['username', 'email', 'phone', 'name', 'wallet'];

function reconExampleText(selectorType) {
  const normalizedType = RECON_SELECTOR_TYPES.includes(String(selectorType || '').trim().toLowerCase())
    ? String(selectorType || '').trim().toLowerCase()
    : 'username';
  const exampleByType = {
    username: 'Example: @johnsmith',
    email: 'Example: jane@example.com',
    phone: 'Example: +12025550199',
    name: 'Example: Jane Doe',
    wallet: 'Example: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
  };
  return exampleByType[normalizedType] || exampleByType.username;
}

function selectorOptionsMarkup(selectedType = 'username') {
  const normalizedType = RECON_SELECTOR_TYPES.includes(String(selectedType || '').trim().toLowerCase())
    ? String(selectedType || '').trim().toLowerCase()
    : 'username';
  return RECON_SELECTOR_TYPES
    .map((type) => `<option value="${type}"${type === normalizedType ? ' selected' : ''}>${type.charAt(0).toUpperCase()}${type.slice(1)}</option>`)
    .join('');
}

function addReconSelectorRow(container, type = 'username', value = '') {
  if (!(container instanceof HTMLElement)) return;
  const row = document.createElement('div');
  row.className = 'recon-selector-row';
  row.innerHTML = `
    <select class="recon-selector-type" aria-label="Selector type">
      ${selectorOptionsMarkup(type)}
    </select>
    <input class="recon-selector-value" type="text" aria-label="Selector value" autocomplete="off" value="${escapeAttr(String(value || '').trim())}" />
    <button class="target-remove recon-selector-remove" type="button" aria-label="Remove selector">×</button>
    <div class="recon-selector-example">${escapeHtml(reconExampleText(type))}</div>
  `;
  container.appendChild(row);
}

function ensureAtLeastOneReconSelectorRow(container = reconSelectorsList) {
  if (!(container instanceof HTMLElement)) return;
  if (container.querySelector('.recon-selector-row')) return;
  addReconSelectorRow(container, 'username', '');
}

function parseReconSelectorsFromRows(container = reconSelectorsList) {
  const rows = Array.from(container?.querySelectorAll('.recon-selector-row') || []);
  const selectors = [];
  const seen = new Set();
  for (const row of rows) {
    const typeEl = row.querySelector('.recon-selector-type');
    const valueEl = row.querySelector('.recon-selector-value');
    const rawType = typeEl instanceof HTMLSelectElement ? String(typeEl.value || '').trim().toLowerCase() : 'username';
    const normalizedType = RECON_SELECTOR_TYPES.includes(rawType) ? rawType : 'username';
    const rawValue = valueEl instanceof HTMLInputElement ? String(valueEl.value || '') : '';
    let value = rawValue.trim();
    if (normalizedType === 'username') value = value.replace(/^@+/, '');
    if (normalizedType === 'email') value = value.toLowerCase();
    if (normalizedType === 'phone') value = value.replace(/[\s().-]+/g, '');
    if (!value) continue;
    if (normalizedType === 'email' && !isValidReconEmail(value)) continue;
    if (normalizedType === 'phone' && !isValidReconPhone(value)) continue;
    const key = `${normalizedType}|${value.toLowerCase()}`;
    if (seen.has(key)) continue;
    seen.add(key);
    selectors.push({ type: normalizedType, value });
  }
  return selectors;
}

async function runRecon(event) {
  event.preventDefault();
  hideReconPreview();
  const selectors = parseReconSelectorsFromRows();
  if (!selectors.length) {
    reconStatus.textContent = 'Enter at least one valid selector value.';
    return;
  }

  setReconBusy(true);
  reconStatus.textContent = `Running reconnaissance for ${selectors.length} selector(s)...`;
  reconResults.classList.add('hidden');
  useReconTargetsBtn.classList.add('hidden');
  useReconTargetsBtn.disabled = true;
  goReconAssessmentBtn?.classList.add('hidden');
  if (goReconAssessmentBtn instanceof HTMLButtonElement) goReconAssessmentBtn.disabled = true;
  reconTargets = [];
  reconProfiles = [];
  reconPersonDataProfile = {};
  reconPersonDataProfiles = [];
  reconOsintProfiles = [];
  reconNumverifyProfiles = [];

  try {
    const response = await fetch('/api/recon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selectors }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const payload = await response.json();
    reconTargets = Array.isArray(payload.collection_targets) ? payload.collection_targets : [];
    reconLeads = Array.isArray(payload.leads) ? payload.leads : [];
    reconProfiles = (Array.isArray(payload.results) ? payload.results : []).filter((row) => String(row?.status || '').trim() === 'present');
    reconPersonDataProfile = payload?.person_data_profile && typeof payload.person_data_profile === 'object'
      ? payload.person_data_profile
      : {};
    reconPersonDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
    reconOsintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
    reconNumverifyProfiles = Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [];
    notifyReconApiModules(payload);
    renderReconResults(payload);
    renderReconResults(payload, footprintReconResults);
    renderLeadsList();
    renderLocationMap(latestPosts);
    renderPatternOfLife(latestPosts);
    if (reconTargets.length > 0) {
      useReconTargetsBtn.classList.remove('hidden');
      useReconTargetsBtn.disabled = false;
    } else {
      useReconTargetsBtn.classList.add('hidden');
      useReconTargetsBtn.disabled = true;
    }
    if (reconTargets.length > 0) {
      footprintUseTargetsBtn?.classList.remove('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = false;
    } else {
      footprintUseTargetsBtn?.classList.add('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    }
    goReconAssessmentBtn?.classList.remove('hidden');
    if (goReconAssessmentBtn instanceof HTMLButtonElement) goReconAssessmentBtn.disabled = false;
    reconStatus.textContent = `Recon complete: ${payload.present_count || 0} account match(es) found across ${payload.checked || 0} checks.`;
    if (footprintReconStatus) {
      footprintReconStatus.textContent = `Recon complete: ${payload.present_count || 0} account match(es) found across ${payload.checked || 0} checks.`;
    }
  } catch (error) {
    console.error(error);
    useReconTargetsBtn.classList.add('hidden');
    useReconTargetsBtn.disabled = true;
    goReconAssessmentBtn?.classList.add('hidden');
    if (goReconAssessmentBtn instanceof HTMLButtonElement) goReconAssessmentBtn.disabled = true;
    footprintUseTargetsBtn?.classList.add('hidden');
    if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    reconPersonDataProfiles = [];
    reconPersonDataProfile = {};
    reconOsintProfiles = [];
    reconNumverifyProfiles = [];
    reconStatus.textContent = `Recon failed: ${error.message || 'unknown error'}`;
    if (footprintReconStatus) footprintReconStatus.textContent = `Recon failed: ${error.message || 'unknown error'}`;
  } finally {
    setReconBusy(false);
  }
}

function openAssessmentFromRecon() {
  if (!activeCaseId) {
    showNotification('Open a case first.', 'warn');
    return;
  }
  setModalOpen(false);
  showDashboard();
  setResultsView('posts');
  setInsightsTab('signals');
  if (!Array.isArray(latestPosts) || !latestPosts.length) {
    queueRefresh();
  }
  showNotification('Opened assessment view without running collection.', 'info');
}

async function runFootprintRecon(event) {
  event.preventDefault();
  hideReconPreview();
  const selectors = parseReconSelectorsFromRows(footprintSelectorsList);
  if (!selectors.length) {
    if (footprintReconStatus) footprintReconStatus.textContent = 'Enter at least one valid selector value.';
    return;
  }

  setFootprintBusy(true);
  if (footprintReconStatus) footprintReconStatus.textContent = `Running reconnaissance for ${selectors.length} selector(s)...`;
  footprintReconResults?.classList.add('hidden');
  footprintUseTargetsBtn?.classList.add('hidden');
  if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
  reconTargets = [];
  reconProfiles = [];
  reconPersonDataProfile = {};
  reconPersonDataProfiles = [];
  reconOsintProfiles = [];
  reconNumverifyProfiles = [];

  try {
    const response = await fetch('/api/recon', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selectors }),
    });
    if (!response.ok) {
      const message = await parseErrorResponse(response);
      throw new Error(message);
    }
    const payload = await response.json();
    reconTargets = Array.isArray(payload.collection_targets) ? payload.collection_targets : [];
    reconLeads = Array.isArray(payload.leads) ? payload.leads : [];
    reconProfiles = (Array.isArray(payload.results) ? payload.results : []).filter((row) => String(row?.status || '').trim() === 'present');
    reconPersonDataProfile = payload?.person_data_profile && typeof payload.person_data_profile === 'object'
      ? payload.person_data_profile
      : {};
    reconPersonDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
    reconOsintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
    reconNumverifyProfiles = Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [];
    notifyReconApiModules(payload);
    renderReconResults(payload, footprintReconResults);
    renderReconResults(payload);
    renderLeadsList();
    renderPatternOfLife(latestPosts);
    if (reconTargets.length > 0) {
      footprintUseTargetsBtn?.classList.remove('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = false;
    } else {
      footprintUseTargetsBtn?.classList.add('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    }
    if (footprintReconStatus) {
      footprintReconStatus.textContent = `Recon complete: ${payload.present_count || 0} account match(es) found across ${payload.checked || 0} checks.`;
    }
  } catch (error) {
    console.error(error);
    footprintUseTargetsBtn?.classList.add('hidden');
    if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    reconPersonDataProfiles = [];
    reconPersonDataProfile = {};
    reconOsintProfiles = [];
    reconNumverifyProfiles = [];
    if (footprintReconStatus) footprintReconStatus.textContent = `Recon failed: ${error.message || 'unknown error'}`;
  } finally {
    setFootprintBusy(false);
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
  if (!activeCaseId) {
    setupStatus.textContent = 'Select or create a case before collection.';
    collectionProgressStatus = 'collection failed: no active case';
    updateStatusLine();
    return false;
  }

  try {
    const response = await fetch('/api/collect/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        targets,
        case_id: activeCaseId,
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
    if (activeCase) {
      dashboardBaseStatus = `Active case: ${activeCase.case_name}`;
    }
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
resultsEl?.addEventListener('click', async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;

  const runInlineFaceBtn = target.closest('[data-face-run-inline]');
  if (runInlineFaceBtn instanceof HTMLElement) {
    const original = runInlineFaceBtn.textContent || 'Run Facial Recognition';
    runInlineFaceBtn.setAttribute('aria-busy', 'true');
    runInlineFaceBtn.textContent = 'Running...';
    try {
      await refreshPosts({ forceFaceRefresh: true });
    } finally {
      runInlineFaceBtn.removeAttribute('aria-busy');
      runInlineFaceBtn.textContent = original;
    }
    return;
  }

  const inlineFaceFilter = target.closest('[data-face-filter-inline]');
  if (inlineFaceFilter instanceof HTMLElement) {
    const personId = String(inlineFaceFilter.getAttribute('data-face-filter-inline') || '').trim().toLowerCase();
    if (!personId) return;
    if (activeFaceFilters.has(personId)) {
      activeFaceFilters.delete(personId);
    } else {
      activeFaceFilters.add(personId);
    }
    renderFaceRecognitionFilters();
    renderPosts(latestPosts);
    return;
  }

  const assessmentNode = target.closest('.llm-assessment[data-post-index]');
  const assessmentPostIndex = assessmentNode instanceof HTMLElement
    ? Number(assessmentNode.getAttribute('data-post-index'))
    : NaN;
  if (target.closest('[data-assessment-toggle]')) {
    if (!Number.isFinite(assessmentPostIndex) || assessmentPostIndex < 0) return;
    activeThreatAssessmentEditorPostIndex = activeThreatAssessmentEditorPostIndex === assessmentPostIndex ? null : assessmentPostIndex;
    renderPosts(latestPosts);
    return;
  }
  if (target.closest('[data-assessment-tag-add]')) {
    if (!(assessmentNode instanceof HTMLElement) || !Number.isFinite(assessmentPostIndex) || assessmentPostIndex < 0) return;
    const post = latestRenderedPosts[assessmentPostIndex];
    if (!post || typeof post !== 'object') return;
    const tagInput = assessmentNode.querySelector('[data-assessment-tag-input]');
    const kindInput = assessmentNode.querySelector('[data-assessment-tag-kind]');
    const raw = tagInput instanceof HTMLInputElement ? String(tagInput.value || '') : '';
    const kind = kindInput instanceof HTMLSelectElement && String(kindInput.value || '').toLowerCase() === 'secondary'
      ? 'secondary'
      : 'primary';
    const additions = raw
      .split(',')
      .map((item) => String(item || '').trim().replace(/\s+/g, ' '))
      .filter(Boolean);
    if (!additions.length) return;
    const next = normalizeEditableLlmAssessment(llmAssessmentFromPost(post));
    const base = kind === 'secondary' ? next.tagged_secondary : next.tagged_primary;
    base.push(...additions);
    const success = await persistThreatAssessmentUpdate(assessmentPostIndex, next);
    if (success) activeThreatAssessmentEditorPostIndex = assessmentPostIndex;
    return;
  }
  if (target.closest('[data-assessment-remove-tag]')) {
    if (!(assessmentNode instanceof HTMLElement) || !Number.isFinite(assessmentPostIndex) || assessmentPostIndex < 0) return;
    const removeBtn = target.closest('[data-assessment-remove-tag]');
    if (!(removeBtn instanceof HTMLElement)) return;
    const post = latestRenderedPosts[assessmentPostIndex];
    if (!post || typeof post !== 'object') return;
    const tagKind = String(removeBtn.getAttribute('data-assessment-tag-kind') || '').trim().toLowerCase();
    const tagLabel = String(removeBtn.getAttribute('data-assessment-tag-label') || '').trim().toLowerCase();
    if (!tagLabel || (tagKind !== 'primary' && tagKind !== 'secondary')) return;
    const next = normalizeEditableLlmAssessment(llmAssessmentFromPost(post));
    if (tagKind === 'primary') {
      next.tagged_primary = next.tagged_primary.filter((item) => String(item || '').trim().toLowerCase() !== tagLabel);
    } else {
      next.tagged_secondary = next.tagged_secondary.filter((item) => String(item || '').trim().toLowerCase() !== tagLabel);
    }
    const success = await persistThreatAssessmentUpdate(assessmentPostIndex, next);
    if (success) activeThreatAssessmentEditorPostIndex = assessmentPostIndex;
    return;
  }
  if (target.closest('[data-assessment-theme-save]')) {
    if (!(assessmentNode instanceof HTMLElement) || !Number.isFinite(assessmentPostIndex) || assessmentPostIndex < 0) return;
    const post = latestRenderedPosts[assessmentPostIndex];
    if (!post || typeof post !== 'object') return;
    const themeInput = assessmentNode.querySelector('[data-assessment-theme-input]');
    const nextTheme = themeInput instanceof HTMLInputElement ? String(themeInput.value || '').trim() : '';
    const next = normalizeEditableLlmAssessment(llmAssessmentFromPost(post));
    next.underlying_theme = nextTheme;
    const success = await persistThreatAssessmentUpdate(assessmentPostIndex, next);
    if (success) activeThreatAssessmentEditorPostIndex = assessmentPostIndex;
    return;
  }
  if (target.closest('[data-assessment-theme-remove]')) {
    if (!Number.isFinite(assessmentPostIndex) || assessmentPostIndex < 0) return;
    const post = latestRenderedPosts[assessmentPostIndex];
    if (!post || typeof post !== 'object') return;
    const next = normalizeEditableLlmAssessment(llmAssessmentFromPost(post));
    next.underlying_theme = '';
    const success = await persistThreatAssessmentUpdate(assessmentPostIndex, next);
    if (success) activeThreatAssessmentEditorPostIndex = assessmentPostIndex;
    return;
  }

  const toggle = target.closest('.content-more-toggle');
  if (toggle instanceof HTMLElement) {
    const contentContainer = toggle.closest('.content');
    const truncated = contentContainer?.querySelector('.content-truncated');
    if (!(truncated instanceof HTMLElement)) return;
    const expanded = String(truncated.getAttribute('data-expanded') || 'false') === 'true';
    const head = String(truncated.getAttribute('data-content-head') || '');
    const rest = String(truncated.getAttribute('data-content-rest') || '');
    if (expanded) {
      truncated.innerHTML = `${escapeHtml(head)}<span class="content-ellipsis">...</span>`;
      truncated.setAttribute('data-expanded', 'false');
      toggle.textContent = 'Show more+';
      toggle.setAttribute('aria-expanded', 'false');
      return;
    }
    truncated.innerHTML = `${escapeHtml(head)}${escapeHtml(rest)}`;
    truncated.setAttribute('data-expanded', 'true');
    toggle.textContent = 'Show less-';
    toggle.setAttribute('aria-expanded', 'true');
    return;
  }

  const mediaTile = target.closest('.media-grid-tile');
  if (mediaTile instanceof HTMLElement) {
    const postIndex = Number(mediaTile.getAttribute('data-post-index'));
    if (Number.isFinite(postIndex) && postIndex >= 0) openPostModal(postIndex);
    return;
  }

  const patternLifePostBtn = target.closest('[data-pattern-life-post-index]');
  if (patternLifePostBtn instanceof HTMLElement) {
    const postIndex = Number(patternLifePostBtn.getAttribute('data-pattern-life-post-index'));
    if (Number.isFinite(postIndex) && postIndex >= 0) {
      scrollToPost(postIndex);
      openPostModal(postIndex);
    }
    return;
  }

  if (target.closest('a, video, iframe, button, input, select, textarea, label')) return;
  const postNode = target.closest('[data-post-index]');
  if (!(postNode instanceof HTMLElement)) return;
  const postIndex = Number(postNode.getAttribute('data-post-index'));
  if (!Number.isFinite(postIndex) || postIndex < 0) return;
  openPostModal(postIndex);
});
resultsEl?.addEventListener('input', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) return;
  if (!target.hasAttribute('data-face-confidence-inline')) return;
  const next = Number(target.value);
  activeFaceMinConfidence = Number.isFinite(next) ? Math.max(0, Math.min(1, next)) : 0;
  renderFaceRecognitionFilters();
  renderPosts(latestPosts);
});
caseSearchInput?.addEventListener('input', renderCases);
caseStatusFilter?.addEventListener('change', renderCases);
caseThreatFilter?.addEventListener('change', renderCases);
caseSortSelect?.addEventListener('change', renderCases);
openNewCaseBtn?.addEventListener('click', createNewCaseAndLaunch);
generateDemoCaseBtn?.addEventListener('click', generateDemoCase);
caseTiles?.addEventListener('click', (event) => {
  const path = typeof event.composedPath === 'function' ? event.composedPath() : [];
  const elementPath = path.filter((node) => node instanceof Element);
  const firstWithAttr = (attrName) => elementPath.find((node) => node.hasAttribute(attrName));
  const deleteNode = firstWithAttr('data-case-delete');
  if (deleteNode instanceof Element) {
    deleteCaseAndContents(deleteNode.getAttribute('data-case-delete'));
    return;
  }
  const editNode = firstWithAttr('data-case-edit');
  if (editNode instanceof Element) {
    openCaseEditModal(editNode.getAttribute('data-case-edit'));
    return;
  }
  const openNode = firstWithAttr('data-case-open');
  if (openNode instanceof Element) {
    openCase(openNode.getAttribute('data-case-open'));
    return;
  }
  const tileNode = firstWithAttr('data-case-id');
  if (tileNode instanceof Element) {
    openCase(tileNode.getAttribute('data-case-id'));
  }
});
caseEditForm?.addEventListener('submit', submitCaseEdit);
caseEditCancelBtn?.addEventListener('click', closeCaseEditModal);
caseEditCloseBtn?.addEventListener('click', closeCaseEditModal);
caseEditStatusSelect?.addEventListener('change', () => {
  setWatchlistCadenceVisibility(
    caseEditStatusSelect,
    caseEditCadenceField,
    caseEditCadenceSelect,
    watchlistCadenceForCase(editingCaseId),
  );
});
clearSearchBtn?.addEventListener('click', () => {
  if (!searchInput.value) return;
  searchInput.value = '';
  queueRefresh();
  searchInput.focus();
});
viewPostsBtn?.addEventListener('click', () => setResultsView('posts'));
viewMediaBtn?.addEventListener('click', () => setResultsView('media'));
viewFootprintBtn?.addEventListener('click', () => setResultsView('footprint'));
viewPatternLifeBtn?.addEventListener('click', () => setResultsView('pattern'));
sortSelect.addEventListener('change', queueRefresh);
setupForm.addEventListener('submit', collectAndOpen);
reconForm.addEventListener('submit', runRecon);
footprintReconForm?.addEventListener('submit', runFootprintRecon);
runAiThreatAssessmentBtn?.addEventListener('click', runAiThreatAssessment);
attachReconPreviewHandlers(reconResults);
attachReconPreviewHandlers(footprintReconResults);
attachReconPreviewHandlers(leadsList);
for (const el of [filterTwitter, filterReddit, filterTiktok, filterBluesky, filterInstagram, filterYoutube, filterPost, filterRepost, filterReply, filterQuote, filterComment, filterSelectors, filterIdeologicalIndicators, filterThreatSignals, filterLLMPrimary, filterLLMSecondary]) {
  if (!el) continue;
  el.addEventListener('change', () => {
    updateFilterToggleLabel();
    queueRefresh();
  });
}
faceRecognitionFilterList?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const button = target.closest('[data-face-filter]');
  if (!(button instanceof HTMLElement)) return;
  const personId = String(button.getAttribute('data-face-filter') || '').trim().toLowerCase();
  if (!personId) return;
  if (activeFaceFilters.has(personId)) {
    activeFaceFilters.delete(personId);
  } else {
    activeFaceFilters.add(personId);
  }
  renderFaceRecognitionFilters();
  updateFilterToggleLabel();
  queueRefresh();
});
runFaceRecognitionBtn?.addEventListener('click', async () => {
  if (!(runFaceRecognitionBtn instanceof HTMLButtonElement)) return;
  const original = runFaceRecognitionBtn.textContent || 'Run Facial Recognition';
  runFaceRecognitionBtn.disabled = true;
  runFaceRecognitionBtn.textContent = 'Running...';
  try {
    await refreshPosts({ forceFaceRefresh: true });
  } finally {
    runFaceRecognitionBtn.disabled = false;
    runFaceRecognitionBtn.textContent = original;
  }
});
faceConfidenceRange?.addEventListener('input', () => {
  const next = Number(faceConfidenceRange.value);
  activeFaceMinConfidence = Number.isFinite(next) ? Math.max(0, Math.min(1, next)) : 0;
  renderFaceRecognitionFilters();
  renderPosts(latestPosts);
});
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
function handleSignalRowFilterClick(event) {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return false;
  const row = target.closest('[data-signal-field][data-signal-value]');
  if (!(row instanceof HTMLElement)) return;
  const fieldName = String(row.getAttribute('data-signal-field') || '').trim();
  const signalValue = String(row.getAttribute('data-signal-value') || '').trim().toLowerCase();
  if (!fieldName || !signalValue) return false;
  const token = `${fieldName}|${signalValue}`;
  if (activeSignalFilters.has(token)) {
    activeSignalFilters.delete(token);
  } else {
    activeSignalFilters.add(token);
  }
  updateFilterToggleLabel();
  queueRefresh();
  return true;
}

threatMix?.addEventListener('click', handleSignalRowFilterClick);
selectorMix?.addEventListener('click', handleSignalRowFilterClick);
threatSignalMix?.addEventListener('click', handleSignalRowFilterClick);
customKeywordMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const row = target.closest('[data-custom-keyword]');
  if (!(row instanceof HTMLElement)) return;
  const keyword = String(row.getAttribute('data-custom-keyword') || '').trim().toLowerCase();
  if (!keyword) return;
  if (activeCustomKeywordFilters.has(keyword)) {
    activeCustomKeywordFilters.delete(keyword);
  } else {
    activeCustomKeywordFilters.add(keyword);
  }
  renderCustomKeywordMix(latestPosts);
  updateFilterToggleLabel();
  queueRefresh();
});
llmPrimaryMix?.addEventListener('click', handleSignalRowFilterClick);
llmSecondaryMix?.addEventListener('click', handleSignalRowFilterClick);
llmThemeMix?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const row = target.closest('[data-post-index]');
  if (!(row instanceof HTMLElement)) return;
  const postIndex = Number(row.getAttribute('data-post-index'));
  if (!Number.isFinite(postIndex) || postIndex < 0) return;
  scrollToPost(postIndex);
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
  if (caseEditModal && !caseEditModal.classList.contains('hidden')) {
    closeCaseEditModal();
    return;
  }
  if (caseSaveModal && !caseSaveModal.classList.contains('hidden')) {
    closeCaseSaveModal();
    return;
  }
  if (caseNotesModal && !caseNotesModal.classList.contains('hidden')) {
    closeCaseNotesModal();
    return;
  }
  if (manualInsertModal && !manualInsertModal.classList.contains('hidden')) {
    closeManualInsertModal();
    return;
  }
  if (postModal && !postModal.classList.contains('hidden')) {
    closePostModal();
    return;
  }
  if (filterPanel.classList.contains('hidden')) return;
  filterPanel.classList.add('hidden');
  filterToggleBtn.setAttribute('aria-expanded', 'false');
});
caseEditModal?.addEventListener('click', (event) => {
  if (!(event.target instanceof HTMLElement)) return;
  if (event.target !== caseEditModal) return;
  closeCaseEditModal();
});
caseSaveModal?.addEventListener('click', (event) => {
  if (!(event.target instanceof HTMLElement)) return;
  if (event.target !== caseSaveModal) return;
  closeCaseSaveModal();
});
caseNotesModal?.addEventListener('click', (event) => {
  if (!(event.target instanceof HTMLElement)) return;
  if (event.target !== caseNotesModal) return;
  closeCaseNotesModal();
});
manualInsertModal?.addEventListener('click', (event) => {
  if (!(event.target instanceof HTMLElement)) return;
  if (event.target !== manualInsertModal) return;
  closeManualInsertModal();
});
postModal?.addEventListener('click', (event) => {
  if (!(event.target instanceof HTMLElement)) return;
  if (event.target !== postModal) return;
  closePostModal();
});
window.addEventListener('resize', () => {
  if (activeInsightsTab !== 'geo') return;
  refreshMapLayout();
});
insightsTabOps?.addEventListener('click', () => setInsightsTab('ops'));
insightsTabGeo?.addEventListener('click', () => setInsightsTab('geo'));
insightsTabSignals?.addEventListener('click', () => setInsightsTab('signals'));
openCaseNotesTopBtn?.addEventListener('click', () => {
  openCaseNotesModal();
});
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
  if (!activeCaseId) {
    showNotification('Open a case first.', 'warn');
    showCaseWorkspace();
    return;
  }
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
backToCasesBtn?.addEventListener('click', async () => {
  if (!confirmUnsavedCaseExit('leave this case')) return;
  const discarded = await discardUnsavedActiveCase();
  if (discarded) {
    showNotification('Unsaved case discarded.', 'info');
  }
  clearCollectionPolling();
  loadCases();
  showCaseWorkspace();
});
saveQuitCaseBtn?.addEventListener('click', openCaseSaveModal);
caseSaveForm?.addEventListener('submit', submitCaseSave);
caseSaveCancelBtn?.addEventListener('click', closeCaseSaveModal);
caseSaveCloseBtn?.addEventListener('click', closeCaseSaveModal);
openConfigBtn?.addEventListener('click', openConfigModal);
configCloseBtn?.addEventListener('click', closeConfigModal);
configCancelBtn?.addEventListener('click', closeConfigModal);
configForm?.addEventListener('submit', saveConfig);
configCustomKeywordInput?.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return;
  event.preventDefault();
  addConfigCustomKeywordTerm(configCustomKeywordInput.value);
  configCustomKeywordInput.value = '';
});
configCustomKeywordPills?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const button = target.closest('[data-config-keyword-pill]');
  if (!(button instanceof HTMLElement)) return;
  removeConfigCustomKeywordTerm(button.getAttribute('data-config-keyword-pill'));
});
openManualInsertBtn?.addEventListener('click', openManualInsertModal);
manualInsertCloseBtn?.addEventListener('click', closeManualInsertModal);
manualInsertCancelBtn?.addEventListener('click', closeManualInsertModal);
manualInsertForm?.addEventListener('submit', submitManualInsert);
postModalCloseBtn?.addEventListener('click', closePostModal);
caseSaveStatusSelect?.addEventListener('change', () => {
  setWatchlistCadenceVisibility(
    caseSaveStatusSelect,
    caseSaveCadenceField,
    caseSaveCadenceSelect,
    watchlistCadenceForCase(activeCaseId),
  );
});
caseNotesForm?.addEventListener('submit', submitCaseNotes);
caseNotesCloseBtn?.addEventListener('click', closeCaseNotesModal);
caseNotesCancelBtn?.addEventListener('click', closeCaseNotesModal);
caseNotesExportPdfBtn?.addEventListener('click', exportCaseNotesPdf);
caseNotesSubjectImageSelect?.addEventListener('change', () => {
  const selected = String(caseNotesSubjectImageSelect.value || '').trim();
  renderCaseNotesSubjectImagePreview(selected);
});
caseNotesSubjectUploadBtn?.addEventListener('click', () => {
  caseNotesSubjectUploadInput?.click();
});
caseNotesSubjectUploadInput?.addEventListener('change', async () => {
  const file = caseNotesSubjectUploadInput?.files?.[0];
  if (!file) return;
  try {
    const imageDataUrl = String(await readImageAsDataUrl(file));
    if (!imageDataUrl) return;
    if (!caseNotesImageChoices.includes(imageDataUrl)) caseNotesImageChoices.unshift(imageDataUrl);
    renderCaseNotesSubjectImageOptions(imageDataUrl);
    renderCaseNotesSubjectImagePreview(imageDataUrl);
  } catch (error) {
    console.error(error);
    showNotification('Upload failed. Choose an image file.', 'error');
  } finally {
    if (caseNotesSubjectUploadInput) caseNotesSubjectUploadInput.value = '';
  }
});
caseNotesAddProfileBtn?.addEventListener('click', () => {
  syncKnownProfilesFromForm();
  caseNotesKnownProfiles.push({
    site: '',
    url: '',
    image_url: '',
    screenshot_url: '',
  });
  renderCaseNotesProfiles();
});
caseNotesProfilesList?.addEventListener('change', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const card = target.closest('.case-notes-profile-card');
  if (!(card instanceof HTMLElement)) return;
  const index = Number(card.getAttribute('data-profile-index'));
  if (Number.isNaN(index)) return;
  if (target.classList.contains('case-notes-profile-upload-image-input') && target instanceof HTMLInputElement) {
    const file = target.files?.[0];
    if (!file) return;
    readImageAsDataUrl(file)
      .then((imageDataUrl) => {
        syncKnownProfilesFromForm();
        const value = String(imageDataUrl || '').trim();
        if (!value) return;
        if (!caseNotesImageChoices.includes(value)) caseNotesImageChoices.unshift(value);
        caseNotesKnownProfiles[index] = { ...(caseNotesKnownProfiles[index] || {}), image_url: value };
        renderCaseNotesProfiles();
      })
      .catch((error) => {
        console.error(error);
        showNotification('Upload failed. Choose an image file.', 'error');
      })
      .finally(() => { target.value = ''; });
    return;
  }
  if (target.classList.contains('case-notes-profile-upload-shot-input') && target instanceof HTMLInputElement) {
    const file = target.files?.[0];
    if (!file) return;
    readImageAsDataUrl(file)
      .then((imageDataUrl) => {
        syncKnownProfilesFromForm();
        const value = String(imageDataUrl || '').trim();
        if (!value) return;
        caseNotesKnownProfiles[index] = { ...(caseNotesKnownProfiles[index] || {}), screenshot_url: value };
        renderCaseNotesProfiles();
      })
      .catch((error) => {
        console.error(error);
        showNotification('Upload failed. Choose an image file.', 'error');
      })
      .finally(() => { target.value = ''; });
    return;
  }
  if (!target.classList.contains('case-notes-profile-image-select')) return;
  syncKnownProfilesFromForm();
  renderCaseNotesProfiles();
});
caseNotesProfilesList?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const card = target.closest('.case-notes-profile-card');
  if (card instanceof HTMLElement) {
    if (target.classList.contains('case-notes-profile-upload-image-btn')) {
      const input = card.querySelector('.case-notes-profile-upload-image-input');
      if (input instanceof HTMLInputElement) input.click();
      return;
    }
    if (target.classList.contains('case-notes-profile-upload-shot-btn')) {
      const input = card.querySelector('.case-notes-profile-upload-shot-input');
      if (input instanceof HTMLInputElement) input.click();
      return;
    }
  }
  if (!target.classList.contains('case-notes-remove-profile-btn')) return;
  syncKnownProfilesFromForm();
  if (!(card instanceof HTMLElement)) return;
  const index = Number(card.getAttribute('data-profile-index'));
  if (Number.isNaN(index)) return;
  caseNotesKnownProfiles = caseNotesKnownProfiles.filter((_, itemIndex) => itemIndex !== index);
  renderCaseNotesProfiles();
});
caseSaveImageOptions?.addEventListener('change', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) return;
  if (target.name !== 'caseSavePoiImage') return;
  caseSaveSelectedImageUrl = String(target.value || '').trim();
});
addTargetBtn.addEventListener('click', () => addTargetRow('twitter', ''));
autofillTargetsBtn.addEventListener('click', autofillTargetUsernames);
closeSetupBtn.addEventListener('click', () => setModalOpen(false));
modeReconBtn.addEventListener('click', () => {
  reconStatus.textContent = '';
  setModalMode('recon');
  ensureAtLeastOneReconSelectorRow();
  const firstInput = reconSelectorsList?.querySelector('.recon-selector-value');
  if (firstInput instanceof HTMLInputElement) firstInput.focus();
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
goReconAssessmentBtn?.addEventListener('click', openAssessmentFromRecon);
addReconSelectorBtn?.addEventListener('click', () => addReconSelectorRow(reconSelectorsList, 'username', ''));
addFootprintSelectorBtn?.addEventListener('click', () => addReconSelectorRow(footprintSelectorsList, 'username', ''));
footprintUseTargetsBtn?.addEventListener('click', () => {
  if (!reconTargets.length) return;
  fillTargetsFromRecon(reconTargets);
  if (footprintReconStatus) footprintReconStatus.textContent = 'Loaded active recon profiles into collection targets.';
});
reconSelectorsList?.addEventListener('change', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (!target.classList.contains('recon-selector-type')) return;
  const row = target.closest('.recon-selector-row');
  if (!(row instanceof HTMLElement)) return;
  const typeValue = target instanceof HTMLSelectElement ? String(target.value || '').trim().toLowerCase() : 'username';
  const exampleEl = row.querySelector('.recon-selector-example');
  if (exampleEl instanceof HTMLElement) {
    exampleEl.textContent = reconExampleText(typeValue);
  }
});
footprintSelectorsList?.addEventListener('change', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (!target.classList.contains('recon-selector-type')) return;
  const row = target.closest('.recon-selector-row');
  if (!(row instanceof HTMLElement)) return;
  const typeValue = target instanceof HTMLSelectElement ? String(target.value || '').trim().toLowerCase() : 'username';
  const exampleEl = row.querySelector('.recon-selector-example');
  if (exampleEl instanceof HTMLElement) {
    exampleEl.textContent = reconExampleText(typeValue);
  }
});
reconSelectorsList?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (!target.classList.contains('recon-selector-remove')) return;
  const row = target.closest('.recon-selector-row');
  if (!(row instanceof HTMLElement)) return;
  row.remove();
  ensureAtLeastOneReconSelectorRow();
});
footprintSelectorsList?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (!target.classList.contains('recon-selector-remove')) return;
  const row = target.closest('.recon-selector-row');
  if (!(row instanceof HTMLElement)) return;
  row.remove();
  ensureAtLeastOneReconSelectorRow(footprintSelectorsList);
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
  await quitPanoptoSession({ clearData: true });
});
quitSessionCaseBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ clearData: true });
});
quitSaveBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ clearData: false });
});
quitSaveSessionCaseBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ clearData: false });
});

async function quitPanoptoSession(options = {}) {
  const clearData = options?.clearData !== false;
  const ok = clearData
    ? window.confirm('Quit PANOPTO and wipe collected session data?')
    : window.confirm('Quit PANOPTO and keep collected results for next demo session?');
  if (!ok) return;
  if (!confirmUnsavedCaseExit('quit PANOPTO')) return;
  if (quitBtn) {
    quitBtn.disabled = true;
    quitBtn.textContent = 'Quitting...';
  }
  if (quitSaveBtn) {
    quitSaveBtn.disabled = true;
    quitSaveBtn.textContent = 'Quitting...';
  }
  if (quitSessionCaseBtn) {
    quitSessionCaseBtn.disabled = true;
    quitSessionCaseBtn.textContent = 'Quitting...';
  }
  if (quitSaveSessionCaseBtn) {
    quitSaveSessionCaseBtn.disabled = true;
    quitSaveSessionCaseBtn.textContent = 'Quitting...';
  }
  try {
    await discardUnsavedActiveCase();
    clearCollectionPolling();
    resetCollectionSourceState();
    activeTargets = [];
    activeStartDate = '';
    activeEndDate = '';
    renderCollectionContext();
    await fetch('/api/session/end', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ shutdown: true, clear_data: clearData }),
      keepalive: true,
    });
    statusEl.textContent = clearData
      ? 'Session ended. Database wiped.'
      : 'Session ended. Results were preserved for later demos.';
    resultsEl.innerHTML = clearData
      ? '<div class="empty">PANOPTO session ended. Restart server to collect again.</div>'
      : '<div class="empty">PANOPTO session ended. Restart server to continue with saved results.</div>';
    // Attempt to close the PANOPTO tab after a successful shutdown.
    window.setTimeout(() => {
      try {
        window.close();
      } catch (closeError) {
        console.error(closeError);
      }
      if (!window.closed) {
        window.location.replace('about:blank');
        window.setTimeout(() => {
          try {
            window.close();
          } catch (closeRetryError) {
            console.error(closeRetryError);
          }
        }, 60);
      }
    }, 80);
  } catch (error) {
    console.error(error);
    statusEl.textContent = 'Failed to end session cleanly.';
  } finally {
    if (quitBtn) {
      quitBtn.disabled = false;
      quitBtn.textContent = 'Quit Session';
    }
    if (quitSaveBtn) {
      quitSaveBtn.disabled = false;
      quitSaveBtn.textContent = 'Quit & Save Results';
    }
    if (quitSessionCaseBtn) {
      quitSessionCaseBtn.disabled = false;
      quitSessionCaseBtn.textContent = 'Quit Session';
    }
    if (quitSaveSessionCaseBtn) {
      quitSaveSessionCaseBtn.disabled = false;
      quitSaveSessionCaseBtn.textContent = 'Quit & Save Results';
    }
  }
}
initializeDateInputs();
addTargetRow('twitter', '');
addReconSelectorRow(reconSelectorsList, 'username', '');
addReconSelectorRow(footprintSelectorsList, 'username', '');
renderLeadsList();
renderCollectionStreams();
applyResultsViewButtonState();
setInsightsTab(activeInsightsTab);
updateStreamActionButtons();
updateFilterToggleLabel();
renderFaceRecognitionFilters();
applyResultsViewButtonState();
renderCollectionContext();
setModalMode('chooser');
setModalOpen(false);
setWatchlistCadenceVisibility(caseEditStatusSelect, caseEditCadenceField, caseEditCadenceSelect);
setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect);
showCaseWorkspace();
loadConfig();
loadCases();
