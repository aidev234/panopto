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
const quitOptionsModal = document.getElementById('quitOptionsModal');
const quitOptionsQuitBtn = document.getElementById('quitOptionsQuitBtn');
const quitOptionsWipeBtn = document.getElementById('quitOptionsWipeBtn');
const quitOptionsSaveBtn = document.getElementById('quitOptionsSaveBtn');
const quitOptionsCancelBtn = document.getElementById('quitOptionsCancelBtn');
const configModal = document.getElementById('configModal');
const configForm = document.getElementById('configForm');
const configPdlApiKeyInput = document.getElementById('configPdlApiKeyInput');
const configPdlApiKeyHint = document.getElementById('configPdlApiKeyHint');
const configOsintIndustriesApiKeyInput = document.getElementById('configOsintIndustriesApiKeyInput');
const configOsintIndustriesApiKeyHint = document.getElementById('configOsintIndustriesApiKeyHint');
const configNumverifyApiKeyInput = document.getElementById('configNumverifyApiKeyInput');
const configNumverifyApiKeyHint = document.getElementById('configNumverifyApiKeyHint');
const configOpenAiApiKeyInput = document.getElementById('configOpenAiApiKeyInput');
const configOpenAiApiKeyHint = document.getElementById('configOpenAiApiKeyHint');
const configApifyApiTokenInput = document.getElementById('configApifyApiTokenInput');
const configApifyApiTokenHint = document.getElementById('configApifyApiTokenHint');
const configDefaultRetentionSelect = document.getElementById('configDefaultRetentionSelect');
const configCustomKeywordInput = document.getElementById('configCustomKeywordInput');
const configCustomKeywordPills = document.getElementById('configCustomKeywordPills');
const configSaveBtn = document.getElementById('configSaveBtn');
const configCloseBtn = document.getElementById('configCloseBtn');
const configCancelBtn = document.getElementById('configCancelBtn');
const configStatus = document.getElementById('configStatus');
const configSecretStateSummary = document.getElementById('configSecretStateSummary');
const caseEditModal = document.getElementById('caseEditModal');
const caseEditForm = document.getElementById('caseEditForm');
const caseEditTitleInput = document.getElementById('caseEditTitleInput');
const caseEditStatusSelect = document.getElementById('caseEditStatusSelect');
const caseEditCadenceField = document.getElementById('caseEditCadenceField');
const caseEditCadenceSelect = document.getElementById('caseEditCadenceSelect');
const caseEditThreatSelect = document.getElementById('caseEditThreatSelect');
const caseEditRetentionSelect = document.getElementById('caseEditRetentionSelect');
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
const caseSaveRetentionSelect = document.getElementById('caseSaveRetentionSelect');
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
const caseNotesSelectorEmailsInput = document.getElementById('caseNotesSelectorEmailsInput');
const caseNotesSelectorPhonesInput = document.getElementById('caseNotesSelectorPhonesInput');
const caseNotesSelectorUsernamesInput = document.getElementById('caseNotesSelectorUsernamesInput');
const caseNotesProfilesList = document.getElementById('caseNotesProfilesList');
const caseNotesFootprintResults = document.getElementById('caseNotesFootprintResults');
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
const viewTimelineBtn = document.getElementById('viewTimelineBtn');
const viewEntityGraphBtn = document.getElementById('viewEntityGraphBtn');
const filterMenu = document.getElementById('filterMenu');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const footprintView = document.getElementById('footprintView');
const patternLifeView = document.getElementById('patternLifeView');
const timelineView = document.getElementById('timelineView');
const entityGraphView = document.getElementById('entityGraphView');
const footprintReconForm = document.getElementById('footprintReconForm');
const footprintSelectorsList = document.getElementById('footprintSelectorsList');
const addFootprintSelectorBtn = document.getElementById('addFootprintSelectorBtn');
const footprintReconBtn = document.getElementById('footprintReconBtn');
const footprintUseTargetsBtn = document.getElementById('footprintUseTargetsBtn');
const footprintReconResults = document.getElementById('footprintReconResults');
const footprintReconStatus = document.getElementById('footprintReconStatus');
const footprintKnownSelectors = document.getElementById('footprintKnownSelectors');
const footprintKnownSelectorsTotal = document.getElementById('footprintKnownSelectorsTotal');
const footprintKnownSelectorsGroups = document.getElementById('footprintKnownSelectorsGroups');
const footprintLikelyName = document.getElementById('footprintLikelyName');
const footprintLikelyNameValue = document.getElementById('footprintLikelyNameValue');
const footprintPivotProgress = document.getElementById('footprintPivotProgress');
const footprintPivotProgressLabel = document.getElementById('footprintPivotProgressLabel');
const footprintReconProgress = document.getElementById('footprintReconProgress');
const footprintReconProgressLabel = document.getElementById('footprintReconProgressLabel');
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
const reconProgress = document.getElementById('reconProgress');
const reconProgressLabel = document.getElementById('reconProgressLabel');
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
const patternLifePlatformFilters = document.getElementById('patternLifePlatformFilters');
const patternLifeRefreshBtn = document.getElementById('patternLifeRefreshBtn');
const patternLifeLikelyLocations = document.getElementById('patternLifeLikelyLocations');
const patternLifeLikelyLocationsEmpty = document.getElementById('patternLifeLikelyLocationsEmpty');
const keywordChart = document.getElementById('keywordChart');
const keywordEmpty = document.getElementById('keywordEmpty');
const typeMix = document.getElementById('typeMix');
const locationMap = document.getElementById('locationMap');
const locationMapEmpty = document.getElementById('locationMapEmpty');
const locationMapTotal = document.getElementById('locationMapTotal');
const patternLifeMap = document.getElementById('patternLifeMap');
const patternLifeMapEmpty = document.getElementById('patternLifeMapEmpty');
const patternLifeLocationMapTotal = document.getElementById('patternLifeLocationMapTotal');
const footprintTimelineSummary = document.getElementById('footprintTimelineSummary');
const footprintTimelineSummaryText = document.getElementById('footprintTimelineSummaryText');
const footprintTimelineEarliest = document.getElementById('footprintTimelineEarliest');
const footprintTimelineEvents = document.getElementById('footprintTimelineEvents');
const footprintTimelineEmpty = document.getElementById('footprintTimelineEmpty');
const footprintEntityGraphSummary = document.getElementById('footprintEntityGraphSummary');
const footprintEntityGraphSummaryText = document.getElementById('footprintEntityGraphSummaryText');
const footprintEntityGraphCanvas = document.getElementById('footprintEntityGraphCanvas');
const footprintEntityGraphDetails = document.getElementById('footprintEntityGraphDetails');
const footprintEntityGraphEmpty = document.getElementById('footprintEntityGraphEmpty');
const footprintEntityGraphQuery = document.getElementById('footprintEntityGraphQuery');
const footprintEntityGraphReset = document.getElementById('footprintEntityGraphReset');
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
let caseNotesFootprintEntries = [];
const caseNotesExcludedSections = new Set();
const caseNotesExcludedFootprintResultKeys = new Set();
let activeStartDate = '';
let activeEndDate = '';
let activeUsername = '';
let activeTargets = [];
let latestFetchedPosts = [];
let latestPosts = [];
let latestRenderedPosts = [];
let activeResultsView = 'posts';
let reconTargets = [];
let reconLeads = [];
let reconProfiles = [];
let latestReconPayload = null;
const hiddenKnownSelectorKeys = new Set();
const hiddenReconRowKeys = new Set();
const hiddenOsintTileKeys = new Set();
const hiddenPdlProfileKeys = new Set();
const hiddenPdlContactValueKeys = new Set();
const hiddenPdlProfileUrlKeys = new Set();
let reconPersonDataProfile = {};
let reconPersonDataProfiles = [];
let reconOsintProfiles = [];
let reconOsintSpecResults = [];
let reconNumverifyProfiles = [];
let reconSnapshotCache = null;
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
let activeKnownSelectorFocusKey = '';
let activeKnownSelectorFocusIndex = -1;
let reconProgressStartedAt = 0;
let reconProgressTimer = null;
let footprintReconProgressStartedAt = 0;
let footprintReconProgressTimer = null;
let footprintPivotProgressStartedAt = 0;
let footprintPivotProgressTimer = null;
let lastAutofilledCaseNotesName = '';
let lastAutofilledCaseNotesLocation = '';
const caseNotesAutoProfileKeys = new Set();
const SELECTOR_CONFIDENCE_OVERRIDE_STORAGE_KEY = 'panopto.selectorConfidenceOverrides.v1';
const SELECTOR_CONFIDENCE_LEVELS = ['high', 'medium', 'low'];
const selectorConfidenceOverrides = new Map();
const CASE_NOTES_MAJOR_PROFILE_SITE_KEYS = new Set(['facebook', 'instagram', 'tiktok']);
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
let patternLifeTargetBoxLayers = [];
let latestPatternLifeMapPoints = [];
let latestPatternLifeMapRoutes = [];
let latestPatternLifeLikelyCandidates = [];
const activePatternLifePlatforms = new Set(SOURCE_ORDER);
const activeTimelineSources = new Set();
const activeTimelineActions = new Set();
let timelineSelectorQuery = '';
let timelineShowOnlyLinked = false;
let entityGraphQuery = '';
let entityGraphSelectedNodeId = '';
let entityGraphViewport = { zoom: 1, offsetX: 0, offsetY: 0 };
let entityGraphModelCache = null;
let entityGraphLayoutCache = null;
let entityGraphPointerPan = null;
const entityGraphManualPositions = new Map();
let entityGraphNodeDrag = null;
let activeFootprintSourceSelectorKey = 'all';
let configCustomKeywordList = [];
const DEFAULT_DATA_RETENTION_PERIOD = '3 months';
const DATA_RETENTION_PERIOD_OPTIONS = ['24h', '1 week', '3 week', '6 weeks', '3 months', '1 year'];
let defaultDataRetentionPeriod = DEFAULT_DATA_RETENTION_PERIOD;
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
  'loc:united-states': { name: 'United States', lat: 39.8283, lon: -98.5795 },
  'loc:canada': { name: 'Canada', lat: 56.1304, lon: -106.3468 },
  'loc:ottawa': { name: 'Ottawa', lat: 45.4215, lon: -75.6972 },
  'loc:nova-scotia': { name: 'Nova Scotia', lat: 44.682, lon: -63.7443 },
  'loc:halifax': { name: 'Halifax', lat: 44.6488, lon: -63.5752 },
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
const LOCATION_ALIAS_TO_TAG = {
  'new york city': 'loc:new-york',
  nyc: 'loc:new-york',
  'washington, dc': 'loc:washington-dc',
  'washington d.c.': 'loc:washington-dc',
  'district of columbia': 'loc:washington-dc',
  dc: 'loc:washington-dc',
  'd.c.': 'loc:washington-dc',
  'united states of america': 'loc:united-states',
  'united states': 'loc:united-states',
  usa: 'loc:united-states',
  'u.s.a.': 'loc:united-states',
  us: 'loc:united-states',
  'u.s.': 'loc:united-states',
  'country us': 'loc:united-states',
  'country usa': 'loc:united-states',
  canada: 'loc:canada',
  'country ca': 'loc:canada',
  ottawa: 'loc:ottawa',
  'ottawa, canada': 'loc:ottawa',
  'city ottawa': 'loc:ottawa',
  'nova scotia': 'loc:nova-scotia',
  halifax: 'loc:halifax',
  'halifax, nova scotia': 'loc:halifax',
  'halifax, nova scotia, canada': 'loc:halifax',
};
const COUNTRY_CODE_TO_LOCATION_TAG = {
  us: 'loc:united-states',
  usa: 'loc:united-states',
  ca: 'loc:canada',
  can: 'loc:canada',
  ua: 'loc:ukraine',
  ukr: 'loc:ukraine',
  il: 'loc:israel',
  isr: 'loc:israel',
  ps: 'loc:palestine',
  pse: 'loc:palestine',
};

function clearHiddenReconEntities() {
  hiddenKnownSelectorKeys.clear();
  hiddenReconRowKeys.clear();
  hiddenOsintTileKeys.clear();
  hiddenPdlProfileKeys.clear();
  hiddenPdlContactValueKeys.clear();
  hiddenPdlProfileUrlKeys.clear();
}

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

function canonicalTargetKey(platform, username) {
  const normalizedPlatform = String(platform || '').trim().toLowerCase();
  const normalizedUsername = normalizeTargetUsername(normalizedPlatform, username);
  const adjusted = adjustTargetUsernameForCollection(normalizedPlatform, normalizedUsername);
  return `${normalizedPlatform}|${String(adjusted || '').trim().toLowerCase()}`;
}

function getTargetsFromForm() {
  const targets = [];
  const seen = new Set();
  for (const row of targetsList.querySelectorAll('.target-row')) {
    const platformEl = row.querySelector('.target-platform');
    const usernameEl = row.querySelector('.target-username');
    if (!platformEl || !usernameEl) continue;
    const platform = platformEl.value.trim().toLowerCase();
    const normalizedUsername = normalizeTargetUsername(platform, usernameEl.value);
    if (!normalizedUsername) continue;
    const adjustedUsername = adjustTargetUsernameForCollection(platform, normalizedUsername);
    const dedupeKey = canonicalTargetKey(platform, adjustedUsername);
    if (seen.has(dedupeKey)) continue;
    seen.add(dedupeKey);
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
    const archiveSelectors = window.confirm('Would you like to save selectors to your internal Known Entities Database?');
    if (archiveSelectors) {
      const archiveResponse = await fetch('/api/known-entities/archive-case', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ case_id: id }),
      });
      if (!archiveResponse.ok) {
        const archiveError = await parseErrorResponse(archiveResponse);
        const continueDelete = window.confirm(
          `Could not save selectors to Known Entities Database (${archiveError}). Continue deleting this case anyway?`,
        );
        if (!continueDelete) return;
      }
    }
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
    showNotification(archiveSelectors ? 'Case deleted (selectors archived)' : 'Case deleted', 'success');
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

function normalizeDataRetentionPeriod(value) {
  const clean = String(value || '').trim().toLowerCase();
  const lookup = {
    '24h': '24h',
    '24 hours': '24h',
    '1 week': '1 week',
    '3 week': '3 week',
    '3 weeks': '3 week',
    '6 weeks': '6 weeks',
    '3 months': '3 months',
    '1 year': '1 year',
  };
  return lookup[clean] || DEFAULT_DATA_RETENTION_PERIOD;
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
  if (caseEditTitleInput instanceof HTMLInputElement) {
    caseEditTitleInput.value = String(row.case_name || 'Untitled Case').trim() || 'Untitled Case';
  }
  if (caseEditStatusSelect) caseEditStatusSelect.value = String(row.status || 'Open');
  if (caseEditThreatSelect) caseEditThreatSelect.value = String(row.threat_level || 'Low Threat');
  if (caseEditRetentionSelect) caseEditRetentionSelect.value = normalizeDataRetentionPeriod(row.data_retention_period);
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
  if (caseEditRetentionSelect) caseEditRetentionSelect.value = DEFAULT_DATA_RETENTION_PERIOD;
  setWatchlistCadenceVisibility(caseEditStatusSelect, caseEditCadenceField, caseEditCadenceSelect);
  setCaseEditModalOpen(false);
}

async function submitCaseEdit(event) {
  event.preventDefault();
  const id = String(editingCaseId || '').trim();
  if (!id) return;
  const nextName = String(caseEditTitleInput?.value || '').trim() || 'Untitled Case';
  const nextStatus = String(caseEditStatusSelect?.value || '').trim();
  const nextCadence = String(caseEditCadenceSelect?.value || '').trim();
  const nextThreat = String(caseEditThreatSelect?.value || '').trim();
  const nextRetention = normalizeDataRetentionPeriod(caseEditRetentionSelect?.value);
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
        case_name: nextName,
        status: nextStatus,
        threat_level: nextThreat,
        data_retention_period: nextRetention,
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
    showNotification('No active case selected.', 'warn');
    showCaseWorkspace();
    return;
  }
  const currentName = String(activeCase?.case_name || '').trim() || 'Untitled Case';
  const currentStatus = String(activeCase?.status || 'Open').trim() || 'Open';
  const currentCadence = watchlistCadenceForCase(activeCaseId, activeCase?.monitoring_refresh_cadence);
  const currentThreat = String(activeCase?.threat_level || 'Low Threat').trim() || 'Low Threat';
  const currentRetention = normalizeDataRetentionPeriod(activeCase?.data_retention_period);
  const currentLocation = String(activeCase?.known_location || 'Unknown').trim() || 'Unknown';
  const currentPoiImage = normalizeProfileImageUrl(activeCase?.poi_image_url);
  if (caseSaveTitleInput) caseSaveTitleInput.value = currentName;
  if (caseSaveStatusSelect) caseSaveStatusSelect.value = currentStatus;
  if (caseSaveCadenceSelect) caseSaveCadenceSelect.value = currentCadence;
  if (caseSaveThreatSelect) caseSaveThreatSelect.value = currentThreat;
  if (caseSaveRetentionSelect) caseSaveRetentionSelect.value = currentRetention;
  if (caseSaveLocationInput) caseSaveLocationInput.value = currentLocation;
  caseSaveImageChoices = currentPoiImage ? [currentPoiImage] : [];
  caseSaveSelectedImageUrl = currentPoiImage || USER_PLACEHOLDER_AVATAR_URL;
  renderCaseSaveImageOptions();
  setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect, currentCadence);
  setCaseSaveModalOpen(true);
  fetchCasePosts(activeCaseId)
    .then((posts) => {
      const associatedImages = uniqueProfileImageUrls(posts);
      if (currentPoiImage && !associatedImages.includes(currentPoiImage)) {
        associatedImages.unshift(currentPoiImage);
      }
      caseSaveImageChoices = associatedImages;
      if (!caseSaveSelectedImageUrl) {
        caseSaveSelectedImageUrl = currentPoiImage || USER_PLACEHOLDER_AVATAR_URL;
      }
      renderCaseSaveImageOptions();
    })
    .catch(() => {
      // Image candidates are optional for save flow.
    });
}

function closeCaseSaveModal() {
  caseSaveSelectedImageUrl = '';
  caseSaveImageChoices = [];
  if (caseSaveCadenceSelect) caseSaveCadenceSelect.value = '';
  if (caseSaveRetentionSelect) caseSaveRetentionSelect.value = DEFAULT_DATA_RETENTION_PERIOD;
  setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect);
  setCaseSaveModalOpen(false);
}

function normalizeCaseNotesObject(raw) {
  if (!raw || typeof raw !== 'object') return {};
  return raw;
}

function normalizeCaseNotesReportPreferences(raw) {
  const prefs = raw && typeof raw === 'object' ? raw : {};
  const excludedSections = Array.isArray(prefs.excluded_sections)
    ? prefs.excluded_sections.map((item) => String(item || '').trim().toLowerCase()).filter(Boolean)
    : [];
  const excludedFootprintResultKeys = Array.isArray(prefs.excluded_footprint_result_keys)
    ? prefs.excluded_footprint_result_keys.map((item) => String(item || '').trim().toLowerCase()).filter(Boolean)
    : [];
  return {
    excluded_sections: [...new Set(excludedSections)],
    excluded_footprint_result_keys: [...new Set(excludedFootprintResultKeys)],
  };
}

function caseNotesFootprintResultKey(source, selectorType, selectorValue, summary) {
  return [
    String(source || '').trim().toLowerCase(),
    String(selectorType || '').trim().toLowerCase(),
    String(selectorValue || '').trim().toLowerCase(),
    String(summary || '').trim().toLowerCase(),
  ].join('|');
}

function splitCommaSeparatedValues(raw) {
  const text = String(raw || '').trim();
  if (!text) return [];
  return text.split(',').map((item) => String(item || '').trim()).filter(Boolean);
}

function joinCommaSeparatedValues(values) {
  return [...new Set((Array.isArray(values) ? values : []).map((item) => String(item || '').trim()).filter(Boolean))].join(', ');
}

function inferSelectorValuesFromCaseNotes(notes) {
  const snapshot = normalizeReconSnapshot(notes?.recon_snapshot);
  const payload = snapshot?.payload || {};
  const emails = [];
  const phones = [];
  const usernames = [];
  const seenEmails = new Set();
  const seenPhones = new Set();
  const seenUsernames = new Set();

  const pushUnique = (bucket, seen, value, formatter = (v) => v) => {
    const clean = String(value || '').trim();
    if (!clean) return;
    const key = formatter(clean).toLowerCase();
    if (!key || seen.has(key)) return;
    seen.add(key);
    bucket.push(clean);
  };

  const pushEmail = (value) => pushUnique(emails, seenEmails, String(value || '').trim().toLowerCase(), (v) => v);
  const pushPhone = (value) => {
    const clean = String(value || '').trim();
    const canonical = clean.replace(/[^\d+]/g, '');
    if (!canonical) return;
    pushUnique(phones, seenPhones, clean, () => canonical);
  };
  const pushUsername = (value) => pushUnique(usernames, seenUsernames, value, (v) => v.replace(/^@+/, ''));
  const pushEmailHint = (value) => {
    const clean = String(value || '').trim().toLowerCase();
    if (!clean) return;
    const exactKey = clean;
    if (seenEmails.has(exactKey)) return;
    pushUnique(emails, seenEmails, `${clean} (email hint)`, (v) => v.replace(/\s*\(email hint\)$/i, ''));
  };
  const pushPhoneHint = (value) => {
    const clean = String(value || '').trim();
    if (!clean) return;
    const exactKey = clean.replace(/[^\d+]/g, '');
    if (exactKey && seenPhones.has(exactKey)) return;
    pushUnique(phones, seenPhones, `${clean} (phone hint)`, (v) => v.replace(/\s*\(phone hint\)$/i, '').replace(/[^\d+]/g, ''));
  };
  const isMediumOrHighConfidenceSelector = (selectorType) => {
    const confidence = selectorConfidenceLevel(selectorType);
    return confidence === 'high' || confidence === 'medium';
  };

  const ingest = (type, value) => {
    const selectorType = String(type || '').trim().toLowerCase();
    const selectorValue = String(value || '').trim();
    if (!selectorType || !selectorValue) return;
    if (!isMediumOrHighConfidenceSelector(selectorType)) return;
    if (selectorType === 'email') {
      pushEmail(selectorValue);
      return;
    }
    if (selectorType === 'phone') {
      pushPhone(selectorValue);
      return;
    }
    if (selectorType === 'username' || selectorType === 'name') {
      pushUsername(selectorValue);
    }
  };

  for (const selector of (Array.isArray(payload?.selectors) ? payload.selectors : [])) {
    if (!selector || typeof selector !== 'object') continue;
    ingest(selector.type, selector.value);
  }
  for (const row of (Array.isArray(payload?.results) ? payload.results : [])) {
    if (!row || typeof row !== 'object') continue;
    ingest(row.selector_type, row.selector);
  }
  for (const row of (Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    if (!isMediumOrHighConfidenceSelector(row.query_type)) continue;
    ingest(row.query_type, row.query_value);
    pushUsername(row.username);
    pushEmail(row.email);
    pushPhone(row.phone);
    pushEmailHint(row.email_hint);
    pushPhoneHint(row.phone_hint);
  }
  for (const row of (Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    if (!isMediumOrHighConfidenceSelector(row.query_type)) continue;
    ingest(row.query_type, row.query_value);
    pushEmail(row.professional_email || row.work_email || row.email);
    for (const item of (Array.isArray(row.personal_emails) ? row.personal_emails : [])) pushEmail(item);
    pushPhone(row.mobile_phone || row.phone);
    for (const item of (Array.isArray(row.personal_phones) ? row.personal_phones : [])) pushPhone(item);
    for (const item of (Array.isArray(row.professional_phones) ? row.professional_phones : [])) pushPhone(item);
  }
  for (const row of (Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    if (!isMediumOrHighConfidenceSelector(row.query_type || 'phone')) continue;
    ingest(row.query_type, row.query_value);
    pushPhone(row.number || row.international_format || row.e164 || row.local_format);
  }
  for (const row of (Array.isArray(payload?.leads) ? payload.leads : [])) {
    if (!row || typeof row !== 'object') continue;
    const attr = String(row.attribute || row.lead_type || '').trim().toLowerCase();
    const value = String(row.value || '').trim();
    if (!value) continue;
    if (attr.includes('email')) {
      if (isMediumOrHighConfidenceSelector('email')) pushEmail(value);
    } else if (attr.includes('phone')) {
      if (isMediumOrHighConfidenceSelector('phone')) pushPhone(value);
    } else if (attr.includes('name')) {
      if (isMediumOrHighConfidenceSelector('name')) pushUsername(value);
    }
  }

  return {
    emails,
    phones,
    usernames,
  };
}

function buildCaseNotesFootprintEntries(notes) {
  const snapshot = normalizeReconSnapshot(notes?.recon_snapshot);
  const payload = snapshot?.payload || {};
  const entries = [];
  const addEntry = ({
    source,
    selectorType,
    selectorValue,
    siteLabel = '',
    profileUrl = '',
    imageUrl = '',
    metadata = [],
  }) => {
    const cleanSource = String(source || '').trim() || 'Digital Footprint';
    const cleanSelectorType = String(selectorType || '').trim().toLowerCase();
    const cleanSelectorValue = String(selectorValue || '').trim();
    const cleanSiteLabel = String(siteLabel || '').trim();
    const cleanProfileUrl = normalizeExternalUrl(profileUrl);
    const cleanImageUrl = normalizeProfileImageUrl(imageUrl) || normalizeExternalUrl(imageUrl);
    const metadataRows = (Array.isArray(metadata) ? metadata : [])
      .map((item) => ({
        label: String(item?.label || '').trim(),
        value: String(item?.value || '').trim(),
      }))
      .filter((item) => item.label && item.value);
    const cleanSummary = metadataRows.length
      ? metadataRows.map((item) => `${item.label}: ${item.value}`).join(' | ')
      : 'No details available.';
    const key = caseNotesFootprintResultKey(
      cleanSource,
      cleanSelectorType,
      cleanSelectorValue,
      [cleanSiteLabel, cleanProfileUrl, cleanImageUrl, cleanSummary].filter(Boolean).join(' | '),
    );
    const confidence = selectorConfidenceLevel(cleanSelectorType);
    entries.push({
      key,
      source: cleanSource,
      selectorType: cleanSelectorType,
      selectorValue: cleanSelectorValue,
      siteLabel: cleanSiteLabel,
      profileUrl: cleanProfileUrl,
      imageUrl: cleanImageUrl,
      metadata: metadataRows,
      summary: cleanSummary,
      confidence,
    });
  };

  for (const row of (Array.isArray(payload?.results) ? payload.results : [])) {
    if (!row || typeof row !== 'object') continue;
    const status = String(row.status || 'unknown').trim().toLowerCase() || 'unknown';
    const site = String(row.site || row.site_key || 'unknown').trim() || 'unknown';
    const profileUrl = String(row.profile_url || '').trim();
    const reason = String(row.reason || '').trim();
    const source = String(row.source || 'Recon').trim() || 'Recon';
    const metadata = [
      { label: 'Status', value: status },
      reason ? { label: 'Reason', value: reason } : null,
    ].filter(Boolean);
    addEntry({
      source: `Recon (${source})`,
      selectorType: row.selector_type,
      selectorValue: row.selector,
      siteLabel: normalizeReconSiteLabel(site, profileUrl, row.site_url),
      profileUrl,
      imageUrl: row.profile_image_url || row.picture_url || row.avatar_url || row.screenshot_url,
      metadata,
    });
  }

  for (const row of (Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    const module = String(row.module || 'osint_industries').trim() || 'osint_industries';
    const website = String(row.website || '').trim();
    const profileUrl = String(row.profile_url || '').trim();
    const username = String(row.username || '').trim();
    const email = String(row.email || '').trim();
    const phone = String(row.phone || '').trim();
    const metadata = [
      { label: 'Module', value: module },
      username ? { label: 'Username', value: username } : null,
      email ? { label: 'Email', value: email } : null,
      phone ? { label: 'Phone', value: phone } : null,
    ].filter(Boolean);
    addEntry({
      source: 'OSINT Industries',
      selectorType: row.query_type,
      selectorValue: row.query_value,
      siteLabel: website || normalizeReconSiteLabel(row.website, profileUrl, row.website),
      profileUrl,
      imageUrl: row.picture_url || row.avatar_url || row.profile_image_url || row.screenshot_url,
      metadata,
    });
  }

  for (const row of (Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    const number = String(row.number || row.international_format || '').trim();
    const country = String(row.country_name || '').trim();
    const carrier = String(row.carrier || '').trim();
    const lineType = String(row.line_type || '').trim();
    const valid = row.valid === true ? 'yes' : 'no';
    const metadata = [
      { label: 'Valid', value: valid },
      number ? { label: 'Number', value: number } : null,
      country ? { label: 'Country', value: country } : null,
      carrier ? { label: 'Carrier', value: carrier } : null,
      lineType ? { label: 'Line Type', value: lineType } : null,
    ].filter(Boolean);
    addEntry({
      source: 'Numverify',
      selectorType: row.query_type || 'phone',
      selectorValue: row.query_value,
      siteLabel: 'Phone Intelligence',
      profileUrl: '',
      imageUrl: '',
      metadata,
    });
  }

  for (const row of (Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [])) {
    if (!row || typeof row !== 'object') continue;
    const fullName = String(row.full_name || '').trim();
    const location = String(row.location_name || '').trim();
    const jobTitle = String(row.job_title || '').trim();
    const company = String(row.job_company_name || '').trim();
    const linkedin = String(row.linkedin_url || '').trim();
    const workEmail = String(row.professional_email || row.work_email || '').trim();
    const mobile = String(row.mobile_phone || '').trim();
    const metadata = [
      fullName ? { label: 'Name', value: fullName } : null,
      location ? { label: 'Location', value: location } : null,
      (jobTitle || company) ? { label: 'Employment', value: `${jobTitle}${company ? ` @ ${company}` : ''}`.trim() } : null,
      workEmail ? { label: 'Work Email', value: workEmail } : null,
      mobile ? { label: 'Mobile', value: mobile } : null,
    ].filter(Boolean);
    addEntry({
      source: 'People Data Labs',
      selectorType: row.query_type,
      selectorValue: row.query_value,
      siteLabel: 'People Data Labs',
      profileUrl: linkedin,
      imageUrl: row.picture_url || row.avatar_url || '',
      metadata,
    });
  }

  return entries;
}

function setCaseNotesSectionExcluded(sectionKey, excluded) {
  const key = String(sectionKey || '').trim().toLowerCase();
  if (!key) return;
  if (key === 'digital_footprint') {
    for (const level of ['digital_footprint_high', 'digital_footprint_medium', 'digital_footprint_low']) {
      if (excluded) caseNotesExcludedSections.add(level);
      else caseNotesExcludedSections.delete(level);
    }
  } else if (excluded) {
    caseNotesExcludedSections.add(key);
  } else {
    caseNotesExcludedSections.delete(key);
  }
}

function renderCaseNotesSectionVisibility() {
  const panels = document.querySelectorAll('[data-case-notes-section-panel]');
  for (const panel of panels) {
    if (!(panel instanceof HTMLElement)) continue;
    const key = String(panel.getAttribute('data-case-notes-section-panel') || '').trim().toLowerCase();
    if (!key) continue;
    const excluded = key === 'digital_footprint'
      ? (
        caseNotesExcludedSections.has('digital_footprint_high')
        && caseNotesExcludedSections.has('digital_footprint_medium')
        && caseNotesExcludedSections.has('digital_footprint_low')
      )
      : caseNotesExcludedSections.has(key);
    panel.classList.toggle('is-excluded', excluded);
    const button = panel.querySelector('[data-case-notes-section-toggle]');
    if (button instanceof HTMLButtonElement) {
      button.textContent = excluded ? '+' : 'x';
      button.setAttribute('aria-label', `${excluded ? 'Restore' : 'Remove'} ${key.replace(/_/g, ' ')} section from report`);
      button.title = excluded ? 'Restore section to report' : 'Remove section from report';
    }
  }
}

function caseNotesMajorProfiles(profiles) {
  return normalizeKnownProfiles(profiles).filter((profile) => {
    if (!String(profile?.site || '').trim() && !String(profile?.url || '').trim()
      && !String(profile?.image_url || '').trim() && !String(profile?.screenshot_url || '').trim()) {
      return true;
    }
    const siteKey = _siteKeyFromKnownProfile(profile);
    return CASE_NOTES_MAJOR_PROFILE_SITE_KEYS.has(siteKey);
  });
}

function renderCaseNotesFootprintResults() {
  if (!(caseNotesFootprintResults instanceof HTMLElement)) return;
  if (!caseNotesFootprintEntries.length) {
    caseNotesFootprintResults.innerHTML = '<p class="case-notes-footprint-empty">No digital footprint results are currently attached to case notes.</p>';
    return;
  }
  const groups = { high: [], medium: [], low: [] };
  for (const entry of caseNotesFootprintEntries) {
    const level = entry.confidence === 'high' ? 'high' : entry.confidence === 'medium' ? 'medium' : 'low';
    groups[level].push(entry);
  }
  caseNotesFootprintResults.innerHTML = ['high', 'medium', 'low'].map((level) => {
    const items = groups[level];
    const title = `${level.charAt(0).toUpperCase()}${level.slice(1)} Confidence`;
    const body = items.length
      ? items.map((entry) => {
        const excluded = caseNotesExcludedFootprintResultKeys.has(entry.key);
        const selectorType = String(entry.selectorType || '').trim().toLowerCase() || 'default';
        const selectorValue = String(entry.selectorValue || '').trim();
        const profileUrl = String(entry.profileUrl || '').trim();
        const imageUrl = String(entry.imageUrl || '').trim();
        const siteLabel = String(entry.siteLabel || '').trim() || String(entry.source || '').trim() || 'Digital Footprint';
        const evidenceLabel = footprintSelectorEvidenceLabel(selectorType, selectorValue);
        const metadataMarkup = Array.isArray(entry.metadata) && entry.metadata.length
          ? `
            <dl class="case-notes-footprint-metadata">
              ${entry.metadata.map((item) => `
                <div class="case-notes-footprint-metadata-row">
                  <dt>${escapeHtml(item.label)}</dt>
                  <dd>${escapeHtml(item.value)}</dd>
                </div>
              `).join('')}
            </dl>
          `
          : '<p class="case-notes-footprint-summary">No associated metadata captured.</p>';
        return `
          <article class="case-notes-footprint-item${excluded ? ' is-excluded' : ''}">
            <div class="case-notes-footprint-item-head">
              <div class="case-notes-footprint-item-meta">
                <span class="case-notes-footprint-source">${escapeHtml(entry.source)}</span>
              </div>
              <button class="secondary-btn case-notes-footprint-toggle" type="button" data-case-notes-footprint-key="${escapeAttr(entry.key)}">${excluded ? 'Restore' : 'Remove'}</button>
            </div>
            <div class="case-notes-footprint-evidence">
              <div class="case-notes-footprint-media">
                ${imageUrl
                  ? `<img class="case-notes-footprint-avatar" src="${escapeAttr(imageUrl)}" alt="${escapeAttr(siteLabel)} profile image" loading="lazy" referrerpolicy="no-referrer" />`
                  : '<div class="case-notes-footprint-avatar case-notes-footprint-avatar-placeholder">No image</div>'}
              </div>
              <div class="case-notes-footprint-body">
                <div class="case-notes-footprint-site-row">
                  <div class="case-notes-footprint-site">
                    ${faviconMarkup(siteLabel, profileUrl || siteLabel)}
                    <span class="case-notes-footprint-site-name">${escapeHtml(siteLabel)}</span>
                  </div>
                  ${selectorConfidenceBadgeMarkup(selectorType, selectorValue, { compact: true, scopeId: `case_notes|${entry.key}` })}
                </div>
                ${profileUrl ? `<div class="case-notes-footprint-url"><a href="${escapeAttr(profileUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(profileUrl)}</a></div>` : '<div class="case-notes-footprint-url case-notes-footprint-url-empty">No profile URL captured</div>'}
                <div class="case-notes-footprint-selector case-notes-footprint-selector-${escapeAttr(selectorTypeColorToken(selectorType))}">
                  <span class="case-notes-footprint-selector-type">${escapeHtml(selectorTypeDisplayLabel(selectorType))}</span>
                  <span class="case-notes-footprint-selector-value">${escapeHtml(evidenceLabel)}</span>
                </div>
                ${metadataMarkup}
              </div>
            </div>
          </article>
        `;
      }).join('')
      : '<p class="case-notes-footprint-empty">No results.</p>';
    return `
      <section class="case-notes-footprint-group case-notes-footprint-group-${escapeAttr(level)}">
        <h4>${escapeHtml(title)} <span>${items.length}</span></h4>
        <div class="case-notes-footprint-group-items">${body}</div>
      </section>
    `;
  }).join('');
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
  const knownProfiles = caseNotesMajorProfiles(notes.known_profiles).filter((profile) => String(profile?.url || '').trim());
  const snapshot = normalizeReconSnapshot(notes.recon_snapshot);
  if (snapshot && applyReconSnapshot(snapshot)) {
    if (footprintReconStatus) {
      const payload = snapshot.payload || {};
      footprintReconStatus.textContent = `Loaded saved recon snapshot: ${Number(payload.present_count) || 0} account match(es) across ${Number(payload.checked) || 0} checks.`;
    }
    return;
  }
  reconSnapshotCache = null;
  if (!knownProfiles.length) {
    latestReconPayload = emptyReconPayload();
    clearHiddenReconEntities();
    applyReconPayload(latestReconPayload, { statusPrefix: 'Recon ready' });
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

  const collectionReadyProfiles = dedupeRowsByProfileUrl(results.filter((row) => row.supported_for_collection && String(row.profile_url || '').trim()));
  const unsupportedProfilesWithUrl = dedupeRowsByProfileUrl(results.filter((row) => !row.supported_for_collection && String(row.profile_url || '').trim()));
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

  const payload = {
    results,
    selectors: [],
    collection_targets: Array.from(targetMap.values()),
    leads: unsupportedProfilesWithUrl.map((row) => ({
      site: row.site,
      profile_url: row.profile_url,
      screenshot_url: row.screenshot_url,
      source: 'seed',
    })),
    checked: results.length,
    present_count: results.length,
    collection_ready_profiles: collectionReadyProfiles,
    unsupported_profiles_with_url: unsupportedProfilesWithUrl,
    known_present_without_url: knownPresentWithoutUrl,
    osint_profiles: [],
    osint_spec_results: [],
    numverify_profiles: [],
    person_data_profile: {},
    person_data_profiles: [],
  };
  clearHiddenReconEntities();
  applyReconPayload(payload, { statusPrefix: 'Seeded recon loaded' });
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

function cloneJsonSafe(value, fallback = null) {
  try {
    return JSON.parse(JSON.stringify(value));
  } catch (error) {
    return fallback;
  }
}

function normalizeReconSnapshot(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const payloadRaw = raw.payload && typeof raw.payload === 'object' ? raw.payload : {};
  return {
    version: Number(raw.version) || 1,
    saved_at: String(raw.saved_at || '').trim(),
    payload: {
      selectors: Array.isArray(payloadRaw.selectors) ? payloadRaw.selectors : [],
      results: Array.isArray(payloadRaw.results) ? payloadRaw.results : [],
      checked: Number(payloadRaw.checked) || 0,
      present_count: Number(payloadRaw.present_count) || 0,
      collection_targets: Array.isArray(payloadRaw.collection_targets) ? payloadRaw.collection_targets : [],
      leads: Array.isArray(payloadRaw.leads) ? payloadRaw.leads : [],
      collection_ready_profiles: Array.isArray(payloadRaw.collection_ready_profiles) ? payloadRaw.collection_ready_profiles : [],
      unsupported_profiles_with_url: Array.isArray(payloadRaw.unsupported_profiles_with_url) ? payloadRaw.unsupported_profiles_with_url : [],
      known_present_without_url: Array.isArray(payloadRaw.known_present_without_url) ? payloadRaw.known_present_without_url : [],
      person_data_profile: payloadRaw.person_data_profile && typeof payloadRaw.person_data_profile === 'object' ? payloadRaw.person_data_profile : {},
      person_data_profiles: Array.isArray(payloadRaw.person_data_profiles) ? payloadRaw.person_data_profiles : [],
      osint_profiles: Array.isArray(payloadRaw.osint_profiles) ? payloadRaw.osint_profiles : [],
      osint_spec_results: Array.isArray(payloadRaw.osint_spec_results) ? payloadRaw.osint_spec_results : [],
      numverify_profiles: Array.isArray(payloadRaw.numverify_profiles) ? payloadRaw.numverify_profiles : [],
      api_modules_queried: Array.isArray(payloadRaw.api_modules_queried) ? payloadRaw.api_modules_queried : [],
    },
  };
}

function buildReconSnapshotFromPayload(payload) {
  const normalized = normalizeReconSnapshot({
    version: 1,
    saved_at: new Date().toISOString(),
    payload: cloneJsonSafe(payload, {}),
  });
  return normalized;
}

function applyReconSnapshot(snapshot) {
  const normalized = normalizeReconSnapshot(snapshot);
  if (!normalized) return false;
  const payload = normalized.payload;
  reconSnapshotCache = normalized;
  latestReconPayload = payload;
  clearHiddenReconEntities();
  applyReconPayload(payload, { statusPrefix: 'Recon snapshot loaded' });
  return true;
}

function setReconSnapshotFromPayload(payload) {
  const snapshot = buildReconSnapshotFromPayload(payload);
  if (!snapshot) return;
  reconSnapshotCache = snapshot;
  if (!activeCase || typeof activeCase !== 'object') return;
  const existingNotes = normalizeCaseNotesObject(activeCase.case_notes || {});
  activeCase.case_notes = {
    ...existingNotes,
    recon_snapshot: snapshot,
  };
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

function profileKeySetForKnownProfiles(profiles) {
  const keys = new Set();
  for (const item of normalizeKnownProfiles(profiles)) {
    keys.add(normalizeProfileKey(item.site, item.url));
  }
  return keys;
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
  const inferredSiteKey = _siteKeyFromKnownProfile(safe);
  const site = CASE_NOTES_MAJOR_PROFILE_SITE_KEYS.has(inferredSiteKey) ? inferredSiteKey : '';
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
              <span>Platform</span>
              <select class="case-notes-profile-site">
                <option value="">Select platform</option>
                <option value="facebook"${site === 'facebook' ? ' selected' : ''}>Facebook</option>
                <option value="instagram"${site === 'instagram' ? ' selected' : ''}>Instagram</option>
                <option value="tiktok"${site === 'tiktok' ? ' selected' : ''}>TikTok</option>
              </select>
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
  caseNotesKnownProfiles = caseNotesMajorProfiles(caseNotesKnownProfiles);
  if (!caseNotesKnownProfiles.length) {
    caseNotesProfilesList.innerHTML = '<div class="empty">No major profiles yet. Add Facebook, Instagram, or TikTok profiles, or run recon.</div>';
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
      site: site instanceof HTMLInputElement || site instanceof HTMLSelectElement ? String(site.value || '').trim() : '',
      url: url instanceof HTMLInputElement ? String(url.value || '').trim() : '',
      image_url: selectedImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(selectedImage),
      screenshot_url: screenshot,
    };
  }).filter((profile) => CASE_NOTES_MAJOR_PROFILE_SITE_KEYS.has(_siteKeyFromKnownProfile(profile)));
}

async function openCaseNotesModal() {
  if (!activeCaseId || !activeCase) {
    showNotification('Open a case first.', 'warn');
    return;
  }
  const notes = normalizeCaseNotesObject(activeCase.case_notes || {});
  const reportPreferences = normalizeCaseNotesReportPreferences(notes.report_preferences);
  caseNotesExcludedSections.clear();
  for (const key of reportPreferences.excluded_sections) caseNotesExcludedSections.add(key);
  caseNotesExcludedFootprintResultKeys.clear();
  for (const key of reportPreferences.excluded_footprint_result_keys) caseNotesExcludedFootprintResultKeys.add(key);
  caseNotesFootprintEntries = buildCaseNotesFootprintEntries(notes);
  const posts = await fetchCasePosts(activeCaseId);
  const associatedImages = uniqueProfileImageUrls(posts);
  const casePoiImage = normalizeProfileImageUrl(activeCase?.poi_image_url);
  const notesSubjectImage = normalizeProfileImageUrl(notes.subject_image_url);
  const notesKnownProfiles = caseNotesMajorProfiles(notes.known_profiles);
  const discoveredFromRecon = defaultKnownProfilesFromRecon();
  const discoveredFromPosts = discoverKnownProfilesFromPosts(posts);
  const discoveredKnownProfiles = mergeDiscoveredKnownProfiles(discoveredFromRecon, discoveredFromPosts);
  const knownProfiles = notesKnownProfiles.length ? mergeDiscoveredKnownProfiles(notesKnownProfiles, discoveredKnownProfiles) : discoveredKnownProfiles;
  caseNotesKnownProfiles = enrichKnownProfilesWithExtractedImages(knownProfiles, posts);
  caseNotesAutoProfileKeys.clear();
  for (const key of profileKeySetForKnownProfiles(discoveredKnownProfiles)) caseNotesAutoProfileKeys.add(key);
  const knownProfileImages = caseNotesKnownProfiles.map((item) => normalizeProfileImageUrl(item.image_url)).filter(Boolean);
  caseNotesImageChoices = [...new Set([USER_PLACEHOLDER_AVATAR_URL, casePoiImage, notesSubjectImage, ...associatedImages, ...knownProfileImages].filter(Boolean))];

  const discoveredName = firstProfileNameCandidate(posts, caseNotesKnownProfiles);
  const likelyName = calculatedLikelyNameForCaseNotes();
  if (caseNotesNameInput) {
    if (String(notes.name || '').trim()) {
      caseNotesNameInput.value = String(notes.name || '').trim();
      lastAutofilledCaseNotesName = '';
      caseNotesNameInput.classList.remove('case-notes-name-autofill');
    } else if (likelyName) {
      caseNotesNameInput.value = likelyName;
      lastAutofilledCaseNotesName = likelyName;
      caseNotesNameInput.classList.add('case-notes-name-autofill');
    } else {
      caseNotesNameInput.value = String(discoveredName || activeCase.case_name || '').trim();
      lastAutofilledCaseNotesName = '';
      caseNotesNameInput.classList.remove('case-notes-name-autofill');
    }
  }
  const notesLocation = String(notes.location || '').trim();
  const caseKnownLocation = String(activeCase.known_location || '').trim();
  const hasUsableKnownLocation = caseKnownLocation && !/^(?:unknown|n\/a|none)$/i.test(caseKnownLocation);
  const inferredLikelyLocation = inferMostLikelyLocationForCaseNotes(posts);
  if (caseNotesLocationInput) {
    const selectedLocation = String(notesLocation || inferredLikelyLocation || (hasUsableKnownLocation ? caseKnownLocation : '') || '').trim();
    caseNotesLocationInput.value = selectedLocation;
    lastAutofilledCaseNotesLocation = notesLocation ? '' : selectedLocation;
  }
  if (caseNotesAgeInput) caseNotesAgeInput.value = String(notes.age || '').trim();
  if (caseNotesAkasInput) caseNotesAkasInput.value = String(notes.akas || '').trim();
  if (caseNotesContextInput) caseNotesContextInput.value = String(notes.context || '').trim();
  if (caseNotesThreatInput) caseNotesThreatInput.value = String(notes.threat_risk_assessment || '').trim();
  if (caseNotesPersonalInput) caseNotesPersonalInput.value = String(notes.personal_details || '').trim();
  const inferredSelectors = inferSelectorValuesFromCaseNotes(notes);
  if (caseNotesSelectorEmailsInput) {
    const saved = splitCommaSeparatedValues(notes.selector_emails);
    caseNotesSelectorEmailsInput.value = joinCommaSeparatedValues([...saved, ...inferredSelectors.emails]);
  }
  if (caseNotesSelectorPhonesInput) {
    const saved = splitCommaSeparatedValues(notes.selector_phone_numbers);
    caseNotesSelectorPhonesInput.value = joinCommaSeparatedValues([...saved, ...inferredSelectors.phones]);
  }
  if (caseNotesSelectorUsernamesInput) {
    const saved = splitCommaSeparatedValues(notes.selector_usernames);
    caseNotesSelectorUsernamesInput.value = joinCommaSeparatedValues([...saved, ...inferredSelectors.usernames]);
  }

  const selectedSubject = notesSubjectImage || casePoiImage || knownProfileImages[0] || associatedImages[0] || USER_PLACEHOLDER_AVATAR_URL;
  renderCaseNotesSubjectImageOptions(selectedSubject);
  renderCaseNotesSubjectImagePreview(selectedSubject);
  renderCaseNotesProfiles();
  renderCaseNotesSectionVisibility();
  renderCaseNotesFootprintResults();
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
  const selectorEmails = joinCommaSeparatedValues(splitCommaSeparatedValues(caseNotesSelectorEmailsInput?.value));
  const selectorPhones = joinCommaSeparatedValues(splitCommaSeparatedValues(caseNotesSelectorPhonesInput?.value));
  const selectorUsernames = joinCommaSeparatedValues(splitCommaSeparatedValues(caseNotesSelectorUsernamesInput?.value));
  const subjectImage = String(caseNotesSubjectImageSelect?.value || '').trim();
  const normalizedSubjectImage = subjectImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(subjectImage);
  const sanitizedProfiles = caseNotesMajorProfiles(caseNotesKnownProfiles)
    .map((profile) => ({
      site: String(profile.site || '').trim(),
      url: String(profile.url || '').trim(),
      image_url: normalizeProfileImageUrl(profile.image_url),
      screenshot_url: String(profile.screenshot_url || '').trim(),
    }))
    .filter((profile) => profile.site || profile.url || profile.image_url || profile.screenshot_url);
  const notes = {
    ...normalizeCaseNotesObject(activeCase?.case_notes || {}),
    name,
    location,
    age,
    akas,
    subject_image_url: normalizedSubjectImage,
    context,
    threat_risk_assessment: threatRisk,
    personal_details: personal,
    selector_emails: selectorEmails,
    selector_phone_numbers: selectorPhones,
    selector_usernames: selectorUsernames,
    known_profiles: sanitizedProfiles,
    report_preferences: {
      excluded_sections: Array.from(caseNotesExcludedSections.values()),
      excluded_footprint_result_keys: Array.from(caseNotesExcludedFootprintResultKeys.values()),
    },
    recon_snapshot: reconSnapshotCache || normalizeReconSnapshot(activeCase?.case_notes?.recon_snapshot),
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
  if (!id) {
    showNotification('Cannot save: no active case selected.', 'error');
    return;
  }
  const nextName = String(caseSaveTitleInput?.value || '').trim();
  const nextStatus = String(caseSaveStatusSelect?.value || '').trim();
  const nextCadence = String(caseSaveCadenceSelect?.value || '').trim();
  const nextThreat = String(caseSaveThreatSelect?.value || '').trim();
  const nextRetention = normalizeDataRetentionPeriod(caseSaveRetentionSelect?.value);
  const nextLocation = String(caseSaveLocationInput?.value || 'Unknown').trim() || 'Unknown';
  const selectedInput = caseSaveForm?.querySelector('input[name="caseSavePoiImage"]:checked');
  const selectedImage = selectedInput instanceof HTMLInputElement ? String(selectedInput.value || '').trim() : '';
  const nextPoiImage = selectedImage === USER_PLACEHOLDER_AVATAR_URL ? '' : normalizeProfileImageUrl(selectedImage);
  const existingNotes = normalizeCaseNotesObject(activeCase?.case_notes || {});
  const existingKnownProfiles = normalizeKnownProfiles(existingNotes.known_profiles);
  const discoveredFromRecon = defaultKnownProfilesFromRecon();
  const discoveredFromPosts = discoverKnownProfilesFromPosts(Array.isArray(latestFetchedPosts) ? latestFetchedPosts : latestPosts);
  const discoveredKnownProfiles = mergeDiscoveredKnownProfiles(discoveredFromRecon, discoveredFromPosts);
  const mergedKnownProfiles = mergeDiscoveredKnownProfiles(existingKnownProfiles, discoveredKnownProfiles);
  const notes = {
    ...existingNotes,
    name: String(existingNotes.name || nextName || '').trim(),
    location: String(nextLocation || existingNotes.location || '').trim(),
    subject_image_url: nextPoiImage,
    known_profiles: mergedKnownProfiles,
    recon_snapshot: reconSnapshotCache || normalizeReconSnapshot(existingNotes.recon_snapshot),
  };
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
        data_retention_period: nextRetention,
        known_location: nextLocation,
        poi_image_url: nextPoiImage,
        case_notes: notes,
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
        data_retention_period: normalizeDataRetentionPeriod(defaultDataRetentionPeriod),
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
  const referenced = String(post?.referenced_username || metadata.quote_username || '').trim();
  const quoteText = inferQuotedText(post);
  if (!quoteText) return '';
  const quoteUrl = String(metadata.quote_url || post?.source_url || '').trim();
  return `
    <blockquote class="quote-nest">
      <div class="quote-meta">${referenced ? `Quoted from @${escapeHtml(referenced)}` : 'Quoted'}</div>
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

function sourceTypeFilterState() {
  const sourceMap = new Map([
    ['twitter', Boolean(filterTwitter?.checked)],
    ['reddit', Boolean(filterReddit?.checked)],
    ['tiktok', Boolean(filterTiktok?.checked)],
    ['bluesky', Boolean(filterBluesky?.checked)],
    ['instagram', Boolean(filterInstagram?.checked)],
    ['youtube', Boolean(filterYoutube?.checked)],
  ]);
  const typeMap = new Map([
    ['post', Boolean(filterPost?.checked)],
    ['repost', Boolean(filterRepost?.checked)],
    ['reply', Boolean(filterReply?.checked)],
    ['quote', Boolean(filterQuote?.checked)],
    ['comment', Boolean(filterComment?.checked)],
  ]);
  return { sourceMap, typeMap };
}

function applySourceAndTypeFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  const state = sourceTypeFilterState();
  return rows.filter((post) => {
    const source = normalizePlatformName(post?.platform);
    if (source && state.sourceMap.has(source) && !state.sourceMap.get(source)) return false;
    const kind = String(post?.post_type || 'post').trim().toLowerCase();
    if (kind && state.typeMap.has(kind) && !state.typeMap.get(kind)) return false;
    return true;
  });
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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

function applyEntityTagFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activeEntityFilters.size) return rows;
  return rows.filter((post) => {
    const tags = Array.isArray(post?.tags) ? post.tags : [];
    const lowered = new Set(tags.map((item) => String(item || '').trim().toLowerCase()).filter(Boolean));
    for (const tag of activeEntityFilters) {
      if (!lowered.has(tag)) return false;
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

let _dashboardFilterCache = { rows: null, key: '', output: [] };

function dashboardFilterCacheKey() {
  const sourceType = sourceTypeFilterState();
  const sourceBits = Array.from(sourceType.sourceMap.entries()).map(([name, enabled]) => `${name}:${enabled ? 1 : 0}`).join('|');
  const postTypeBits = Array.from(sourceType.typeMap.entries()).map(([name, enabled]) => `${name}:${enabled ? 1 : 0}`).join('|');
  const signalBits = [
    filterSelectors?.checked ? 1 : 0,
    filterIdeologicalIndicators?.checked ? 1 : 0,
    filterThreatSignals?.checked ? 1 : 0,
    filterLLMPrimary?.checked ? 1 : 0,
    filterLLMSecondary?.checked ? 1 : 0,
  ].join('');
  const setKey = (values) => Array.from(values).sort().join(',');
  return [
    sourceBits,
    postTypeBits,
    signalBits,
    setKey(activeEntityFilters),
    setKey(activeMixFilters),
    setKey(activeSignalFilters),
    setKey(activeCustomKeywordFilters),
    setKey(activeFaceFilters),
    activeFaceMinConfidence.toFixed(2),
  ].join('||');
}

function applyDashboardFilters(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  const key = dashboardFilterCacheKey();
  if (_dashboardFilterCache.rows === rows && _dashboardFilterCache.key === key) {
    return _dashboardFilterCache.output;
  }
  const output = applyFaceFilters(
    applyCustomKeywordFilters(
      applySignalTagFilters(
        applyMixFilters(
          applyEntityTagFilters(
            applySignalTypeFilter(
              applySourceAndTypeFilters(rows),
            ),
          ),
        ),
      ),
    ),
  );
  _dashboardFilterCache = { rows, key, output };
  return output;
}

function rerenderFromCurrentFilters() {
  const filteredPosts = applyDashboardFilters(latestFetchedPosts);
  renderPosts(filteredPosts);
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
          color: 'rgba(217, 119, 6, 0.9)',
          weight: 1,
          fillColor: 'rgba(245, 158, 11, 0.2)',
          fillOpacity: 0.56,
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
      updatePatternLifeMapViewport(latestPatternLifeMapPoints, latestPatternLifeMapRoutes);
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
    if (name && _hasUsableGeoPoint(lat, lon)) {
      addMention(name, lat, lon);
      continue;
    }
    if (!name) continue;
    const selected = _selectMostSpecificLocationMatch(name, _resolvedLocationsFromText(name, locationPairsByName));
    if (selected) {
      addMention(selected.name, selected.lat, selected.lon);
      continue;
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

function _normalizeLocationProbeText(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[_\u2013\u2014-]+/g, ' ')
    .replace(/[()[\]{}]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function _locationFromCountryCode(rawCode) {
  const code = String(rawCode || '').trim().toLowerCase();
  if (!code) return null;
  const tag = COUNTRY_CODE_TO_LOCATION_TAG[code];
  if (!tag) return null;
  return LOCATION_COORDS_BY_TAG[tag] || null;
}

function _locationCandidateFragments(text) {
  const normalized = _normalizeLocationProbeText(text);
  if (!normalized) return [];
  const seen = new Set();
  const out = [];
  const pushCandidate = (candidate) => {
    const clean = _normalizeLocationProbeText(candidate)
      .replace(/^(?:biolocation|bio location|location|loc|city|state|province|region|country)\s*[:=]?\s*/i, '')
      .replace(/\s+(?:country|region|province|state|city)\s*$/i, '')
      .trim();
    if (!clean || seen.has(clean)) return;
    seen.add(clean);
    out.push(clean);
  };
  pushCandidate(normalized);
  for (const part of normalized.split(/[|/;,]+/g)) pushCandidate(part);
  for (const part of normalized.split(/\s+(?:or|and)\s+/g)) pushCandidate(part);
  return out;
}

function _resolvedLocationsFromText(text, pairs) {
  const normalized = _normalizeLocationProbeText(text);
  if (!normalized) return [];
  const hits = [];
  const seen = new Set();
  for (const probe of _locationCandidateFragments(normalized)) {
    const aliasTag = LOCATION_ALIAS_TO_TAG[probe];
    const aliasLocation = aliasTag ? LOCATION_COORDS_BY_TAG[aliasTag] : null;
    if (aliasLocation) {
      const aliasName = String(aliasLocation.name || '').trim().toLowerCase();
      if (aliasName && !seen.has(aliasName)) {
        seen.add(aliasName);
        hits.push(aliasLocation);
      }
    }
    const countryLocation = _locationFromCountryCode(probe);
    if (!countryLocation) continue;
    const countryName = String(countryLocation.name || '').trim().toLowerCase();
    if (!countryName || seen.has(countryName)) continue;
    seen.add(countryName);
    hits.push(countryLocation);
  }
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

function _locationHierarchyLevel(location) {
  const name = String(location?.name || '').trim().toLowerCase();
  if (!name) return 0;
  const countryNames = new Set(['united states', 'canada', 'ukraine', 'israel', 'palestine']);
  const regionNames = new Set(['washington', 'texas', 'california', 'florida', 'nova scotia', 'gaza']);
  if (countryNames.has(name)) return 1;
  if (regionNames.has(name)) return 2;
  return 3;
}

function _selectMostSpecificLocationMatch(rawText, matches) {
  if (!Array.isArray(matches) || !matches.length) return null;
  const fragments = _locationCandidateFragments(rawText);
  const uniqueMatches = [];
  const seenNames = new Set();
  for (const row of matches) {
    const name = String(row?.name || '').trim().toLowerCase();
    if (!name || seenNames.has(name)) continue;
    seenNames.add(name);
    uniqueMatches.push(row);
  }
  for (const fragment of fragments) {
    const hit = uniqueMatches.find((row) => String(row?.name || '').trim().toLowerCase() === fragment);
    if (hit) return hit;
  }
  const ranked = uniqueMatches.slice().sort((a, b) => {
    const aName = String(a?.name || '').trim().toLowerCase();
    const bName = String(b?.name || '').trim().toLowerCase();
    const hierarchyDelta = _locationHierarchyLevel(b) - _locationHierarchyLevel(a);
    if (hierarchyDelta !== 0) return hierarchyDelta;
    const aWords = aName ? aName.split(/\s+/g).length : 0;
    const bWords = bName ? bName.split(/\s+/g).length : 0;
    if (aWords !== bWords) return bWords - aWords;
    return bName.length - aName.length;
  });
  return ranked[0] || null;
}

function _hasUsableGeoPoint(lat, lon) {
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return false;
  if (lat < -90 || lat > 90 || lon < -180 || lon > 180) return false;
  // Reject Null Island defaults often returned by weak profile enrichments.
  if (Math.abs(lat) < 0.000001 && Math.abs(lon) < 0.000001) return false;
  return true;
}

function _primaryLocationLabel(locationName, fallbackLabel = 'Unknown') {
  const clean = String(locationName || '').trim();
  if (!clean) return fallbackLabel;
  return clean;
}

function _cleanLocationEntityLabel(value) {
  const clean = String(value || '')
    .trim()
    .replace(/^(?:biolocation|bio location|location|loc|city|state|province|region|country)\s*[:=]?\s*/i, '')
    .replace(/\s+/g, ' ')
    .trim();
  return clean;
}

function collectPatternOfLifeLocationPoints(posts) {
  const locationPairsByName = _locationPairsByName();
  const AMBIGUOUS_LOCATION_TOKENS = new Set([
    'washington',
    'georgia',
    'victoria',
    'queens',
    'hamilton',
  ]);
  const pointsByKey = new Map();
  const routesByKey = new Map();
  const kindKey = (kind) => {
    const normalized = String(kind || '').trim().toLowerCase();
    if (normalized === 'post' || normalized === 'post_ner' || normalized === 'post_text') return 'post';
    if (normalized === 'osint_industries_route') return 'osint_industries';
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
        const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}|${reference.profileUrl || ''}`;
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
      const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}|${reference.profileUrl || ''}`;
      refKeys.add(refKey);
      references.push(reference);
    }
    pointsByKey.set(key, { name, lat, lon, count: 1, references, refKeys, sourceCounts });
  };
  const addRoute = (name, coordinates, reference = null) => {
    const points = Array.isArray(coordinates)
      ? coordinates
        .map((item) => {
          const lat = Number(item?.lat);
          const lon = Number(item?.lon);
          if (Number.isNaN(lat) || Number.isNaN(lon)) return null;
          return { lat, lon };
        })
        .filter(Boolean)
      : [];
    if (points.length < 2) return;
    const start = points[0];
    const end = points[points.length - 1];
    const key = `${name}|${start.lat.toFixed(4)}|${start.lon.toFixed(4)}|${end.lat.toFixed(4)}|${end.lon.toFixed(4)}|${points.length}`;
    const existing = routesByKey.get(key);
    if (existing) {
      existing.count += 1;
      const sourceKind = kindKey(reference?.kind);
      existing.sourceCounts.set(sourceKind, (existing.sourceCounts.get(sourceKind) || 0) + 1);
      if (reference && existing.refKeys.size < 24) {
        const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}|${reference.profileUrl || ''}`;
        if (!existing.refKeys.has(refKey)) {
          existing.refKeys.add(refKey);
          existing.references.push(reference);
        }
      }
      return;
    }
    const center = points[Math.floor(points.length / 2)] || start;
    const references = [];
    const refKeys = new Set();
    const sourceCounts = new Map();
    const sourceKind = kindKey(reference?.kind);
    sourceCounts.set(sourceKind, 1);
    if (reference) {
      const refKey = `${reference.kind || 'source'}|${reference.label || ''}|${reference.postIndex ?? ''}|${reference.detail || ''}|${reference.profileUrl || ''}`;
      refKeys.add(refKey);
      references.push(reference);
    }
    routesByKey.set(key, {
      name: String(name || 'Route').trim() || 'Route',
      coordinates: points.slice(0, 1000),
      count: 1,
      lat: Number(center?.lat),
      lon: Number(center?.lon),
      references,
      refKeys,
      sourceCounts,
    });
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

  const addFromTextSource = (rawText, label, detail, kind, profileUrl = '', options = {}) => {
    const strict = Boolean(options?.strict);
    const preferMostSpecific = Boolean(options?.preferMostSpecific);
    const matches = _resolvedLocationsFromText(rawText, locationPairsByName);
    if (preferMostSpecific && matches.length) {
      const selected = _selectMostSpecificLocationMatch(rawText, matches);
      if (selected) {
        const locationName = String(selected?.name || '').trim().toLowerCase();
        if (!(strict && AMBIGUOUS_LOCATION_TOKENS.has(locationName))) {
          addPoint(selected.name, selected.lat, selected.lon, {
            kind,
            label,
            detail: String(detail || '').trim(),
            profileUrl: String(profileUrl || '').trim(),
          });
          return;
        }
      }
    }
    for (const location of matches) {
      const locationName = String(location?.name || '').trim().toLowerCase();
      if (strict && AMBIGUOUS_LOCATION_TOKENS.has(locationName)) continue;
      addPoint(location.name, location.lat, location.lon, {
        kind,
        label,
        detail: String(detail || '').trim(),
        profileUrl: String(profileUrl || '').trim(),
      });
    }
  };
  const extractCoordinateSignals = (value, maxDepth = 6) => {
    const found = [];
    const seen = new Set();
    const walk = (node, path = '', depth = 0) => {
      if (depth > maxDepth || node === null || node === undefined) return;
      if (Array.isArray(node)) {
        for (let i = 0; i < Math.min(node.length, 160); i += 1) {
          walk(node[i], `${path}[${i}]`, depth + 1);
        }
        return;
      }
      if (typeof node !== 'object') return;
      const entries = Object.entries(node);
      const lowered = new Map(entries.map(([key, raw]) => [String(key || '').trim().toLowerCase(), raw]));
      const latKeys = Array.from(lowered.keys()).filter((key) => key === 'lat' || key === 'latitude' || key.endsWith('_lat') || key.endsWith('_latitude') || key.includes('latitude'));
      const lonKeys = Array.from(lowered.keys()).filter((key) => key === 'lon' || key === 'lng' || key === 'longitude' || key.endsWith('_lon') || key.endsWith('_lng') || key.endsWith('_longitude') || key.includes('longitude'));
      const parseNum = (input) => {
        if (typeof input === 'number' && Number.isFinite(input)) return Number(input);
        const text = String(input || '').trim();
        if (!text) return Number.NaN;
        const parsed = Number(text);
        return Number.isFinite(parsed) ? parsed : Number.NaN;
      };
      for (const latKey of latKeys) {
        const lat = parseNum(lowered.get(latKey));
        for (const lonKey of lonKeys) {
          const lon = parseNum(lowered.get(lonKey));
          if (Number.isNaN(lat) || Number.isNaN(lon)) continue;
          let mappedLat = lat;
          let mappedLon = lon;
          if (!(mappedLat >= -90 && mappedLat <= 90 && mappedLon >= -180 && mappedLon <= 180)) {
            if (mappedLon >= -90 && mappedLon <= 90 && mappedLat >= -180 && mappedLat <= 180) {
              mappedLat = lon;
              mappedLon = lat;
            } else {
              continue;
            }
          }
          const dedupe = `${mappedLat.toFixed(6)}|${mappedLon.toFixed(6)}`;
          if (seen.has(dedupe)) continue;
          seen.add(dedupe);
          const label = _cleanLocationEntityLabel(node?.name || node?.title || node?.location || node?.address || '');
          const detail = String(node?.bio || node?.review || node?.review_text || node?.description || '').trim();
          found.push({
            path,
            label,
            detail,
            lat: mappedLat,
            lon: mappedLon,
          });
        }
      }
      for (const [key, child] of entries) {
        const nextPath = path ? `${path}.${key}` : String(key || '');
        walk(child, nextPath, depth + 1);
      }
    };
    walk(value);
    return found;
  };
  const pdlProfileUrl = (profile) => {
    const candidateList = [];
    if (Array.isArray(profile?.profile_urls)) candidateList.push(...profile.profile_urls);
    candidateList.push(profile?.linkedin_url, profile?.facebook_url, profile?.twitter_url, profile?.github_url);
    for (const candidate of candidateList) {
      const clean = String(candidate || '').trim();
      if (clean) return clean;
    }
    return '';
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
    const profileUrl = pdlProfileUrl(profile);
    const label = `PDL: ${String(profile?.full_name || profile?.query_value || 'profile').trim() || 'profile'}`;
    const detail = `primary location: ${locName || 'unknown'}`;
    const countryCode = String(profile?.location_country_code || profile?.country_code || '').trim().toLowerCase();
    const countryName = String(profile?.location_country || profile?.country || '').trim();
    const lat = Number(profile?.location_latitude);
    const lon = Number(profile?.location_longitude);
    if (_hasUsableGeoPoint(lat, lon)) {
      addPoint(locName || 'PDL location', lat, lon, { kind: 'pdl', label, detail, profileUrl });
    } else if (locName) {
      // Strict mode avoids low-confidence text-to-city fallbacks for ambiguous labels.
      addFromTextSource(locName, label, detail, 'pdl', profileUrl, { strict: true, preferMostSpecific: true });
    }
    if (countryCode) {
      addFromTextSource(countryCode, label, `country_code: ${countryCode}`, 'pdl', profileUrl, { strict: true, preferMostSpecific: true });
    }
    if (countryName) {
      addFromTextSource(countryName, label, `country: ${countryName}`, 'pdl', profileUrl, { strict: true, preferMostSpecific: true });
    }
    for (const geo of extractCoordinateSignals(profile)) {
      if (!_hasUsableGeoPoint(geo.lat, geo.lon)) continue;
      addPoint(geo.label || locName || 'PDL location', geo.lat, geo.lon, {
        kind: 'pdl',
        label,
        detail: `${geo.path || 'geo'}${geo.detail ? ` • ${geo.detail}` : ''}`,
        profileUrl,
      });
    }
  }

  const osintProfiles = Array.isArray(reconOsintProfiles) ? reconOsintProfiles : [];
  for (const profile of osintProfiles) {
    const title = String(profile?.title || profile?.name || profile?.username || 'profile').trim();
    const profileUrl = String(profile?.profile_url || profile?.website || '').trim();
    const location = _cleanLocationEntityLabel(profile?.location || '');
    const biolocation = _cleanLocationEntityLabel(profile?.biolocation || '');
    const bio = String(profile?.bio || '').trim();
    const geoSignals = Array.isArray(profile?.geo_signals) ? profile.geo_signals : [];
    for (const signal of geoSignals) {
      const kind = String(signal?.kind || '').trim().toLowerCase();
      const path = String(signal?.path || '').trim();
      const signalLabel = _cleanLocationEntityLabel(signal?.label || '');
      const detailText = String(signal?.detail || '').trim();
      const detailParts = [];
      if (signalLabel) detailParts.push(signalLabel);
      if (path) detailParts.push(path);
      if (detailText) detailParts.push(detailText);
      const detail = detailParts.join(' • ').slice(0, 260);
      if (kind === 'point') {
        const lat = Number(signal?.lat);
        const lon = Number(signal?.lon);
        if (Number.isNaN(lat) || Number.isNaN(lon)) continue;
        const pointName = _cleanLocationEntityLabel(signalLabel || title || 'OSINT location') || 'OSINT location';
        addPoint(pointName, lat, lon, {
          kind: 'osint_industries',
          label: `OSINT Industries: ${title}`,
          detail,
          profileUrl,
        });
      } else if (kind === 'polyline') {
        const coords = Array.isArray(signal?.coordinates) ? signal.coordinates : [];
        addRoute(_cleanLocationEntityLabel(signalLabel || `${title} route`) || `${title} route`, coords, {
          kind: 'osint_industries_route',
          label: `OSINT Industries: ${title}`,
          detail: detail || 'route geometry',
          profileUrl,
        });
      }
    }
    if (location) {
      addFromTextSource(location, `OSINT Industries: ${title}`, `location: ${location}`, 'osint_industries', profileUrl, { strict: true, preferMostSpecific: true });
    }
    if (biolocation) {
      addFromTextSource(biolocation, `OSINT Industries: ${title}`, `biolocation: ${biolocation}`, 'osint_industries', profileUrl, { strict: true, preferMostSpecific: true });
    }
    if (bio) {
      addFromTextSource(bio, `OSINT Industries: ${title}`, `bio: ${bio.slice(0, 180)}`, 'osint_industries', profileUrl);
    }
    for (const geo of extractCoordinateSignals(profile?.parsed_values || profile?.spec_format || profile)) {
      addPoint(geo.label || title || 'OSINT location', geo.lat, geo.lon, {
        kind: 'osint_industries',
        label: `OSINT Industries: ${title}`,
        detail: `${geo.path || 'geo'}${geo.detail ? ` • ${geo.detail}` : ''}`,
        profileUrl,
      });
    }
  }

  const numverifyProfiles = Array.isArray(reconNumverifyProfiles) ? reconNumverifyProfiles : [];
  for (const profile of numverifyProfiles) {
    const number = String(profile?.number || profile?.international_format || 'number').trim();
    const location = String(profile?.location || '').trim();
    const country = String(profile?.country_name || '').trim();
    const countryCode = String(profile?.country_code || '').trim().toLowerCase();
    if (location) {
      addFromTextSource(location, `Numverify: ${number}`, `location: ${location}`, 'numverify', '', { strict: true, preferMostSpecific: true });
    }
    if (country) {
      addFromTextSource(country, `Numverify: ${number}`, `country: ${country}`, 'numverify');
    }
    if (countryCode) {
      addFromTextSource(countryCode, `Numverify: ${number}`, `country_code: ${countryCode}`, 'numverify', '', { strict: true, preferMostSpecific: true });
    }
    for (const geo of extractCoordinateSignals(profile?.raw || profile)) {
      addPoint(geo.label || location || country || number, geo.lat, geo.lon, {
        kind: 'numverify',
        label: `Numverify: ${number}`,
        detail: `${geo.path || 'geo'}${geo.detail ? ` • ${geo.detail}` : ''}`,
      });
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
  const routes = Array.from(routesByKey.values())
    .map((row) => ({
      ...row,
      references: row.references.slice(0, 10),
      sourceCounts: Object.fromEntries(row.sourceCounts.entries()),
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
  for (const route of routes) {
    delete route.refKeys;
    const sourceRows = Object.entries(route.sourceCounts || {}).sort((a, b) => Number(b[1]) - Number(a[1]));
    route.dominantKind = String(sourceRows[0]?.[0] || 'other');
  }
  return { points, routes };
}

function _geoDistanceKm(aLat, aLon, bLat, bLon) {
  const toRad = (value) => (Number(value) * Math.PI) / 180;
  const dLat = toRad(Number(bLat) - Number(aLat));
  const dLon = toRad(Number(bLon) - Number(aLon));
  const lat1 = toRad(aLat);
  const lat2 = toRad(bLat);
  const sinLat = Math.sin(dLat / 2);
  const sinLon = Math.sin(dLon / 2);
  const hav = sinLat * sinLat + Math.cos(lat1) * Math.cos(lat2) * sinLon * sinLon;
  return 6371 * 2 * Math.atan2(Math.sqrt(hav), Math.sqrt(1 - hav));
}

function _wrappedLongitudeDelta(a, b) {
  return Math.abs((((Number(a) - Number(b)) % 360) + 540) % 360 - 180);
}

function _patternLifeTimezoneWeight(lon, rhythm) {
  if (!rhythm || rhythm.insufficient) return 1;
  const expectedLon = Math.max(-180, Math.min(180, Number(rhythm.offset || 0) * 15));
  const delta = _wrappedLongitudeDelta(lon, expectedLon);
  if (delta <= 15) return 1.16;
  if (delta <= 30) return 1.06;
  if (delta <= 45) return 0.94;
  if (delta <= 75) return 0.84;
  return 0.74;
}

function _patternLifeSpecificityWeight(name) {
  const level = _locationHierarchyLevel({ name });
  if (level >= 3) return 1.18;
  if (level === 2) return 0.92;
  if (level === 1) return 0.68;
  return 0.86;
}

function _patternLifeSourceWeight(kind) {
  const normalized = String(kind || '').trim().toLowerCase();
  if (normalized === 'pdl') return 1.28;
  if (normalized === 'post') return 1.1;
  if (normalized === 'osint_industries') return 1.06;
  if (normalized === 'numverify') return 0.93;
  if (normalized === 'other') return 0.85;
  return 0.9;
}

function _nearestKnownLocationLabel(lat, lon, maxDistanceKm = 220) {
  let best = null;
  let bestDistance = Number.POSITIVE_INFINITY;
  for (const location of _locationPairsByName()) {
    const distanceKm = _geoDistanceKm(lat, lon, location.lat, location.lon);
    if (distanceKm < bestDistance) {
      bestDistance = distanceKm;
      best = location;
    }
  }
  if (!best || bestDistance > maxDistanceKm) return '';
  return String(best.name || '').trim();
}

function synthesizePatternLifeLikelyLocations(geo, rhythm = null) {
  const points = Array.isArray(geo?.points) ? geo.points : [];
  const routes = Array.isArray(geo?.routes) ? geo.routes : [];
  const clusters = [];

  const attachSignal = (lat, lon, name, weight, signalCount, sourceCounts, routeSignalCount = 0, options = {}) => {
    let bestCluster = null;
    let bestDistance = Number.POSITIVE_INFINITY;
    for (const cluster of clusters) {
      const distanceKm = _geoDistanceKm(lat, lon, cluster.centerLat, cluster.centerLon);
      if (distanceKm < 90 && distanceKm < bestDistance) {
        bestDistance = distanceKm;
        bestCluster = cluster;
      }
    }
    if (!bestCluster) {
      bestCluster = {
        weight: 0,
        signalCount: 0,
        routeSignalCount: 0,
        weightedLat: 0,
        weightedLonX: 0,
        weightedLonY: 0,
        centerLat: Number(lat),
        centerLon: Number(lon),
        sourceCounts: new Map(),
        labelWeights: new Map(),
      };
      clusters.push(bestCluster);
    }
    const normalizedWeight = Math.max(0.001, Number(weight) || 0.001);
    bestCluster.weight += normalizedWeight;
    bestCluster.signalCount += Math.max(0, Number(signalCount) || 0);
    bestCluster.routeSignalCount += Math.max(0, Number(routeSignalCount) || 0);
    bestCluster.weightedLat += Number(lat) * normalizedWeight;
    const lonRad = (Number(lon) * Math.PI) / 180;
    bestCluster.weightedLonX += Math.cos(lonRad) * normalizedWeight;
    bestCluster.weightedLonY += Math.sin(lonRad) * normalizedWeight;
    bestCluster.centerLat = bestCluster.weightedLat / bestCluster.weight;
    bestCluster.centerLon = (Math.atan2(bestCluster.weightedLonY, bestCluster.weightedLonX) * 180) / Math.PI;
    const normalizedName = String(name || '').trim();
    if (normalizedName && options.useLabel !== false) {
      const score = bestCluster.labelWeights.get(normalizedName) || 0;
      bestCluster.labelWeights.set(normalizedName, score + normalizedWeight * _patternLifeSpecificityWeight(normalizedName));
    }
    for (const [kind, count] of Object.entries(sourceCounts || {})) {
      bestCluster.sourceCounts.set(kind, (bestCluster.sourceCounts.get(kind) || 0) + Number(count || 0));
    }
  };

  for (const point of points) {
    const pointCount = Math.max(1, Number(point?.count) || 0);
    const pointName = String(point?.name || '').trim() || 'Unknown';
    const timezoneWeight = _patternLifeTimezoneWeight(point?.lon, rhythm);
    const specificityWeight = _patternLifeSpecificityWeight(pointName);
    const sourceCounts = point?.sourceCounts && typeof point.sourceCounts === 'object' ? point.sourceCounts : {};
    const totalSourceSignals = Object.values(sourceCounts).reduce((sum, value) => sum + Math.max(0, Number(value) || 0), 0);
    const weightedSourceSignals = Object.entries(sourceCounts)
      .reduce((sum, [kind, count]) => sum + Math.max(0, Number(count) || 0) * _patternLifeSourceWeight(kind), 0);
    const sourceWeight = totalSourceSignals > 0 ? (weightedSourceSignals / totalSourceSignals) : _patternLifeSourceWeight(point?.dominantKind);
    const score = pointCount * sourceWeight * specificityWeight * timezoneWeight;
    attachSignal(point?.lat, point?.lon, pointName, score, pointCount, sourceCounts, 0);
  }

  for (const route of routes) {
    const routeCount = Math.max(1, Number(route?.count) || 0);
    const routeName = String(route?.name || '').trim() || 'Route';
    const timezoneWeight = _patternLifeTimezoneWeight(route?.lon, rhythm);
    const sourceCounts = route?.sourceCounts && typeof route.sourceCounts === 'object' ? route.sourceCounts : {};
    const totalSourceSignals = Object.values(sourceCounts).reduce((sum, value) => sum + Math.max(0, Number(value) || 0), 0);
    const weightedSourceSignals = Object.entries(sourceCounts)
      .reduce((sum, [kind, count]) => sum + Math.max(0, Number(count) || 0) * _patternLifeSourceWeight(kind), 0);
    const sourceWeight = totalSourceSignals > 0 ? (weightedSourceSignals / totalSourceSignals) : _patternLifeSourceWeight(route?.dominantKind);
    const score = routeCount * sourceWeight * timezoneWeight * 0.95;
    attachSignal(route?.lat, route?.lon, routeName, score, routeCount, sourceCounts, routeCount, { useLabel: false });
  }

  const ranked = clusters
    .map((cluster) => {
      const labelRows = Array.from(cluster.labelWeights.entries())
        .sort((a, b) => Number(b[1]) - Number(a[1]) || String(a[0]).localeCompare(String(b[0])));
      const sourceRows = Array.from(cluster.sourceCounts.entries())
        .sort((a, b) => Number(b[1]) - Number(a[1]) || String(a[0]).localeCompare(String(b[0])));
      const fallbackLabel = _nearestKnownLocationLabel(cluster.centerLat, cluster.centerLon);
      return {
        name: String(labelRows[0]?.[0] || fallbackLabel || 'Likely area'),
        lat: Number(cluster.centerLat.toFixed(5)),
        lon: Number(cluster.centerLon.toFixed(5)),
        score: cluster.weight,
        signalCount: cluster.signalCount,
        routeSignalCount: cluster.routeSignalCount,
        sourceCounts: Object.fromEntries(sourceRows),
      };
    })
    .filter((row) => _hasUsableGeoPoint(row.lat, row.lon) && row.score > 0)
    .sort((a, b) => Number(b.score) - Number(a.score) || String(a.name).localeCompare(String(b.name)));

  if (!ranked.length) {
    return { candidates: [] };
  }
  const totalScore = ranked.reduce((sum, row) => sum + Math.max(0, Number(row.score) || 0), 0);
  const candidates = ranked
    .slice(0, 5)
    .map((row) => {
      const probability = totalScore > 0 ? (row.score / totalScore) : 0;
      return {
        ...row,
        confidencePct: Math.max(1, Math.min(99, Math.round(probability * 1000) / 10)),
      };
    });
  return { candidates };
}

function renderPatternLifeLikelyLocations(synthesis) {
  if (!(patternLifeLikelyLocations instanceof HTMLElement) || !(patternLifeLikelyLocationsEmpty instanceof HTMLElement)) return;
  const rows = Array.isArray(synthesis?.candidates) ? synthesis.candidates : [];
  latestPatternLifeLikelyCandidates = rows.slice();
  if (!rows.length) {
    patternLifeLikelyLocations.innerHTML = '';
    patternLifeLikelyLocationsEmpty.classList.remove('hidden');
    return;
  }
  patternLifeLikelyLocationsEmpty.classList.add('hidden');
  patternLifeLikelyLocations.innerHTML = rows
    .map((row, index) => {
      const sourceMix = Object.entries(row.sourceCounts || {})
        .slice(0, 3)
        .map(([kind, count]) => `${kind.replace(/_/g, ' ')} ${count}`)
        .join(' • ');
      const routeLabel = Number(row.routeSignalCount || 0) > 0
        ? `${row.routeSignalCount} route signal${row.routeSignalCount === 1 ? '' : 's'}`
        : 'no route signals';
      return `
        <article class="pattern-life-likely-row">
          <div class="pattern-life-likely-head">
            <strong>${index + 1}. ${escapeHtml(row.name)}</strong>
            <span class="pattern-life-likely-confidence">${row.confidencePct.toFixed(1)}%</span>
          </div>
          <div class="pattern-life-likely-meta">${row.signalCount} total signal${row.signalCount === 1 ? '' : 's'} • ${escapeHtml(routeLabel)} • lat ${row.lat.toFixed(4)}, lon ${row.lon.toFixed(4)}</div>
          <div class="pattern-life-likely-bar"><span style="width:${Math.max(4, row.confidencePct)}%"></span></div>
          <div class="pattern-life-likely-sources">${escapeHtml(sourceMix || 'source mix unavailable')}</div>
        </article>
      `;
    })
    .join('');
}

function inferMostLikelyLocationForCaseNotes(posts) {
  const geo = collectPatternOfLifeLocationPoints(posts);
  const rhythm = summarizePostingRhythm(posts);
  const synthesis = synthesizePatternLifeLikelyLocations(geo, rhythm);
  const top = Array.isArray(synthesis?.candidates) ? synthesis.candidates[0] : null;
  const name = String(top?.name || '').trim();
  return name;
}

function patternLifeMarkerStyle(point, maxCount) {
  const sizeRatio = maxCount > 0 ? Number(point?.count || 0) / maxCount : 0;
  const radius = 4 + Math.max(0.1, sizeRatio) * 8;
  const kind = String(point?.dominantKind || 'other').toLowerCase();
  if (kind === 'post') {
    return {
      radius,
      color: '#a5f3fc',
      fillColor: '#06b6d4',
      fillOpacity: 0.86,
      haloColor: 'rgba(34, 211, 238, 0.34)',
      haloWeight: 9,
    };
  }
  if (kind === 'pdl') {
    return {
      radius,
      color: '#bfdbfe',
      fillColor: '#3b82f6',
      fillOpacity: 0.84,
      haloColor: 'rgba(59, 130, 246, 0.34)',
      haloWeight: 9,
    };
  }
  if (kind === 'osint_industries') {
    return {
      radius,
      color: '#93c5fd',
      fillColor: '#2563eb',
      fillOpacity: 0.84,
      haloColor: 'rgba(37, 99, 235, 0.33)',
      haloWeight: 9,
    };
  }
  if (kind === 'numverify') {
    return {
      radius,
      color: '#c7d2fe',
      fillColor: '#4f46e5',
      fillOpacity: 0.85,
      haloColor: 'rgba(79, 70, 229, 0.34)',
      haloWeight: 9,
    };
  }
  return {
    radius,
    color: '#d1d5db',
    fillColor: '#6b7280',
    fillOpacity: 0.8,
    haloColor: 'rgba(148, 163, 184, 0.3)',
    haloWeight: 8,
  };
}

function patternLifeRouteStyle(route) {
  const kind = String(route?.dominantKind || '').trim().toLowerCase();
  if (kind === 'osint_industries') {
    return {
      haloColor: 'rgba(59, 130, 246, 0.26)',
      color: '#93c5fd',
      dashArray: '4 6',
    };
  }
  if (kind === 'pdl') {
    return {
      haloColor: 'rgba(34, 211, 238, 0.24)',
      color: '#67e8f9',
      dashArray: '6 7',
    };
  }
  return {
    haloColor: 'rgba(14, 165, 233, 0.24)',
    color: '#7dd3fc',
    dashArray: '5 7',
  };
}

function patternLifeTargetingOverlayForCandidate(candidate) {
  if (!candidate) return null;
  const lat = Number(candidate.lat);
  const lon = Number(candidate.lon);
  if (!_hasUsableGeoPoint(lat, lon)) return null;
  const confidence = Math.max(1, Math.min(99, Number(candidate.confidencePct) || 0));
  const hierarchy = _locationHierarchyLevel({ name: candidate.name });
  const hierarchyBonus = hierarchy <= 1 ? 1.9 : hierarchy === 2 ? 0.95 : 0.3;
  const baseHalfSpan = 0.22 + ((100 - confidence) / 100) * 4.6 + hierarchyBonus;
  const latHalfSpan = Math.max(0.12, Math.min(12, baseHalfSpan));
  const lonScale = Math.max(0.2, Math.cos((Math.abs(lat) * Math.PI) / 180));
  const lonHalfSpan = Math.max(0.2, Math.min(20, latHalfSpan / lonScale));
  const south = Math.max(-85, lat - latHalfSpan);
  const north = Math.min(85, lat + latHalfSpan);
  let west = lon - lonHalfSpan;
  let east = lon + lonHalfSpan;
  if (west < -180) west += 360;
  if (east > 180) east -= 360;
  const wrapsDateline = west > east;
  return { lat, lon, south, north, west, east, wrapsDateline };
}

function patternLifeTargetBoxFillOpacityForZoom(zoom) {
  const z = Number(zoom);
  if (!Number.isFinite(z)) return 0.5;
  const clamped = Math.max(2, Math.min(12, z));
  const ratio = (clamped - 2) / 10;
  return Number((0.5 - (ratio * 0.34)).toFixed(2));
}

function updatePatternLifeTargetBoxTransparency() {
  if (!patternLifeMapInstance || !Array.isArray(patternLifeTargetBoxLayers) || !patternLifeTargetBoxLayers.length) return;
  const fillOpacity = patternLifeTargetBoxFillOpacityForZoom(patternLifeMapInstance.getZoom());
  for (const layer of patternLifeTargetBoxLayers) {
    if (layer && typeof layer.setStyle === 'function') {
      layer.setStyle({ fillOpacity });
    }
  }
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

function patternLifeSourceHeaderMarkup(label, profileUrl = '') {
  const cleanLabel = String(label || '').trim() || 'source';
  const cleanUrl = normalizeExternalUrl(profileUrl);
  const icon = faviconMarkup(cleanLabel, cleanUrl);
  return `<span class="pattern-life-source-head">${icon}<span class="pattern-life-source-label">${escapeHtml(cleanLabel)}</span></span>`;
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
      L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
      }).addTo(patternLifeMapInstance);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 20,
        opacity: 0.68,
        pane: 'overlayPane',
      }).addTo(patternLifeMapInstance);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', {
        subdomains: 'abcd',
        maxZoom: 20,
        opacity: 0.9,
        pane: 'overlayPane',
      }).addTo(patternLifeMapInstance);
      patternLifeMapLayer = L.layerGroup().addTo(patternLifeMapInstance);
      patternLifeMapInstance.on('zoomend', () => {
        updatePatternLifeTargetBoxTransparency();
      });
    }
    return L;
  });
}

function updatePatternLifeMapViewport(points, routes = []) {
  if (!patternLifeMapInstance) return;
  const pointRows = Array.isArray(points) ? points : [];
  const routeRows = Array.isArray(routes) ? routes : [];
  if (!pointRows.length && !routeRows.length) {
    patternLifeMapInstance.setView([20, 0], 2);
    return;
  }
  const bounds = [];
  for (const point of pointRows.slice(0, 80)) {
    bounds.push([point.lat, point.lon]);
  }
  for (const route of routeRows.slice(0, 24)) {
    const coords = Array.isArray(route?.coordinates) ? route.coordinates : [];
    for (const coord of coords.slice(0, 200)) {
      const lat = Number(coord?.lat);
      const lon = Number(coord?.lon);
      if (Number.isNaN(lat) || Number.isNaN(lon)) continue;
      bounds.push([lat, lon]);
    }
  }
  if (!bounds.length) {
    patternLifeMapInstance.setView([20, 0], 2);
    return;
  }
  if (bounds.length === 1) {
    patternLifeMapInstance.setView(bounds[0], 13);
  } else {
    patternLifeMapInstance.fitBounds(bounds, { padding: [20, 20], maxZoom: 16 });
  }
}

function renderPatternLifeMap(posts, analysis = null) {
  if (!patternLifeMap || !patternLifeMapEmpty || !patternLifeLocationMapTotal) return;
  const rows = Array.isArray(posts) ? posts : [];
  const rhythm = analysis || summarizePostingRhythm(posts);
  const geo = collectPatternOfLifeLocationPoints(posts);
  const points = Array.isArray(geo?.points) ? geo.points : [];
  const routes = Array.isArray(geo?.routes) ? geo.routes : [];
  const synthesis = synthesizePatternLifeLikelyLocations(geo, rhythm);
  renderPatternLifeLikelyLocations(synthesis);
  const topLikelyCandidate = Array.isArray(synthesis?.candidates) ? synthesis.candidates[0] : null;
  latestPatternLifeMapPoints = points;
  latestPatternLifeMapRoutes = routes;
  const totalMentions = points.reduce((sum, point) => sum + point.count, 0) + routes.reduce((sum, route) => sum + route.count, 0);
  patternLifeLocationMapTotal.textContent = `${totalMentions} point${totalMentions === 1 ? '' : 's'}`;
  patternLifeMapEmpty.classList.toggle('hidden', (points.length + routes.length) > 0);

  ensurePatternLifeMapInstance()
    .then((L) => {
      if (!L || !patternLifeMapLayer || !patternLifeMapInstance) return;
      patternLifeMapLayer.clearLayers();
      patternLifeTargetBoxLayers = [];

      if (!rhythm?.insufficient) {
        const minOffset = -12;
        const maxOffset = 14;
        const clampedOffset = Math.max(minOffset, Math.min(maxOffset, Number(rhythm?.offset || 0)));
        const centerLongitude = Math.max(-180, Math.min(180, clampedOffset * 15));
        const west = centerLongitude - 15;
        const east = centerLongitude + 15;
        const addCorridor = (westBound, eastBound) => {
          L.rectangle([[-85, westBound], [85, eastBound]], {
            color: 'rgba(217, 119, 6, 0.9)',
            weight: 1,
            fillColor: 'rgba(245, 158, 11, 0.18)',
            fillOpacity: 0.52,
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

      const targetingOverlay = patternLifeTargetingOverlayForCandidate(topLikelyCandidate);
      if (targetingOverlay) {
        L.polyline([[-85, targetingOverlay.lon], [85, targetingOverlay.lon]], {
          color: 'rgba(253, 224, 71, 0.94)',
          weight: 1.2,
          opacity: 0.95,
          dashArray: '8 6',
          interactive: false,
          className: 'pattern-life-target-line',
          lineCap: 'round',
        }).addTo(patternLifeMapLayer);
        L.polyline([[targetingOverlay.lat, -180], [targetingOverlay.lat, 180]], {
          color: 'rgba(253, 224, 71, 0.94)',
          weight: 1.2,
          opacity: 0.95,
          dashArray: '8 6',
          interactive: false,
          className: 'pattern-life-target-line',
          lineCap: 'round',
        }).addTo(patternLifeMapLayer);
        const addTargetBox = (west, east) => {
          const targetBox = L.rectangle([[targetingOverlay.south, west], [targetingOverlay.north, east]], {
            color: 'rgba(254, 240, 138, 0.96)',
            weight: 2.1,
            fillColor: 'rgba(250, 204, 21, 0.22)',
            fillOpacity: 0.5,
            interactive: false,
            className: 'pattern-life-target-box',
          }).addTo(patternLifeMapLayer);
          patternLifeTargetBoxLayers.push(targetBox);
        };
        if (targetingOverlay.wrapsDateline) {
          addTargetBox(targetingOverlay.west, 180);
          addTargetBox(-180, targetingOverlay.east);
        } else {
          addTargetBox(targetingOverlay.west, targetingOverlay.east);
        }
        L.circleMarker([targetingOverlay.lat, targetingOverlay.lon], {
          radius: 8.4,
          color: 'rgba(254, 240, 138, 0.98)',
          weight: 1.6,
          fillColor: 'rgba(250, 204, 21, 0.4)',
          fillOpacity: 0.9,
          interactive: false,
          className: 'pattern-life-target-center',
        }).addTo(patternLifeMapLayer);
        updatePatternLifeTargetBoxTransparency();
      }

      for (const route of routes.slice(0, 30)) {
        const coords = Array.isArray(route?.coordinates) ? route.coordinates : [];
        const latLngs = coords
          .map((row) => {
            const lat = Number(row?.lat);
            const lon = Number(row?.lon);
            if (Number.isNaN(lat) || Number.isNaN(lon)) return null;
            return [lat, lon];
          })
          .filter(Boolean);
        if (latLngs.length < 2) continue;
        const sourceBreakdown = Object.entries(route.sourceCounts || {})
          .sort((a, b) => Number(b[1]) - Number(a[1]))
          .slice(0, 4)
          .map(([kind, count]) => `${kind.replace(/_/g, ' ')}: ${count}`)
          .join(' • ');
        const hoverRows = route.references
          .slice(0, 3)
          .map((ref) => {
            const label = String(ref?.label || '').trim() || 'source';
            const detail = String(ref?.detail || '').trim();
            return `<div><strong>${escapeHtml(label)}</strong>${detail ? `<div>${escapeHtml(detail)}</div>` : ''}</div>`;
          })
          .join('');
        const popupRows = route.references
          .slice(0, 8)
          .map((ref) => {
            const label = String(ref?.label || '').trim() || 'source';
            const detail = String(ref?.detail || '').trim();
            const profileUrl = normalizeExternalUrl(ref?.profileUrl);
            const linkMarkup = profileUrl
              ? `<a href="${escapeAttr(profileUrl)}" target="_blank" rel="noopener noreferrer">open profile</a>`
              : '';
            return `<div class="pattern-life-popup-row">${patternLifeSourceHeaderMarkup(label, profileUrl)}<small>${escapeHtml(detail || 'route signal')}${linkMarkup ? ` • ${linkMarkup}` : ''}</small></div>`;
          })
          .join('');
        const routeStyle = patternLifeRouteStyle(route);
        L.polyline(latLngs, {
          color: routeStyle.haloColor,
          weight: 7.4,
          opacity: 0.9,
          interactive: false,
          className: 'pattern-life-route-halo',
          lineCap: 'round',
          lineJoin: 'round',
        }).addTo(patternLifeMapLayer);
        const routeLine = L.polyline(latLngs, {
          color: routeStyle.color,
          weight: 2.8,
          opacity: 0.92,
          dashArray: routeStyle.dashArray,
          className: 'pattern-life-route-core',
          lineCap: 'round',
          lineJoin: 'round',
        });
        routeLine.bindTooltip(
          `<div class="pattern-life-tooltip"><strong>${escapeHtml(route.name || 'Route')}</strong><div>${route.count} signal${route.count === 1 ? '' : 's'}</div>${sourceBreakdown ? `<div>${escapeHtml(sourceBreakdown)}</div>` : ''}${hoverRows}</div>`,
          { sticky: true, direction: 'top', opacity: 0.96 },
        );
        routeLine.bindPopup(
          `<div class="pattern-life-popup"><h4>${escapeHtml(route.name || 'Route')}</h4><p>${route.count} signal${route.count === 1 ? '' : 's'} mapped</p><div class="pattern-life-popup-list">${popupRows}</div></div>`,
          { maxWidth: 520, autoPan: false },
        );
        routeLine.addTo(patternLifeMapLayer);
      }

      if (!points.length && !routes.length) {
        updatePatternLifeMapViewport(points, routes);
        return;
      }

      const maxCount = Math.max(...points.map((point) => point.count), 1);
      for (const point of points.slice(0, 80)) {
        const markerStyle = patternLifeMarkerStyle(point, maxCount);
        L.circleMarker([point.lat, point.lon], {
          radius: markerStyle.radius + 2.8,
          stroke: false,
          fillColor: markerStyle.haloColor,
          fillOpacity: 0.82,
          interactive: false,
          className: 'pattern-life-marker-halo',
        }).addTo(patternLifeMapLayer);
        const popupRows = point.references
          .slice(0, 8)
          .map((ref) => {
            const label = String(ref?.label || '').trim() || 'source';
            const detail = String(ref?.detail || '').trim();
            const postIndex = Number(ref?.postIndex);
            if (Number.isFinite(postIndex) && postIndex >= 0) {
              return patternLifePostPreviewMarkup(rows[postIndex], ref, point.name);
            }
            const profileUrl = normalizeExternalUrl(ref?.profileUrl);
            const linkMarkup = profileUrl
              ? `<a href="${escapeAttr(profileUrl)}" target="_blank" rel="noopener noreferrer">open profile</a>`
              : '';
            return `<div class="pattern-life-popup-row">${patternLifeSourceHeaderMarkup(label, profileUrl)}<small>${escapeHtml(detail || 'location signal')}${linkMarkup ? ` • ${linkMarkup}` : ''}</small></div>`;
          })
          .join('');
        const marker = L.circleMarker([point.lat, point.lon], {
          radius: markerStyle.radius,
          color: markerStyle.color,
          weight: 1.4,
          fillColor: markerStyle.fillColor,
          fillOpacity: markerStyle.fillOpacity,
          className: 'pattern-life-marker-core',
        });
        marker
          .bindPopup(
            `<div class="pattern-life-popup"><h4>${escapeHtml(point.name)}</h4><p>${point.count} signal${point.count === 1 ? '' : 's'} mapped</p><div class="pattern-life-popup-list">${popupRows}</div></div>`,
            { maxWidth: 500, autoPan: false },
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
          popup.options.maxWidth = (nextPlacement === 'left' || nextPlacement === 'right') ? 540 : 500;
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
      updatePatternLifeMapViewport(points, routes);
      if (activeResultsView === 'pattern') {
        window.requestAnimationFrame(() => patternLifeMapInstance?.invalidateSize());
      }
    })
    .catch(() => {
      patternLifeMap.textContent = (points.length || routes.length)
        ? [
          ...points.slice(0, 6).map((item) => `${item.name} (${item.count})`),
          ...routes.slice(0, 2).map((item) => `${item.name || 'Route'} (${item.count})`),
        ].join(' • ')
        : 'Map unavailable';
    });
}

function normalizePlatformSetFromPosts(posts) {
  const available = new Set();
  for (const post of Array.isArray(posts) ? posts : []) {
    const platform = normalizePlatformName(post?.platform);
    if (SOURCE_ORDER.includes(platform)) {
      available.add(platform);
    }
  }
  return available;
}

function renderPatternLifePlatformFilters(posts) {
  if (!(patternLifePlatformFilters instanceof HTMLElement)) return;
  const available = normalizePlatformSetFromPosts(posts);
  if (!available.size) {
    activePatternLifePlatforms.clear();
    patternLifePlatformFilters.innerHTML = '<span class="theme-filter-empty">No platform data available.</span>';
    return;
  }
  for (const platform of Array.from(activePatternLifePlatforms)) {
    if (!available.has(platform)) activePatternLifePlatforms.delete(platform);
  }
  if (!activePatternLifePlatforms.size) {
    for (const platform of available) activePatternLifePlatforms.add(platform);
  }
  const ordered = SOURCE_ORDER.filter((platform) => available.has(platform));
  patternLifePlatformFilters.innerHTML = ordered
    .map((platform) => {
      const active = activePatternLifePlatforms.has(platform);
      return `<button type="button" class="mix-pill mix-filter-pill${active ? ' is-active' : ''}" data-pattern-platform="${escapeAttr(platform)}"><span>${escapeHtml(platformDisplayName(platform))}</span></button>`;
    })
    .join('');
}

function filterPatternLifePosts(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  if (!activePatternLifePlatforms.size) return rows;
  return rows.filter((post) => activePatternLifePlatforms.has(normalizePlatformName(post?.platform)));
}

function renderPatternOfLife(posts) {
  const rows = Array.isArray(posts) ? posts : [];
  renderPatternLifePlatformFilters(rows);
  const scopedRows = filterPatternLifePosts(rows);
  const analysis = summarizePostingRhythm(scopedRows);
  renderPatternPostingRhythm(scopedRows, analysis);
  renderPatternLifeMap(scopedRows, analysis);
}

function refreshPatternOfLifeEstimate() {
  renderPatternOfLife(latestPosts);
  refreshMapLayout();
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
    customKeywordMixEmpty.textContent = 'No custom keywords configured. Add keywords in Master Settings.';
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
  if (activeStartDate) params.set('start_date', activeStartDate);
  if (activeEndDate) params.set('end_date', activeEndDate);
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
    latestFetchedPosts = Array.isArray(data.posts) ? data.posts : [];
    _dashboardFilterCache = { rows: null, key: '', output: [] };
    rerenderFromCurrentFilters();
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
  const timelineMode = activeResultsView === 'timeline';
  const entityGraphMode = activeResultsView === 'entitygraph';
  viewPostsBtn?.classList.toggle('is-active', postView);
  viewMediaBtn?.classList.toggle('is-active', mediaView);
  viewFootprintBtn?.classList.toggle('is-active', footprintMode);
  viewPatternLifeBtn?.classList.toggle('is-active', patternLifeMode);
  viewTimelineBtn?.classList.toggle('is-active', timelineMode);
  viewEntityGraphBtn?.classList.toggle('is-active', entityGraphMode);
  viewPostsBtn?.setAttribute('aria-pressed', String(postView));
  viewMediaBtn?.setAttribute('aria-pressed', String(mediaView));
  viewFootprintBtn?.setAttribute('aria-pressed', String(footprintMode));
  viewPatternLifeBtn?.setAttribute('aria-pressed', String(patternLifeMode));
  viewTimelineBtn?.setAttribute('aria-pressed', String(timelineMode));
  viewEntityGraphBtn?.setAttribute('aria-pressed', String(entityGraphMode));
  const hideStandardLayout = footprintMode || patternLifeMode || timelineMode || entityGraphMode;
  resultsEl?.classList.toggle('hidden', hideStandardLayout);
  dashboardContent?.classList.toggle('media-grid-mode', mediaView);
  const insightsEl = dashboardContent?.querySelector('.insights');
  if (insightsEl instanceof HTMLElement) insightsEl.classList.toggle('hidden', hideStandardLayout || mediaView);
  footprintView?.classList.toggle('hidden', !footprintMode);
  patternLifeView?.classList.toggle('hidden', !patternLifeMode);
  timelineView?.classList.toggle('hidden', !timelineMode);
  entityGraphView?.classList.toggle('hidden', !entityGraphMode);
  if (filterMenu instanceof HTMLElement) filterMenu.classList.toggle('hidden', hideStandardLayout);
}

function setResultsView(mode) {
  const normalized = String(mode || '').trim().toLowerCase();
  const next = normalized === 'media'
    ? 'media'
    : (normalized === 'footprint'
      ? 'footprint'
      : (normalized === 'pattern'
        ? 'pattern'
        : (normalized === 'timeline'
          ? 'timeline'
          : ((normalized === 'entitygraph' || normalized === 'entity_graph' || normalized === 'graph') ? 'entitygraph' : 'posts'))));
  if (activeResultsView === next) return;
  activeResultsView = next;
  if (activeResultsView === 'footprint') {
    ensureAtLeastOneReconSelectorRow(footprintSelectorsList);
  }
  applyResultsViewButtonState();
  if (activeResultsView === 'pattern') {
    activePatternLifePlatforms.clear();
    for (const platform of SOURCE_ORDER) activePatternLifePlatforms.add(platform);
    renderPatternOfLife(latestPosts);
    refreshMapLayout();
    window.setTimeout(refreshMapLayout, 80);
  }
  if (activeResultsView === 'timeline') {
    renderFootprintTimeline();
  }
  if (activeResultsView === 'entitygraph') {
    renderFootprintEntityGraph();
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
  const quitOptionsOpen = quitOptionsModal && !quitOptionsModal.classList.contains('hidden');
  document.body.classList.toggle(
    'modal-active',
    Boolean(setupOpen || editOpen || saveOpen || notesOpen || configOpen || manualInsertOpen || postOpen || quitOptionsOpen),
  );
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
    if (configCustomKeywordInput instanceof HTMLInputElement) configCustomKeywordInput.value = '';
    configCustomKeywordList = normalizeCustomKeywordList(payload?.custom_keyword_list);
    defaultDataRetentionPeriod = normalizeDataRetentionPeriod(payload?.default_data_retention_period);
    if (configDefaultRetentionSelect instanceof HTMLSelectElement) {
      configDefaultRetentionSelect.value = defaultDataRetentionPeriod;
    }
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
      Boolean(payload?.apify_api_token_configured),
    ];
    summarizeSecretState(secretFlags.filter(Boolean).length, secretFlags.length, storageMode);
    setConfiguredHint(configPdlApiKeyInput, configPdlApiKeyHint, secretFlags[0], storageMode);
    setConfiguredHint(configOsintIndustriesApiKeyInput, configOsintIndustriesApiKeyHint, secretFlags[1], storageMode);
    setConfiguredHint(configNumverifyApiKeyInput, configNumverifyApiKeyHint, secretFlags[2], storageMode);
    setConfiguredHint(configOpenAiApiKeyInput, configOpenAiApiKeyHint, secretFlags[3], storageMode);
    setConfiguredHint(configApifyApiTokenInput, configApifyApiTokenHint, secretFlags[4], storageMode);
  } catch (error) {
    console.error(error);
    defaultDataRetentionPeriod = DEFAULT_DATA_RETENTION_PERIOD;
    if (configDefaultRetentionSelect instanceof HTMLSelectElement) {
      configDefaultRetentionSelect.value = defaultDataRetentionPeriod;
    }
    if (configStatus) configStatus.textContent = 'Failed to load master settings.';
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
    || !configApifyApiTokenInput
  ) return;
  if (configSaveBtn instanceof HTMLButtonElement) configSaveBtn.disabled = true;
  if (configStatus) configStatus.textContent = 'Saving master settings...';
  try {
    if (configCustomKeywordInput instanceof HTMLInputElement) {
      addConfigCustomKeywordTerm(configCustomKeywordInput.value);
      configCustomKeywordInput.value = '';
    }
    const body = {
      custom_keyword_list: normalizeCustomKeywordList(configCustomKeywordList),
      default_data_retention_period: normalizeDataRetentionPeriod(configDefaultRetentionSelect?.value),
    };
    const pdlKey = String(configPdlApiKeyInput.value || '').trim();
    const osintKey = String(configOsintIndustriesApiKeyInput.value || '').trim();
    const numverifyKey = String(configNumverifyApiKeyInput.value || '').trim();
    const openAiKey = String(configOpenAiApiKeyInput.value || '').trim();
    const apifyToken = String(configApifyApiTokenInput.value || '').trim();
    if (pdlKey) body.pdl_api_key = pdlKey;
    if (osintKey) body.osint_industries_api_key = osintKey;
    if (numverifyKey) body.numverify_api_key = numverifyKey;
    if (openAiKey) body.openai_api_key = openAiKey;
    if (apifyToken) body.apify_api_token = apifyToken;
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    await loadConfig();
    if (configStatus) {
      configStatus.textContent = 'Master settings saved. API keys are write-only and never returned by the API.';
    }
  } catch (error) {
    console.error(error);
    if (configStatus) configStatus.textContent = `Failed to save master settings: ${error.message || 'unknown error'}`;
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
  toggleReconProgress(isBusy);
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
  toggleFootprintReconProgress(isBusy);
}

function formatReconElapsed(seconds) {
  const total = Math.max(0, Number(seconds) || 0);
  if (total < 60) return `${total}s`;
  const mins = Math.floor(total / 60);
  const rem = total % 60;
  return `${mins}m ${rem}s`;
}

function toggleReconProgress(isBusy) {
  if (!(reconProgress instanceof HTMLElement)) return;
  if (!isBusy) {
    reconProgress.classList.add('hidden');
    if (reconProgressTimer) {
      clearInterval(reconProgressTimer);
      reconProgressTimer = null;
    }
    reconProgressStartedAt = 0;
    if (reconProgressLabel instanceof HTMLElement) {
      reconProgressLabel.textContent = 'Recon modules are running...';
    }
    return;
  }
  reconProgress.classList.remove('hidden');
  reconProgressStartedAt = Date.now();
  if (reconProgressLabel instanceof HTMLElement) {
    reconProgressLabel.textContent = 'Recon modules are running... (0s elapsed)';
  }
  if (reconProgressTimer) clearInterval(reconProgressTimer);
  reconProgressTimer = setInterval(() => {
    const elapsedSeconds = Math.max(0, Math.floor((Date.now() - reconProgressStartedAt) / 1000));
    if (reconProgressLabel instanceof HTMLElement) {
      reconProgressLabel.textContent = `Recon modules are running... (${formatReconElapsed(elapsedSeconds)} elapsed)`;
    }
  }, 1000);
}

function toggleFootprintReconProgress(isBusy) {
  if (!(footprintReconProgress instanceof HTMLElement)) return;
  if (!isBusy) {
    footprintReconProgress.classList.add('hidden');
    if (footprintReconProgressTimer) {
      clearInterval(footprintReconProgressTimer);
      footprintReconProgressTimer = null;
    }
    footprintReconProgressStartedAt = 0;
    if (footprintReconProgressLabel instanceof HTMLElement) {
      footprintReconProgressLabel.textContent = 'Recon modules are running...';
    }
    return;
  }
  footprintReconProgress.classList.remove('hidden');
  footprintReconProgressStartedAt = Date.now();
  if (footprintReconProgressLabel instanceof HTMLElement) {
    footprintReconProgressLabel.textContent = 'Recon modules are running... (0s elapsed)';
  }
  if (footprintReconProgressTimer) clearInterval(footprintReconProgressTimer);
  footprintReconProgressTimer = setInterval(() => {
    const elapsedSeconds = Math.max(0, Math.floor((Date.now() - footprintReconProgressStartedAt) / 1000));
    if (footprintReconProgressLabel instanceof HTMLElement) {
      footprintReconProgressLabel.textContent = `Recon modules are running... (${formatReconElapsed(elapsedSeconds)} elapsed)`;
    }
  }, 1000);
}

function toggleFootprintPivotProgress(isBusy, prefix = 'Pivot recon running') {
  if (!(footprintPivotProgress instanceof HTMLElement)) return;
  const cleanPrefix = String(prefix || '').trim() || 'Pivot recon running';
  if (!isBusy) {
    footprintPivotProgress.classList.add('hidden');
    if (footprintPivotProgressTimer) {
      clearInterval(footprintPivotProgressTimer);
      footprintPivotProgressTimer = null;
    }
    footprintPivotProgressStartedAt = 0;
    if (footprintPivotProgressLabel instanceof HTMLElement) {
      footprintPivotProgressLabel.textContent = `${cleanPrefix}...`;
    }
    return;
  }
  footprintPivotProgress.classList.remove('hidden');
  footprintPivotProgressStartedAt = Date.now();
  if (footprintPivotProgressLabel instanceof HTMLElement) {
    footprintPivotProgressLabel.textContent = `${cleanPrefix}... (0s elapsed)`;
  }
  if (footprintPivotProgressTimer) clearInterval(footprintPivotProgressTimer);
  footprintPivotProgressTimer = setInterval(() => {
    const elapsedSeconds = Math.max(0, Math.floor((Date.now() - footprintPivotProgressStartedAt) / 1000));
    if (footprintPivotProgressLabel instanceof HTMLElement) {
      footprintPivotProgressLabel.textContent = `${cleanPrefix}... (${formatReconElapsed(elapsedSeconds)} elapsed)`;
    }
  }, 1000);
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
  const value = normalizeExternalUrl(url);
  if (!value) return '';
  try {
    const parsed = new URL(value);
    return String(parsed.hostname || '').replace(/^www\./i, '').toLowerCase();
  } catch (error) {
    return '';
  }
}

function normalizeExternalUrl(rawUrl) {
  const raw = String(rawUrl || '').trim();
  if (!raw) return '';
  if (/^https?:\/\//i.test(raw)) return raw;
  if (/^\/\//.test(raw)) return `https:${raw}`;
  const candidate = raw.replace(/^\/+/, '');
  if (/^[a-z0-9.-]+\.[a-z]{2,}(?:[/:?#]|$)/i.test(candidate)) return `https://${candidate}`;
  return '';
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

const NON_PROFILE_PATH_SEGMENTS = new Set([
  'about', 'account', 'accounts', 'app', 'apps', 'blog', 'careers', 'company', 'contact', 'dashboard',
  'developers', 'discover', 'docs', 'download', 'explore', 'features', 'help', 'home', 'jobs', 'join',
  'legal', 'login', 'pricing', 'privacy', 'products', 'search', 'settings', 'signup', 'support', 'terms',
]);

function isLikelyAccountProfileUrl(rawUrl) {
  const value = normalizeExternalUrl(rawUrl);
  if (!value) return false;
  try {
    const parsed = new URL(value);
    const host = String(parsed.hostname || '').trim().toLowerCase();
    if (!host || !host.includes('.')) return false;
    const segments = String(parsed.pathname || '').split('/').filter(Boolean);
    if (!segments.length) return false;
    const first = segments[0].toLowerCase();
    if (NON_PROFILE_PATH_SEGMENTS.has(first)) return false;
    if (segments.length === 1 && (first === 'www' || first === 'm')) return false;
    return true;
  } catch (error) {
    return false;
  }
}

function siteDisplayNameFromDomain(domain) {
  const clean = String(domain || '').trim().toLowerCase().replace(/^www\./, '');
  if (!clean) return '';
  if (clean === 'x.com' || clean.endsWith('.x.com') || clean.includes('twitter.com')) return 'Twitter/X';
  if (clean.includes('reddit.com')) return 'Reddit';
  if (clean.includes('tiktok.com')) return 'TikTok';
  if (clean.includes('bsky.app') || clean.includes('bsky.social')) return 'Bluesky';
  if (clean.includes('instagram.com')) return 'Instagram';
  if (clean.includes('youtube.com') || clean.includes('youtu.be')) return 'YouTube';
  if (clean.includes('linkedin.com')) return 'LinkedIn';
  if (clean.includes('facebook.com')) return 'Facebook';
  if (clean.includes('threads.net')) return 'Threads';
  if (clean.includes('github.com')) return 'GitHub';
  if (clean.includes('gitlab.com')) return 'GitLab';
  if (clean.includes('twitch.tv')) return 'Twitch';
  if (clean.includes('medium.com')) return 'Medium';
  const root = clean.split('.')[0] || clean;
  return titleCaseLabel(root);
}

function normalizeReconSiteLabel(rawSite, profileUrl = '', siteUrl = '') {
  const cleanSite = String(rawSite || '').trim();
  const normalized = normalizePlatformName(cleanSite);
  if (normalized) return platformDisplayName(normalized);
  if (cleanSite && !isHttpUrl(cleanSite)) {
    const asDomain = cleanSite.replace(/^https?:\/\//i, '').split('/')[0].trim();
    if (/^[a-z0-9.-]+\.[a-z]{2,}$/i.test(asDomain)) return siteDisplayNameFromDomain(asDomain);
    return titleCaseLabel(cleanSite);
  }
  const domain = profileDomain(profileUrl) || profileDomain(siteUrl);
  if (domain) return siteDisplayNameFromDomain(domain);
  return cleanSite || 'Unknown';
}

function reconRowVisibilityKey(row) {
  return [
    String(row?.selector_type || '').trim().toLowerCase(),
    String(row?.selector || '').trim().toLowerCase(),
    String(row?.site_key || row?.site || '').trim().toLowerCase(),
    String(row?.profile_url || '').trim().toLowerCase(),
    String(row?.source || '').trim().toLowerCase(),
  ].join('|');
}

function osintTileVisibilityKey(profile) {
  return [
    String(profile?.module || '').trim().toLowerCase(),
    String(profile?.query_type || '').trim().toLowerCase(),
    String(profile?.query_value || '').trim().toLowerCase(),
    String(profile?.profile_url || '').trim().toLowerCase(),
    String(profile?.website || '').trim().toLowerCase(),
    String(profile?.username || '').trim().toLowerCase(),
    String(profile?.email || '').trim().toLowerCase(),
    String(profile?.phone || '').trim().toLowerCase(),
  ].join('|');
}

function pdlProfileVisibilityKey(profile) {
  return [
    String(profile?.id || '').trim().toLowerCase(),
    String(profile?.query_type || '').trim().toLowerCase(),
    String(profile?.query_value || '').trim().toLowerCase(),
    String(profile?.full_name || '').trim().toLowerCase(),
  ].join('|');
}

function pdlContactVisibilityKey(profile, label, value) {
  return [
    pdlProfileVisibilityKey(profile),
    String(label || '').trim().toLowerCase(),
    String(value || '').trim().toLowerCase(),
  ].join('|');
}

function dedupeRowsByProfileUrl(rows) {
  const items = Array.isArray(rows) ? rows : [];
  const seen = new Set();
  const output = [];
  for (const row of items) {
    const normalized = normalizeExternalUrl(row?.profile_url) || String(row?.profile_url || '').trim();
    const key = String(normalized || '').toLowerCase();
    if (!key || seen.has(key)) continue;
    seen.add(key);
    output.push(row);
  }
  return output;
}

function filteredReconPayload(payload) {
  const base = payload && typeof payload === 'object' ? payload : emptyReconPayload();
  const resultsRaw = Array.isArray(base?.results) ? base.results : [];
  const osintProfilesRaw = Array.isArray(base?.osint_profiles) ? base.osint_profiles : [];
  const personDataProfilesRaw = Array.isArray(base?.person_data_profiles) ? base.person_data_profiles : [];
  const pdlProfileQueryKeys = new Set(
    personDataProfilesRaw
      .filter((profile) => hiddenPdlProfileKeys.has(pdlProfileVisibilityKey(profile)))
      .map((profile) => `${String(profile?.query_type || '').trim().toLowerCase()}|${String(profile?.query_value || '').trim().toLowerCase()}`),
  );
  const hiddenOsintKeys = new Set(
    osintProfilesRaw
      .filter((profile) => hiddenOsintTileKeys.has(osintTileVisibilityKey(profile)))
      .map((profile) => osintTileVisibilityKey(profile)),
  );

  const results = resultsRaw.filter((row) => {
    const rowKey = reconRowVisibilityKey(row);
    if (hiddenReconRowKeys.has(rowKey)) return false;
    const source = String(row?.source || '').trim().toLowerCase();
    const queryKey = `${String(row?.selector_type || '').trim().toLowerCase()}|${String(row?.selector || '').trim().toLowerCase()}`;
    if (source === 'pdl' && pdlProfileQueryKeys.has(queryKey)) return false;
    if (source === 'pdl' && hiddenPdlProfileUrlKeys.has(String(row?.profile_url || '').trim().toLowerCase())) return false;
    if (source === 'osint_industries') {
      const profile = row?.osint_profile;
      if (profile && hiddenOsintKeys.has(osintTileVisibilityKey(profile))) return false;
    }
    return true;
  });

  const osintProfiles = osintProfilesRaw.filter((profile) => !hiddenOsintTileKeys.has(osintTileVisibilityKey(profile)));
  const personDataProfiles = personDataProfilesRaw.filter((profile) => !hiddenPdlProfileKeys.has(pdlProfileVisibilityKey(profile)));
  const personDataProfile = personDataProfiles[0] || {};
  const leadsRaw = Array.isArray(base?.leads) ? base.leads : [];
  const leads = leadsRaw.filter((lead) => {
    const source = String(lead?.source || '').trim().toLowerCase();
    const leadUrl = String(lead?.profile_url || '').trim().toLowerCase();
    if (leadUrl && hiddenPdlProfileUrlKeys.has(leadUrl)) return false;
    if (source === 'pdl' && String(lead?.lead_type || '').trim().toLowerCase() === 'attribute') {
      const profileName = String(lead?.profile_name || '').trim().toLowerCase();
      const label = String(lead?.attribute || '').trim();
      const value = String(lead?.value || '').trim();
      const matchedProfile = personDataProfiles.find((profile) => String(profile?.full_name || '').trim().toLowerCase() === profileName);
      if (matchedProfile && hiddenPdlContactValueKeys.has(pdlContactVisibilityKey(matchedProfile, label, value))) return false;
      if (!matchedProfile) {
        const syntheticKey = ['unknown-profile', String(label || '').trim().toLowerCase(), String(value || '').trim().toLowerCase()].join('|');
        if (hiddenPdlContactValueKeys.has(syntheticKey)) return false;
      }
    }
    return true;
  });

  const output = {
    ...base,
    results,
    osint_profiles: osintProfiles,
    person_data_profiles: personDataProfiles,
    person_data_profile: personDataProfile,
    leads,
  };
  output.collection_ready_profiles = dedupeRowsByProfileUrl(results.filter((row) => row?.status === 'present' && row?.supported_for_collection && String(row?.profile_url || '').trim()));
  output.unsupported_profiles_with_url = dedupeRowsByProfileUrl(results.filter((row) => row?.status === 'present' && !row?.supported_for_collection && String(row?.profile_url || '').trim()));
  output.known_present_without_url = results.filter((row) => row?.status === 'present' && !String(row?.profile_url || '').trim());
  output.checked = results.length;
  output.present_count = results.filter((row) => row?.status === 'present').length;
  return output;
}

function isHibpModuleName(value) {
  const moduleName = String(value || '').trim().toLowerCase();
  if (!moduleName) return false;
  return moduleName === 'hibp'
    || moduleName.includes('haveibeenpwned')
    || moduleName.includes('have_i_been_pwned')
    || moduleName.includes('pwned');
}

function pivotSelectorActionMarkup(type, value, title = 'Pivot Search') {
  const cleanType = String(type || '').trim().toLowerCase();
  const cleanValue = String(value || '').trim();
  if (!['username', 'email', 'phone'].includes(cleanType) || !cleanValue) return '';
  return `
    <button type="button" class="known-selector-action pivot recon-pill-action" data-recon-pivot-type="${escapeAttr(cleanType)}" data-recon-pivot-value="${escapeAttr(cleanValue)}" title="${escapeAttr(title)}" aria-label="${escapeAttr(title)}">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="6.5"></circle><path d="M16.5 16.5L21 21"></path></svg>
    </button>
  `;
}

function selectorConfidenceLevel(selectorType) {
  const cleanType = String(selectorType || '').trim().toLowerCase();
  if (cleanType === 'email' || cleanType === 'phone' || cleanType === 'wallet') return 'high';
  if (cleanType === 'profile') return 'medium';
  if (cleanType === 'username' || cleanType === 'name' || cleanType === 'location') return 'low';
  return 'low';
}

function selectorConfidenceOverrideKey(selectorType, selectorValue, scopeId = '') {
  const type = String(selectorType || '').trim().toLowerCase();
  const value = String(selectorValue || '').trim().toLowerCase();
  const scope = String(scopeId || '').trim().toLowerCase();
  return scope ? `${scope}|${type}|${value}` : `${type}|${value}`;
}

function loadSelectorConfidenceOverrides() {
  try {
    if (!window?.localStorage) return;
    const raw = String(window.localStorage.getItem(SELECTOR_CONFIDENCE_OVERRIDE_STORAGE_KEY) || '').trim();
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object') return;
    for (const [key, value] of Object.entries(parsed)) {
      const cleanKey = String(key || '').trim().toLowerCase();
      const level = String(value || '').trim().toLowerCase();
      if (!cleanKey || !cleanKey.includes('|')) continue;
      if (!SELECTOR_CONFIDENCE_LEVELS.includes(level)) continue;
      selectorConfidenceOverrides.set(cleanKey, level);
    }
  } catch (error) {
    console.warn('Unable to load selector confidence overrides:', error);
  }
}

function saveSelectorConfidenceOverrides() {
  try {
    if (!window?.localStorage) return;
    const payload = Object.fromEntries(selectorConfidenceOverrides.entries());
    window.localStorage.setItem(SELECTOR_CONFIDENCE_OVERRIDE_STORAGE_KEY, JSON.stringify(payload));
  } catch (error) {
    console.warn('Unable to save selector confidence overrides:', error);
  }
}

function selectorConfidenceLevelEffective(selectorType, selectorValue = '', scopeId = '') {
  const key = selectorConfidenceOverrideKey(selectorType, selectorValue, scopeId);
  const override = selectorConfidenceOverrides.get(key);
  if (override && SELECTOR_CONFIDENCE_LEVELS.includes(override)) return override;
  return selectorConfidenceLevel(selectorType);
}

function selectorConfidenceMeta(selectorType, selectorValue = '', scopeId = '') {
  const level = selectorConfidenceLevelEffective(selectorType, selectorValue, scopeId);
  if (level === 'high') {
    return { level, label: 'High Confidence', short: 'High', guidance: 'Unique selector; stronger identity linkage.' };
  }
  if (level === 'medium') {
    return { level, label: 'Medium Confidence', short: 'Medium', guidance: 'Handle reuse is possible across people/platforms.' };
  }
  return { level, label: 'Low Confidence', short: 'Low', guidance: 'Non-unique selector; corroborate with additional evidence.' };
}

function selectorConfidenceDisplayValue(selectorType, selectorValue) {
  const type = String(selectorType || '').trim().toLowerCase();
  const value = String(selectorValue || '').trim();
  if (!value) return 'unknown';
  if (type === 'username') return value.startsWith('@') ? value : `@${value}`;
  return value;
}

function selectorConfidenceTooltip(selectorType, selectorValue, scopeId = '') {
  const level = selectorConfidenceLevelEffective(selectorType, selectorValue, scopeId);
  const displayValue = selectorConfidenceDisplayValue(selectorType, selectorValue);
  if (level === 'high') {
    return `Result is high confidence as it was returned by a unique selector >${displayValue}<`;
  }
  if (level === 'low') {
    return `Result is low confidence since it was discovered via a nonunique selector >${displayValue}<`;
  }
  return `Result confidence is medium because selector uniqueness is mixed for >${displayValue}<`;
}

function selectorConfidenceBadgeMarkup(selectorType, selectorValue = '', options = {}) {
  const scopeId = String(options?.scopeId || '').trim();
  const meta = selectorConfidenceMeta(selectorType, selectorValue, scopeId);
  const compact = options?.compact === true;
  const label = compact ? meta.short : meta.label;
  const tooltip = selectorConfidenceTooltip(selectorType, selectorValue, scopeId);
  const key = selectorConfidenceOverrideKey(selectorType, selectorValue, scopeId);
  return `<button type="button" class="selector-confidence-badge is-${escapeAttr(meta.level)}" data-confidence-key="${escapeAttr(key)}" data-confidence-type="${escapeAttr(String(selectorType || '').trim().toLowerCase())}" data-confidence-value="${escapeAttr(String(selectorValue || '').trim())}" title="${escapeAttr(tooltip)}">${escapeHtml(label)}</button>`;
}

function cycleSelectorConfidenceLevel(level) {
  const clean = String(level || '').trim().toLowerCase();
  const index = SELECTOR_CONFIDENCE_LEVELS.indexOf(clean);
  if (index < 0) return SELECTOR_CONFIDENCE_LEVELS[0];
  return SELECTOR_CONFIDENCE_LEVELS[(index + 1) % SELECTOR_CONFIDENCE_LEVELS.length];
}

function selectorConfidenceLevelFromOverrideKey(overrideKey, fallbackSelectorType = '') {
  const cleanKey = String(overrideKey || '').trim().toLowerCase();
  const override = selectorConfidenceOverrides.get(cleanKey);
  if (override && SELECTOR_CONFIDENCE_LEVELS.includes(override)) return override;
  return selectorConfidenceLevel(fallbackSelectorType);
}

function rerenderConfidenceOverriddenViews() {
  const payload = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
  renderReconResults(payload, footprintReconResults);
  renderReconResults(payload, reconResults);
  renderKnownSelectorsPanel(payload);
}

function toReconBadge(row, clsName = 'lead', options = {}) {
  const removable = options?.removable === true;
  const rowKey = reconRowVisibilityKey(row);
  const label = normalizeReconSiteLabel(row?.site, row?.profile_url, row?.site_url);
  const url = isLikelyAccountProfileUrl(row?.profile_url) ? normalizeExternalUrl(row?.profile_url) : '';
  const screenshotUrl = String(row.screenshot_url || '').trim();
  const avatarUrl = normalizeExternalUrl(row.picture_url || row.avatar_url || '');
  const source = String(row.source || '').trim().toLowerCase();
  const icon = faviconMarkup(label, url);
  const avatarMarkup = avatarUrl
    ? `<img class="recon-pill-avatar" src="${escapeAttr(avatarUrl)}" alt="${escapeAttr(label)} profile image" loading="lazy" referrerpolicy="no-referrer" />`
    : '';
  const content = `<span class="recon-label">${avatarMarkup}${icon}<span>${escapeHtml(label)}</span></span>`;
  const classes = source === 'pdl' ? `${clsName} pdl` : clsName;
  const selectorType = String(row?.selector_type || '').trim().toLowerCase();
  const selectorValue = String(row?.selector || '').trim();
  const selectorTypeClass = selectorTypeColorToken(selectorType);
  const selectorKey = sourceSelectorKey(selectorType, selectorValue);
  const selectorAttr = selectorKey ? ` data-source-selector-key="${escapeAttr(selectorKey)}"` : '';
  const confidenceBadge = selectorConfidenceBadgeMarkup(selectorType, selectorValue, { compact: true, scopeId: rowKey });
  const pivotMarkup = options?.pivotable === false ? '' : pivotSelectorActionMarkup(selectorType, selectorValue, 'Pivot from selector');
  const removeMarkup = removable
    ? `<button type="button" class="known-selector-action recon-pill-remove recon-pill-action" data-recon-remove="${escapeAttr(rowKey)}" title="Remove result">×</button>`
    : '';
  if (!url) return `<span class="recon-pill ${escapeHtml(classes)} recon-pill-${escapeAttr(selectorTypeClass)}"${selectorAttr}>${content}${confidenceBadge}${pivotMarkup}${removeMarkup}</span>`;
  const previewAttr = screenshotUrl ? ` data-preview-image="${escapeAttr(screenshotUrl)}"` : '';
  const previewLabelAttr = screenshotUrl ? ` data-preview-label="${escapeAttr(label)}"` : '';
  return `
    <span class="recon-pill ${escapeHtml(classes)} recon-pill-${escapeAttr(selectorTypeClass)}"${selectorAttr}${previewAttr}${previewLabelAttr}>
      <a class="lead-link recon-pill-link" target="_blank" rel="noopener noreferrer" href="${escapeHtml(url)}">${content}</a>
      ${confidenceBadge}
      ${pivotMarkup}
      ${removeMarkup}
    </span>
  `;
}

function formatSelectorLabel(selectorType, selectorValue) {
  const value = String(selectorValue || '').trim() || 'unknown';
  return value;
}

function selectorTypeDisplayLabel(selectorType) {
  const clean = String(selectorType || '').trim().toLowerCase();
  if (!clean) return 'Selector';
  return clean.charAt(0).toUpperCase() + clean.slice(1);
}

function footprintSelectorEvidenceLabel(selectorType, selectorValue) {
  const typeLabel = selectorTypeDisplayLabel(selectorType);
  const value = String(selectorValue || '').trim();
  if (!value) return `Identified via ${typeLabel} selector`;
  return `Identified via ${typeLabel} selector: ${value}`;
}

function sourceSelectorKey(selectorType, selectorValue) {
  const type = String(selectorType || '').trim().toLowerCase();
  const value = String(selectorValue || '').trim();
  if (!type || !value) return '';
  return `${type}|${value.toLowerCase()}`;
}

function sourceSelectorParts(key) {
  const raw = String(key || '').trim().toLowerCase();
  if (!raw || !raw.includes('|')) return { type: '', value: '' };
  const [type, ...rest] = raw.split('|');
  const value = rest.join('|').trim();
  return { type: String(type || '').trim(), value };
}

function collectSourceSelectorFilterOptions(results) {
  const rows = Array.isArray(results) ? results : [];
  const counts = new Map();
  const metaByKey = new Map();
  for (const row of rows) {
    const type = String(row?.selector_type || '').trim().toLowerCase();
    const value = String(row?.selector || '').trim();
    const key = sourceSelectorKey(type, value);
    if (!key) continue;
    counts.set(key, (counts.get(key) || 0) + 1);
    if (!metaByKey.has(key)) {
      metaByKey.set(key, {
        label: formatSelectorLabel(type, value),
        confidenceLevel: selectorConfidenceMeta(type, value).level,
      });
    }
  }
  return Array.from(counts.entries())
    .map(([key, count]) => ({
      key,
      count,
      label: metaByKey.get(key)?.label || key,
      confidenceLevel: metaByKey.get(key)?.confidenceLevel || 'low',
    }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

const KNOWN_SELECTOR_GROUPS = ['email', 'phone', 'username', 'name', 'location'];
const KNOWN_SELECTOR_NAME_SITE_WORDS = new Set([
  'x', 'twitter', 'reddit', 'instagram', 'facebook', 'youtube', 'tiktok', 'bluesky', 'github', 'gitlab',
  'linkedin', 'threads', 'twitch', 'medium', 'strava', 'airbnb', 'google', 'maps', 'website', 'profile',
  'osint', 'industries',
]);
const KNOWN_SELECTOR_COMPANY_TERMS = new Set([
  'inc', 'llc', 'ltd', 'corp', 'corporation', 'co', 'company', 'solutions', 'technology', 'technologies',
  'tech', 'group', 'media', 'systems', 'labs', 'ventures', 'partners', 'associates', 'agency', 'capital',
  'holdings',
]);
const KNOWN_SELECTOR_NON_PERSON_NAME_TERMS = new Set([
  'manager', 'senior', 'public', 'sector', 'transformation', 'director', 'lead', 'team', 'official',
  'account', 'verified',
]);

function normalizeKnownSelectorValue(type, value) {
  const normalizedType = String(type || '').trim().toLowerCase();
  const raw = String(value || '').trim();
  if (!raw) return '';
  if (normalizedType === 'location') {
    // Remove categorical prefixes from location payload fragments (e.g., "Country: CA City: Halifax").
    const stripped = raw
      .replace(/\b(?:country|state|city|raw)\s*:\s*/gi, '')
      .replace(/\s{2,}/g, ' ')
      .trim();
    return stripped;
  }
  if (normalizedType === 'email') return raw.toLowerCase();
  if (normalizedType === 'phone') return raw.replace(/[^\d+]/g, '');
  if (normalizedType === 'username') return raw.replace(/^@+/, '');
  if (normalizedType === 'name') return raw.replace(/\s+/g, ' ');
  return raw;
}

function isLikelyPersonName(value) {
  const clean = String(value || '').trim().replace(/\s+/g, ' ');
  if (!clean) return false;
  if (isHttpUrl(clean) || clean.includes('@') || /^\+?[\d().\s-]{6,}$/.test(clean)) return false;
  if (/\b[a-z0-9-]+\.(?:com|net|org|io|co|ai|dev|gov|edu|us)\b/i.test(clean)) return false;
  if (/[(),]/.test(clean)) return false;
  if (/\d/.test(clean)) return false;
  if (clean.length > 80 || clean.length < 2) return false;
  if (/[|/\\]/.test(clean)) return false;
  const pieces = clean.split(' ').filter(Boolean);
  if (!pieces.length || pieces.length > 4) return false;
  if (pieces.length === 1 && !/^[A-Za-z][A-Za-z'.-]{1,}$/.test(pieces[0])) return false;
  const lowered = clean.toLowerCase();
  if (KNOWN_SELECTOR_NAME_SITE_WORDS.has(lowered)) return false;
  const nonPersonHits = pieces.filter((piece) => KNOWN_SELECTOR_NON_PERSON_NAME_TERMS.has(piece.toLowerCase().replace(/[.,]/g, ''))).length;
  if (nonPersonHits > 0) return false;
  const companyHits = pieces.filter((piece) => KNOWN_SELECTOR_COMPANY_TERMS.has(piece.toLowerCase().replace(/[.,]/g, ''))).length;
  if (companyHits > 0) return false;
  const wordHits = pieces.filter((piece) => KNOWN_SELECTOR_NAME_SITE_WORDS.has(piece.toLowerCase())).length;
  if (wordHits && wordHits === pieces.length) return false;
  return true;
}

function isLikelyUsername(value) {
  const clean = String(value || '').trim().replace(/^@+/, '');
  if (!clean) return false;
  if (clean.length < 2 || clean.length > 48) return false;
  if (clean.includes(' ') || isHttpUrl(clean)) return false;
  if (/[(),]/.test(clean)) return false;
  if (/^[a-z0-9-]+\.(?:com|net|org|io|co|ai|dev|gov|edu|us)$/i.test(clean)) return false;
  if (!/^[a-z0-9._-]+$/i.test(clean)) return false;
  if (KNOWN_SELECTOR_NAME_SITE_WORDS.has(clean.toLowerCase())) return false;
  return true;
}

function addKnownSelector(map, type, value) {
  const normalizedType = String(type || '').trim().toLowerCase();
  if (!KNOWN_SELECTOR_GROUPS.includes(normalizedType)) return '';
  const normalizedValue = normalizeKnownSelectorValue(normalizedType, value);
  if (!normalizedValue) return '';
  if (normalizedType === 'name' && !isLikelyPersonName(normalizedValue)) return '';
  if (normalizedType === 'username' && !isLikelyUsername(normalizedValue)) return '';
  if (!map.has(normalizedType)) map.set(normalizedType, new Set());
  map.get(normalizedType).add(normalizedValue);
  return normalizedValue;
}

function inferKnownSelectorType(raw) {
  const clean = String(raw || '').trim();
  if (!clean) return '';
  if (isValidReconEmail(clean)) return 'email';
  const compact = clean.replace(/[^\d+]/g, '');
  if (isValidReconPhone(compact)) return 'phone';
  if (clean.startsWith('@')) return 'username';
  if (/[a-z0-9_]{2,}/i.test(clean) && !clean.includes(' ')) return 'username';
  return 'name';
}

function selectorQueryPriorityWeight(selectorType) {
  const cleanType = String(selectorType || '').trim().toLowerCase();
  if (cleanType === 'email' || cleanType === 'phone') return 6;
  if (cleanType === 'username' || cleanType === 'name') return 2;
  if (cleanType === 'location') return 1;
  return 1;
}

function toLikelyNameCase(value) {
  return String(value || '')
    .trim()
    .split(/\s+/g)
    .filter(Boolean)
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1).toLowerCase())
    .join(' ');
}

function buildLikelyNameFromHandle(rawHandle, knownNameTokens = []) {
  const handle = String(rawHandle || '').trim().replace(/^@+/, '');
  if (!handle) return '';
  const direct = handle.replace(/[._-]+/g, ' ').replace(/\s+/g, ' ').trim();
  const directParts = direct.split(' ').filter(Boolean);
  if (directParts.length >= 2 && directParts.every((part) => /^[a-z][a-z'-]{1,}$/i.test(part))) {
    const candidate = toLikelyNameCase(directParts.join(' '));
    return isLikelyPersonName(candidate) ? candidate : '';
  }
  let compact = handle.toLowerCase().replace(/[^a-z]/g, '');
  if (!compact || compact.length < 4) return '';
  compact = compact.replace(/(?:official|real|thereal|the|_)+$/g, '');
  compact = compact.replace(/(?:usa|canada|can|uk|ca|us)+$/g, '');
  if (compact.length < 4) return '';
  const tokenPool = (Array.isArray(knownNameTokens) ? knownNameTokens : [])
    .map((token) => String(token || '').trim().toLowerCase())
    .filter((token) => token.length >= 3);
  tokenPool.sort((a, b) => b.length - a.length);
  for (const first of tokenPool) {
    const idx = compact.indexOf(first);
    if (idx < 0) continue;
    const remaining = `${compact.slice(0, idx)} ${compact.slice(idx + first.length)}`.trim().replace(/\s+/g, ' ');
    if (!remaining) continue;
    const second = tokenPool.find((token) => remaining.includes(token) && token !== first);
    if (!second) continue;
    const candidate = toLikelyNameCase(`${first} ${second}`);
    if (isLikelyPersonName(candidate)) return candidate;
  }
  return '';
}

function collectLikelyNameSummary(payload) {
  const rows = Array.isArray(payload?.results) ? payload.results : [];
  const selectors = Array.isArray(payload?.selectors) ? payload.selectors : [];
  const osintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
  const personDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
  const leads = Array.isArray(payload?.leads) ? payload.leads : [];
  const stats = new Map();
  const explicitNameTokens = new Set();

  const statKey = (name) => String(name || '').trim().toLowerCase();
  const ensure = (name) => {
    const key = statKey(name);
    if (!key) return null;
    if (!stats.has(key)) {
      stats.set(key, {
        name: toLikelyNameCase(name),
        score: 0,
        sources: new Set(),
        profiles: new Set(),
        evidence: new Set(),
      });
    }
    return stats.get(key);
  };

  const nameFieldWeight = (fieldType) => {
    const kind = String(fieldType || '').trim().toLowerCase();
    if (kind === 'name') return 18;
    if (kind === 'username') return 7;
    if (kind === 'email') return 6;
    return 2;
  };

  const addNameEvidence = (
    rawName,
    {
      fieldType = 'name',
      queryType = '',
      sourceKey = '',
      profileKey = '',
      evidenceKey = '',
    } = {},
  ) => {
    const normalized = normalizeKnownSelectorValue('name', rawName);
    if (!normalized || !isLikelyPersonName(normalized)) return;
    const record = ensure(normalized);
    if (!record) return;
    const base = nameFieldWeight(fieldType);
    const queryWeight = selectorQueryPriorityWeight(queryType);
    const weighted = base * (1 + (queryWeight * 0.35));
    record.score += weighted;
    const src = String(sourceKey || '').trim().toLowerCase();
    if (src) record.sources.add(src);
    const profile = String(profileKey || '').trim().toLowerCase();
    if (profile) record.profiles.add(profile);
    const evidence = String(evidenceKey || '').trim().toLowerCase();
    if (evidence) record.evidence.add(evidence);
    for (const token of normalized.toLowerCase().split(/\s+/g)) {
      if (token.length >= 3) explicitNameTokens.add(token);
    }
  };

  const addHandleEvidence = (rawHandle, options = {}) => {
    const candidate = buildLikelyNameFromHandle(rawHandle, Array.from(explicitNameTokens));
    if (!candidate) return;
    addNameEvidence(candidate, options);
  };

  const addEmailEvidence = (rawEmail, options = {}) => {
    const email = String(rawEmail || '').trim().toLowerCase();
    if (!isValidReconEmail(email)) return;
    const local = email.split('@')[0] || '';
    if (!local) return;
    addHandleEvidence(local, { ...options, fieldType: 'email' });
  };

  for (const selector of selectors) {
    const selectorType = String(selector?.type || '').trim().toLowerCase();
    const selectorValue = String(selector?.value || '').trim();
    const profileKey = `query|${selectorType}|${selectorValue.toLowerCase()}`;
    if (selectorType === 'name') addNameEvidence(selectorValue, { fieldType: 'name', queryType: selectorType, sourceKey: 'query_input', profileKey, evidenceKey: profileKey });
    else if (selectorType === 'username') addHandleEvidence(selectorValue, { fieldType: 'username', queryType: selectorType, sourceKey: 'query_input', profileKey, evidenceKey: profileKey });
    else if (selectorType === 'email') addEmailEvidence(selectorValue, { queryType: selectorType, sourceKey: 'query_input', profileKey, evidenceKey: profileKey });
  }

  for (const profile of personDataProfiles) {
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const profileKey = [
      String(profile?.id || '').trim().toLowerCase(),
      String(profile?.full_name || '').trim().toLowerCase(),
      String(profile?.query_value || '').trim().toLowerCase(),
    ].join('|');
    addNameEvidence(profile?.full_name, { fieldType: 'name', queryType, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|name|${profileKey}` });
    addEmailEvidence(profile?.professional_email || profile?.work_email, { queryType, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|professional_email|${profileKey}` });
    for (const email of (Array.isArray(profile?.personal_emails) ? profile.personal_emails : [])) {
      addEmailEvidence(email, { queryType, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|personal_email|${profileKey}|${String(email || '').trim().toLowerCase()}` });
    }
    const usernames = [profile?.username, profile?.linkedin_username, profile?.twitter_username];
    for (const handle of usernames) {
      addHandleEvidence(handle, { fieldType: 'username', queryType, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|username|${profileKey}|${String(handle || '').trim().toLowerCase()}` });
    }
  }

  for (const profile of osintProfiles) {
    const moduleName = String(profile?.module || '').trim().toLowerCase() || 'osint';
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const profileKey = [
      moduleName,
      String(profile?.profile_url || '').trim().toLowerCase(),
      String(profile?.website || '').trim().toLowerCase(),
      String(profile?.username || '').trim().toLowerCase(),
      String(profile?.email || '').trim().toLowerCase(),
    ].join('|');
    addNameEvidence(profile?.name, { fieldType: 'name', queryType, sourceKey: `osint:${moduleName}`, profileKey, evidenceKey: `osint:${moduleName}|name|${profileKey}` });
    addNameEvidence(`${profile?.first_name || ''} ${profile?.last_name || ''}`, { fieldType: 'name', queryType, sourceKey: `osint:${moduleName}`, profileKey, evidenceKey: `osint:${moduleName}|first_last|${profileKey}` });
    addHandleEvidence(profile?.username, { fieldType: 'username', queryType, sourceKey: `osint:${moduleName}`, profileKey, evidenceKey: `osint:${moduleName}|username|${profileKey}` });
    addEmailEvidence(profile?.email, { queryType, sourceKey: `osint:${moduleName}`, profileKey, evidenceKey: `osint:${moduleName}|email|${profileKey}` });
    addEmailEvidence(profile?.email_hint, { queryType, sourceKey: `osint:${moduleName}`, profileKey, evidenceKey: `osint:${moduleName}|email_hint|${profileKey}` });
  }

  for (const row of rows) {
    const source = String(row?.source || row?.site || row?.site_key || 'result').trim().toLowerCase();
    const selectorType = String(row?.selector_type || '').trim().toLowerCase();
    const selectorValue = String(row?.selector || '').trim();
    const profileKey = String(row?.profile_url || `${source}|${selectorType}|${selectorValue}`).trim().toLowerCase();
    addNameEvidence(row?.profile_name || row?.title, { fieldType: 'name', queryType: selectorType, sourceKey: `result:${source}`, profileKey, evidenceKey: `result:${source}|name|${profileKey}` });
    if (selectorType === 'name') addNameEvidence(selectorValue, { fieldType: 'name', queryType: selectorType, sourceKey: `result:${source}`, profileKey, evidenceKey: `result:${source}|selector_name|${profileKey}` });
    if (selectorType === 'username') addHandleEvidence(selectorValue, { fieldType: 'username', queryType: selectorType, sourceKey: `result:${source}`, profileKey, evidenceKey: `result:${source}|selector_username|${profileKey}` });
    if (selectorType === 'email') addEmailEvidence(selectorValue, { queryType: selectorType, sourceKey: `result:${source}`, profileKey, evidenceKey: `result:${source}|selector_email|${profileKey}` });
  }

  for (const lead of leads) {
    const leadType = String(lead?.lead_type || '').trim().toLowerCase();
    if (leadType !== 'attribute') continue;
    const attribute = String(lead?.attribute || '').trim().toLowerCase();
    const value = String(lead?.value || '').trim();
    if (!value) continue;
    const source = String(lead?.source || 'lead').trim().toLowerCase();
    const profileKey = `${source}|${String(lead?.profile_name || lead?.profile_url || '').trim().toLowerCase() || value.toLowerCase()}`;
    if (attribute.includes('name')) addNameEvidence(value, { fieldType: 'name', sourceKey: `lead:${source}`, profileKey, evidenceKey: `lead:${source}|name|${value.toLowerCase()}|${profileKey}` });
    else if (attribute.includes('username') || attribute.includes('handle')) addHandleEvidence(value, { fieldType: 'username', sourceKey: `lead:${source}`, profileKey, evidenceKey: `lead:${source}|username|${value.toLowerCase()}|${profileKey}` });
    else if (attribute.includes('email')) addEmailEvidence(value, { sourceKey: `lead:${source}`, profileKey, evidenceKey: `lead:${source}|email|${value.toLowerCase()}|${profileKey}` });
  }

  const ranked = Array.from(stats.values())
    .map((item) => {
      const diversityBonus = (item.sources.size * 16) + (item.profiles.size * 7) + (item.evidence.size * 1.5);
      return { ...item, totalScore: item.score + diversityBonus };
    })
    .sort((a, b) => b.totalScore - a.totalScore || b.profiles.size - a.profiles.size || a.name.localeCompare(b.name));
  const top = ranked[0] || null;
  return {
    name: top?.name || '',
    candidates: ranked,
  };
}

function formatLikelyNameForCaseNotes(rawName) {
  const normalized = normalizeKnownSelectorValue('name', rawName);
  if (!normalized || !isLikelyPersonName(normalized)) return '';
  const parts = normalized.split(/\s+/g).filter(Boolean);
  if (parts.length < 2) return toLikelyNameCase(normalized);
  const lastName = String(parts[parts.length - 1] || '').replace(/[^A-Za-z'-]/g, '');
  const firstNames = parts.slice(0, -1).join(' ').trim();
  if (!lastName || !firstNames) return toLikelyNameCase(normalized);
  return `${lastName.toUpperCase()}, ${toLikelyNameCase(firstNames)}`;
}

function calculatedLikelyNameForCaseNotes() {
  const payload = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
  const summary = collectLikelyNameSummary(payload);
  return formatLikelyNameForCaseNotes(summary?.name || '');
}

function maybeAutofillCaseNotesLikelyName(options = {}) {
  if (!(caseNotesNameInput instanceof HTMLInputElement)) return;
  if (!(caseNotesModal instanceof HTMLElement) || caseNotesModal.classList.contains('hidden')) return;
  const force = options?.force === true;
  const candidate = calculatedLikelyNameForCaseNotes();
  if (!candidate) return;
  const current = String(caseNotesNameInput.value || '').trim();
  const previousAuto = String(lastAutofilledCaseNotesName || '').trim();
  const canReplace = force
    || !current
    || (previousAuto && current.toLowerCase() === previousAuto.toLowerCase());
  if (!canReplace) return;
  caseNotesNameInput.value = candidate;
  lastAutofilledCaseNotesName = candidate;
  caseNotesNameInput.classList.add('case-notes-name-autofill');
}

function maybeAutofillCaseNotesLikelyLocation(options = {}) {
  if (!(caseNotesLocationInput instanceof HTMLInputElement)) return;
  if (!(caseNotesModal instanceof HTMLElement) || caseNotesModal.classList.contains('hidden')) return;
  const force = options?.force === true;
  const candidate = inferMostLikelyLocationForCaseNotes(Array.isArray(latestFetchedPosts) && latestFetchedPosts.length ? latestFetchedPosts : latestPosts);
  if (!candidate) return;
  const current = String(caseNotesLocationInput.value || '').trim();
  const previousAuto = String(lastAutofilledCaseNotesLocation || '').trim();
  const canReplace = force
    || !current
    || (previousAuto && current.toLowerCase() === previousAuto.toLowerCase());
  if (!canReplace) return;
  caseNotesLocationInput.value = candidate;
  lastAutofilledCaseNotesLocation = candidate;
}

function syncOpenCaseNotesKnownProfilesFromRecon() {
  if (!(caseNotesModal instanceof HTMLElement) || caseNotesModal.classList.contains('hidden')) return;
  if (!(caseNotesProfilesList instanceof HTMLElement)) return;
  syncKnownProfilesFromForm();
  const discoveredFromRecon = caseNotesMajorProfiles(defaultKnownProfilesFromRecon());
  const discoveredFromPosts = caseNotesMajorProfiles(discoverKnownProfilesFromPosts(Array.isArray(latestFetchedPosts) && latestFetchedPosts.length ? latestFetchedPosts : latestPosts));
  const discoveredKnownProfiles = mergeDiscoveredKnownProfiles(discoveredFromRecon, discoveredFromPosts);
  const manualProfiles = caseNotesMajorProfiles(caseNotesKnownProfiles).filter((profile) => {
    const key = normalizeProfileKey(profile.site, profile.url);
    return !caseNotesAutoProfileKeys.has(key);
  });
  const mergedProfiles = mergeDiscoveredKnownProfiles(manualProfiles, discoveredKnownProfiles);
  caseNotesKnownProfiles = caseNotesMajorProfiles(enrichKnownProfilesWithExtractedImages(mergedProfiles, Array.isArray(latestFetchedPosts) && latestFetchedPosts.length ? latestFetchedPosts : latestPosts));
  caseNotesAutoProfileKeys.clear();
  for (const key of profileKeySetForKnownProfiles(discoveredKnownProfiles)) caseNotesAutoProfileKeys.add(key);
  const currentSubjectValue = caseNotesSubjectImageSelect instanceof HTMLSelectElement
    ? String(caseNotesSubjectImageSelect.value || '').trim()
    : '';
  const selectedSubject = currentSubjectValue || USER_PLACEHOLDER_AVATAR_URL;
  renderCaseNotesSubjectImageOptions(selectedSubject);
  renderCaseNotesSubjectImagePreview(selectedSubject);
  renderCaseNotesProfiles();
}

function collectKnownSelectors(payload) {
  const selectorMap = new Map(KNOWN_SELECTOR_GROUPS.map((type) => [type, new Set()]));
  const selectorStats = new Map();
  const confidenceScoreForType = (selectorType) => {
    const level = selectorConfidenceLevel(selectorType);
    if (level === 'high') return 3;
    if (level === 'medium') return 2;
    return 1;
  };
  const statKeyFor = (type, value) => `${String(type || '').trim().toLowerCase()}|${String(value || '').trim().toLowerCase()}`;
  const ensureStat = (type, value) => {
    const key = statKeyFor(type, value);
    if (!selectorStats.has(key)) {
      selectorStats.set(key, {
        queried: false,
        queryHits: 0,
        querySignal: 0,
        sourceKeys: new Set(),
        profileKeys: new Set(),
        evidenceKeys: new Set(),
        queryConfidenceScore: 0,
        queryConfidenceType: '',
        queryConfidenceValue: '',
      });
    }
    return selectorStats.get(key);
  };
  const trackKnownSelector = (
    type,
    rawValue,
    {
      queried = false,
      queryWeight = 1,
      querySelectorType = '',
      querySelectorValue = '',
      sourceKey = '',
      profileKey = '',
      evidenceKey = '',
    } = {},
  ) => {
    const normalizedType = String(type || '').trim().toLowerCase();
    const normalizedValue = addKnownSelector(selectorMap, normalizedType, rawValue);
    if (!normalizedType || !normalizedValue) return;
    const stat = ensureStat(normalizedType, normalizedValue);
    if (queried) {
      stat.queried = true;
      stat.queryHits += 1;
      stat.querySignal += Number.isFinite(Number(queryWeight)) ? Math.max(0, Number(queryWeight)) : 1;
      const confidenceType = String(querySelectorType || normalizedType).trim().toLowerCase();
      const confidenceValue = String(querySelectorValue || rawValue || '').trim();
      const confidenceScore = confidenceScoreForType(confidenceType);
      if (confidenceScore >= stat.queryConfidenceScore) {
        stat.queryConfidenceScore = confidenceScore;
        stat.queryConfidenceType = confidenceType;
        stat.queryConfidenceValue = confidenceValue;
      }
    }
    const cleanSourceKey = String(sourceKey || '').trim().toLowerCase();
    if (cleanSourceKey) stat.sourceKeys.add(cleanSourceKey);
    const cleanProfileKey = String(profileKey || '').trim().toLowerCase();
    if (cleanProfileKey) stat.profileKeys.add(cleanProfileKey);
    const cleanEvidenceKey = String(evidenceKey || '').trim().toLowerCase();
    if (cleanEvidenceKey) stat.evidenceKeys.add(cleanEvidenceKey);
  };
  const sortByPriority = (type, values) => {
    const typed = String(type || '').trim().toLowerCase();
    const scoreFor = (value) => {
      const stat = selectorStats.get(statKeyFor(typed, value));
      if (!stat) return 0;
      const queriedBoost = stat.queried ? 1_000_000 : 0;
      const queryWeight = Math.min(10_000, stat.querySignal) * 100;
      const sourceDiversity = stat.sourceKeys.size * 1_000;
      const profileFrequency = stat.profileKeys.size * 100;
      const evidenceFrequency = stat.evidenceKeys.size;
      return queriedBoost + queryWeight + sourceDiversity + profileFrequency + evidenceFrequency;
    };
    return [...values].sort((a, b) => scoreFor(b) - scoreFor(a) || a.localeCompare(b));
  };
  const rows = Array.isArray(payload?.results) ? payload.results : [];
  const selectors = Array.isArray(payload?.selectors) ? payload.selectors : [];
  const osintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
  const numverifyProfiles = Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [];
  const personDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
  const leads = Array.isArray(payload?.leads) ? payload.leads : [];

  for (const selector of selectors) {
    const selectorType = String(selector?.type || '').trim().toLowerCase();
    const selectorValue = String(selector?.value || '').trim();
    trackKnownSelector(selector?.type, selector?.value, {
      queried: true,
      queryWeight: selectorQueryPriorityWeight(selectorType),
      querySelectorType: selectorType,
      querySelectorValue: selectorValue,
      sourceKey: 'query_input',
      profileKey: `query_input|${selectorType}|${selectorValue.toLowerCase()}`,
      evidenceKey: `query_input|${selectorType}|${selectorValue.toLowerCase()}`,
    });
  }
  for (const row of rows) {
    const source = String(row?.source || row?.site_key || row?.site || 'result').trim().toLowerCase();
    const selectorType = String(row?.selector_type || '').trim().toLowerCase();
    const selectorValue = String(row?.selector || '').trim();
    const profileUrl = String(row?.profile_url || '').trim().toLowerCase();
    const profileIdentity = profileUrl || `${source}|${selectorType}|${selectorValue.toLowerCase()}`;
    trackKnownSelector(selectorType, selectorValue, {
      queried: true,
      queryWeight: selectorQueryPriorityWeight(selectorType),
      querySelectorType: selectorType,
      querySelectorValue: selectorValue,
      sourceKey: `result:${source}`,
      profileKey: `result:${profileIdentity}`,
      evidenceKey: `result:${source}|${profileIdentity}`,
    });
  }

  for (const profile of osintProfiles) {
    const moduleName = String(profile?.module || '').trim().toLowerCase();
    if (isHibpModuleName(moduleName)) continue;
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const queryValue = String(profile?.query_value || '').trim();
    const profileKey = [
      moduleName || 'osint',
      String(profile?.profile_url || '').trim().toLowerCase(),
      String(profile?.website || '').trim().toLowerCase(),
      String(profile?.username || '').trim().toLowerCase(),
      String(profile?.email || '').trim().toLowerCase(),
      String(profile?.phone || '').trim().toLowerCase(),
      String(profile?.name || '').trim().toLowerCase(),
      String(profile?.title || '').trim().toLowerCase(),
    ].join('|');
    trackKnownSelector('email', profile?.email, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|email|${profileKey}` });
    trackKnownSelector('phone', profile?.phone, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|phone|${profileKey}` });
    trackKnownSelector('username', profile?.username, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|username|${profileKey}` });
    trackKnownSelector('name', profile?.name, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|name|${profileKey}` });
    trackKnownSelector('location', profile?.location, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|location|${profileKey}` });
    trackKnownSelector('phone', profile?.phone_hint, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|phone_hint|${profileKey}` });
    trackKnownSelector('email', profile?.email_hint, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: `osint:${moduleName || 'unknown'}`, profileKey, evidenceKey: `osint:${moduleName}|email_hint|${profileKey}` });
  }

  for (const profile of personDataProfiles) {
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const queryValue = String(profile?.query_value || '').trim();
    const profileKey = [
      String(profile?.id || '').trim().toLowerCase(),
      String(profile?.full_name || '').trim().toLowerCase(),
      String(profile?.query_type || '').trim().toLowerCase(),
      String(profile?.query_value || '').trim().toLowerCase(),
    ].join('|');
    trackKnownSelector('name', profile?.full_name, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|name|${profileKey}` });
    trackKnownSelector('location', profile?.location_name, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|location|${profileKey}` });
    trackKnownSelector('email', profile?.professional_email || profile?.work_email, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|professional_email|${profileKey}` });
    for (const row of (Array.isArray(profile?.personal_emails) ? profile.personal_emails : [])) {
      trackKnownSelector('email', row, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|personal_email|${profileKey}|${String(row || '').trim().toLowerCase()}` });
    }
    trackKnownSelector('phone', profile?.mobile_phone, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|mobile_phone|${profileKey}` });
    for (const row of (Array.isArray(profile?.personal_phones) ? profile.personal_phones : [])) {
      trackKnownSelector('phone', row, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|personal_phone|${profileKey}|${String(row || '').trim().toLowerCase()}` });
    }
    for (const row of (Array.isArray(profile?.professional_phones) ? profile.professional_phones : [])) {
      trackKnownSelector('phone', row, { queried: true, querySelectorType: queryType, querySelectorValue: queryValue, sourceKey: 'pdl', profileKey, evidenceKey: `pdl|professional_phone|${profileKey}|${String(row || '').trim().toLowerCase()}` });
    }
  }

  for (const profile of numverifyProfiles) {
    const queryType = String(profile?.query_type || 'phone').trim().toLowerCase();
    const queryValue = String(profile?.query_value || profile?.number || profile?.international_format || '').trim();
    const profileKey = [
      String(profile?.number || profile?.international_format || profile?.e164 || '').trim().toLowerCase(),
      String(profile?.country_code || '').trim().toLowerCase(),
      String(profile?.carrier || '').trim().toLowerCase(),
    ].join('|');
    trackKnownSelector('phone', profile?.number || profile?.international_format || profile?.e164, {
      queried: true,
      querySelectorType: queryType,
      querySelectorValue: queryValue,
      sourceKey: 'numverify',
      profileKey,
      evidenceKey: `numverify|phone|${profileKey}`,
    });
    trackKnownSelector('location', profile?.location, {
      queried: true,
      querySelectorType: queryType,
      querySelectorValue: queryValue,
      sourceKey: 'numverify',
      profileKey,
      evidenceKey: `numverify|location|${profileKey}`,
    });
  }

  for (const lead of leads) {
    const leadType = String(lead?.lead_type || '').trim().toLowerCase();
    if (leadType !== 'attribute') continue;
    const attr = String(lead?.attribute || '').trim().toLowerCase();
    const value = String(lead?.value || '').trim();
    if (!value) continue;
    if (attr.includes('company') || attr.includes('breach') || attr.includes('site') || attr.includes('job title') || attr === 'title') continue;
    const leadSource = String(lead?.source || 'lead').trim().toLowerCase();
    const profileName = String(lead?.profile_name || '').trim().toLowerCase();
    const leadProfileUrl = String(lead?.profile_url || '').trim().toLowerCase();
    const profileKey = `${leadSource}|${profileName || leadProfileUrl || value.toLowerCase()}`;
    const evidenceKey = `${leadSource}|${attr}|${value.toLowerCase()}|${profileKey}`;
    if (attr.includes('email')) trackKnownSelector('email', value, { sourceKey: `lead:${leadSource}`, profileKey, evidenceKey });
    else if (attr.includes('phone')) trackKnownSelector('phone', value, { sourceKey: `lead:${leadSource}`, profileKey, evidenceKey });
    else if (attr.includes('name')) trackKnownSelector('name', value, { sourceKey: `lead:${leadSource}`, profileKey, evidenceKey });
    else if (attr.includes('location')) trackKnownSelector('location', value, { sourceKey: `lead:${leadSource}`, profileKey, evidenceKey });
    else trackKnownSelector(inferKnownSelectorType(value), value, { sourceKey: `lead:${leadSource}`, profileKey, evidenceKey });
  }

  return Object.fromEntries(
    KNOWN_SELECTOR_GROUPS.map((type) => [
      type,
      sortByPriority(type, Array.from(selectorMap.get(type) || []))
        .map((value) => {
          const stat = selectorStats.get(statKeyFor(type, value));
          return {
            value,
            confidence_source_type: String(stat?.queryConfidenceType || type).trim().toLowerCase(),
            confidence_source_value: String(stat?.queryConfidenceValue || value).trim(),
          };
        }),
    ]),
  );
}

function titleCaseLabel(value) {
  return String(value || '')
    .trim()
    .split(/[\s_-]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(' ');
}

function parseTimelineDateValue(value) {
  if (value === null || value === undefined) return null;
  if (value instanceof Date && !Number.isNaN(value.getTime())) return value;
  if (typeof value === 'number' && Number.isFinite(value)) {
    const abs = Math.abs(value);
    const asMillis = abs > 1e12 ? value : (abs > 1e9 ? value * 1000 : NaN);
    if (Number.isFinite(asMillis)) {
      const date = new Date(asMillis);
      if (!Number.isNaN(date.getTime())) return date;
    }
    return null;
  }
  const text = String(value).trim();
  if (!text) return null;
  if (/^\d{10}$/.test(text) || /^\d{13}$/.test(text)) {
    const numeric = Number(text);
    if (Number.isFinite(numeric)) {
      const date = new Date(text.length === 13 ? numeric : numeric * 1000);
      if (!Number.isNaN(date.getTime())) return date;
    }
  }
  const parsed = new Date(text);
  if (Number.isNaN(parsed.getTime())) return null;
  const year = parsed.getUTCFullYear();
  if (year < 1970 || year > 2105) return null;
  return parsed;
}

function timelineKeyLooksRelevant(pathKey) {
  const key = String(pathKey || '').toLowerCase();
  if (!key) return false;
  const hints = [
    'date', 'time', 'seen', 'last_seen', 'last active', 'active', 'created', 'creation', 'registered',
    'joined', 'signup', 'review', 'comment', 'post', 'activity', 'updated', 'update', 'login',
    'breach', 'timeline',
  ];
  return hints.some((hint) => key.includes(hint));
}

function timelineActivityLabel(pathKey) {
  const key = String(pathKey || '').toLowerCase();
  if (key.includes('creation') || key.includes('created') || key.includes('registered') || key.includes('joined') || key.includes('signup')) {
    return 'Account Created';
  }
  if (key.includes('last_seen') || key.includes('last seen') || key.includes('last_active') || key.includes('last active') || key.includes('seen') || key.includes('active')) {
    return 'Last Seen';
  }
  if (key.includes('review')) return 'Review Left';
  if (key.includes('comment')) return 'Comment Activity';
  if (key.includes('post')) return 'Post Activity';
  if (key.includes('login')) return 'Login Activity';
  if (key.includes('update')) return 'Updated Activity';
  const leaf = key.split('.').pop() || key;
  return titleCaseLabel(leaf) || 'Observed Activity';
}

function collectTimelineDateEntries(value, path = '', output = []) {
  if (value === null || value === undefined) return output;
  if (Array.isArray(value)) {
    const max = Math.min(value.length, 30);
    for (let index = 0; index < max; index += 1) {
      const nextPath = path ? `${path}[${index}]` : `[${index}]`;
      collectTimelineDateEntries(value[index], nextPath, output);
    }
    return output;
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value);
    for (const [rawKey, child] of entries) {
      const key = String(rawKey || '').trim();
      if (!key) continue;
      const nextPath = path ? `${path}.${key}` : key;
      collectTimelineDateEntries(child, nextPath, output);
    }
    return output;
  }
  const parsed = parseTimelineDateValue(value);
  if (!parsed) return output;
  if (!timelineKeyLooksRelevant(path)) return output;
  output.push({ path, date: parsed, raw: value });
  return output;
}

function firstHttpUrlFromObject(value) {
  if (value === null || value === undefined) return '';
  if (typeof value === 'string') {
    const text = value.trim();
    return /^https?:\/\//i.test(text) ? text : '';
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = firstHttpUrlFromObject(item);
      if (found) return found;
    }
    return '';
  }
  if (typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      const lower = String(key || '').toLowerCase();
      if (!lower.includes('url') && !lower.includes('website') && !lower.includes('link')) continue;
      const found = firstHttpUrlFromObject(child);
      if (found) return found;
    }
    for (const child of Object.values(value)) {
      const found = firstHttpUrlFromObject(child);
      if (found) return found;
    }
  }
  return '';
}

function entityGraphExternalUrlsFromPdlProfile(profile) {
  if (!profile || typeof profile !== 'object') return [];
  const candidates = [
    profile?.linkedin_url,
    profile?.facebook_url,
    profile?.twitter_url,
    profile?.github_url,
    profile?.work_email_provider_url,
  ];
  if (Array.isArray(profile?.profile_urls)) {
    for (const item of profile.profile_urls) candidates.push(item);
  }
  const values = [];
  const seen = new Set();
  for (const candidate of candidates) {
    const url = normalizeExternalUrl(candidate);
    if (!url) continue;
    const key = url.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    values.push(url);
  }
  return values;
}

function timelineSourceDisplayName(event) {
  const rawSite = String(event?.site || event?.module || '').trim();
  const normalized = normalizePlatformName(rawSite);
  if (normalized) return platformDisplayName(normalized);
  const domain = profileDomain(event?.profileUrl);
  if (domain) {
    const root = domain.split('.')[0] || domain;
    return titleCaseLabel(root);
  }
  return titleCaseLabel(rawSite) || 'Source';
}

function timelineActionCode(actionLabel) {
  const action = String(actionLabel || '').trim().toLowerCase();
  if (action.includes('account created')) return 'AC';
  if (action.includes('last seen')) return 'LS';
  if (action.includes('review')) return 'RV';
  if (action.includes('comment')) return 'CM';
  if (action.includes('post')) return 'PO';
  if (action.includes('login')) return 'LG';
  if (action.includes('update')) return 'UP';
  if (action.includes('geo') || action.includes('route')) return 'GE';
  return 'EV';
}

function timelineSourceIconMarkup(event) {
  return faviconMarkup(event?.site, event?.profileUrl)
    || `<span class="timeline-source-fallback" aria-hidden="true">${escapeHtml(timelineSourceDisplayName(event).slice(0, 1).toUpperCase())}</span>`;
}

function collectOsintTimelineModel() {
  const profiles = Array.isArray(reconOsintProfiles) ? reconOsintProfiles : [];
  const specRows = Array.isArray(reconOsintSpecResults) ? reconOsintSpecResults : [];
  const events = [];
  const selectors = new Map();
  const profileLookup = new Map();
  const seenEvents = new Set();

  const selectorKeyFor = (selectorType, selectorValue) => {
    const type = String(selectorType || '').trim().toLowerCase() || 'selector';
    const value = String(selectorValue || '').trim();
    return `${type}|${value.toLowerCase()}`;
  };

  const addSelector = (selectorType, selectorValue) => {
    const key = selectorKeyFor(selectorType, selectorValue);
    if (!selectors.has(key)) {
      selectors.set(key, {
        selectorType: String(selectorType || '').trim().toLowerCase() || 'selector',
        selectorValue: String(selectorValue || '').trim() || 'unknown',
      });
    }
    return key;
  };

  const addEvent = (event) => {
    if (!(event?.date instanceof Date) || Number.isNaN(event.date.getTime())) return;
    const selectorType = String(event.selectorType || '').trim().toLowerCase() || 'selector';
    const selectorValue = String(event.selectorValue || '').trim() || 'unknown';
    const selectorKey = addSelector(selectorType, selectorValue);
    const label = String(event.label || '').trim() || 'Observed Activity';
    const moduleName = String(event.module || '').trim().toLowerCase() || 'osint';
    const profileUrl = normalizeExternalUrl(event.profileUrl);
    const dedupeKey = `${selectorKey}|${moduleName}|${label.toLowerCase()}|${event.date.toISOString()}|${profileUrl.toLowerCase()}`;
    if (seenEvents.has(dedupeKey)) return;
    seenEvents.add(dedupeKey);
    events.push({
      selectorKey,
      selectorType,
      selectorValue,
      label,
      module: String(event.module || '').trim() || 'OSINT',
      profileUrl,
      site: String(event.site || event.module || '').trim() || 'osint',
      date: event.date,
      detail: String(event.detail || '').trim(),
    });
  };

  for (const profile of profiles) {
    const selectorType = String(profile?.query_type || '').trim();
    const selectorValue = String(profile?.query_value || '').trim();
    const moduleName = String(profile?.module || '').trim() || 'osint';
    const profileUrl = normalizeExternalUrl(profile?.profile_url || profile?.website || '');
    const lookupKey = `${selectorKeyFor(selectorType, selectorValue)}|${moduleName.toLowerCase()}`;
    if (!profileLookup.has(lookupKey)) profileLookup.set(lookupKey, profile);
    addSelector(selectorType, selectorValue);

    const creationDate = parseTimelineDateValue(profile?.creation_date);
    if (creationDate) {
      addEvent({
        selectorType,
        selectorValue,
        module: moduleName,
        profileUrl,
        site: moduleName,
        date: creationDate,
        label: 'Account Created',
      });
    }
    const lastSeen = parseTimelineDateValue(profile?.last_seen);
    if (lastSeen) {
      addEvent({
        selectorType,
        selectorValue,
        module: moduleName,
        profileUrl,
        site: moduleName,
        date: lastSeen,
        label: 'Last Seen',
      });
    }
    const geoSignals = Array.isArray(profile?.geo_signals) ? profile.geo_signals : [];
    for (const signal of geoSignals) {
      const signalDate = parseTimelineDateValue(signal?.timestamp || signal?.date || signal?.datetime);
      if (!signalDate) continue;
      const signalKind = String(signal?.kind || '').trim().toLowerCase();
      const pathText = String(signal?.path || '').trim();
      const detailText = String(signal?.detail || '').trim();
      addEvent({
        selectorType,
        selectorValue,
        module: moduleName,
        profileUrl,
        site: moduleName,
        date: signalDate,
        label: signalKind === 'polyline' ? 'Route Activity' : 'Geo Activity',
        detail: [pathText, detailText].filter(Boolean).join(' • '),
      });
    }
  }

  for (const row of specRows) {
    const selectorType = String(row?.query_type || '').trim();
    const selectorValue = String(row?.query_value || '').trim();
    const moduleName = String(row?.module || '').trim() || 'osint';
    const selectorKey = selectorKeyFor(selectorType, selectorValue);
    const lookupKey = `${selectorKey}|${moduleName.toLowerCase()}`;
    const linkedProfile = profileLookup.get(lookupKey);
    const parsedValues = row?.parsed_values && typeof row.parsed_values === 'object' ? row.parsed_values : {};
    const specFormat = row?.spec_format && typeof row.spec_format === 'object' ? row.spec_format : {};
    const timelineEntries = collectTimelineDateEntries(parsedValues);
    if (!timelineEntries.length) collectTimelineDateEntries(specFormat, 'spec', timelineEntries);
    addSelector(selectorType, selectorValue);

    const profileUrl = normalizeExternalUrl(linkedProfile?.profile_url || linkedProfile?.website || firstHttpUrlFromObject(parsedValues) || firstHttpUrlFromObject(specFormat));
    for (const entry of timelineEntries) {
      addEvent({
        selectorType,
        selectorValue,
        module: moduleName,
        profileUrl,
        site: moduleName,
        date: entry.date,
        label: timelineActivityLabel(entry.path),
        detail: entry.path,
      });
    }
  }

  events.sort((a, b) => b.date.getTime() - a.date.getTime());
  const selectorTimeline = new Map();
  for (const event of events) {
    const row = selectorTimeline.get(event.selectorKey) || {
      earliest: null,
      latest: null,
      totalEvents: 0,
    };
    row.totalEvents += 1;
    if (!row.earliest || event.date.getTime() < row.earliest.date.getTime()) row.earliest = event;
    if (!row.latest || event.date.getTime() > row.latest.date.getTime()) row.latest = event;
    selectorTimeline.set(event.selectorKey, row);
  }

  const selectorRanges = [];
  for (const [selectorKey, selector] of selectors.entries()) {
    const timeline = selectorTimeline.get(selectorKey) || {};
    selectorRanges.push({
      selectorKey,
      selectorType: selector.selectorType,
      selectorValue: selector.selectorValue,
      earliest: timeline.earliest || null,
      latest: timeline.latest || null,
      totalEvents: Number.isFinite(timeline.totalEvents) ? timeline.totalEvents : 0,
    });
  }
  selectorRanges.sort((a, b) => {
    if (!a.earliest && !b.earliest) return a.selectorValue.localeCompare(b.selectorValue);
    if (!a.earliest) return 1;
    if (!b.earliest) return -1;
    return a.earliest.date.getTime() - b.earliest.date.getTime();
  });

  return { events, selectorRanges };
}

function renderFootprintTimeline() {
  if (
    !(footprintTimelineSummary instanceof HTMLElement)
    || !(footprintTimelineSummaryText instanceof HTMLElement)
    || !(footprintTimelineEarliest instanceof HTMLElement)
    || !(footprintTimelineEvents instanceof HTMLElement)
    || !(footprintTimelineEmpty instanceof HTMLElement)
  ) {
    return;
  }

  const model = collectOsintTimelineModel();
  const events = model.events;
  const selectorRanges = model.selectorRanges;
  const selectorCount = selectorRanges.length;

  if (!events.length) {
    footprintTimelineSummary.textContent = selectorCount
      ? `${selectorCount} selector${selectorCount === 1 ? '' : 's'} • 0 events`
      : 'No OSINT timeline data';
    footprintTimelineSummaryText.textContent = selectorCount
      ? 'Selectors were detected but no date-stamped activity was returned from OSINT Industries.'
      : 'Run Digital Footprint recon to map OSINT Industries activity signals.';
    footprintTimelineEarliest.innerHTML = selectorRanges.length
      ? selectorRanges.map((row) => `<article class="timeline-earliest-card"><p>${escapeHtml(formatSelectorLabel(row.selectorType, row.selectorValue))}</p><strong>No dated observation</strong></article>`).join('')
      : '';
    footprintTimelineEvents.innerHTML = '';
    footprintTimelineEmpty.classList.remove('hidden');
    return;
  }

  const enriched = events.map((event) => ({
    ...event,
    sourceName: timelineSourceDisplayName(event),
    actionLabel: String(event.label || '').trim() || 'Unknown activity',
    moduleName: String(event.module || '').trim() || 'unknown',
    selectorLabel: formatSelectorLabel(event.selectorType, event.selectorValue),
  }));

  const sourceCounts = new Map();
  const actionCounts = new Map();
  let linkedProfilesTotal = 0;
  for (const event of enriched) {
    sourceCounts.set(event.sourceName, (sourceCounts.get(event.sourceName) || 0) + 1);
    actionCounts.set(event.actionLabel, (actionCounts.get(event.actionLabel) || 0) + 1);
    if (event.profileUrl) linkedProfilesTotal += 1;
  }
  for (const source of Array.from(activeTimelineSources)) {
    if (!sourceCounts.has(source)) activeTimelineSources.delete(source);
  }
  for (const action of Array.from(activeTimelineActions)) {
    if (!actionCounts.has(action)) activeTimelineActions.delete(action);
  }
  if (!activeTimelineSources.size) {
    for (const source of sourceCounts.keys()) activeTimelineSources.add(source);
  }
  if (!activeTimelineActions.size) {
    for (const action of actionCounts.keys()) activeTimelineActions.add(action);
  }

  const query = timelineSelectorQuery.trim().toLowerCase();
  const filteredEvents = enriched.filter((event) => {
    if (!activeTimelineSources.has(event.sourceName)) return false;
    if (!activeTimelineActions.has(event.actionLabel)) return false;
    if (timelineShowOnlyLinked && !event.profileUrl) return false;
    if (!query) return true;
    const haystack = [
      event.sourceName,
      event.moduleName,
      event.actionLabel,
      event.selectorLabel,
      event.selectorType,
      event.selectorValue,
      event.detail,
    ].join(' ').toLowerCase();
    return haystack.includes(query);
  });

  const sourceFilterActive = activeTimelineSources.size !== sourceCounts.size;
  const actionFilterActive = activeTimelineActions.size !== actionCounts.size;
  const queryFilterActive = Boolean(query);
  const linkFilterActive = timelineShowOnlyLinked;
  const filteredCount = filteredEvents.length;
  const hasActiveFilters = sourceFilterActive || actionFilterActive || queryFilterActive || linkFilterActive;

  footprintTimelineSummary.textContent = `${events.length} event${events.length === 1 ? '' : 's'} • ${selectorCount} selector${selectorCount === 1 ? '' : 's'}${hasActiveFilters ? ` • showing ${filteredCount}` : ''}`;
  footprintTimelineSummaryText.textContent = hasActiveFilters
    ? 'Filters active. Review is scoped to the visible events below.'
    : 'Chronological OSINT activity feed from profile creation, last seen, and other timestamped enrichment fields.';
  footprintTimelineEmpty.classList.add('hidden');

  footprintTimelineEarliest.innerHTML = selectorRanges.map((row) => {
    const selectorLabel = formatSelectorLabel(row.selectorType, row.selectorValue);
    if (!row.earliest || !row.latest) {
      return `
        <article class="timeline-earliest-card">
          <header>
            <p>${escapeHtml(selectorLabel)}</p>
            <strong>No dated observation</strong>
          </header>
          <span>OSINT returned no usable timeline fields for this selector.</span>
        </article>
      `;
    }
    const spanDays = Math.max(1, Math.round((row.latest.date.getTime() - row.earliest.date.getTime()) / 86400000) + 1);
    return `
      <article class="timeline-earliest-card">
        <header>
          <p>${escapeHtml(selectorLabel)}</p>
          <span class="timeline-selector-event-total">${row.totalEvents} event${row.totalEvents === 1 ? '' : 's'}</span>
        </header>
        <div class="timeline-selector-range">
          <div class="timeline-selector-range-row">
            <span>First observed</span>
            <strong>${escapeHtml(formatIsoDateTime(row.earliest.date.toISOString()))}</strong>
            <em>${escapeHtml(`${row.earliest.label} • ${row.earliest.module}`)}</em>
          </div>
          <div class="timeline-selector-range-row">
            <span>Latest activity</span>
            <strong>${escapeHtml(formatIsoDateTime(row.latest.date.toISOString()))}</strong>
            <em>${escapeHtml(`${row.latest.label} • ${row.latest.module}`)}</em>
          </div>
        </div>
        <span>${spanDays} day${spanDays === 1 ? '' : 's'} of observed activity</span>
      </article>
    `;
  }).join('');

  const axisEvents = filteredEvents.length ? filteredEvents : enriched;
  const minTs = Math.min(...axisEvents.map((event) => event.date.getTime()));
  const maxTs = Math.max(...axisEvents.map((event) => event.date.getTime()));
  const daySpan = Math.max(1, Math.round((maxTs - minTs) / 86400000) + 1);
  const topSourceRow = Array.from(sourceCounts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0];
  const topActionRow = Array.from(actionCounts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0];

  const filteredSourceCounts = new Map();
  for (const event of filteredEvents) {
    filteredSourceCounts.set(event.sourceName, (filteredSourceCounts.get(event.sourceName) || 0) + 1);
  }
  const sourceLegend = Array.from((filteredEvents.length ? filteredSourceCounts : sourceCounts).entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 8)
    .map(([source, count]) => `<span class="recon-pill"><span>${escapeHtml(source)}</span><strong>${count}</strong></span>`)
    .join('');
  const eventDensity = new Map();
  for (const event of (filteredEvents.length ? filteredEvents : axisEvents)) {
    const key = dayKey(event.date.toISOString());
    if (!key) continue;
    eventDensity.set(key, (eventDensity.get(key) || 0) + 1);
  }
  const densityRows = Array.from(eventDensity.entries()).sort((a, b) => a[0].localeCompare(b[0]));
  const maxDensity = Math.max(1, ...densityRows.map((row) => row[1]));
  const densityMarkup = densityRows.length
    ? densityRows.map(([key, count]) => {
      const pct = Math.max(10, Math.round((count / maxDensity) * 100));
      return `
        <span class="timeline-density-bar" style="height:${pct}%;" title="${escapeAttr(`${shortDayLabel(key)}: ${count} events`)}" aria-label="${escapeAttr(`${shortDayLabel(key)}: ${count} events`)}"></span>
      `;
    }).join('')
    : '<span class="timeline-density-empty">No visible timeline density</span>';

  const sourceFilters = Array.from(sourceCounts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([source, count]) => {
      const active = activeTimelineSources.has(source);
      return `<button type="button" class="mix-pill mix-filter-pill timeline-filter-pill${active ? ' is-active' : ''}" data-timeline-source="${escapeAttr(source)}"><span>${escapeHtml(source)}</span><strong>${count}</strong></button>`;
    })
    .join('');
  const actionFilters = Array.from(actionCounts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([action, count]) => {
      const active = activeTimelineActions.has(action);
      return `<button type="button" class="mix-pill mix-filter-pill timeline-filter-pill${active ? ' is-active' : ''}" data-timeline-action="${escapeAttr(action)}"><span>${escapeHtml(action)}</span><strong>${count}</strong></button>`;
    })
    .join('');

  const feedRows = [];
  let lastDayKey = '';
  for (const event of filteredEvents) {
    const sourceName = event.sourceName;
    const selectorValue = String(event.selectorValue || '').trim() || 'unknown';
    const actionTitle = `${sourceName} - ${event.actionLabel} (${selectorValue})`;
    const when = formatIsoDateTime(event.date.toISOString());
    const recency = formatRecency(event.date.toISOString());
    const actionCode = timelineActionCode(event.actionLabel);
    const sourceIcon = timelineSourceIconMarkup(event);
    const selectorLabel = event.selectorLabel;
    const eventDayKey = dayKey(event.date.toISOString());
    if (eventDayKey && eventDayKey !== lastDayKey) {
      feedRows.push(`
        <div class="timeline-feed-day">
          <span>${escapeHtml(shortDayLabel(eventDayKey))}</span>
        </div>
      `);
      lastDayKey = eventDayKey;
    }
    const linkMarkup = event.profileUrl
      ? `<a class="timeline-event-link lead-link" href="${escapeAttr(event.profileUrl)}" target="_blank" rel="noopener noreferrer">open profile</a>`
      : '';
    feedRows.push(`
      <article class="timeline-feed-event">
        <div class="timeline-vis-pin">
          <span class="timeline-vis-source">${sourceIcon}</span>
        </div>
        <div class="timeline-vis-card">
          <p class="timeline-vis-title">
            <span class="timeline-action-icon" aria-hidden="true">${escapeHtml(actionCode)}</span>
            <span>${escapeHtml(actionTitle)}</span>
          </p>
          <p class="timeline-vis-meta">${escapeHtml(`${when} • ${recency}`)}</p>
          <div class="recon-pills">
            <span class="recon-pill">${escapeHtml(selectorLabel)}</span>
            <span class="recon-pill">${escapeHtml(sourceName)}</span>
            ${linkMarkup}
          </div>
        </div>
      </article>
    `);
  }

  if (!feedRows.length) {
    feedRows.push(`
      <article class="timeline-filter-empty">
        <strong>No events match current filters</strong>
        <span>Clear filters or widen the selector query to continue review.</span>
      </article>
    `);
  }

  footprintTimelineEvents.innerHTML = `
    <div class="timeline-vis">
      <div class="timeline-factor-grid">
        <article class="timeline-factor-card">
          <p>Visible Events</p>
          <strong>${filteredCount}</strong>
          <span>${events.length === filteredCount ? 'No filters applied' : `${events.length - filteredCount} hidden by filters`}</span>
        </article>
        <article class="timeline-factor-card">
          <p>Date Window</p>
          <strong>${daySpan} day${daySpan === 1 ? '' : 's'}</strong>
          <span>${escapeHtml(`${formatIsoDateTime(new Date(minTs).toISOString())} to ${formatIsoDateTime(new Date(maxTs).toISOString())}`)}</span>
        </article>
        <article class="timeline-factor-card">
          <p>Top Source</p>
          <strong>${escapeHtml(topSourceRow?.[0] || 'Unknown')}</strong>
          <span>${topSourceRow ? `${topSourceRow[1]} event${topSourceRow[1] === 1 ? '' : 's'}` : 'No source data'}</span>
        </article>
        <article class="timeline-factor-card">
          <p>Top Activity</p>
          <strong>${escapeHtml(topActionRow?.[0] || 'Unknown')}</strong>
          <span>${escapeHtml(`${linkedProfilesTotal} linked profile${linkedProfilesTotal === 1 ? '' : 's'}`)}</span>
        </article>
      </div>
      <div class="timeline-filter-panel">
        <div class="timeline-filter-controls">
          <label class="timeline-search">
            <span>Find in timeline</span>
            <input
              type="search"
              data-timeline-query
              value="${escapeAttr(timelineSelectorQuery)}"
              placeholder="selector, source, module, activity"
              autocomplete="off"
            />
          </label>
          <label class="timeline-filter-toggle">
            <input type="checkbox" data-timeline-linked-only ${timelineShowOnlyLinked ? 'checked' : ''} />
            <span>Only events with profile links</span>
          </label>
          <button type="button" class="secondary-btn timeline-filter-reset" data-timeline-reset>Reset filters</button>
        </div>
        <div class="timeline-filter-row">
          <span class="filter-label">Sources</span>
          <div class="type-mix">${sourceFilters}</div>
        </div>
        <div class="timeline-filter-row">
          <span class="filter-label">Activity</span>
          <div class="type-mix">${actionFilters}</div>
        </div>
      </div>
      <div class="timeline-vis-axis">
        <span>${escapeHtml(formatIsoDateTime(new Date(minTs).toISOString()))}</span>
        <span>${escapeHtml(formatIsoDateTime(new Date(maxTs).toISOString()))}</span>
      </div>
      <div class="timeline-density-track" role="img" aria-label="Timeline event density by day">
        ${densityMarkup}
      </div>
      <div class="timeline-vis-track timeline-feed-scroll">
        <div class="timeline-feed-line" aria-hidden="true"></div>
        ${feedRows.join('')}
      </div>
      <div class="timeline-vis-legend">${sourceLegend}</div>
    </div>
  `;
}

function entityGraphNodeTypeLabel(nodeType) {
  if (nodeType === 'selector') return 'Selector';
  if (nodeType === 'site') return 'Platform';
  if (nodeType === 'profile') return 'Profile';
  if (nodeType === 'image') return 'Profile Image';
  return 'Entity';
}

function selectorTypeColorToken(selectorType) {
  const clean = String(selectorType || '').trim().toLowerCase();
  if (clean === 'email') return 'email';
  if (clean === 'phone') return 'phone';
  if (clean === 'username') return 'username';
  if (clean === 'name') return 'name';
  if (clean === 'location') return 'location';
  return 'default';
}

function profileImageHashKey(profile, row) {
  const candidates = [
    profile?.picture_hash, profile?.avatar_hash, profile?.image_hash, profile?.profile_image_hash,
    row?.picture_hash, row?.avatar_hash, row?.image_hash, row?.profile_image_hash,
  ];
  for (const candidate of candidates) {
    const value = String(candidate || '').trim().toLowerCase();
    if (value) return value;
  }
  const imageUrl = normalizeExternalUrl(profile?.picture_url || profile?.avatar_url || row?.picture_url || row?.avatar_url || '');
  if (!imageUrl) return '';
  return `urlhash:${entityGraphHash(imageUrl).toString(16)}`;
}

function entityGraphPlatformLabel(value) {
  const normalized = normalizePlatformName(value);
  if (normalized) return platformDisplayName(normalized);
  return titleCaseLabel(String(value || '').replace(/[_-]+/g, ' ')) || 'Platform';
}

function entityGraphIconKind(value) {
  const clean = String(value || '').trim().toLowerCase();
  if (!clean) return '';
  if (clean.startsWith('email')) return 'email';
  if (clean.startsWith('phone')) return 'phone';
  if (clean === 'username') return 'username';
  if (clean === 'name') return 'name';
  return '';
}

function entityGraphIconMarkup(kind, options = {}) {
  const clean = entityGraphIconKind(kind);
  if (!clean) return '';
  const compact = options?.compact === true;
  const transform = compact ? ' scale(0.8)' : '';
  if (clean === 'username') {
    return `<text class="entity-graph-node-icon entity-graph-node-icon-at${compact ? ' is-compact' : ''}" text-anchor="middle" dominant-baseline="central">@</text>`;
  }
  if (clean === 'email') {
    return `
      <g class="entity-graph-glyph${compact ? ' is-compact' : ''}" transform="${transform}">
        <rect x="-7" y="-4.5" width="14" height="9" rx="1.6" ry="1.6"></rect>
        <path d="M-6.2 -3.2L0 1.1 6.2 -3.2"></path>
      </g>
    `;
  }
  if (clean === 'phone') {
    return `
      <g class="entity-graph-glyph${compact ? ' is-compact' : ''}" transform="${transform}">
        <path d="M-3.8 -6.2c.8-1 2.1-1.2 3.1-.5l1.4 1c.9.6 1.1 1.8.6 2.7l-.8 1.2c1.3 2.1 3.1 3.8 5.2 5.2l1.2-.8c.9-.6 2.1-.3 2.7.6l1 1.4c.7 1 .5 2.3-.5 3.1l-1.2.9c-1 .8-2.3 1.1-3.5.7-2.3-.8-4.8-2.5-7-4.8-2.3-2.3-4-4.7-4.8-7-.4-1.2-.2-2.5.7-3.5z"></path>
      </g>
    `;
  }
  return `
    <g class="entity-graph-glyph${compact ? ' is-compact' : ''}" transform="${transform}">
      <circle cx="0" cy="-3.7" r="3.2"></circle>
      <path d="M-6 6.3c0-3.1 2.7-5.4 6-5.4s6 2.3 6 5.4"></path>
    </g>
  `;
}

function shouldSkipEntityGraphField(fieldName) {
  const clean = String(fieldName || '').trim().toLowerCase();
  if (!clean) return false;
  if (clean === 'title') return true;
  if (clean.includes('creation_date') || clean.includes('created') || clean.includes('creation')) return true;
  if (clean.includes('last_seen') || clean.includes('last seen')) return true;
  return false;
}

function entityGraphAttributeKind(field, value) {
  const cleanField = String(field || '').trim().toLowerCase();
  const cleanValue = String(value || '').trim();
  if (!cleanValue) return 'attribute';
  if (cleanField.includes('url') || cleanField.includes('site') || isHttpUrl(cleanValue)) return 'url';
  if (cleanField.includes('email') || isValidReconEmail(cleanValue)) return 'email';
  if (cleanField.includes('phone') || cleanField.includes('mobile') || cleanField.includes('tel') || isValidReconPhone(cleanValue.replace(/[^\d+]/g, ''))) return 'phone';
  if (cleanField.includes('loc') || cleanField.includes('city') || cleanField.includes('country') || cleanField.includes('address')) return 'location';
  if (cleanField.includes('date') || cleanField.includes('seen') || cleanField.includes('created') || parseTimelineDateValue(cleanValue)) return 'date';
  if (cleanField.includes('name') || cleanField.includes('title')) return 'name';
  if (cleanField.includes('user') || cleanField.includes('handle')) return 'username';
  return 'attribute';
}

function entityGraphAttributeKeyValue(kind, value) {
  const cleanValue = String(value || '').trim();
  if (!cleanValue) return '';
  if (kind === 'url') {
    const normalized = normalizeExternalUrl(cleanValue);
    if (normalized) return profileDomain(normalized) || normalized.toLowerCase();
  }
  if (kind === 'date') {
    const parsed = parseTimelineDateValue(cleanValue);
    if (parsed) return dayKey(parsed.toISOString()) || parsed.toISOString();
  }
  if (kind === 'location') {
    const cleanLocation = _cleanLocationEntityLabel(cleanValue);
    if (!cleanLocation) return '';
    const matches = _resolvedLocationsFromText(cleanLocation, _locationPairsByName());
    const selected = _selectMostSpecificLocationMatch(cleanLocation, matches) || matches[0] || null;
    if (selected?.name) return String(selected.name).trim().toLowerCase();
    return cleanLocation.toLowerCase();
  }
  if (kind === 'phone') return cleanValue.replace(/[^\d+]/g, '');
  return cleanValue.toLowerCase();
}

function entityGraphAttributeLabel(kind, value) {
  const cleanValue = String(value || '').trim();
  if (!cleanValue) return '';
  if (kind === 'url') {
    const normalized = normalizeExternalUrl(cleanValue);
    if (normalized) return profileDomain(normalized) || normalized;
  }
  if (kind === 'date') {
    const parsed = parseTimelineDateValue(cleanValue);
    if (parsed) return formatIsoDateTime(parsed.toISOString());
  }
  if (kind === 'location') {
    const cleanLocation = _cleanLocationEntityLabel(cleanValue);
    if (!cleanLocation) return '';
    const matches = _resolvedLocationsFromText(cleanLocation, _locationPairsByName());
    const selected = _selectMostSpecificLocationMatch(cleanLocation, matches) || matches[0] || null;
    if (selected?.name) return String(selected.name).trim();
    return cleanLocation;
  }
  if (cleanValue.length > 56) return `${cleanValue.slice(0, 53)}...`;
  return cleanValue;
}

function entityGraphHintKeyValue(kind, value) {
  const cleanValue = String(value || '').trim().toLowerCase();
  if (!cleanValue) return '';
  if (kind === 'email') return cleanValue.replace(/\s+/g, '');
  if (kind === 'phone') return cleanValue.replace(/[^\dx+*]/gi, '').replace(/^0+(?=\d)/, '');
  return cleanValue;
}

function entityGraphEmailHintMatches(hintValue, emailValue) {
  const hint = String(hintValue || '').trim().toLowerCase().replace(/\s+/g, '');
  const email = String(emailValue || '').trim().toLowerCase();
  if (!hint || !email || !isValidReconEmail(email) || hint === email) return false;
  const hasMask = /[*xX\u2022\u00B7]/.test(hint);
  const literal = hint.replace(/[*xX\u2022\u00B7]/g, '');
  if (literal.length < 4 || !hint.includes('@')) return false;
  if (!hasMask) return email.includes(hint);
  const escaped = hint.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
  const patternSource = escaped.replace(/[*xX\u2022\u00B7]+/g, '.*');
  if (!patternSource || patternSource === '.*') return false;
  const pattern = new RegExp(`^${patternSource}$`, 'i');
  return pattern.test(email);
}

function entityGraphPhoneHintMatches(hintValue, phoneValue) {
  const hintRaw = String(hintValue || '').trim();
  const phoneDigits = String(phoneValue || '').replace(/[^\d]/g, '');
  if (!hintRaw || !phoneDigits) return false;
  const hint = hintRaw.replace(/\s+/g, '');
  const digitsInHint = hint.replace(/[^\d]/g, '');
  if (digitsInHint.length < 4) return false;
  const hasMask = /[*xX\u2022\u00B7]/.test(hint);
  if (!hasMask) return phoneDigits.includes(digitsInHint);
  const normalizedMask = hint.replace(/[^\dxX*\u2022\u00B7+]/g, '').replace(/[xX\u2022\u00B7]/g, '*').replace(/\+/g, '');
  const escaped = normalizedMask.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
  const patternSource = escaped.replace(/\*+/g, '\\d*').replace(/[^\d\\*]/g, '');
  if (!patternSource || patternSource === '\\d*') return false;
  const pattern = new RegExp(`^${patternSource}$`);
  return pattern.test(phoneDigits);
}

function collectEntityGraphFieldValues(value, path = '', output = []) {
  if (output.length > 64) return output;
  if (value === null || value === undefined) return output;
  if (Array.isArray(value)) {
    const max = Math.min(8, value.length);
    for (let idx = 0; idx < max; idx += 1) collectEntityGraphFieldValues(value[idx], path, output);
    return output;
  }
  if (typeof value === 'object') {
    const entries = Object.entries(value).slice(0, 20);
    for (const [key, child] of entries) {
      const nextPath = path ? `${path}.${key}` : String(key || '').trim();
      if (!nextPath) continue;
      collectEntityGraphFieldValues(child, nextPath, output);
    }
    return output;
  }
  const text = String(value).trim();
  if (!text) return output;
  const lowerPath = String(path || '').toLowerCase();
  if (
    lowerPath.includes('user')
    || lowerPath.includes('name')
    || lowerPath.includes('email')
    || lowerPath.includes('phone')
    || lowerPath.includes('title')
    || lowerPath.includes('location')
    || lowerPath.includes('city')
    || lowerPath.includes('country')
    || lowerPath.includes('url')
    || lowerPath.includes('site')
    || lowerPath.includes('date')
    || lowerPath.includes('seen')
    || lowerPath.includes('create')
  ) {
    output.push({ field: path || 'attribute', value: text });
  }
  return output;
}

function collectEntityGraphModel() {
  if (entityGraphModelCache) return entityGraphModelCache;
  const payload = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
  const selectors = Array.isArray(payload?.selectors) ? payload.selectors : [];
  const resultRows = Array.isArray(payload?.results) ? payload.results : [];
  const numverifyProfiles = Array.isArray(payload?.numverify_profiles) ? payload.numverify_profiles : [];
  const personDataProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
  const profiles = (Array.isArray(reconOsintProfiles) ? reconOsintProfiles : [])
    .filter((row) => !isHibpModuleName(row?.module));
  const specRows = (Array.isArray(reconOsintSpecResults) ? reconOsintSpecResults : [])
    .filter((row) => !isHibpModuleName(row?.module));
  const nodeMap = new Map();
  const edgeMap = new Map();
  const selectorNodeByKey = new Map();
  const siteNodeBySelectorModule = new Map();
  const profileRowByCompositeKey = new Map();
  const selectorIdentityMap = new Map();
  const contactExactNodes = {
    email: new Map(),
    phone: new Map(),
  };
  const contactHintNodes = {
    email: [],
    phone: [],
  };

  const addNode = (id, init = {}) => {
    const cleanId = String(id || '').trim();
    if (!cleanId) return null;
    if (!nodeMap.has(cleanId)) {
      nodeMap.set(cleanId, {
        id: cleanId,
        type: String(init.type || 'attribute').trim().toLowerCase(),
        label: String(init.label || '').trim() || cleanId,
        subType: String(init.subType || '').trim().toLowerCase(),
        detail: String(init.detail || '').trim(),
        url: normalizeExternalUrl(init.url || ''),
        site: String(init.site || '').trim(),
        iconUrl: normalizeExternalUrl(init.iconUrl || ''),
        pictureUrl: normalizeExternalUrl(init.pictureUrl || ''),
        colorToken: String(init.colorToken || '').trim().toLowerCase(),
        degree: 0,
      });
    }
    const node = nodeMap.get(cleanId);
    if (init.label && !node.label) node.label = String(init.label).trim();
    if (init.subType && !node.subType) node.subType = String(init.subType).trim().toLowerCase();
    if (init.detail && !node.detail) node.detail = String(init.detail).trim();
    if (init.url && !node.url) node.url = normalizeExternalUrl(init.url);
    if (init.site && !node.site) node.site = String(init.site).trim();
    if (init.iconUrl && !node.iconUrl) node.iconUrl = normalizeExternalUrl(init.iconUrl);
    if (init.pictureUrl && !node.pictureUrl) node.pictureUrl = normalizeExternalUrl(init.pictureUrl);
    if (init.colorToken && !node.colorToken) node.colorToken = String(init.colorToken).trim().toLowerCase();
    return node;
  };

  const addEdge = (source, target, relation = '', weight = 1) => {
    const sourceId = String(source || '').trim();
    const targetId = String(target || '').trim();
    if (!sourceId || !targetId || sourceId === targetId) return;
    const left = sourceId < targetId ? sourceId : targetId;
    const right = sourceId < targetId ? targetId : sourceId;
    const key = `${left}|${right}|${String(relation || '').trim().toLowerCase()}`;
    const existing = edgeMap.get(key);
    if (existing) {
      existing.weight = Math.max(Number(existing.weight) || 1, Number(weight) || 1);
      return;
    }
    edgeMap.set(key, {
      source: sourceId,
      target: targetId,
      relation: String(relation || '').trim(),
      weight: Number.isFinite(Number(weight)) ? Number(weight) : 1,
    });
  };

  const selectorNodeIdFor = (selectorType, selectorValue) => {
    const type = String(selectorType || '').trim().toLowerCase() || 'selector';
    const value = String(selectorValue || '').trim() || 'unknown';
    const key = `${type}|${value.toLowerCase()}`;
    if (selectorNodeByKey.has(key)) return selectorNodeByKey.get(key);
    const nodeId = `selector:${key}`;
    addNode(nodeId, {
      type: 'selector',
      subType: type,
      label: value,
      detail: `${titleCaseLabel(type)} query`,
      colorToken: selectorTypeColorToken(type),
    });
    selectorNodeByKey.set(key, nodeId);
    selectorIdentityMap.set(nodeId, { type, value });
    return nodeId;
  };

  const siteNodeIdFor = (selectorType, selectorValue, moduleName, profileUrl = '') => {
    const selectorKey = `${String(selectorType || '').trim().toLowerCase()}|${String(selectorValue || '').trim().toLowerCase()}`;
    const siteKey = `${selectorKey}|${String(moduleName || '').trim().toLowerCase()}`;
    if (siteNodeBySelectorModule.has(siteKey)) {
      const existing = siteNodeBySelectorModule.get(siteKey);
      const existingNode = nodeMap.get(existing);
      if (existingNode && profileUrl && !existingNode.url) existingNode.url = normalizeExternalUrl(profileUrl);
      return existing;
    }
    const selectorNodeId = selectorNodeIdFor(selectorType, selectorValue);
    const nodeId = `site:${siteKey}`;
    addNode(nodeId, {
      type: 'site',
      subType: String(moduleName || '').trim().toLowerCase(),
      label: entityGraphPlatformLabel(moduleName),
      detail: 'Identified platform',
      url: profileUrl,
      iconUrl: faviconUrl(moduleName, profileUrl || ''),
    });
    addEdge(selectorNodeId, nodeId, 'identified_platform', 2.4);
    siteNodeBySelectorModule.set(siteKey, nodeId);
    return nodeId;
  };

  const addProfileAttribute = (parentNodeId, fieldName, rawValue) => {
    if (shouldSkipEntityGraphField(fieldName)) return;
    if (!parentNodeId) return;
    const cleanFieldName = String(fieldName || '').trim().toLowerCase();
    const hintField = cleanFieldName.includes('hint');
    const values = Array.isArray(rawValue) ? rawValue : [rawValue];
    const maxValues = Math.min(values.length, 8);
    for (let idx = 0; idx < maxValues; idx += 1) {
      const value = values[idx];
      const clean = String(value || '').trim();
      if (!clean) continue;
      const kind = entityGraphAttributeKind(fieldName, clean);
      const keyValue = hintField
        ? entityGraphHintKeyValue(kind, clean)
        : entityGraphAttributeKeyValue(kind, clean);
      if (!keyValue) continue;
      const nodeId = hintField
        ? `attr:${kind}_hint|${keyValue}`
        : `attr:${kind}|${keyValue}`;
      addNode(nodeId, {
        type: 'attribute',
        subType: hintField ? `${kind}_hint` : kind,
        label: entityGraphAttributeLabel(kind, clean),
        detail: titleCaseLabel(fieldName.replace(/[_-]+/g, ' ')),
        iconUrl: kind === 'url' ? faviconUrl(fieldName, clean) : '',
      });
      addEdge(parentNodeId, nodeId, fieldName);
      if ((kind === 'email' || kind === 'phone') && !hintField) {
        contactExactNodes[kind].set(keyValue, { nodeId, value: clean });
      }
      if ((kind === 'email' || kind === 'phone') && hintField) {
        contactHintNodes[kind].push({ nodeId, value: clean });
      }
    }
  };

  for (const row of resultRows) {
    const source = String(row?.source || '').trim().toLowerCase();
    if (source !== 'osint_industries') continue;
    const moduleName = String(row?.site_key || row?.site || row?.module || '').trim().toLowerCase();
    if (isHibpModuleName(moduleName)) continue;
    const profileUrl = normalizeExternalUrl(row?.profile_url || row?.website || '');
    const selectorType = String(row?.selector_type || '').trim().toLowerCase();
    const selectorValue = String(row?.selector || '').trim().toLowerCase();
    const key = `${selectorType}|${selectorValue}|${moduleName}|${profileUrl.toLowerCase()}`;
    if (!profileRowByCompositeKey.has(key)) profileRowByCompositeKey.set(key, row);
  }

  for (const selector of selectors) {
    selectorNodeIdFor(selector?.type, selector?.value);
  }

  for (const profile of profiles) {
    const moduleName = String(profile?.module || '').trim() || 'OSINT';
    const profileUrl = normalizeExternalUrl(profile?.profile_url || profile?.website || '');
    const siteNodeId = siteNodeIdFor(profile?.query_type, profile?.query_value, moduleName, profileUrl);
    const selectorTypeKey = String(profile?.query_type || '').trim().toLowerCase();
    const selectorValueKey = String(profile?.query_value || '').trim().toLowerCase();
    const moduleKey = moduleName.toLowerCase();
    const profileRow = profileRowByCompositeKey.get(`${selectorTypeKey}|${selectorValueKey}|${moduleKey}|${profileUrl.toLowerCase()}`) || null;
    const pictureUrl = normalizeExternalUrl(profile?.picture_url || profile?.avatar_url || profileRow?.picture_url || profileRow?.avatar_url || '');
    const selectorKey = `${String(profile?.query_type || '').trim().toLowerCase()}|${String(profile?.query_value || '').trim().toLowerCase()}`;
    siteNodeBySelectorModule.set(`${selectorKey}|${moduleName.toLowerCase()}`, siteNodeId);
    addProfileAttribute(siteNodeId, 'username', profile?.username);
    addProfileAttribute(siteNodeId, 'name', profile?.name);
    addProfileAttribute(siteNodeId, 'email', profile?.email);
    addProfileAttribute(siteNodeId, 'phone', profile?.phone);
    addProfileAttribute(siteNodeId, 'location', profile?.location);
    addProfileAttribute(siteNodeId, 'website', profile?.website);
    addProfileAttribute(siteNodeId, 'profile_url', profile?.profile_url);
    addProfileAttribute(siteNodeId, 'email_hint', profile?.email_hint);
    addProfileAttribute(siteNodeId, 'phone_hint', profile?.phone_hint);
    const geoSignals = Array.isArray(profile?.geo_signals) ? profile.geo_signals : [];
    for (const signal of geoSignals.slice(0, 8)) {
      addProfileAttribute(siteNodeId, 'geo_location', signal?.name || signal?.city || signal?.detail || signal?.path);
    }
    const imageHash = profileImageHashKey(profile, profileRow);
    if (imageHash && pictureUrl) {
      const imageNodeId = `image:${imageHash}`;
      addNode(imageNodeId, {
        type: 'image',
        subType: 'profile_image',
        label: '',
        detail: 'Shared profile picture hash',
        pictureUrl,
      });
      addEdge(siteNodeId, imageNodeId, 'profile_image');
    }
  }

  for (const row of specRows) {
    const moduleName = String(row?.module || '').trim() || 'osint';
    const selectorKey = `${String(row?.query_type || '').trim().toLowerCase()}|${String(row?.query_value || '').trim().toLowerCase()}`;
    const siteNodeId = siteNodeBySelectorModule.get(`${selectorKey}|${moduleName.toLowerCase()}`)
      || siteNodeIdFor(
        row?.query_type,
        row?.query_value,
        moduleName,
        firstHttpUrlFromObject(row?.parsed_values) || firstHttpUrlFromObject(row?.spec_format),
      );
    const values = [];
    collectEntityGraphFieldValues(row?.parsed_values, 'parsed', values);
    if (!values.length) collectEntityGraphFieldValues(row?.spec_format, 'spec', values);
    for (const item of values) {
      addProfileAttribute(siteNodeId, item.field, item.value);
    }
  }

  for (const profile of personDataProfiles) {
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const queryValue = String(profile?.query_value || '').trim();
    if (!queryType || !queryValue) continue;
    const externalUrls = entityGraphExternalUrlsFromPdlProfile(profile);
    const primaryUrl = externalUrls[0] || '';
    const siteNodeId = siteNodeIdFor(queryType, queryValue, 'people_data_labs', primaryUrl);
    addProfileAttribute(siteNodeId, 'full_name', profile?.full_name);
    addProfileAttribute(siteNodeId, 'location_name', profile?.location_name);
    addProfileAttribute(siteNodeId, 'job_title', profile?.job_title);
    addProfileAttribute(siteNodeId, 'job_company_name', profile?.job_company_name);
    addProfileAttribute(siteNodeId, 'professional_email', profile?.professional_email || profile?.work_email || profile?.email);
    addProfileAttribute(siteNodeId, 'personal_emails', Array.isArray(profile?.personal_emails) ? profile.personal_emails : []);
    addProfileAttribute(siteNodeId, 'mobile_phone', profile?.mobile_phone || profile?.phone);
    addProfileAttribute(siteNodeId, 'personal_phones', Array.isArray(profile?.personal_phones) ? profile.personal_phones : []);
    addProfileAttribute(siteNodeId, 'professional_phones', Array.isArray(profile?.professional_phones) ? profile.professional_phones : []);
    addProfileAttribute(siteNodeId, 'linkedin_url', profile?.linkedin_url);
    addProfileAttribute(siteNodeId, 'facebook_url', profile?.facebook_url);
    addProfileAttribute(siteNodeId, 'twitter_url', profile?.twitter_url);
    addProfileAttribute(siteNodeId, 'github_url', profile?.github_url);
    addProfileAttribute(siteNodeId, 'profile_urls', externalUrls);
  }

  for (const profile of numverifyProfiles) {
    const queryType = String(profile?.query_type || 'phone').trim().toLowerCase() || 'phone';
    const queryValue = String(profile?.query_value || profile?.number || profile?.international_format || '').trim();
    if (!queryValue) continue;
    const siteNodeId = siteNodeIdFor(queryType, queryValue, 'numverify', '');
    addProfileAttribute(siteNodeId, 'number', profile?.number || profile?.international_format || profile?.e164 || profile?.local_format);
    addProfileAttribute(siteNodeId, 'international_format', profile?.international_format);
    addProfileAttribute(siteNodeId, 'local_format', profile?.local_format);
    addProfileAttribute(siteNodeId, 'e164', profile?.e164);
    addProfileAttribute(siteNodeId, 'location', profile?.location);
    addProfileAttribute(siteNodeId, 'country_name', profile?.country_name);
    addProfileAttribute(siteNodeId, 'country_code', profile?.country_code);
    addProfileAttribute(siteNodeId, 'carrier', profile?.carrier);
    addProfileAttribute(siteNodeId, 'line_type', profile?.line_type);
  }

  for (const [selectorNodeId, selectorIdentity] of selectorIdentityMap.entries()) {
    const selectorType = String(selectorIdentity?.type || '').trim().toLowerCase();
    const selectorValue = String(selectorIdentity?.value || '').trim();
    if (!selectorType || !selectorValue) continue;
    const exactKey = entityGraphAttributeKeyValue(selectorType, selectorValue);
    if (!exactKey) continue;
    const exactNodeId = `attr:${selectorType}|${exactKey}`;
    if (nodeMap.has(exactNodeId)) {
      addEdge(selectorNodeId, exactNodeId, 'queried_match', 2.1);
      continue;
    }
    const hintKey = entityGraphHintKeyValue(selectorType, selectorValue);
    if (!hintKey) continue;
    const hintNodeId = `attr:${selectorType}_hint|${hintKey}`;
    if (nodeMap.has(hintNodeId)) addEdge(selectorNodeId, hintNodeId, 'queried_match', 1.4);
  }

  for (const hint of contactHintNodes.email) {
    for (const exact of contactExactNodes.email.values()) {
      if (!hint?.nodeId || !exact?.nodeId || hint.nodeId === exact.nodeId) continue;
      if (!entityGraphEmailHintMatches(hint.value, exact.value)) continue;
      addEdge(hint.nodeId, exact.nodeId, 'partial_match', 0.72);
    }
  }
  for (const hint of contactHintNodes.phone) {
    for (const exact of contactExactNodes.phone.values()) {
      if (!hint?.nodeId || !exact?.nodeId || hint.nodeId === exact.nodeId) continue;
      if (!entityGraphPhoneHintMatches(hint.value, exact.value)) continue;
      addEdge(hint.nodeId, exact.nodeId, 'partial_match', 0.72);
    }
  }

  const nodes = Array.from(nodeMap.values());
  const edges = Array.from(edgeMap.values());
  for (const edge of edges) {
    const source = nodeMap.get(edge.source);
    const target = nodeMap.get(edge.target);
    if (source) source.degree += 1;
    if (target) target.degree += 1;
  }

  const maxAttributeNodes = 180;
  const attributeNodes = nodes.filter((node) => node.type === 'attribute');
  if (attributeNodes.length > maxAttributeNodes) {
    const keepSet = new Set(attributeNodes
      .sort((a, b) => b.degree - a.degree || a.label.localeCompare(b.label))
      .slice(0, maxAttributeNodes)
      .map((node) => node.id));
    const keepNodeIds = new Set(nodes.filter((node) => node.type !== 'attribute').map((node) => node.id));
    for (const id of keepSet) keepNodeIds.add(id);
    const trimmedEdges = edges.filter((edge) => keepNodeIds.has(edge.source) && keepNodeIds.has(edge.target));
    const trimmedNodeMap = new Map(nodes.filter((node) => keepNodeIds.has(node.id)).map((node) => [node.id, { ...node, degree: 0 }]));
    for (const edge of trimmedEdges) {
      const source = trimmedNodeMap.get(edge.source);
      const target = trimmedNodeMap.get(edge.target);
      if (source) source.degree += 1;
      if (target) target.degree += 1;
    }
    const trimmedNodes = Array.from(trimmedNodeMap.values());
    entityGraphModelCache = {
      nodes: trimmedNodes,
      edges: trimmedEdges,
      sharedAttributes: trimmedNodes.filter((node) => node.type === 'attribute' && node.degree > 1).length,
    };
    return entityGraphModelCache;
  }

  entityGraphModelCache = {
    nodes,
    edges,
    sharedAttributes: nodes.filter((node) => node.type === 'attribute' && node.degree > 1).length,
  };
  return entityGraphModelCache;
}

function entityGraphHash(value) {
  let hash = 2166136261;
  const text = String(value || '');
  for (let idx = 0; idx < text.length; idx += 1) {
    hash ^= text.charCodeAt(idx);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0);
}

function entityGraphSelectorBoxWidth(node) {
  const fullLabel = String(node?.label || '').trim();
  return Math.max(104, (fullLabel.length * 8.9) + 34);
}

function entityGraphNodeCollisionRadius(node) {
  if (!node || typeof node !== 'object') return 16;
  if (node.type === 'selector') {
    const w = entityGraphSelectorBoxWidth(node);
    const h = 28;
    return Math.max(34, Math.sqrt((w * w) + (h * h)) * 0.38);
  }
  if (node.type === 'site') return 24;
  if (node.type === 'profile') return 19;
  if (node.type === 'image') return 18;
  return 14;
}

function computeEntityGraphLayout(model, width, height) {
  const nodeSig = (Array.isArray(model?.nodes) ? model.nodes : []).map((node) => node.id).sort().join(',');
  const edgeSig = (Array.isArray(model?.edges) ? model.edges : []).map((edge) => `${edge.source}>${edge.target}`).sort().join(',');
  const cacheKey = `${nodeSig}|${edgeSig}|${Math.round(width)}|${Math.round(height)}`;
  if (entityGraphLayoutCache?.key === cacheKey) return entityGraphLayoutCache.positions;
  const nodes = Array.isArray(model?.nodes) ? model.nodes : [];
  const edges = Array.isArray(model?.edges) ? model.edges : [];
  const positions = new Map();
  if (!nodes.length) return positions;
  const minX = 48;
  const minY = 36;
  const maxX = Math.max(minX + 1, width - 48);
  const maxY = Math.max(minY + 1, height - 36);
  const nodeById = new Map(nodes.map((node) => [node.id, node]));
  const adjacency = new Map(nodes.map((node) => [node.id, new Set()]));
  const siteParentByNodeId = new Map();
  const selectorParentBySiteId = new Map();
  for (const edge of edges) {
    adjacency.get(edge.source)?.add(edge.target);
    adjacency.get(edge.target)?.add(edge.source);
    const sourceNode = nodeById.get(edge.source);
    const targetNode = nodeById.get(edge.target);
    if (sourceNode?.type === 'site' && (targetNode?.type === 'attribute' || targetNode?.type === 'image')) {
      siteParentByNodeId.set(targetNode.id, sourceNode.id);
    } else if (targetNode?.type === 'site' && (sourceNode?.type === 'attribute' || sourceNode?.type === 'image')) {
      siteParentByNodeId.set(sourceNode.id, targetNode.id);
    }
    if (sourceNode?.type === 'selector' && targetNode?.type === 'site') {
      selectorParentBySiteId.set(targetNode.id, sourceNode.id);
    } else if (targetNode?.type === 'selector' && sourceNode?.type === 'site') {
      selectorParentBySiteId.set(sourceNode.id, targetNode.id);
    }
  }

  const rankForNode = (node) => {
    if (node.type === 'selector') return 0;
    if (node.type === 'site') return 1;
    if (node.type === 'image') return 3;
    return 2;
  };

  const rankNodes = [[], [], [], []];
  for (const node of nodes) {
    const rank = rankForNode(node);
    rankNodes[rank].push(node);
  }

  const sortRank = (items, neighborRank) => {
    const ranked = items.map((node) => {
      const neighborIndexes = Array.from(adjacency.get(node.id) || [])
        .map((id) => rankNodes[neighborRank].findIndex((item) => item.id === id))
        .filter((index) => index >= 0);
      const barycenter = neighborIndexes.length
        ? neighborIndexes.reduce((sum, index) => sum + index, 0) / neighborIndexes.length
        : Number.MAX_SAFE_INTEGER;
      return { node, barycenter };
    });
    ranked.sort((a, b) => {
      if (a.barycenter !== b.barycenter) return a.barycenter - b.barycenter;
      return b.node.degree - a.node.degree || a.node.label.localeCompare(b.node.label);
    });
    return ranked.map((item) => item.node);
  };

  rankNodes[1] = sortRank(rankNodes[1], 0);
  rankNodes[2] = sortRank(rankNodes[2], 1);
  rankNodes[3] = sortRank(rankNodes[3], 1);
  for (let pass = 0; pass < 4; pass += 1) {
    rankNodes[2] = sortRank(rankNodes[2], 1);
    rankNodes[1] = sortRank(rankNodes[1], 2);
    rankNodes[3] = sortRank(rankNodes[3], 1);
  }

  const columnX = [
    minX + ((maxX - minX) * 0.12),
    minX + ((maxX - minX) * 0.4),
    minX + ((maxX - minX) * 0.72),
    minX + ((maxX - minX) * 0.88),
  ];

  const placeRank = (items, rank) => {
    if (!items.length) return;
    const radii = items.map((node) => entityGraphNodeCollisionRadius(node));
    const totalHeight = radii.reduce((sum, radius) => sum + (radius * 2), 0);
    const totalGap = Math.max(0, items.length - 1) * 18;
    const availableHeight = maxY - minY;
    const startY = minY + Math.max(0, (availableHeight - (totalHeight + totalGap)) / 2);
    let cursorY = startY;
    items.forEach((node, index) => {
      const manual = entityGraphManualPositions.get(node.id);
      const radius = radii[index];
      const y = manual?.y ?? (cursorY + radius);
      const x = manual?.x ?? columnX[rank];
      positions.set(node.id, {
        x: Math.min(maxX, Math.max(minX, x)),
        y: Math.min(maxY, Math.max(minY, y)),
        vx: 0,
        vy: 0,
      });
      cursorY += (radius * 2) + 18;
    });
  };

  placeRank(rankNodes[0], 0);
  placeRank(rankNodes[1], 1);
  placeRank(rankNodes[2], 2);
  placeRank(rankNodes[3], 3);

  for (let pass = 0; pass < 12; pass += 1) {
    for (let rank = 1; rank < rankNodes.length; rank += 1) {
      const items = rankNodes[rank];
      if (!items.length) continue;
      items.sort((a, b) => {
        const posA = positions.get(a.id);
        const posB = positions.get(b.id);
        const neighborsA = Array.from(adjacency.get(a.id) || []).map((id) => positions.get(id)?.y).filter(Number.isFinite);
        const neighborsB = Array.from(adjacency.get(b.id) || []).map((id) => positions.get(id)?.y).filter(Number.isFinite);
        let targetA = neighborsA.length ? neighborsA.reduce((sum, y) => sum + y, 0) / neighborsA.length : (posA?.y || 0);
        let targetB = neighborsB.length ? neighborsB.reduce((sum, y) => sum + y, 0) / neighborsB.length : (posB?.y || 0);
        if (rank === 1) {
          const selectorA = selectorParentBySiteId.get(a.id);
          const selectorB = selectorParentBySiteId.get(b.id);
          const selectorAY = selectorA ? positions.get(selectorA)?.y : null;
          const selectorBY = selectorB ? positions.get(selectorB)?.y : null;
          if (Number.isFinite(selectorAY)) targetA = (targetA * 0.52) + (selectorAY * 0.48);
          if (Number.isFinite(selectorBY)) targetB = (targetB * 0.52) + (selectorBY * 0.48);
        }
        if (rank >= 2) {
          const siteA = siteParentByNodeId.get(a.id);
          const siteB = siteParentByNodeId.get(b.id);
          const siteAY = siteA ? positions.get(siteA)?.y : null;
          const siteBY = siteB ? positions.get(siteB)?.y : null;
          if (Number.isFinite(siteAY)) targetA = (targetA * 0.28) + (siteAY * 0.72);
          if (Number.isFinite(siteBY)) targetB = (targetB * 0.28) + (siteBY * 0.72);
          if (siteA && siteB && siteA !== siteB) {
            const siteCompare = (positions.get(siteA)?.y || 0) - (positions.get(siteB)?.y || 0);
            if (Math.abs(siteCompare) > 1) return siteCompare;
          }
        }
        return targetA - targetB || b.degree - a.degree || a.label.localeCompare(b.label);
      });
      let cursorY = minY;
      for (const node of items) {
        const pos = positions.get(node.id);
        if (!pos || entityGraphManualPositions.has(node.id)) continue;
        const radius = entityGraphNodeCollisionRadius(node);
        const neighbors = Array.from(adjacency.get(node.id) || []).map((id) => positions.get(id)?.y).filter(Number.isFinite);
        let targetY = neighbors.length ? neighbors.reduce((sum, y) => sum + y, 0) / neighbors.length : pos.y;
        if (rank === 1) {
          const selectorId = selectorParentBySiteId.get(node.id);
          const selectorY = selectorId ? positions.get(selectorId)?.y : null;
          if (Number.isFinite(selectorY)) targetY = (targetY * 0.52) + (selectorY * 0.48);
        }
        if (rank >= 2) {
          const siteId = siteParentByNodeId.get(node.id);
          const siteY = siteId ? positions.get(siteId)?.y : null;
          if (Number.isFinite(siteY)) {
            const siblingIds = items.filter((item) => siteParentByNodeId.get(item.id) === siteId).map((item) => item.id);
            const siblingIndex = siblingIds.indexOf(node.id);
            const siblingCenter = (siblingIds.length - 1) / 2;
            const bandOffset = (siblingIndex - siblingCenter) * ((radius * 2) + 8);
            targetY = (targetY * 0.22) + ((siteY + bandOffset) * 0.78);
          }
        }
        pos.y = Math.max(cursorY + radius, Math.min(maxY - radius, targetY));
        cursorY = pos.y + radius + (rank >= 2 ? 10 : 14);
      }
      for (let idx = items.length - 2; idx >= 0; idx -= 1) {
        const current = positions.get(items[idx].id);
        const next = positions.get(items[idx + 1].id);
        if (!current || !next || entityGraphManualPositions.has(items[idx].id)) continue;
        const currentRadius = entityGraphNodeCollisionRadius(items[idx]);
        const nextRadius = entityGraphNodeCollisionRadius(items[idx + 1]);
        const currentSite = siteParentByNodeId.get(items[idx].id);
        const nextSite = siteParentByNodeId.get(items[idx + 1].id);
        const gap = rank >= 2 && currentSite && nextSite && currentSite === nextSite ? 8 : 14;
        const maxAllowedY = next.y - nextRadius - currentRadius - gap;
        current.y = Math.min(current.y, maxAllowedY);
      }
    }
  }

  for (const [nodeId, pos] of positions.entries()) {
    if (!entityGraphManualPositions.has(nodeId)) continue;
    entityGraphManualPositions.set(nodeId, { x: pos.x, y: pos.y });
  }
  entityGraphLayoutCache = { key: cacheKey, positions };
  return positions;
}

function applyEntityGraphTransform() {
  const panGroup = footprintEntityGraphCanvas?.querySelector('[data-entity-graph-pan]');
  if (!(panGroup instanceof SVGGElement)) return;
  const zoom = Number.isFinite(entityGraphViewport.zoom) ? Math.max(0.35, Math.min(2.8, entityGraphViewport.zoom)) : 1;
  const offsetX = Number.isFinite(entityGraphViewport.offsetX) ? entityGraphViewport.offsetX : 0;
  const offsetY = Number.isFinite(entityGraphViewport.offsetY) ? entityGraphViewport.offsetY : 0;
  panGroup.setAttribute('transform', `translate(${offsetX.toFixed(2)} ${offsetY.toFixed(2)}) scale(${zoom.toFixed(3)})`);
}

function entityGraphEdgePath(edge, sourcePos, targetPos) {
  const relation = String(edge?.relation || '').trim().toLowerCase();
  if (relation === 'partial_match') {
    const dx = targetPos.x - sourcePos.x;
    const sweep = sourcePos.y <= targetPos.y ? 1 : 0;
    const radius = Math.max(26, Math.abs(dx) * 0.45);
    return `M ${sourcePos.x.toFixed(2)} ${sourcePos.y.toFixed(2)} A ${radius.toFixed(2)} ${radius.toFixed(2)} 0 0 ${sweep} ${targetPos.x.toFixed(2)} ${targetPos.y.toFixed(2)}`;
  }
  const dx = targetPos.x - sourcePos.x;
  const controlOffset = Math.max(26, Math.abs(dx) * 0.42);
  const c1x = sourcePos.x + controlOffset;
  const c1y = sourcePos.y;
  const c2x = targetPos.x - controlOffset;
  const c2y = targetPos.y;
  return `M ${sourcePos.x.toFixed(2)} ${sourcePos.y.toFixed(2)} C ${c1x.toFixed(2)} ${c1y.toFixed(2)}, ${c2x.toFixed(2)} ${c2y.toFixed(2)}, ${targetPos.x.toFixed(2)} ${targetPos.y.toFixed(2)}`;
}

function renderFootprintEntityGraph() {
  if (
    !(footprintEntityGraphSummary instanceof HTMLElement)
    || !(footprintEntityGraphSummaryText instanceof HTMLElement)
    || !(footprintEntityGraphCanvas instanceof HTMLElement)
    || !(footprintEntityGraphDetails instanceof HTMLElement)
    || !(footprintEntityGraphEmpty instanceof HTMLElement)
  ) return;
  const model = collectEntityGraphModel();
  const allNodes = Array.isArray(model?.nodes) ? model.nodes : [];
  const allEdges = Array.isArray(model?.edges) ? model.edges : [];
  if (!allNodes.length || !allEdges.length) {
    footprintEntityGraphSummary.textContent = 'No graph data';
    footprintEntityGraphSummaryText.textContent = 'Run Digital Footprint recon to map queried selectors, identified platforms, and linked entities.';
    footprintEntityGraphCanvas.innerHTML = '';
    footprintEntityGraphDetails.innerHTML = '';
    footprintEntityGraphEmpty.classList.remove('hidden');
    entityGraphSelectedNodeId = '';
    return;
  }

  const query = entityGraphQuery.trim().toLowerCase();
  let nodes = allNodes;
  let edges = allEdges;
  if (query) {
    const matchedIds = new Set(allNodes.filter((node) => {
      const haystack = `${node.label} ${node.detail} ${node.subType} ${node.site}`.toLowerCase();
      return haystack.includes(query);
    }).map((node) => node.id));
    if (matchedIds.size) {
      const expanded = new Set(matchedIds);
      for (const edge of allEdges) {
        if (matchedIds.has(edge.source) || matchedIds.has(edge.target)) {
          expanded.add(edge.source);
          expanded.add(edge.target);
        }
      }
      nodes = allNodes.filter((node) => expanded.has(node.id));
      edges = allEdges.filter((edge) => expanded.has(edge.source) && expanded.has(edge.target));
    } else {
      nodes = [];
      edges = [];
    }
  }

  if (!nodes.length || !edges.length) {
    footprintEntityGraphSummary.textContent = `${allNodes.length} nodes • ${allEdges.length} links`;
    footprintEntityGraphSummaryText.textContent = 'No nodes match the current search query.';
    footprintEntityGraphCanvas.innerHTML = '';
    footprintEntityGraphDetails.innerHTML = '';
    footprintEntityGraphEmpty.classList.remove('hidden');
    return;
  }

  const canvasRect = footprintEntityGraphCanvas.getBoundingClientRect();
  const width = Math.max(520, Math.round(canvasRect.width || 980));
  const height = Math.max(360, Math.min(820, Math.round(window.innerHeight * 0.62)));
  const scopedModel = { nodes, edges };
  const positions = computeEntityGraphLayout(scopedModel, width, height);
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const neighborMap = new Map(nodes.map((node) => [node.id, new Set()]));
  for (const edge of edges) {
    neighborMap.get(edge.source)?.add(edge.target);
    neighborMap.get(edge.target)?.add(edge.source);
  }
  if (!byId.has(entityGraphSelectedNodeId)) {
    entityGraphSelectedNodeId = nodes.find((node) => node.type === 'selector')?.id || nodes[0]?.id || '';
  }
  const selectedNeighbors = new Set(neighborMap.get(entityGraphSelectedNodeId) || []);
  const selectedNode = byId.get(entityGraphSelectedNodeId) || null;

  const selectorCount = allNodes.filter((node) => node.type === 'selector').length;
  const platformCount = allNodes.filter((node) => node.type === 'site').length;
  footprintEntityGraphSummary.textContent = `${allNodes.length} nodes • ${allEdges.length} links`;
  footprintEntityGraphSummaryText.textContent = `${selectorCount} selector${selectorCount === 1 ? '' : 's'} • ${platformCount} platform${platformCount === 1 ? '' : 's'} • ${model.sharedAttributes} shared entit${model.sharedAttributes === 1 ? 'y' : 'ies'}`;
  footprintEntityGraphEmpty.classList.add('hidden');

  const edgeMarkup = edges.map((edge) => {
    const sourcePos = positions.get(edge.source);
    const targetPos = positions.get(edge.target);
    if (!sourcePos || !targetPos) return '';
    const active = edge.source === entityGraphSelectedNodeId || edge.target === entityGraphSelectedNodeId;
    const partial = String(edge?.relation || '').trim().toLowerCase() === 'partial_match';
    return `<path class="entity-graph-edge${partial ? ' is-partial' : ''}${active ? ' is-active' : ''}" d="${entityGraphEdgePath(edge, sourcePos, targetPos)}"></path>`;
  }).join('');

  const nodeMarkup = nodes.map((node) => {
    const pos = positions.get(node.id);
    if (!pos) return '';
    const radiusBase = node.type === 'selector' ? 13 : (node.type === 'profile' ? 10.5 : (node.type === 'site' ? 12.4 : 8.6));
    const radius = Math.min(24, radiusBase + Math.min(10, node.degree * 0.52));
    const isSelected = node.id === entityGraphSelectedNodeId;
    const isNeighbor = selectedNeighbors.has(node.id);
    const selectorColorClass = node.type === 'selector' ? ` entity-graph-selector-${escapeAttr(selectorTypeColorToken(node.subType || node.colorToken))}` : '';
    const nodeClass = `entity-graph-node entity-graph-node-${escapeAttr(node.type)}${selectorColorClass}${isSelected ? ' is-selected' : ''}${isNeighbor ? ' is-neighbor' : ''}${node.type === 'attribute' && node.degree > 1 ? ' is-shared' : ''}`;
    const icon = node.type === 'selector' ? 'S' : (node.type === 'profile' ? 'P' : (node.type === 'site' ? 'W' : (node.type === 'image' ? 'I' : 'E')));
    const label = String(node.label || '').trim();
    const iconImage = normalizeExternalUrl(node.pictureUrl || node.iconUrl || '');
    const imageSize = radius * 1.72;
    const imageOffset = imageSize / 2;
    const iconKind = entityGraphIconKind(node.subType);
    const nodeImageMarkup = iconImage
      ? `<image class="entity-graph-node-thumb" href="${escapeAttr(iconImage)}" x="${(-imageOffset).toFixed(2)}" y="${(-imageOffset).toFixed(2)}" width="${imageSize.toFixed(2)}" height="${imageSize.toFixed(2)}" preserveAspectRatio="xMidYMid slice" />`
      : (entityGraphIconMarkup(iconKind) || `<text class="entity-graph-node-icon" text-anchor="middle" dominant-baseline="central">${escapeHtml(icon)}</text>`);
    if (node.type === 'selector') {
      const token = String(selectorTypeColorToken(node.subType || node.colorToken) || 'default');
      const fullLabel = String(node.label || '').trim();
      const displayLabel = fullLabel;
      const selectorIcon = entityGraphIconMarkup(node.subType || node.colorToken, { compact: true });
      const hasSelectorIcon = Boolean(selectorIcon);
      const boxWidth = Math.max(104, (displayLabel.length * 8.9) + (hasSelectorIcon ? 50 : 34));
      const boxHeight = 36;
      return `
        <g class="${nodeClass}" data-entity-node-id="${escapeAttr(node.id)}" transform="translate(${pos.x.toFixed(2)} ${pos.y.toFixed(2)})">
          <rect class="entity-graph-selector-box entity-graph-selector-box-${escapeAttr(token)}" x="${(-boxWidth / 2).toFixed(2)}" y="${(-boxHeight / 2).toFixed(2)}" width="${boxWidth.toFixed(2)}" height="${boxHeight}" rx="8" ry="8"></rect>
          ${hasSelectorIcon ? `<g class="entity-graph-selector-icon" transform="translate(${(-boxWidth / 2) + 19} 0)">${selectorIcon}</g>` : ''}
          <text class="entity-graph-selector-text" x="${hasSelectorIcon ? 11 : 0}" text-anchor="middle" dominant-baseline="central">${escapeHtml(displayLabel)}</text>
        </g>
      `;
    }
    return `
      <g class="${nodeClass}" data-entity-node-id="${escapeAttr(node.id)}" transform="translate(${pos.x.toFixed(2)} ${pos.y.toFixed(2)})">
        <circle r="${radius.toFixed(2)}"></circle>
        ${nodeImageMarkup}
        ${node.type === 'image' ? '' : `<text class="entity-graph-node-label" y="${(radius + 16).toFixed(2)}" text-anchor="middle">${escapeHtml(label)}</text>`}
      </g>
    `;
  }).join('');

  footprintEntityGraphCanvas.innerHTML = `
    <svg class="entity-graph-svg" viewBox="0 0 ${width} ${height}" aria-hidden="true">
      <g data-entity-graph-pan>
        ${edgeMarkup}
        ${nodeMarkup}
      </g>
    </svg>
  `;
  applyEntityGraphTransform();

  if (!selectedNode) {
    footprintEntityGraphDetails.innerHTML = '';
    return;
  }
  const connected = Array.from(selectedNeighbors)
    .map((id) => byId.get(id))
    .filter(Boolean)
    .sort((a, b) => b.degree - a.degree || a.label.localeCompare(b.label))
    .slice(0, 18);
  const detailType = selectedNode.subType ? `${entityGraphNodeTypeLabel(selectedNode.type)} • ${titleCaseLabel(selectedNode.subType)}` : entityGraphNodeTypeLabel(selectedNode.type);
  const selectedNodeTitle = String(selectedNode.label || '').trim() || entityGraphNodeTypeLabel(selectedNode.type);
  const urlMarkup = selectedNode.url
    ? `<a class="lead-link" href="${escapeAttr(selectedNode.url)}" target="_blank" rel="noopener noreferrer">open profile</a>`
    : '';
  footprintEntityGraphDetails.innerHTML = `
    <div class="entity-graph-detail-card">
      <div class="viz-head">
        <h3>${escapeHtml(selectedNodeTitle)}</h3>
        <span class="viz-total">${escapeHtml(detailType)}</span>
      </div>
      <p class="posting-rhythm-summary">${escapeHtml(selectedNode.detail || 'Entity node')}</p>
      <div class="recon-pills">
        <span class="recon-pill">${selectedNode.degree} connection${selectedNode.degree === 1 ? '' : 's'}</span>
        ${urlMarkup}
      </div>
      <div class="entity-graph-neighbors">
        ${connected.length
    ? connected.map((node) => `<button type="button" class="mix-pill mix-filter-pill" data-entity-focus-id="${escapeAttr(node.id)}"><span>${escapeHtml(String(node.label || '').trim() || entityGraphNodeTypeLabel(node.type))}</span><strong>${node.degree}</strong></button>`).join('')
    : '<span class="recon-pill">No linked nodes</span>'}
      </div>
    </div>
  `;
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
  if (!(anchor instanceof Element)) return;
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
    const anchor = target.closest('[data-preview-image]');
    if (!(anchor instanceof Element)) return;
    showReconPreview(anchor, event);
  });
  container.addEventListener('mousemove', (event) => {
    if (!(activeReconPreviewAnchor instanceof Element)) return;
    positionReconPreviewTooltip(event);
  });
  container.addEventListener('mouseout', (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    const fromAnchor = target.closest('[data-preview-image]');
    if (!(fromAnchor instanceof Element)) return;
    const related = event.relatedTarget;
    if (related instanceof Node && fromAnchor.contains(related)) return;
    hideReconPreview();
  });
}

function personDataProfileMarkup(profile, totalProfiles = 0, pdlProfiles = [], options = {}) {
  const removable = options?.removable === true;
  if (!profile || typeof profile !== 'object' || !Object.keys(profile).length) {
    return '';
  }
  const profileKey = pdlProfileVisibilityKey(profile);
  const fullName = String(profile.full_name || '').trim();
  const title = String(profile.job_title || '').trim();
  const company = String(profile.job_company_name || '').trim();
  const location = String(profile.location_name || '').trim();
  const queryType = String(profile.query_type || '').trim() || 'unknown';
  const queryValue = String(profile.query_value || '').trim() || 'unknown';
  const profileConfidenceBadge = selectorConfidenceBadgeMarkup(queryType, queryValue, { compact: true, scopeId: profileKey });
  const profileSelectorKey = sourceSelectorKey(queryType, queryValue);
  const profileSelectorAttr = profileSelectorKey ? ` data-source-selector-key="${escapeAttr(profileSelectorKey)}"` : '';
  const proEmail = String(profile.professional_email || profile.work_email || '').trim();
  const personalEmails = Array.isArray(profile.personal_emails) ? profile.personal_emails.filter(Boolean).map((item) => String(item).trim()) : [];
  const mobilePhone = String(profile.mobile_phone || profile.phone || '').trim();
  const personalPhones = Array.isArray(profile.personal_phones) ? profile.personal_phones.filter(Boolean).map((item) => String(item).trim()) : [];
  const professionalPhones = Array.isArray(profile.professional_phones) ? profile.professional_phones.filter(Boolean).map((item) => String(item).trim()) : [];
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
  const filterVisibleContactValues = (label, values) => values.filter((value) => !hiddenPdlContactValueKeys.has(pdlContactVisibilityKey(profile, label, value)));
  const professionalEmailValues = filterVisibleContactValues('Professional Email', uniqueValues(proEmail ? [proEmail] : []));
  const personalEmailValues = filterVisibleContactValues('Personal Email', uniqueValues(personalEmails));
  const professionalPhoneValues = filterVisibleContactValues('Professional Phone', uniqueValues(professionalPhones));
  const personalPhoneValues = filterVisibleContactValues('Personal Phone', uniqueValues([mobilePhone, ...personalPhones]));
  const contactSelectorType = (heading) => {
    const lowered = String(heading || '').toLowerCase();
    if (lowered.includes('email')) return 'email';
    if (lowered.includes('phone')) return 'phone';
    return '';
  };
  const contactGroupMarkup = (heading, values) => `
    <div class="pdl-contact-group">
      <span class="pdl-contact-heading">${escapeHtml(heading)}</span>
      <div class="recon-pills pdl-contact-pills">
        ${values.length ? values.map((value) => `
          <span class="recon-pill">
            <span>${escapeHtml(value)}</span>
            ${selectorConfidenceBadgeMarkup(contactSelectorType(heading) || queryType, value, { compact: true, scopeId: pdlContactVisibilityKey(profile, heading.replace(/s$/, ''), value) })}
            ${pivotSelectorActionMarkup(contactSelectorType(heading), value, 'Pivot Search')}
            ${removable ? `<button type="button" class="known-selector-action recon-pill-remove recon-pill-action" data-pdl-contact-remove="${escapeAttr(pdlContactVisibilityKey(profile, heading.replace(/s$/, ''), value))}" title="Remove value">×</button>` : ''}
          </span>
        `).join('') : '<span class="recon-pill">None</span>'}
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
    return rows.filter((row) => !hiddenPdlProfileUrlKeys.has(String(row?.profile_url || '').trim().toLowerCase()));
  })();
  return `
    <div class="recon-group">
      <p>Person Data Profile${totalProfiles > 1 ? ` (${totalProfiles} matches)` : ''}</p>
      <div class="pdl-poi-profile"${profileSelectorAttr}>
        ${removable ? `<button type="button" class="known-selector-action recon-tile-remove" data-pdl-profile-remove="${escapeAttr(profileKey)}" title="Remove Person Data Profile">×</button>` : ''}
        <div class="recon-pills">
          <span class="recon-pill">${escapeHtml(fullName || `${queryType}: ${queryValue}`)}</span>
          ${profileConfidenceBadge}
        </div>
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
    ? mergedProfileRows.map((row) => {
      const rowWithSelector = { ...row, selector_type: queryType, selector: String(queryValue || '').trim() };
      if (!removable) return toReconBadge(rowWithSelector, 'lead', { pivotable: false });
      return toReconBadge(rowWithSelector, 'lead', {
        removable: true,
        pivotable: false,
      }).replace('data-recon-remove=', 'data-pdl-url-remove=');
    }).join('')
    : '<span class="recon-pill">No profile URLs returned by People Data Labs.</span>'}
          </div>
        </div>
        <div class="pdl-contact-sections">
          ${contactGroupMarkup('Personal Emails', personalEmailValues)}
          ${contactGroupMarkup('Professional Emails', professionalEmailValues)}
          ${contactGroupMarkup('Personal Phones', personalPhoneValues)}
          ${contactGroupMarkup('Professional Phones', professionalPhoneValues)}
        </div>
        <div class="recon-pills">
          <span class="recon-pill">${escapeHtml(identificationText)}</span>
        </div>
      </div>
    </div>
  `;
}

function osintProfilesMarkup(profiles, rows = [], options = {}) {
  const removable = options?.removable === true;
  const items = Array.isArray(profiles) ? profiles : [];
  const resultRows = Array.isArray(rows) ? rows : [];
  if (!items.length && !resultRows.length) return '';
  const screenshotByUrl = new Map();
  for (const row of resultRows) {
    if (String(row?.source || '').trim().toLowerCase() !== 'osint_industries') continue;
    const url = normalizeExternalUrl(row?.profile_url);
    const shot = String(row?.screenshot_url || '').trim();
    if (!url || !shot || screenshotByUrl.has(url.toLowerCase())) continue;
    screenshotByUrl.set(url.toLowerCase(), shot);
  }
  const normalizedSiteLabel = (value) => {
    const clean = String(value || '').trim();
    if (!clean) return 'OSINT';
    return clean.replace(/_/g, ' ');
  };
  const linkPill = (label, rawUrl, screenshotLabel, cls = '') => {
    const url = normalizeExternalUrl(rawUrl);
    if (!url) return '';
    const screenshotUrl = screenshotByUrl.get(url.toLowerCase()) || '';
    const previewAttr = screenshotUrl ? ` data-preview-image="${escapeAttr(screenshotUrl)}"` : '';
    const previewLabelAttr = screenshotUrl ? ` data-preview-label="${escapeAttr(screenshotLabel)}"` : '';
    const classAttr = cls ? ` ${cls}` : '';
    return `<a class="recon-pill lead-link${classAttr}" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer"${previewAttr}${previewLabelAttr}>${escapeHtml(label)}</a>`;
  };
  const valueItem = (label, value, options = {}) => {
    if (value === null || value === undefined) return '';
    const clean = typeof value === 'string' ? value.trim() : String(value).trim();
    if (!clean) return '';
    const wideClass = options?.wide ? ' osint-value-wide' : '';
    return `<div class="osint-value${wideClass}"><span class="osint-key">${escapeHtml(label)}</span><strong>${escapeHtml(clean)}</strong></div>`;
  };
  const rowsByUrl = new Map();
  for (const row of resultRows) {
    if (String(row?.source || '').trim().toLowerCase() !== 'osint_industries') continue;
    const profileUrl = normalizeExternalUrl(row?.profile_url);
    if (!profileUrl) continue;
    if (!rowsByUrl.has(profileUrl.toLowerCase())) rowsByUrl.set(profileUrl.toLowerCase(), row);
  }
  const mergedItems = (() => {
    const output = [];
    const seen = new Set();
    for (const profile of items) {
      const title = String(profile?.title || profile?.name || profile?.username || '').trim();
      const profileUrl = normalizeExternalUrl(profile?.profile_url);
      const website = normalizeExternalUrl(profile?.website);
      const dedupe = [
        String(profile?.module || '').trim().toLowerCase(),
        profileUrl.toLowerCase(),
        String(profile?.username || '').trim().toLowerCase(),
        String(profile?.email || '').trim().toLowerCase(),
        String(profile?.phone || '').trim().toLowerCase(),
        title.toLowerCase(),
      ].join('|');
      if (seen.has(dedupe)) continue;
      seen.add(dedupe);
      output.push({ profile, profileUrl, website, title });
    }
    return output;
  })();
  const cards = mergedItems.map((entry, index) => {
    const profile = entry.profile;
    const profileKey = osintTileVisibilityKey(profile);
    const title = entry.title || `Result ${index + 1}`;
    const displayName = String(profile?.name || '').trim() || 'Unnamed';
    const username = String(profile?.username || '').trim();
    const profileUrl = entry.profileUrl;
    const website = entry.website;
    const siteLabel = normalizedSiteLabel(profile?.module || rowsByUrl.get(profileUrl.toLowerCase())?.site || 'osint');
    const row = rowsByUrl.get(profileUrl.toLowerCase());
    const selectorKey = sourceSelectorKey(
      profile?.query_type || row?.selector_type,
      profile?.query_value || row?.selector,
    );
    const selectorType = String(profile?.query_type || row?.selector_type || '').trim().toLowerCase() || 'name';
    const confidenceBadge = selectorConfidenceBadgeMarkup(selectorType, String(profile?.query_value || row?.selector || '').trim(), { compact: true, scopeId: profileKey });
    const selectorAttr = selectorKey ? ` data-source-selector-key="${escapeAttr(selectorKey)}"` : '';
    const websiteLink = website && website !== profileUrl ? linkPill('Website', website, `${title} website`, 'osint-website-link') : '';
    const confidenceAction = `<div class="osint-profile-confidence">${confidenceBadge}</div>`;
    const profileAction = profileUrl
      ? `
        <a class="known-selector-action osint-profile-open" href="${escapeHtml(profileUrl)}" target="_blank" rel="noopener noreferrer" title="Open profile URL" aria-label="Open profile URL">
          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path d="M14 4h6v6"></path>
            <path d="M10 14L20 4"></path>
            <path d="M20 13v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h6"></path>
          </svg>
        </a>
      `
      : '';
    const removeAction = removable
      ? `<button type="button" class="known-selector-action recon-tile-remove" data-osint-remove="${escapeAttr(profileKey)}" title="Remove OSINT tile">×</button>`
      : '';
    const topActions = confidenceAction || profileAction || removeAction
      ? `<div class="osint-profile-actions">${confidenceAction}${profileAction}${removeAction}</div>`
      : '';
    const imageUrl = normalizeExternalUrl(profile?.picture_url || profile?.avatar_url || '') || normalizeExternalUrl(row?.picture_url || '');
    const siteIcon = faviconMarkup(siteLabel, profileUrl || website);
    const avatarMarkup = imageUrl
      ? `<img class="osint-profile-avatar" src="${escapeHtml(imageUrl)}" alt="${escapeAttr(title)}" loading="lazy" referrerpolicy="no-referrer" />`
      : `
        <div class="osint-profile-avatar empty" aria-label="No profile image">
          <svg class="osint-profile-avatar-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor">
            <circle cx="12" cy="8" r="4" fill="none"></circle>
            <path d="M4.5 20c0-3.9 3.3-7 7.5-7s7.5 3.1 7.5 7" fill="none"></path>
          </svg>
        </div>
      `;
    const valueRows = [
      ['location', profile?.location],
      ['biolocation', profile?.biolocation],
      ['gender', profile?.gender],
      ['age', profile?.age],
      ['email', profile?.email],
      ['phone', profile?.phone],
      ['email_hint', profile?.email_hint],
      ['phone_hint', profile?.phone_hint],
      ['language', profile?.language],
      ['bio', profile?.bio],
      ['breach', profile?.breach],
    ];
    const isLongEntityText = (rawValue) => {
      if (rawValue === null || rawValue === undefined) return false;
      const clean = typeof rawValue === 'string' ? rawValue.trim() : String(rawValue).trim();
      if (!clean) return false;
      return clean.length >= 96 || /\S{45,}/.test(clean);
    };
    const stackValues = valueRows.some(([, value]) => isLongEntityText(value));
    const valuesMarkup = valueRows
      .map(([label, value]) => valueItem(label, value, { wide: stackValues }))
      .join('');
    return `
      <article class="osint-profile-card"${selectorAttr}>
        ${topActions}
        <div class="osint-profile-head">
          ${avatarMarkup}
          <div>
            <p class="osint-profile-site">${siteIcon}<span>${escapeHtml(siteLabel)}</span></p>
            <h4>${escapeHtml(title)}</h4>
            ${displayName && displayName.toLowerCase() !== title.toLowerCase() ? `<p>${escapeHtml(displayName)}</p>` : ''}
            ${username && username.toLowerCase() !== title.toLowerCase() && username.toLowerCase() !== displayName.toLowerCase()
    ? `<p>@${escapeHtml(username)}</p>`
    : ''}
          </div>
        </div>
        <div class="osint-profile-grid${stackValues ? ' osint-profile-grid-stacked' : ''}">
          ${valuesMarkup}
        </div>
        <div class="osint-profile-links">
          ${websiteLink}
        </div>
      </article>
    `;
  }).join('');
  if (!cards) return '';
  return `
    <div class="recon-group">
      <p>OSINT Industries Tiles (${mergedItems.length})</p>
      <div class="osint-profiles-list">${cards}</div>
    </div>
  `;
}

function hibpAggregateMarkup(profiles, specRows = []) {
  const items = Array.isArray(profiles) ? profiles : [];
  const rows = Array.isArray(specRows) ? specRows : [];
  const hibpProfiles = items.filter((row) => isHibpModuleName(row?.module));
  const hibpSpecs = rows.filter((row) => isHibpModuleName(row?.module));
  if (!hibpProfiles.length && !hibpSpecs.length) return '';

  const bySelector = new Map();
  const ensureSelector = (selectorType, selectorValue) => {
    const type = String(selectorType || '').trim().toLowerCase() || 'selector';
    const value = String(selectorValue || '').trim() || 'unknown';
    const key = `${type}|${value.toLowerCase()}`;
    if (!bySelector.has(key)) {
      bySelector.set(key, { selectorType: type, selectorValue: value, breaches: new Map() });
    }
    return bySelector.get(key);
  };
  const sanitizeBreachName = (raw) => {
    let normalized = String(raw || '').trim();
    if (!normalized) return '';
    normalized = normalized.replace(/^["']+|["']+$/g, '').trim();
    if (/:\s*\d/.test(normalized)) normalized = normalized.split(':')[0].trim();
    if (!normalized) return '';
    if (/^\d+$/.test(normalized)) return '';
    if (/^\d{4}-\d{2}-\d{2}/.test(normalized)) return '';
    if (normalized.length > 96) return '';
    if (!/[A-Za-z]/.test(normalized)) return '';
    return normalized;
  };
  const formatBreachMonthYear = (raw) => {
    const clean = String(raw || '').trim();
    if (!clean) return '';
    const parsed = new Date(clean);
    if (Number.isNaN(parsed.getTime())) return '';
    return new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' }).format(parsed);
  };
  const breachEntry = (nameRaw, dateRaw = '', logoRaw = '') => {
    const name = sanitizeBreachName(nameRaw);
    if (!name) return null;
    const dateLabel = formatBreachMonthYear(dateRaw);
    const logo = normalizeExternalUrl(logoRaw);
    const key = `${String(name).toLowerCase()}|${String(dateLabel).toLowerCase()}`;
    return { key, name, dateLabel, logo };
  };
  const parseBreachesFromValue = (value) => {
    const output = [];
    const append = (nameRaw, dateRaw = '', logoRaw = '') => {
      const entry = breachEntry(nameRaw, dateRaw, logoRaw);
      if (!entry) return;
      output.push(entry);
    };
    const parseMaybeJson = (text) => {
      const raw = String(text || '').trim();
      if (!raw) return null;
      if (!((raw.startsWith('{') && raw.endsWith('}')) || (raw.startsWith('[') && raw.endsWith(']')))) return null;
      try {
        return JSON.parse(raw);
      } catch (_error) {
        return null;
      }
    };
    const objectValue = (node, aliases) => {
      if (!node || typeof node !== 'object') return undefined;
      const lookup = new Set(aliases.map((item) => String(item || '').toLowerCase()));
      for (const [key, val] of Object.entries(node)) {
        if (lookup.has(String(key || '').toLowerCase())) return val;
      }
      return undefined;
    };
    const walk = (node) => {
      if (node === null || node === undefined) return;
      if (Array.isArray(node)) {
        for (const item of node) walk(item);
        return;
      }
      if (typeof node === 'string') {
        const parsed = parseMaybeJson(node);
        if (parsed !== null) {
          walk(parsed);
          return;
        }
        for (const part of node.split(/[,;\n]+/g)) append(part);
        return;
      }
      if (typeof node === 'object') {
        const nameValue = objectValue(node, ['name', 'title', 'breach', 'breach_name', 'breachname']);
        const dateValue = objectValue(node, ['creation_date', 'breach_date', 'date', 'added_date', 'modified_date', 'creation date', 'breach date', 'added date', 'modified date']);
        const logoValue = objectValue(node, ['picture_url', 'picture url', 'logo', 'logo_url', 'logo url', 'favicon', 'icon']);
        if (nameValue !== undefined) append(nameValue, dateValue, logoValue);
        for (const item of Object.values(node)) walk(item);
        return;
      }
      // Ignore primitive numeric/boolean values (e.g. PwnCount) that are not breach names.
    };
    walk(value);
    return output;
  };

  for (const profile of hibpProfiles) {
    const bucket = ensureSelector(profile?.query_type, profile?.query_value);
    const directProfileBreach = breachEntry(
      profile?.title || profile?.name || profile?.breach,
      profile?.creation_date,
      profile?.picture_url,
    );
    if (directProfileBreach) bucket.breaches.set(directProfileBreach.key, directProfileBreach);
    for (const breach of parseBreachesFromValue(profile?.breach)) bucket.breaches.set(breach.key, breach);
    for (const breach of parseBreachesFromValue(profile?.parsed_values)) bucket.breaches.set(breach.key, breach);
    for (const breach of parseBreachesFromValue(profile?.spec_format)) bucket.breaches.set(breach.key, breach);
    const parsedValues = profile?.parsed_values && typeof profile.parsed_values === 'object' ? profile.parsed_values : {};
    for (const [key, value] of Object.entries(parsedValues)) {
      const lowered = String(key || '').toLowerCase();
      if (!lowered.includes('breach') && !lowered.includes('pwn')) continue;
      for (const breach of parseBreachesFromValue(value)) bucket.breaches.set(breach.key, breach);
    }
  }
  for (const row of hibpSpecs) {
    const bucket = ensureSelector(row?.query_type, row?.query_value);
    for (const breach of parseBreachesFromValue(row?.parsed_values)) bucket.breaches.set(breach.key, breach);
    for (const breach of parseBreachesFromValue(row?.spec_format)) bucket.breaches.set(breach.key, breach);
    const parsedValues = row?.parsed_values && typeof row.parsed_values === 'object' ? row.parsed_values : {};
    for (const [key, value] of Object.entries(parsedValues)) {
      const lowered = String(key || '').toLowerCase();
      if (!lowered.includes('breach') && !lowered.includes('pwn')) continue;
      for (const breach of parseBreachesFromValue(value)) bucket.breaches.set(breach.key, breach);
    }
  }

  const selectorRows = Array.from(bySelector.values());
  if (!selectorRows.length) return '';
  const cards = selectorRows.map((row) => {
    const selectorLabel = formatSelectorLabel(row.selectorType, row.selectorValue);
    const breaches = Array.from(row.breaches.values()).sort((a, b) => a.name.localeCompare(b.name));
    return `
      <article class="hibp-selector-result">
        <p>${escapeHtml(selectorLabel)}</p>
        <div class="recon-pills">
          ${breaches.length
    ? breaches.map((breach) => {
      const label = breach.dateLabel ? `${breach.name} (${breach.dateLabel})` : breach.name;
      const logoMarkup = breach.logo
        ? `<img class="site-favicon" src="${escapeHtml(breach.logo)}" alt="" aria-hidden="true" loading="lazy" referrerpolicy="no-referrer" />`
        : '';
      return `<span class="recon-pill">${logoMarkup}<span>${escapeHtml(label)}</span></span>`;
    }).join('')
    : '<span class="recon-pill">No breach names returned.</span>'}
        </div>
      </article>
    `;
  }).join('');
  return `
    <div class="recon-group recon-group-low-priority">
      <p>HIBP Breach Summary (Deprioritized)</p>
      <div>${cards}</div>
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
    const queryType = String(profile?.query_type || 'phone').trim().toLowerCase() || 'phone';
    const confidenceBadge = selectorConfidenceBadgeMarkup(queryType, String(profile?.query_value || profile?.number || '').trim(), {
      compact: true,
      scopeId: `numverify|${String(profile?.number || profile?.international_format || profile?.e164 || title || '').trim().toLowerCase()}`,
    });
    return `
      <article class="osint-profile-card">
        <div class="osint-profile-head">
          <div class="osint-profile-avatar empty">Phone</div>
          <div>
            <div class="osint-profile-confidence">${confidenceBadge}</div>
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

function knownSelectorPillMarkup(type, value, confidenceSourceType = '', confidenceSourceValue = '') {
  const key = `${type}|${String(value || '').toLowerCase()}`;
  if (hiddenKnownSelectorKeys.has(key)) return '';
  const confidenceType = String(confidenceSourceType || type).trim().toLowerCase();
  const confidenceValue = String(confidenceSourceValue || value).trim();
  const confidence = selectorConfidenceMeta(confidenceType, confidenceValue);
  const typeLabel = selectorTypeDisplayLabel(type);
  return `
    <span class="known-selector-pill known-selector-pill-${escapeAttr(type)}" data-known-focus-key="${escapeAttr(key)}" title="${escapeAttr(confidence.guidance)}">
      <span class="known-selector-main">
        <span class="known-selector-type">${escapeHtml(typeLabel)}</span>
        <span class="known-selector-value">${escapeHtml(value)}</span>
      </span>
      ${selectorConfidenceBadgeMarkup(confidenceType, confidenceValue, { compact: true, scopeId: `known_selector|${key}` })}
      <button type="button" class="known-selector-action pivot" data-known-pivot-type="${escapeAttr(type)}" data-known-pivot-value="${escapeAttr(value)}" title="Pivot Search" aria-label="Pivot Search">
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="11" cy="11" r="6.5"></circle><path d="M16.5 16.5L21 21"></path></svg>
      </button>
      <button type="button" class="known-selector-action" data-known-remove="${escapeAttr(key)}" title="Remove selector">×</button>
    </span>
  `;
}

function hideResultsForSelector(selectorKey) {
  const cleanKey = String(selectorKey || '').trim().toLowerCase();
  if (!cleanKey || cleanKey === 'all') return false;
  const { type, value } = sourceSelectorParts(cleanKey);
  if (!type || !value) return false;
  const payload = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
  const rows = Array.isArray(payload?.results) ? payload.results : [];
  const osintProfiles = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
  const pdlProfiles = Array.isArray(payload?.person_data_profiles) ? payload.person_data_profiles : [];
  let hiddenCount = 0;

  for (const row of rows) {
    const rowType = String(row?.selector_type || '').trim().toLowerCase();
    const rowValue = String(row?.selector || '').trim().toLowerCase();
    if (rowType !== type || rowValue !== value) continue;
    const rowKey = reconRowVisibilityKey(row);
    if (!hiddenReconRowKeys.has(rowKey)) {
      hiddenReconRowKeys.add(rowKey);
      hiddenCount += 1;
    }
    const source = String(row?.source || '').trim().toLowerCase();
    if (source === 'osint_industries' && row?.osint_profile) {
      hiddenOsintTileKeys.add(osintTileVisibilityKey(row.osint_profile));
    }
    if (source === 'pdl') {
      const urlKey = String(row?.profile_url || '').trim().toLowerCase();
      if (urlKey) hiddenPdlProfileUrlKeys.add(urlKey);
    }
  }

  for (const profile of osintProfiles) {
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const queryValue = String(profile?.query_value || '').trim().toLowerCase();
    if (queryType === type && queryValue === value) {
      hiddenOsintTileKeys.add(osintTileVisibilityKey(profile));
    }
  }

  for (const profile of pdlProfiles) {
    const queryType = String(profile?.query_type || '').trim().toLowerCase();
    const queryValue = String(profile?.query_value || '').trim().toLowerCase();
    if (queryType === type && queryValue === value) {
      hiddenPdlProfileKeys.add(pdlProfileVisibilityKey(profile));
    }
  }

  hiddenKnownSelectorKeys.add(cleanKey);
  return hiddenCount > 0;
}

function focusKnownSelectorInstances(selectorKey) {
  const cleanKey = String(selectorKey || '').trim().toLowerCase();
  if (!cleanKey || cleanKey === 'all') return false;
  if (!(footprintReconResults instanceof HTMLElement)) return false;
  const payload = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
  if (activeFootprintSourceSelectorKey !== 'all') {
    activeFootprintSourceSelectorKey = 'all';
    renderReconResults(payload, footprintReconResults);
  }
  const candidates = Array.from(footprintReconResults.querySelectorAll('[data-source-selector-key]'));
  const matches = candidates.filter((node) => String(node.getAttribute('data-source-selector-key') || '').trim().toLowerCase() === cleanKey);
  for (const node of candidates) {
    node.classList.remove('selector-match', 'selector-match-active');
  }
  const knownPills = Array.from(footprintKnownSelectorsGroups?.querySelectorAll('[data-known-focus-key]') || []);
  for (const pill of knownPills) {
    const isActive = String(pill.getAttribute('data-known-focus-key') || '').trim().toLowerCase() === cleanKey;
    pill.classList.toggle('known-selector-pill-focus', isActive);
  }
  if (!matches.length) {
    activeKnownSelectorFocusKey = '';
    activeKnownSelectorFocusIndex = -1;
    if (footprintReconStatus) footprintReconStatus.textContent = `No visible instances found for ${cleanKey}.`;
    return false;
  }
  const nextIndex = activeKnownSelectorFocusKey === cleanKey
    ? (activeKnownSelectorFocusIndex + 1) % matches.length
    : 0;
  activeKnownSelectorFocusKey = cleanKey;
  activeKnownSelectorFocusIndex = nextIndex;
  for (const node of matches) node.classList.add('selector-match');
  const current = matches[nextIndex];
  current.classList.add('selector-match-active');
  current.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
  const parts = sourceSelectorParts(cleanKey);
  const label = formatSelectorLabel(parts.type, parts.value);
  if (footprintReconStatus) footprintReconStatus.textContent = `Selector focus: ${label} (${nextIndex + 1}/${matches.length})`;
  return true;
}

function renderFootprintLikelyName(payload) {
  if (!(footprintLikelyNameValue instanceof HTMLElement)) return;
  const summary = collectLikelyNameSummary(payload || {});
  const value = String(summary?.name || '').trim();
  footprintLikelyNameValue.textContent = value || 'Unknown';
  if (footprintLikelyName instanceof HTMLElement) {
    footprintLikelyName.classList.toggle('is-empty', !value);
  }
}

function renderKnownSelectorsPanel(payload) {
  if (!(footprintKnownSelectorsGroups instanceof HTMLElement) || !(footprintKnownSelectorsTotal instanceof HTMLElement)) return;
  const known = collectKnownSelectors(payload || {});
  const labels = {
    email: 'Email/s',
    phone: 'Phone/s',
    username: 'Username/s',
    name: 'Name/s',
    location: 'Location/s',
  };
  let total = 0;
  const sections = KNOWN_SELECTOR_GROUPS
    .map((type) => {
      const items = Array.isArray(known?.[type]) ? known[type] : [];
      const pills = items
        .map((item) => knownSelectorPillMarkup(type, item?.value, item?.confidence_source_type, item?.confidence_source_value))
        .filter(Boolean)
        .join('');
      const count = pills ? items.filter((item) => !hiddenKnownSelectorKeys.has(`${type}|${String(item?.value || '').toLowerCase()}`)).length : 0;
      total += Math.max(0, count);
      return `
        <section class="known-selector-group">
          <h5>${escapeHtml(labels[type] || type)}</h5>
          <div class="known-selector-pills">
            ${pills || '<span class="recon-pill">None</span>'}
          </div>
        </section>
      `;
    })
    .join('');
  footprintKnownSelectorsTotal.textContent = String(total);
  footprintKnownSelectorsGroups.innerHTML = sections || '<p class="viz-empty">No selectors returned yet.</p>';
}

function emptyReconPayload() {
  return {
    selectors: [],
    results: [],
    collection_targets: [],
    leads: [],
    osint_profiles: [],
    osint_spec_results: [],
    numverify_profiles: [],
    person_data_profile: {},
    person_data_profiles: [],
    api_modules_queried: [],
    collection_ready_profiles: [],
    unsupported_profiles_with_url: [],
    known_present_without_url: [],
    checked: 0,
    present_count: 0,
  };
}

function mergeReconPayloads(basePayload, incomingPayload) {
  const base = basePayload && typeof basePayload === 'object' ? basePayload : emptyReconPayload();
  const incoming = incomingPayload && typeof incomingPayload === 'object' ? incomingPayload : emptyReconPayload();
  const dedupeBy = (rows, keyFn) => {
    const output = [];
    const seen = new Set();
    for (const row of rows) {
      const key = keyFn(row);
      if (!key || seen.has(key)) continue;
      seen.add(key);
      output.push(row);
    }
    return output;
  };
  const merged = {
    selectors: dedupeBy([...(base.selectors || []), ...(incoming.selectors || [])], (row) => `${String(row?.type || '').toLowerCase()}|${String(row?.value || '').toLowerCase()}`),
    results: dedupeBy([...(base.results || []), ...(incoming.results || [])], (row) => [
      String(row?.selector_type || '').toLowerCase(),
      String(row?.selector || '').toLowerCase(),
      String(row?.site_key || row?.site || '').toLowerCase(),
      String(row?.profile_url || '').toLowerCase(),
      String(row?.source || '').toLowerCase(),
    ].join('|')),
    collection_targets: dedupeBy([...(base.collection_targets || []), ...(incoming.collection_targets || [])], (row) => `${String(row?.platform || '').toLowerCase()}|${String(row?.username || '').toLowerCase()}`),
    leads: dedupeBy([...(base.leads || []), ...(incoming.leads || [])], (row) => [
      String(row?.site || '').toLowerCase(),
      String(row?.profile_url || '').toLowerCase(),
      String(row?.lead_type || '').toLowerCase(),
      String(row?.attribute || '').toLowerCase(),
      String(row?.value || '').toLowerCase(),
      String(row?.profile_name || '').toLowerCase(),
    ].join('|')),
    osint_profiles: dedupeBy([...(base.osint_profiles || []), ...(incoming.osint_profiles || [])], (row) => [
      String(row?.module || '').toLowerCase(),
      String(row?.profile_url || '').toLowerCase(),
      String(row?.website || '').toLowerCase(),
      String(row?.username || '').toLowerCase(),
      String(row?.email || '').toLowerCase(),
      String(row?.phone || '').toLowerCase(),
      String(row?.title || '').toLowerCase(),
    ].join('|')),
    osint_spec_results: dedupeBy([...(base.osint_spec_results || []), ...(incoming.osint_spec_results || [])], (row) => [
      String(row?.module || '').toLowerCase(),
      String(row?.query_type || '').toLowerCase(),
      String(row?.query_value || '').toLowerCase(),
      String(row?.title || '').toLowerCase(),
    ].join('|')),
    numverify_profiles: dedupeBy([...(base.numverify_profiles || []), ...(incoming.numverify_profiles || [])], (row) => `${String(row?.number || row?.query_value || '').toLowerCase()}`),
    person_data_profiles: dedupeBy([...(base.person_data_profiles || []), ...(incoming.person_data_profiles || [])], (row) => `${String(row?.id || '').toLowerCase()}|${String(row?.full_name || '').toLowerCase()}|${String(row?.query_value || '').toLowerCase()}`),
    api_modules_queried: dedupeBy([...(base.api_modules_queried || []), ...(incoming.api_modules_queried || [])], (row) => `${String(row?.module || '').toLowerCase()}`),
  };
  merged.person_data_profile = merged.person_data_profiles[0] || {};
  merged.collection_ready_profiles = dedupeRowsByProfileUrl(merged.results.filter((row) => row?.status === 'present' && row?.supported_for_collection && String(row?.profile_url || '').trim()));
  merged.unsupported_profiles_with_url = dedupeRowsByProfileUrl(merged.results.filter((row) => row?.status === 'present' && !row?.supported_for_collection && String(row?.profile_url || '').trim()));
  merged.known_present_without_url = merged.results.filter((row) => row?.status === 'present' && !String(row?.profile_url || '').trim());
  merged.checked = merged.results.length;
  merged.present_count = merged.results.filter((row) => row?.status === 'present').length;
  return merged;
}

function collectionTargetsFromReconResults(results) {
  const rows = Array.isArray(results) ? results : [];
  const seenUrls = new Set();
  const seenTargets = new Set();
  const targets = [];
  for (const row of rows) {
    if (String(row?.status || '').trim().toLowerCase() !== 'present') continue;
    if (!row?.supported_for_collection) continue;
    const normalizedUrl = normalizeExternalUrl(row?.profile_url);
    if (!normalizedUrl) continue;
    const urlKey = normalizedUrl.toLowerCase();
    if (seenUrls.has(urlKey)) continue;
    seenUrls.add(urlKey);
    const platform = normalizePlatformName(row?.site || inferPlatformFromProfileUrl(normalizedUrl));
    if (!COLLECTION_READY_SITE_KEYS.has(platform)) continue;
    const handle = extractHandleFromProfileUrl(normalizedUrl);
    if (!handle) continue;
    const username = adjustTargetUsernameForCollection(platform, handle);
    const targetKey = `${platform}|${String(username || '').trim().toLowerCase()}`;
    if (!username || seenTargets.has(targetKey)) continue;
    seenTargets.add(targetKey);
    targets.push({ platform, username });
  }
  return targets;
}

function applyReconPayload(payload, options = {}) {
  const { statusPrefix = 'Recon complete', footprintOnly = false, notifyModules = false } = options;
  const rawPayload = payload && typeof payload === 'object' ? payload : emptyReconPayload();
  latestReconPayload = rawPayload;
  const normalized = filteredReconPayload(rawPayload);
  const derivedTargets = collectionTargetsFromReconResults(normalized.results);
  reconTargets = derivedTargets.length
    ? derivedTargets
    : (Array.isArray(normalized.collection_targets) ? normalized.collection_targets : []);
  if (useReconTargetsBtn instanceof HTMLButtonElement) {
    useReconTargetsBtn.disabled = reconTargets.length === 0;
    useReconTargetsBtn.classList.toggle('hidden', reconTargets.length === 0);
  }
  if (footprintUseTargetsBtn instanceof HTMLButtonElement) {
    footprintUseTargetsBtn.disabled = reconTargets.length === 0;
    footprintUseTargetsBtn.classList.toggle('hidden', reconTargets.length === 0);
  }
  reconLeads = Array.isArray(normalized.leads) ? normalized.leads : [];
  reconProfiles = (Array.isArray(normalized.results) ? normalized.results : []).filter((row) => String(row?.status || '').trim() === 'present');
  reconPersonDataProfile = normalized?.person_data_profile && typeof normalized.person_data_profile === 'object'
    ? normalized.person_data_profile
    : {};
  reconPersonDataProfiles = Array.isArray(normalized?.person_data_profiles) ? normalized.person_data_profiles : [];
  reconOsintProfiles = Array.isArray(normalized?.osint_profiles) ? normalized.osint_profiles : [];
  reconOsintSpecResults = Array.isArray(normalized?.osint_spec_results) ? normalized.osint_spec_results : [];
  reconNumverifyProfiles = Array.isArray(normalized?.numverify_profiles) ? normalized.numverify_profiles : [];
  entityGraphModelCache = null;
  entityGraphLayoutCache = null;
  entityGraphManualPositions.clear();
  if (notifyModules) notifyReconApiModules(normalized);
  renderReconResults(normalized, footprintReconResults);
  if (!footprintOnly) renderReconResults(normalized);
  renderFootprintLikelyName(normalized);
  renderKnownSelectorsPanel(normalized);
  renderLeadsList();
  renderFootprintTimeline();
  renderFootprintEntityGraph();
  renderPatternOfLife(latestPosts);
  renderLocationMap(latestPosts);
  const statusText = `${statusPrefix}: ${normalized.present_count || 0} account match(es) found across ${normalized.checked || 0} checks.`;
  if (footprintReconStatus) footprintReconStatus.textContent = statusText;
  if (!footprintOnly) reconStatus.textContent = statusText;
  maybeAutofillCaseNotesLikelyName();
  maybeAutofillCaseNotesLikelyLocation();
  syncOpenCaseNotesKnownProfilesFromRecon();
}

function renderReconResults(payload, targetEl = reconResults) {
  if (!(targetEl instanceof HTMLElement)) return;
  const rawResults = Array.isArray(payload?.results) ? payload.results : [];
  const rawOsintSpecRows = Array.isArray(payload?.osint_spec_results) ? payload.osint_spec_results : [];
  const sourceSelectorOptions = collectSourceSelectorFilterOptions(rawResults);
  const showSourceSelectorFilter = targetEl === footprintReconResults && sourceSelectorOptions.length > 1;
  if (showSourceSelectorFilter) {
    const valid = sourceSelectorOptions.some((item) => item.key === activeFootprintSourceSelectorKey);
    if (!valid) activeFootprintSourceSelectorKey = 'all';
  } else {
    activeFootprintSourceSelectorKey = 'all';
  }
  const results = activeFootprintSourceSelectorKey !== 'all'
    ? rawResults.filter((row) => sourceSelectorKey(row?.selector_type, row?.selector) === activeFootprintSourceSelectorKey)
    : rawResults;
  const osintSpecRows = activeFootprintSourceSelectorKey !== 'all'
    ? rawOsintSpecRows.filter((row) => sourceSelectorKey(row?.query_type, row?.query_value) === activeFootprintSourceSelectorKey)
    : rawOsintSpecRows;
  const allOsintProfiles = (() => {
    const explicitRaw = Array.isArray(payload?.osint_profiles) ? payload.osint_profiles : [];
    const explicit = activeFootprintSourceSelectorKey !== 'all'
      ? explicitRaw.filter((item) => sourceSelectorKey(item?.query_type, item?.query_value) === activeFootprintSourceSelectorKey)
      : explicitRaw;
    const fromRows = results
      .map((row) => row?.osint_profile)
      .filter((item) => item && typeof item === 'object');
    const merged = [...explicit, ...fromRows];
    const deduped = [];
    const seen = new Set();
    for (const item of merged) {
      const key = [
        String(item?.module || '').trim().toLowerCase(),
        String(item?.profile_url || '').trim().toLowerCase(),
        String(item?.website || '').trim().toLowerCase(),
        String(item?.username || '').trim().toLowerCase(),
        String(item?.email || '').trim().toLowerCase(),
        String(item?.phone || '').trim().toLowerCase(),
      ].join('|');
      if (seen.has(key)) continue;
      seen.add(key);
      deduped.push(item);
    }
    return deduped;
  })();
  const osintProfiles = allOsintProfiles.filter((item) => !isHibpModuleName(item?.module));
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
    : dedupeRowsByProfileUrl(results.filter((row) => row.status === 'present' && row.supported_for_collection && String(row.profile_url || '').trim()));
  const leadPresent = Array.isArray(payload?.unsupported_profiles_with_url)
    ? payload.unsupported_profiles_with_url
    : dedupeRowsByProfileUrl(results.filter((row) => row.status === 'present' && !row.supported_for_collection && String(row.profile_url || '').trim()));
  const nonPdlSupportedPresent = supportedPresent.filter((row) => String(row.source || '').trim().toLowerCase() !== 'pdl');
  const nonPdlLeadPresent = leadPresent.filter((row) => {
    const source = String(row.source || '').trim().toLowerCase();
    if (source === 'pdl') return false;
    if (row?.has_direct_profile_url === false) return false;
    if (!isLikelyAccountProfileUrl(row?.profile_url)) return false;
    return true;
  });
  const knownPresentNoUrl = Array.isArray(payload?.known_present_without_url)
    ? payload.known_present_without_url
    : results.filter((row) => row.status === 'present' && !String(row.profile_url || '').trim());
  const unknown = results.filter((row) => row.status === 'unknown');
  const querySelectors = Array.isArray(payload?.selectors) ? payload.selectors : [];
  const confidenceCounts = { high: 0, medium: 0, low: 0 };
  for (const selector of querySelectors) {
    const level = selectorConfidenceLevel(selector?.type);
    confidenceCounts[level] = (confidenceCounts[level] || 0) + 1;
  }
  const confidenceNote = (() => {
    const total = querySelectors.length;
    if (!total) return '';
    if (confidenceCounts.low > 0) {
      return `<div class="recon-confidence-note warn">Confidence warning: ${confidenceCounts.low} low-confidence selector(s) queried (non-unique, e.g. names/usernames). Validate matches with unique selectors like email/phone.</div>`;
    }
    if (confidenceCounts.medium > 0) {
      return `<div class="recon-confidence-note medium">Confidence caution: ${confidenceCounts.medium} medium-confidence selector(s) queried (usernames can be reused). Corroborate with other evidence.</div>`;
    }
    return '<div class="recon-confidence-note high">High-confidence query set detected (unique selectors such as email/phone/wallet).</div>';
  })();
  const showHibpAggregate = targetEl === footprintReconResults;
  const activeSelectorLabel = activeFootprintSourceSelectorKey === 'all'
    ? ''
    : (sourceSelectorOptions.find((item) => item.key === activeFootprintSourceSelectorKey)?.label || activeFootprintSourceSelectorKey);
  const sourceSelectorFilterMarkup = showSourceSelectorFilter
    ? `
      <div class="recon-group">
        <p>Source Selector Filter</p>
        <div class="type-mix">
          <button type="button" class="mix-pill mix-filter-pill${activeFootprintSourceSelectorKey === 'all' ? ' is-active' : ''}" data-footprint-source-selector="all">
            <span>All selectors</span>
            <strong>${rawResults.length}</strong>
          </button>
          ${sourceSelectorOptions.map((item) => `
            <div class="mix-pill mix-filter-pill mix-filter-pill-with-clear mix-filter-pill-confidence-${escapeAttr(item.confidenceLevel)}${item.key === activeFootprintSourceSelectorKey ? ' is-active' : ''}">
              <button type="button" class="mix-pill-select" data-footprint-source-selector="${escapeAttr(item.key)}">
                <span>${escapeHtml(item.label)}</span>
                <strong>${item.count}</strong>
              </button>
              <button type="button" class="known-selector-action recon-pill-remove recon-pill-action mix-pill-clear" data-footprint-source-clear="${escapeAttr(item.key)}" title="Clear all records for this selector" aria-label="Clear all records for this selector">×</button>
            </div>
          `).join('')}
        </div>
      </div>
    `
    : '';

  targetEl.classList.remove('hidden');
  targetEl.innerHTML = `
    ${sourceSelectorFilterMarkup}
    <div class="recon-summary">
      ${activeSelectorLabel ? `Filtered by ${escapeHtml(activeSelectorLabel)} • ` : ''}
      Checked ${results.length} records • ${nonPdlSupportedPresent.length} collection-ready with URL • ${nonPdlLeadPresent.length} unsupported with URL • ${knownPresentNoUrl.length} known without URL • ${unknown.length} unknown
    </div>
    ${confidenceNote}
    ${osintProfilesMarkup(osintProfiles, results, { removable: targetEl === footprintReconResults })}
    <div class="recon-status-stack">
    <div class="recon-group">
      <p>Collection-ready with account URL</p>
      <div class="recon-pills">
        ${nonPdlSupportedPresent.length
    ? nonPdlSupportedPresent.map((row) => toReconBadge(row, 'success', { removable: targetEl === footprintReconResults, pivotable: false })).join('')
    : '<span class="recon-pill">No supported profiles with direct URLs</span>'}
      </div>
    </div>
    <div class="recon-group">
      <p>Unsupported with account URL</p>
      <div class="recon-pills">
        ${nonPdlLeadPresent.length ? nonPdlLeadPresent.map((row) => toReconBadge(row, 'lead', { removable: targetEl === footprintReconResults, pivotable: false })).join('') : '<span class="recon-pill">No unsupported account URLs detected</span>'}
      </div>
    </div>
    <div class="recon-group">
      <p>Known present without direct account URL</p>
      <div class="recon-pills">
        ${knownPresentNoUrl.length ? knownPresentNoUrl.map((row) => toReconBadge(row, 'warn', { removable: targetEl === footprintReconResults, pivotable: false })).join('') : '<span class="recon-pill">No known-present no-URL results</span>'}
      </div>
    </div>
    </div>
    ${numverifyProfilesMarkup(numverifyProfiles)}
    ${personDataProfileMarkup(personDataProfile, personDataProfiles.length, pdlProfiles, { removable: targetEl === footprintReconResults })}
    ${showHibpAggregate ? hibpAggregateMarkup(allOsintProfiles, osintSpecRows) : ''}
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
  const seen = new Set();
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
    const canonical = canonicalTargetKey(platform, target.username);
    if (seen.has(canonical)) continue;
    seen.add(canonical);
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
    rerenderFromCurrentFilters();
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
  const allPosts = collectionAppendMode ? mergePostsForAppend(latestFetchedPosts, incomingPosts) : incomingPosts;
  latestFetchedPosts = Array.isArray(allPosts) ? allPosts : [];
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  latestFaceClusters = [];
  activeFaceFilters.clear();
  latestFaceRecognition = { available: false, reason: 'not_run' };
  renderFaceRecognitionFilters();
  rerenderFromCurrentFilters();
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
  if (errorData.code === 'apify_token_required') {
    const platforms = Array.isArray(errorData.platforms) ? errorData.platforms.join(', ') : '';
    return `Apify API token is required for ${platforms || 'selected platform(s)'}. Open Config and set Apify API Token.`;
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
  const confidence = selectorConfidenceMeta(normalizedType);
  return `${exampleByType[normalizedType] || exampleByType.username} • ${confidence.label}: ${confidence.guidance}`;
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

function selectorsFromTargetsForKnownEntities(targets) {
  const rows = Array.isArray(targets) ? targets : [];
  const output = [];
  const seen = new Set();
  for (const row of rows) {
    const platform = normalizePlatformName(row?.platform);
    const username = String(row?.username || '').trim().replace(/^@+/, '').toLowerCase();
    if (!username) continue;
    const usernameKey = `username|${username}`;
    if (!seen.has(usernameKey)) {
      seen.add(usernameKey);
      output.push({ type: 'username', value: username });
    }
    if (platform) {
      const platformKey = `platform_username|${platform}|${username}`;
      if (!seen.has(platformKey)) {
        seen.add(platformKey);
        output.push({ type: 'platform_username', value: `${platform}|${username}` });
      }
    }
  }
  return output;
}

function selectorsFromReconForKnownEntities(selectors) {
  const rows = Array.isArray(selectors) ? selectors : [];
  const output = [];
  const seen = new Set();
  for (const row of rows) {
    if (!row || typeof row !== 'object') continue;
    const type = String(row.type || '').trim().toLowerCase();
    const value = String(row.value || '').trim();
    if (!type || !value) continue;
    const key = `${type}|${value.toLowerCase()}`;
    if (seen.has(key)) continue;
    seen.add(key);
    output.push({ type, value });
  }
  return output;
}

async function maybeRestoreArchivedCaseForSelectors(selectors) {
  const rows = Array.isArray(selectors) ? selectors : [];
  if (!rows.length) return false;
  try {
    const matchResponse = await fetch('/api/known-entities/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selectors: rows }),
    });
    if (!matchResponse.ok) return false;
    const matchPayload = await matchResponse.json();
    const matches = Array.isArray(matchPayload?.matches) ? matchPayload.matches : [];
    if (!matches.length) return false;
    const best = matches[0] || {};
    const shouldRestore = window.confirm(
      'This selector is associated with a Known Enitity, would you like to retrieve the case file from archive?',
    );
    if (!shouldRestore) return false;

    const archiveId = String(best.archive_id || '').trim();
    if (!archiveId) return false;
    const restoreResponse = await fetch('/api/known-entities/restore', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ archive_id: archiveId }),
    });
    if (!restoreResponse.ok) {
      const message = await parseErrorResponse(restoreResponse);
      throw new Error(message);
    }
    const restorePayload = await restoreResponse.json();
    const restoredCase = restorePayload?.case && typeof restorePayload.case === 'object' ? restorePayload.case : null;
    if (!restoredCase) return false;
    clearCollectionPolling();
    activeCaseId = String(restoredCase.case_id || '').trim();
    activeCase = restoredCase;
    activeCaseExplicitlySaved = true;
    await loadCases();
    showDashboard();
    setModalOpen(false);
    await refreshPosts();
    const restoredName = String(restoredCase.case_name || 'Archived case').trim() || 'Archived case';
    showNotification(`Restored archived case: ${restoredName}`, 'success');
    return true;
  } catch (error) {
    console.error(error);
    showNotification(`Archive lookup failed: ${error.message || 'unknown error'}`, 'error');
    return false;
  }
}

async function consumeReconStream(selectors, handlers = {}) {
  const onStart = typeof handlers.onStart === 'function' ? handlers.onStart : () => {};
  const onProgress = typeof handlers.onProgress === 'function' ? handlers.onProgress : () => {};
  const onChunk = typeof handlers.onChunk === 'function' ? handlers.onChunk : () => {};
  const onDone = typeof handlers.onDone === 'function' ? handlers.onDone : () => {};
  const response = await fetch('/api/recon/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ selectors }),
  });
  if (!response.ok) {
    const message = await parseErrorResponse(response);
    throw new Error(message);
  }
  if (!response.body || typeof response.body.getReader !== 'function') {
    const payload = await response.json();
    if (payload && typeof payload === 'object') onChunk(payload, { event: 'chunk', selector_index: 1, selectors_total: 1 });
    onDone({ event: 'done', selectors_processed: 1 });
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    while (true) {
      const split = buffer.indexOf('\n');
      if (split < 0) break;
      const line = buffer.slice(0, split).trim();
      buffer = buffer.slice(split + 1);
      if (!line) continue;
      let event;
      try {
        event = JSON.parse(line);
      } catch (error) {
        continue;
      }
      const kind = String(event?.event || '').trim().toLowerCase();
      if (kind === 'start') {
        onStart(event);
        continue;
      }
      if (kind === 'progress') {
        onProgress(event);
        continue;
      }
      if (kind === 'chunk') {
        const payload = event?.payload;
        if (payload && typeof payload === 'object') onChunk(payload, event);
        continue;
      }
      if (kind === 'error') {
        throw new Error(String(event?.message || 'streaming recon failed'));
      }
      if (kind === 'done') {
        onDone(event);
      }
    }
  }
  if (buffer.trim()) {
    try {
      const event = JSON.parse(buffer.trim());
      if (String(event?.event || '').trim().toLowerCase() === 'done') onDone(event);
    } catch (error) {
      // ignore trailing parse errors
    }
  }
}

async function runRecon(event) {
  event.preventDefault();
  hideReconPreview();
  const selectors = parseReconSelectorsFromRows();
  if (!selectors.length) {
    reconStatus.textContent = 'Enter at least one valid selector value.';
    return;
  }
  const archivedRestored = await maybeRestoreArchivedCaseForSelectors(selectorsFromReconForKnownEntities(selectors));
  if (archivedRestored) {
    reconStatus.textContent = 'Known entity case restored from archive.';
    return;
  }

  setReconBusy(true);
  reconStatus.textContent = `Running reconnaissance for ${selectors.length} selector(s)...`;
  reconResults.classList.add('hidden');
  useReconTargetsBtn.classList.add('hidden');
  useReconTargetsBtn.disabled = true;
  goReconAssessmentBtn?.classList.add('hidden');
  if (goReconAssessmentBtn instanceof HTMLButtonElement) goReconAssessmentBtn.disabled = true;
  clearHiddenReconEntities();

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
    latestReconPayload = payload;
    setReconSnapshotFromPayload(payload);
    applyReconPayload(payload, { statusPrefix: 'Recon complete', notifyModules: true });
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
  } catch (error) {
    console.error(error);
    useReconTargetsBtn.classList.add('hidden');
    useReconTargetsBtn.disabled = true;
    goReconAssessmentBtn?.classList.add('hidden');
    if (goReconAssessmentBtn instanceof HTMLButtonElement) goReconAssessmentBtn.disabled = true;
    footprintUseTargetsBtn?.classList.add('hidden');
    if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    latestReconPayload = emptyReconPayload();
    applyReconPayload(latestReconPayload, { statusPrefix: 'Recon failed' });
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
  const archivedRestored = await maybeRestoreArchivedCaseForSelectors(selectorsFromReconForKnownEntities(selectors));
  if (archivedRestored) {
    if (footprintReconStatus) footprintReconStatus.textContent = 'Known entity case restored from archive.';
    return;
  }

  setFootprintBusy(true);
  toggleFootprintPivotProgress(false);
  activeFootprintSourceSelectorKey = 'all';
  if (footprintReconStatus) footprintReconStatus.textContent = `Running reconnaissance for ${selectors.length} selector(s)...`;
  footprintReconResults?.classList.add('hidden');
  footprintUseTargetsBtn?.classList.add('hidden');
  if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
  clearHiddenReconEntities();

  try {
    let aggregate = emptyReconPayload();
    await consumeReconStream(selectors, {
      onStart: (event) => {
        const total = Number(event?.selectors_total) || selectors.length;
        if (footprintReconStatus) footprintReconStatus.textContent = `Recon stream started for ${total} selector(s)...`;
      },
      onProgress: (event) => {
        const idx = Number(event?.selector_index) || 1;
        const total = Number(event?.selectors_total) || selectors.length;
        const type = String(event?.selector_type || '').trim();
        const value = String(event?.selector_value || '').trim();
        if (footprintReconStatus) footprintReconStatus.textContent = `Recon in progress (${idx}/${total}): ${formatSelectorLabel(type, value)}`;
      },
      onChunk: (chunkPayload, event) => {
        aggregate = mergeReconPayloads(aggregate, chunkPayload);
        latestReconPayload = aggregate;
        setReconSnapshotFromPayload(aggregate);
        const idx = Number(event?.selector_index) || selectors.length;
        const total = Number(event?.selectors_total) || selectors.length;
        applyReconPayload(aggregate, { statusPrefix: `Recon streaming (${idx}/${total})`, footprintOnly: true, notifyModules: true });
      },
      onDone: () => {},
    });
    latestReconPayload = aggregate;
    setReconSnapshotFromPayload(aggregate);
    applyReconPayload(aggregate, { statusPrefix: 'Recon complete', footprintOnly: true, notifyModules: true });
    if (reconTargets.length > 0) {
      footprintUseTargetsBtn?.classList.remove('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = false;
    } else {
      footprintUseTargetsBtn?.classList.add('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    }
  } catch (error) {
    console.error(error);
    footprintUseTargetsBtn?.classList.add('hidden');
    if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = true;
    latestReconPayload = emptyReconPayload();
    applyReconPayload(latestReconPayload, { statusPrefix: 'Recon failed', footprintOnly: true });
    if (footprintReconStatus) footprintReconStatus.textContent = `Recon failed: ${error.message || 'unknown error'}`;
  } finally {
    setFootprintBusy(false);
  }
}

async function pivotKnownSelector(selectorType, selectorValue) {
  const type = String(selectorType || '').trim().toLowerCase();
  let value = String(selectorValue || '').trim();
  if (!KNOWN_SELECTOR_GROUPS.includes(type) || !value) return;
  if (type === 'email') value = value.toLowerCase();
  if (type === 'phone') value = value.replace(/[^\d+]/g, '');
  if (type === 'username') value = value.replace(/^@+/, '');
  const pivotType = type === 'location' ? 'name' : type;
  const pivotLabel = formatSelectorLabel(type, value);
  const confirmed = window.confirm(`Run recon?\n${pivotLabel}`);
  if (!confirmed) {
    if (footprintReconStatus) footprintReconStatus.textContent = `Pivot canceled for ${pivotLabel}.`;
    return;
  }

  const selectors = [{ type: pivotType, value }];
  setFootprintBusy(true);
  toggleFootprintPivotProgress(true, `Pivot recon: ${pivotType}`);
  if (footprintReconStatus) footprintReconStatus.textContent = `Pivoting on ${pivotLabel}...`;
  if (footprintSelectorsList instanceof HTMLElement) {
    const existing = parseReconSelectorsFromRows(footprintSelectorsList);
    const exists = existing.some((row) => String(row?.type || '').toLowerCase() === pivotType && String(row?.value || '').toLowerCase() === value.toLowerCase());
    if (!exists) addReconSelectorRow(footprintSelectorsList, pivotType, value);
  }
  try {
    let aggregate = latestReconPayload && typeof latestReconPayload === 'object' ? latestReconPayload : emptyReconPayload();
    await consumeReconStream(selectors, {
      onProgress: (event) => {
        const idx = Number(event?.selector_index) || 1;
        const total = Number(event?.selectors_total) || 1;
        const type = String(event?.selector_type || '').trim();
        const value = String(event?.selector_value || '').trim();
        if (footprintReconStatus) footprintReconStatus.textContent = `Pivot recon running (${idx}/${total}): ${formatSelectorLabel(type, value)}`;
      },
      onChunk: (chunkPayload, event) => {
        aggregate = mergeReconPayloads(aggregate, chunkPayload);
        activeFootprintSourceSelectorKey = 'all';
        latestReconPayload = aggregate;
        setReconSnapshotFromPayload(aggregate);
        const idx = Number(event?.selector_index) || 1;
        const total = Number(event?.selectors_total) || 1;
        applyReconPayload(aggregate, { statusPrefix: `Pivot appended (${idx}/${total})`, footprintOnly: true, notifyModules: true });
      },
      onDone: () => {},
    });
    activeFootprintSourceSelectorKey = 'all';
    latestReconPayload = aggregate;
    setReconSnapshotFromPayload(aggregate);
    applyReconPayload(aggregate, { statusPrefix: 'Pivot appended', footprintOnly: true, notifyModules: true });
    if (reconTargets.length > 0) {
      footprintUseTargetsBtn?.classList.remove('hidden');
      if (footprintUseTargetsBtn instanceof HTMLButtonElement) footprintUseTargetsBtn.disabled = false;
    }
  } catch (error) {
    console.error(error);
    if (footprintReconStatus) footprintReconStatus.textContent = `Pivot failed: ${error.message || 'unknown error'}`;
  } finally {
    toggleFootprintPivotProgress(false);
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

  const requiresApifyPlatforms = ['twitter', 'tiktok', 'instagram'];
  const requestedPlatforms = new Set((Array.isArray(targets) ? targets : []).map((item) => normalizePlatformName(item?.platform)));
  const apifyNeeded = requiresApifyPlatforms.filter((platform) => requestedPlatforms.has(platform));
  if (apifyNeeded.length) {
    try {
      const configResponse = await fetch('/api/config');
      if (configResponse.ok) {
        const configPayload = await configResponse.json();
        const apifyConfigured = Boolean(configPayload?.apify_api_token_configured);
        if (!apifyConfigured) {
          const platformLabel = apifyNeeded.map((item) => platformDisplayName(item)).join(', ');
          const warning = `Apify API token is required before collecting ${platformLabel}. Open Config to add token.`;
          setupStatus.textContent = warning;
          collectionProgressStatus = 'collection blocked: missing apify token';
          updateStatusLine();
          showNotification(warning, 'warn');
          return false;
        }
      }
    } catch (_error) {
      // Backend validation will still block unsupported runs if config check fails.
    }
  }

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
  const archivedRestored = await maybeRestoreArchivedCaseForSelectors(selectorsFromTargetsForKnownEntities(targets));
  if (archivedRestored) {
    setupStatus.textContent = 'Known entity case restored from archive.';
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
viewTimelineBtn?.addEventListener('click', () => setResultsView('timeline'));
viewEntityGraphBtn?.addEventListener('click', () => setResultsView('entitygraph'));
sortSelect.addEventListener('change', queueRefresh);
setupForm.addEventListener('submit', collectAndOpen);
reconForm.addEventListener('submit', runRecon);
footprintReconForm?.addEventListener('submit', runFootprintRecon);
runAiThreatAssessmentBtn?.addEventListener('click', runAiThreatAssessment);
attachReconPreviewHandlers(reconResults);
attachReconPreviewHandlers(footprintReconResults);
attachReconPreviewHandlers(leadsList);
footprintReconResults?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const clearSelectorBtn = target.closest('[data-footprint-source-clear]');
  if (clearSelectorBtn instanceof Element) {
    const key = String(clearSelectorBtn.getAttribute('data-footprint-source-clear') || '').trim().toLowerCase();
    if (!key) return;
    hideResultsForSelector(key);
    if (activeFootprintSourceSelectorKey === key) activeFootprintSourceSelectorKey = 'all';
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'Selector records cleared', footprintOnly: true });
    return;
  }
  const reconRemoveBtn = target.closest('[data-recon-remove]');
  if (reconRemoveBtn instanceof Element) {
    const key = String(reconRemoveBtn.getAttribute('data-recon-remove') || '').trim().toLowerCase();
    if (!key) return;
    hiddenReconRowKeys.add(key);
    const rows = Array.isArray(latestReconPayload?.results) ? latestReconPayload.results : [];
    const row = rows.find((item) => reconRowVisibilityKey(item) === key);
    if (row) {
      const source = String(row?.source || '').trim().toLowerCase();
      if (source === 'osint_industries' && row?.osint_profile) {
        hiddenOsintTileKeys.add(osintTileVisibilityKey(row.osint_profile));
      }
      if (source === 'pdl') {
        const urlKey = String(row?.profile_url || '').trim().toLowerCase();
        if (urlKey) hiddenPdlProfileUrlKeys.add(urlKey);
        const queryType = String(row?.selector_type || '').trim().toLowerCase();
        const queryValue = String(row?.selector || '').trim().toLowerCase();
        const pdlProfiles = Array.isArray(latestReconPayload?.person_data_profiles) ? latestReconPayload.person_data_profiles : [];
        for (const profile of pdlProfiles) {
          if (String(profile?.query_type || '').trim().toLowerCase() !== queryType) continue;
          if (String(profile?.query_value || '').trim().toLowerCase() !== queryValue) continue;
          hiddenPdlProfileKeys.add(pdlProfileVisibilityKey(profile));
        }
      }
    }
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'Result removed', footprintOnly: true });
    return;
  }
  const osintRemoveBtn = target.closest('[data-osint-remove]');
  if (osintRemoveBtn instanceof Element) {
    const key = String(osintRemoveBtn.getAttribute('data-osint-remove') || '').trim().toLowerCase();
    if (!key) return;
    hiddenOsintTileKeys.add(key);
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'OSINT tile removed', footprintOnly: true });
    return;
  }
  const pdlProfileRemoveBtn = target.closest('[data-pdl-profile-remove]');
  if (pdlProfileRemoveBtn instanceof Element) {
    const key = String(pdlProfileRemoveBtn.getAttribute('data-pdl-profile-remove') || '').trim().toLowerCase();
    if (!key) return;
    hiddenPdlProfileKeys.add(key);
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'Person Data Profile removed', footprintOnly: true });
    return;
  }
  const pdlContactRemoveBtn = target.closest('[data-pdl-contact-remove]');
  if (pdlContactRemoveBtn instanceof Element) {
    const key = String(pdlContactRemoveBtn.getAttribute('data-pdl-contact-remove') || '').trim().toLowerCase();
    if (!key) return;
    hiddenPdlContactValueKeys.add(key);
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'PDL value removed', footprintOnly: true });
    return;
  }
  const pdlUrlRemoveBtn = target.closest('[data-pdl-url-remove]');
  if (pdlUrlRemoveBtn instanceof Element) {
    const key = String(pdlUrlRemoveBtn.getAttribute('data-pdl-url-remove') || '').trim().toLowerCase();
    if (!key) return;
    hiddenPdlProfileUrlKeys.add(key);
    applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'Profile URL removed', footprintOnly: true });
    return;
  }
  const pivotBtn = target.closest('[data-recon-pivot-type][data-recon-pivot-value]');
  if (pivotBtn instanceof Element) {
    const type = String(pivotBtn.getAttribute('data-recon-pivot-type') || '').trim().toLowerCase();
    const value = String(pivotBtn.getAttribute('data-recon-pivot-value') || '').trim();
    if (!type || !value) return;
    pivotKnownSelector(type, value);
    return;
  }
  const filterBtn = target.closest('[data-footprint-source-selector]');
  if (!(filterBtn instanceof Element)) return;
  const key = String(filterBtn.getAttribute('data-footprint-source-selector') || '').trim().toLowerCase();
  if (!key) return;
  activeFootprintSourceSelectorKey = key;
  renderReconResults(latestReconPayload || emptyReconPayload(), footprintReconResults);
});
for (const el of [filterTwitter, filterReddit, filterTiktok, filterBluesky, filterInstagram, filterYoutube, filterPost, filterRepost, filterReply, filterQuote, filterComment, filterSelectors, filterIdeologicalIndicators, filterThreatSignals, filterLLMPrimary, filterLLMSecondary]) {
  if (!el) continue;
  el.addEventListener('change', () => {
    updateFilterToggleLabel();
    _dashboardFilterCache = { rows: null, key: '', output: [] };
    rerenderFromCurrentFilters();
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
  const needsFaceRefresh = activeFaceFilters.size > 0
    && !latestFetchedPosts.some((post) => Array.isArray(post?.metadata?.face_recognition) && post.metadata.face_recognition.length > 0);
  if (needsFaceRefresh) {
    refreshPosts();
    return;
  }
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
  _dashboardFilterCache = { rows: null, key: '', output: [] };
  rerenderFromCurrentFilters();
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
patternLifePlatformFilters?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const btn = target.closest('[data-pattern-platform]');
  if (!(btn instanceof HTMLElement)) return;
  const platform = String(btn.getAttribute('data-pattern-platform') || '').trim().toLowerCase();
  if (!platform || !SOURCE_ORDER.includes(platform)) return;
  if (activePatternLifePlatforms.has(platform)) {
    if (activePatternLifePlatforms.size <= 1) return;
    activePatternLifePlatforms.delete(platform);
  } else {
    activePatternLifePlatforms.add(platform);
  }
  refreshPatternOfLifeEstimate();
});
patternLifeRefreshBtn?.addEventListener('click', () => {
  refreshPatternOfLifeEstimate();
  showNotification('Pattern-of-life timezone estimate refreshed.', 'info');
});
footprintTimelineEvents?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const sourceButton = target.closest('[data-timeline-source]');
  if (sourceButton instanceof HTMLElement) {
    const sourceName = String(sourceButton.getAttribute('data-timeline-source') || '').trim();
    if (!sourceName) return;
    if (activeTimelineSources.has(sourceName)) {
      if (activeTimelineSources.size <= 1) return;
      activeTimelineSources.delete(sourceName);
    } else {
      activeTimelineSources.add(sourceName);
    }
    renderFootprintTimeline();
    return;
  }
  const actionButton = target.closest('[data-timeline-action]');
  if (actionButton instanceof HTMLElement) {
    const actionName = String(actionButton.getAttribute('data-timeline-action') || '').trim();
    if (!actionName) return;
    if (activeTimelineActions.has(actionName)) {
      if (activeTimelineActions.size <= 1) return;
      activeTimelineActions.delete(actionName);
    } else {
      activeTimelineActions.add(actionName);
    }
    renderFootprintTimeline();
    return;
  }
  const resetButton = target.closest('[data-timeline-reset]');
  if (!(resetButton instanceof HTMLElement)) return;
  activeTimelineSources.clear();
  activeTimelineActions.clear();
  timelineSelectorQuery = '';
  timelineShowOnlyLinked = false;
  renderFootprintTimeline();
});
footprintTimelineEvents?.addEventListener('input', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (target.matches('[data-timeline-query]') && target instanceof HTMLInputElement) {
    const nextSelectionStart = target.selectionStart;
    const nextSelectionEnd = target.selectionEnd;
    timelineSelectorQuery = target.value || '';
    renderFootprintTimeline();
    const replacement = footprintTimelineEvents.querySelector('[data-timeline-query]');
    if (replacement instanceof HTMLInputElement) {
      replacement.focus();
      if (Number.isFinite(nextSelectionStart) && Number.isFinite(nextSelectionEnd)) {
        replacement.setSelectionRange(nextSelectionStart, nextSelectionEnd);
      }
    }
    return;
  }
  if (target.matches('[data-timeline-linked-only]') && target instanceof HTMLInputElement) {
    timelineShowOnlyLinked = target.checked;
    renderFootprintTimeline();
  }
});
footprintEntityGraphQuery?.addEventListener('input', () => {
  entityGraphQuery = String(footprintEntityGraphQuery.value || '');
  renderFootprintEntityGraph();
});
footprintEntityGraphReset?.addEventListener('click', () => {
  entityGraphViewport = { zoom: 1, offsetX: 0, offsetY: 0 };
  entityGraphQuery = '';
  entityGraphSelectedNodeId = '';
  entityGraphManualPositions.clear();
  entityGraphLayoutCache = null;
  if (footprintEntityGraphQuery instanceof HTMLInputElement) footprintEntityGraphQuery.value = '';
  renderFootprintEntityGraph();
});
footprintEntityGraphCanvas?.addEventListener('wheel', (event) => {
  event.preventDefault();
  const direction = event.deltaY > 0 ? -1 : 1;
  entityGraphViewport.zoom = Math.max(0.35, Math.min(2.8, entityGraphViewport.zoom + (direction * 0.08)));
  applyEntityGraphTransform();
}, { passive: false });
footprintEntityGraphCanvas?.addEventListener('pointerdown', (event) => {
  if (event.button !== 0) return;
  if (!(event.target instanceof Element)) return;
  const nodeEl = event.target.closest('[data-entity-node-id]');
  if (nodeEl instanceof Element) {
    const nodeId = String(nodeEl.getAttribute('data-entity-node-id') || '').trim();
    const pos = entityGraphLayoutCache?.positions?.get(nodeId);
    if (!nodeId || !pos) return;
    entityGraphNodeDrag = {
      nodeId,
      x: event.clientX,
      y: event.clientY,
      startX: pos.x,
      startY: pos.y,
    };
    footprintEntityGraphCanvas.setPointerCapture(event.pointerId);
    return;
  }
  entityGraphPointerPan = {
    x: event.clientX,
    y: event.clientY,
    offsetX: entityGraphViewport.offsetX,
    offsetY: entityGraphViewport.offsetY,
  };
  footprintEntityGraphCanvas.setPointerCapture(event.pointerId);
});
footprintEntityGraphCanvas?.addEventListener('pointermove', (event) => {
  if (entityGraphNodeDrag) {
    const zoom = Math.max(0.35, Math.min(2.8, Number(entityGraphViewport.zoom) || 1));
    const dx = (event.clientX - entityGraphNodeDrag.x) / zoom;
    const dy = (event.clientY - entityGraphNodeDrag.y) / zoom;
    entityGraphManualPositions.set(entityGraphNodeDrag.nodeId, {
      x: entityGraphNodeDrag.startX + dx,
      y: entityGraphNodeDrag.startY + dy,
    });
    entityGraphSelectedNodeId = entityGraphNodeDrag.nodeId;
    entityGraphLayoutCache = null;
    renderFootprintEntityGraph();
    return;
  }
  if (!entityGraphPointerPan) return;
  const dx = event.clientX - entityGraphPointerPan.x;
  const dy = event.clientY - entityGraphPointerPan.y;
  entityGraphViewport.offsetX = entityGraphPointerPan.offsetX + dx;
  entityGraphViewport.offsetY = entityGraphPointerPan.offsetY + dy;
  applyEntityGraphTransform();
});
footprintEntityGraphCanvas?.addEventListener('pointerup', (event) => {
  if (entityGraphNodeDrag) {
    entityGraphNodeDrag = null;
  }
  if (footprintEntityGraphCanvas.hasPointerCapture(event.pointerId)) {
    footprintEntityGraphCanvas.releasePointerCapture(event.pointerId);
  }
  entityGraphPointerPan = null;
});
footprintEntityGraphCanvas?.addEventListener('pointercancel', () => {
  entityGraphNodeDrag = null;
  entityGraphPointerPan = null;
});
footprintEntityGraphCanvas?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const node = target.closest('[data-entity-node-id]');
  if (!(node instanceof Element)) return;
  const nodeId = String(node.getAttribute('data-entity-node-id') || '').trim();
  if (!nodeId) return;
  entityGraphSelectedNodeId = nodeId;
  renderFootprintEntityGraph();
});
footprintEntityGraphDetails?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const focusBtn = target.closest('[data-entity-focus-id]');
  if (!(focusBtn instanceof Element)) return;
  const nodeId = String(focusBtn.getAttribute('data-entity-focus-id') || '').trim();
  if (!nodeId) return;
  entityGraphSelectedNodeId = nodeId;
  renderFootprintEntityGraph();
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
document.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const badge = target.closest('.selector-confidence-badge[data-confidence-key]');
  if (!(badge instanceof HTMLElement)) return;
  const key = String(badge.getAttribute('data-confidence-key') || '').trim().toLowerCase();
  const type = String(badge.getAttribute('data-confidence-type') || '').trim().toLowerCase();
  if (!key || !type) return;
  const current = selectorConfidenceLevelFromOverrideKey(key, type);
  const next = cycleSelectorConfidenceLevel(current);
  selectorConfidenceOverrides.set(key, next);
  saveSelectorConfidenceOverrides();
  rerenderConfidenceOverriddenViews();
});
window.addEventListener('resize', () => {
  if (activeInsightsTab === 'geo') refreshMapLayout();
  if (activeResultsView === 'entitygraph') {
    entityGraphLayoutCache = null;
    renderFootprintEntityGraph();
  }
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
caseNotesNameInput?.addEventListener('input', () => {
  const current = String(caseNotesNameInput.value || '').trim();
  const previousAuto = String(lastAutofilledCaseNotesName || '').trim();
  if (previousAuto && current.toLowerCase() === previousAuto.toLowerCase()) {
    caseNotesNameInput.classList.add('case-notes-name-autofill');
    return;
  }
  if (!current) {
    caseNotesNameInput.classList.remove('case-notes-name-autofill');
    return;
  }
  lastAutofilledCaseNotesName = '';
  caseNotesNameInput.classList.remove('case-notes-name-autofill');
});
caseNotesLocationInput?.addEventListener('input', () => {
  const current = String(caseNotesLocationInput.value || '').trim();
  const previousAuto = String(lastAutofilledCaseNotesLocation || '').trim();
  if (previousAuto && current.toLowerCase() === previousAuto.toLowerCase()) return;
  if (!current) return;
  lastAutofilledCaseNotesLocation = '';
});
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
caseNotesForm?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const toggle = target.closest('[data-case-notes-section-toggle]');
  if (!(toggle instanceof HTMLElement)) return;
  const key = String(toggle.getAttribute('data-case-notes-section-toggle') || '').trim().toLowerCase();
  if (!key) return;
  const excluded = key === 'digital_footprint'
    ? (
      caseNotesExcludedSections.has('digital_footprint_high')
      && caseNotesExcludedSections.has('digital_footprint_medium')
      && caseNotesExcludedSections.has('digital_footprint_low')
    )
    : caseNotesExcludedSections.has(key);
  setCaseNotesSectionExcluded(key, !excluded);
  renderCaseNotesSectionVisibility();
});
caseNotesFootprintResults?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  const toggleBtn = target.closest('[data-case-notes-footprint-key]');
  if (!(toggleBtn instanceof HTMLElement)) return;
  const key = String(toggleBtn.getAttribute('data-case-notes-footprint-key') || '').trim().toLowerCase();
  if (!key) return;
  if (caseNotesExcludedFootprintResultKeys.has(key)) caseNotesExcludedFootprintResultKeys.delete(key);
  else caseNotesExcludedFootprintResultKeys.add(key);
  renderCaseNotesFootprintResults();
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
  setModalMode('collection');
  setModalOpen(true);
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
footprintKnownSelectorsGroups?.addEventListener('click', async (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const removeBtn = target.closest('[data-known-remove]');
  if (removeBtn instanceof Element) {
    const key = String(removeBtn.getAttribute('data-known-remove') || '').trim().toLowerCase();
    if (!key) return;
    const cleared = hideResultsForSelector(key);
    if (cleared) {
      applyReconPayload(latestReconPayload || emptyReconPayload(), { statusPrefix: 'Selector records cleared', footprintOnly: true });
    } else {
      hiddenKnownSelectorKeys.add(key);
      renderKnownSelectorsPanel(latestReconPayload || emptyReconPayload());
    }
    return;
  }
  const pivotBtn = target.closest('[data-known-pivot-type][data-known-pivot-value]');
  if (!(pivotBtn instanceof Element)) return;
  const type = String(pivotBtn.getAttribute('data-known-pivot-type') || '').trim().toLowerCase();
  const value = String(pivotBtn.getAttribute('data-known-pivot-value') || '').trim();
  if (!type || !value) return;
  await pivotKnownSelector(type, value);
});
footprintKnownSelectorsGroups?.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  if (target.closest('[data-known-remove], [data-known-pivot-type], [data-known-pivot-value]')) return;
  const pill = target.closest('[data-known-focus-key]');
  if (!(pill instanceof Element)) return;
  const key = String(pill.getAttribute('data-known-focus-key') || '').trim().toLowerCase();
  if (!key) return;
  setResultsView('footprint');
  focusKnownSelectorInstances(key);
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
  openQuitOptionsModal();
});
quitSessionCaseBtn?.addEventListener('click', async () => {
  openQuitOptionsModal();
});
quitOptionsCancelBtn?.addEventListener('click', closeQuitOptionsModal);
quitOptionsQuitBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ mode: 'quit' });
});
quitOptionsWipeBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ mode: 'wipe' });
});
quitOptionsSaveBtn?.addEventListener('click', async () => {
  await quitPanoptoSession({ mode: 'save' });
});

function openQuitOptionsModal() {
  quitOptionsModal?.classList.remove('hidden');
  syncModalActiveState();
}

function closeQuitOptionsModal() {
  quitOptionsModal?.classList.add('hidden');
  syncModalActiveState();
}

async function quitPanoptoSession(options = {}) {
  const mode = String(options?.mode || 'quit').toLowerCase();
  const clearData = mode === 'wipe';
  const clearConfig = mode === 'wipe';
  if (!confirmUnsavedCaseExit('quit PANOPTO')) return;
  closeQuitOptionsModal();
  if (quitBtn) {
    quitBtn.disabled = true;
    quitBtn.textContent = 'Quitting...';
  }
  if (quitSessionCaseBtn) {
    quitSessionCaseBtn.disabled = true;
    quitSessionCaseBtn.textContent = 'Quitting...';
  }
  if (quitOptionsQuitBtn) {
    quitOptionsQuitBtn.disabled = true;
    quitOptionsQuitBtn.textContent = 'Quitting...';
  }
  if (quitOptionsWipeBtn) {
    quitOptionsWipeBtn.disabled = true;
    quitOptionsWipeBtn.textContent = 'Quitting...';
  }
  if (quitOptionsSaveBtn) {
    quitOptionsSaveBtn.disabled = true;
    quitOptionsSaveBtn.textContent = 'Quitting...';
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
      body: JSON.stringify({ shutdown: true, clear_data: clearData, clear_config: clearConfig }),
      keepalive: true,
    });
    if (mode === 'wipe') {
      statusEl.textContent = 'Session ended. Wiped API keys, cases, and collected data.';
      resultsEl.innerHTML = '<div class="empty">PANOPTO session ended. Restart server to begin fresh.</div>';
    } else if (mode === 'save') {
      statusEl.textContent = 'Session ended. API keys, cases, and associated data were saved.';
      resultsEl.innerHTML = '<div class="empty">PANOPTO session ended. Restart server to continue with saved state.</div>';
    } else {
      statusEl.textContent = 'Session ended.';
      resultsEl.innerHTML = '<div class="empty">PANOPTO session ended.</div>';
    }
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
      quitBtn.textContent = 'Quit';
    }
    if (quitSessionCaseBtn) {
      quitSessionCaseBtn.disabled = false;
      quitSessionCaseBtn.textContent = 'Quit';
    }
    if (quitOptionsQuitBtn) {
      quitOptionsQuitBtn.disabled = false;
      quitOptionsQuitBtn.textContent = 'Quit';
    }
    if (quitOptionsWipeBtn) {
      quitOptionsWipeBtn.disabled = false;
      quitOptionsWipeBtn.textContent = 'Quit and Wipe';
    }
    if (quitOptionsSaveBtn) {
      quitOptionsSaveBtn.disabled = false;
      quitOptionsSaveBtn.textContent = 'Quit and Save';
    }
  }
}
loadSelectorConfidenceOverrides();
initializeDateInputs();
addTargetRow('twitter', '');
addReconSelectorRow(reconSelectorsList, 'username', '');
addReconSelectorRow(footprintSelectorsList, 'username', '');
renderLeadsList();
renderFootprintTimeline();
renderFootprintEntityGraph();
renderFootprintLikelyName(emptyReconPayload());
renderKnownSelectorsPanel(emptyReconPayload());
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
if (caseEditRetentionSelect instanceof HTMLSelectElement) caseEditRetentionSelect.value = DEFAULT_DATA_RETENTION_PERIOD;
if (caseSaveRetentionSelect instanceof HTMLSelectElement) caseSaveRetentionSelect.value = DEFAULT_DATA_RETENTION_PERIOD;
if (configDefaultRetentionSelect instanceof HTMLSelectElement) configDefaultRetentionSelect.value = DEFAULT_DATA_RETENTION_PERIOD;
setWatchlistCadenceVisibility(caseEditStatusSelect, caseEditCadenceField, caseEditCadenceSelect);
setWatchlistCadenceVisibility(caseSaveStatusSelect, caseSaveCadenceField, caseSaveCadenceSelect);
showCaseWorkspace();
loadConfig();
loadCases();
