from pathlib import Path


def test_index_uses_local_assets_only():
    html = Path("frontend/static/index.html").read_text(encoding="utf-8")

    assert "http://" not in html
    assert "https://" not in html
    assert "/styles.css" in html
    assert "/app.js" in html
    assert "id=\"collectionStreams\"" in html
    assert "id=\"collectionStreamsSummary\"" in html
    assert "id=\"refreshStreamsBtn\"" in html
    assert "id=\"rerunFailedBtn\"" in html
    assert "id=\"insightsTabGeo\"" in html
    assert "id=\"insightsTabSignals\"" in html
    assert "id=\"openCaseNotesTopBtn\"" in html
    assert "id=\"clearSearchBtn\"" in html
    assert "id=\"collectionContext\"" in html
    assert "id=\"contextTargets\"" in html
    assert "id=\"contextRange\"" in html
    assert "id=\"postingTimezoneMap\"" in html
    assert "id=\"openLlmSandboxBtn\"" in html
    assert "id=\"viewPatternLifeBtn\"" in html
    assert "id=\"viewTimelineBtn\"" in html
    assert "id=\"patternLifeView\"" in html
    assert "id=\"llmSandboxView\"" in html
    assert "id=\"llmSandboxAnalyzeBtn\"" in html
    assert "id=\"llmSandboxResult\"" in html
    assert "id=\"patternLifeMap\"" in html
    assert "id=\"timelineView\"" in html
    assert "id=\"faceRecognitionFilterList\"" in html
    assert "id=\"faceRecognitionFilterEmpty\"" in html
    assert "id=\"runFaceRecognitionBtn\"" in html
    assert "id=\"faceRecognitionStatus\"" in html
    assert "id=\"faceConfidenceRange\"" in html
    assert "id=\"faceConfidenceValue\"" in html
    assert "id=\"quitBtn\"" in html
    assert "id=\"quitSessionCaseBtn\"" in html
    assert "id=\"quitOptionsModal\"" in html
    assert "id=\"quitOptionsSaveBtn\"" in html
    assert "id=\"quitOptionsWipeBtn\"" in html
    assert "id=\"quitOptionsQuitBtn\"" in html


def test_collection_target_platform_options_include_instagram():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "{ value: 'instagram', label: 'Instagram' }" in app_js
    assert "selectors: Array.isArray(payloadRaw.selectors) ? payloadRaw.selectors : []" in app_js
    assert "function renderCollectionStreams()" in app_js
    assert "function startBackgroundCollection(" in app_js
    assert "function beginProgressNotification(" in app_js
    assert "function updateProgressNotification(" in app_js
    assert "function finishProgressNotification(" in app_js
    assert "function setInsightsTab(" in app_js
    assert "function openLlmSandboxFromCaseWorkspace(" in app_js
    assert "function runLlmSandboxAnalysis(" in app_js
    assert "function renderIdentityIntelDetail(" in app_js
    assert "function sandboxAnalysisStatusFromPost(" in app_js
    assert "function renderSandboxDebugDetail(" in app_js
    assert "fetch(`/api/cases/${encodeURIComponent(activeCaseId)}/notes.pdf`, {" in app_js
    assert "method: 'POST'" in app_js
    assert "body: JSON.stringify(draft || {})" in app_js
    assert "Combined Messages" in app_js
    assert "Request Text" in app_js
    assert "renderLlmSandboxExamples();" in app_js
    assert "function applyMixFilters(" in app_js
    assert "function applyFaceFilters(" in app_js
    assert "function renderFaceRecognitionFilters(" in app_js
    assert "function updateFaceRecognitionStatus(" in app_js
    assert "function updateFaceConfidenceDisplays(" in app_js
    assert "function focusFootprintSelectorMatch(" in app_js
    assert "No visible footprint sources found for" in app_js
    assert "data-mix-filter" in app_js
    assert "data-face-filter" in app_js
    assert "data-face-confidence-inline" in app_js
    assert "data-assessment-toggle" in app_js
    assert "persistThreatAssessmentUpdate" in app_js
    assert "showCaseWorkspace() {\n  closeCaseOpenLoadingOverlay();" in app_js
    assert "setModalOpen(false);\n  syncModalActiveState();\n}" in app_js
    assert "showDashboard() {\n  caseWorkspace?.classList.add('hidden');" in app_js
    assert "syncDashboardCaseTitleFromActiveCase();\n  syncModalActiveState();\n}" in app_js


def test_hibp_breach_summary_only_uses_breach_fields():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "const nameValue = objectValue(node, ['breach', 'breach_name', 'breachname']);" in app_js
    assert "profile?.title || profile?.name || profile?.breach" not in app_js
    assert "if (/^(true|false|null|none|yes|no)$/i.test(normalized)) return '';" in app_js
    assert "Array.isArray(payload?.breach_records) ? payload.breach_records : []" in app_js
    assert "breach_records: Array.isArray(payloadRaw.breach_records) ? payloadRaw.breach_records : []" in app_js
    assert "breach_records: dedupeBy([...(base.breach_records || []), ...(incoming.breach_records || [])]" in app_js
    assert "await consumeReconStream(selectors" in app_js
    assert "streamEvent?.partial === true" in app_js
    assert "let aggregate = emptyReconPayload();" in app_js
    assert "activeReconStreamController?.abort();" in app_js
    assert "const dedupeByLatest" in app_js
    assert "Fictional demo" not in app_js
    assert "Fictionalized demonstration data" not in app_js
    assert "fictional.demo.hash" not in app_js


def test_recon_profile_cards_render_registered_and_collection_ready_profiles():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert "url.startsWith('/')" in app_js
    assert "Registered Profiles (${mergedItems.length})" in app_js
    assert "function collectionReadyProfilesMarkup(" in app_js
    assert "'facebook'" in app_js
    assert "Private/Locked" in app_js
    assert "collection-profile-note" in app_js
    assert "collection-profile-card" in app_js
    assert "data-recon-collect-all=\"supported\"" in app_js
    assert ".osint-profile-card {" in css
    assert ".collection-profile-card {" in css
    assert ".collection-profile-grid {" in css


def test_dashboard_header_actions_stay_above_case_view_content():
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert ".case-shell-head {\n  position: relative;\n  z-index: 3;" in css
    assert ".case-head-actions {\n  position: relative;\n  z-index: 4;" in css
    assert ".case-head-actions button {\n  position: relative;\n  z-index: 5;\n}" in css
    assert ".app-header {\n  position: relative;\n  z-index: 3;" in css
    assert ".header-actions {\n  position: relative;\n  z-index: 4;" in css
    assert ".header-actions button {\n  position: relative;\n  z-index: 5;\n}" in css
