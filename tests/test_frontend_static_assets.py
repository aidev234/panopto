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
    assert "function profileAvatarMarkup(className, imageUrl, alt)" in app_js
    assert "const source = normalizeProfileImageUrl(imageUrl) || USER_PLACEHOLDER_AVATAR_URL;" in app_js
    assert "document.addEventListener('error', useProfileAvatarFallback, true);" in app_js
    assert "image.src = USER_PLACEHOLDER_AVATAR_URL;" in app_js
    assert "const MIN_AUTO_CASE_NAME_SOURCES = 3;" in app_js
    assert "case_name_manually_set: true" in app_js
    assert "Number(item?.returnedSources?.size || 0) >= MIN_AUTO_CASE_NAME_SOURCES" in app_js
    assert "const returnedProfileRows = [" in app_js
    assert "profile location: ${location}" in app_js
    assert "function patternLifeProfileSourceCardMarkup(" in app_js
    assert "patternLifeProfileSourceCardMarkup(ref, 'location signal')" in app_js
    assert "Registered Profiles (${mergedItems.length})" in app_js
    assert "function collectionReadyProfilesMarkup(" in app_js
    assert "'facebook'" in app_js
    assert "Private/Locked" in app_js
    assert "collection-profile-note" in app_js
    assert "collection-profile-card" in app_js
    assert "const selectorPill = selectorValue" in app_js
    assert "const targetPill = selectorValue" in app_js
    assert "osint-profile-card${targetPill ? ' has-selector-target' : ''}" in app_js
    assert "const usernameSubheading = username && normalizedUsername !== normalizedIdentity" in app_js
    assert '<div class="collection-profile-actions">${openMarkup}${collectMarkup}${removeMarkup}</div>' in app_js
    assert "data-recon-collect-all=\"supported\"" in app_js
    assert ".osint-profile-card {" in css
    assert ".osint-profile-card.has-selector-target .osint-profile-head" in css
    assert ".osint-profile-card.has-selector-target .osint-profile-actions" in css
    assert ".collection-profile-card {" in css
    assert ".collection-profile-grid {" in css


def test_case_notes_subject_image_prefers_corroborated_returned_profiles():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "function corroboratedSubjectImageCandidates(payload = latestReconPayload)" in app_js
    assert "corroboration += matches.length * 40;" in app_js
    assert "corroboration += matches.length * 30;" in app_js
    assert "function maybeAutofillCaseNotesSubjectImage()" in app_js
    assert "function syncAutofilledSubjectImageToCaseTile()" in app_js
    assert "body: JSON.stringify({ poi_image_url: imageUrl, case_notes: updatedNotes })" in app_js
    assert "const corroboratedReconImage = preferredSubjectImageFromRecon();" in app_js
    assert "maybeAutofillCaseNotesSubjectImage();" in app_js
    assert "syncAutofilledSubjectImageToCaseTile();" in app_js


def test_recon_discovers_profile_names_and_locations_as_known_selectors():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "const addProfileIdentitySelectors = (profile, source, searchedSelectorKey = '') =>" in app_js
    assert "addProfileIdentitySelectors(row?.scanner_result, source, searchedSelectorKey);" in app_js
    assert "addProfileIdentitySelectors(result, normalizeReconSiteLabel(" in app_js
    assert "profileFields?.['extra.location']" in app_js


def test_known_selector_tooltip_reports_corroborating_source_count():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert "corroborating source${sourceCount === 1 ? '' : 's'}" in app_js
    assert 'data-tooltip="${escapeAttr(tooltip)}"' in app_js
    assert "searched selector${searchedSelectorCount === 1 ? '' : 's'}" in app_js
    assert "Search inputs returning this selector" in app_js
    assert "known-selector-tooltip-metrics" in css
    assert ".known-selector-pill:hover .known-selector-tooltip" in css


def test_discovered_selectors_prioritize_cross_query_corroboration():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")
    index_html = Path("frontend/static/index.html").read_text(encoding="utf-8")

    assert "searchedSelectors: new Set()" in app_js
    assert "metaB.searchedSelectors.size - metaA.searchedSelectors.size" in app_js
    assert "searchedSelectorCount" in app_js
    assert "known-selectors-info" in index_html


def test_discovered_selector_tooltips_overlay_the_scrollable_selector_rail():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert "function positionKnownSelectorTooltip(pill)" in app_js
    assert "positionKnownSelectorTooltip(pill);" in app_js
    assert "z-index: 9500;" in css
    assert "--known-selector-tooltip-left" in css


def test_in_case_new_recon_search_appends_to_existing_results():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "const existingPayload = latestReconPayload && typeof latestReconPayload === 'object'" in app_js
    assert "let aggregate = existingPayload;" in app_js
    assert "New recon failed; existing results retained" in app_js


def test_recon_discovers_parsed_osint_industries_selectors():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "const addOsintProfileSelectors = (profile, source, searchedSelectorKey = '') =>" in app_js
    assert "const parsedValues = profile?.parsed_values" in app_js
    assert "addOsintProfileSelectors(profile, normalizeReconSiteLabel(" in app_js


def test_dashboard_header_actions_stay_above_case_view_content():
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert ".case-shell-head {\n  position: relative;\n  z-index: 3;" in css
    assert ".case-head-actions {\n  position: relative;\n  z-index: 4;" in css
    assert ".case-head-actions button {\n  position: relative;\n  z-index: 5;\n}" in css
    assert ".app-header {\n  position: relative;\n  z-index: 3;" in css
    assert ".header-actions {\n  position: relative;\n  z-index: 4;" in css
    assert ".header-actions button {\n  position: relative;\n  z-index: 5;\n}" in css


def test_returned_card_fields_over_80_characters_are_expandable():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")
    css = Path("frontend/static/styles.css").read_text(encoding="utf-8")

    assert "function expandableReturnedFieldMarkup(value)" in app_js
    assert "const previewLength = 80;" in app_js
    assert "data-returned-field-toggle" in app_js
    assert "returnedFieldToggle.textContent = expanded ? 'See more' : 'See less';" in app_js
    assert ".returned-field-toggle" in css


def test_discovered_selectors_use_case_insensitive_canonical_values():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "normalize('NFKC')" in app_js
    assert "if (normalizedType === 'name') return raw.replace(/\\s+/g, ' ').toLocaleLowerCase();" in app_js
    assert ".replace(/\\.bsky\\.social$/i, '')\n      .trim()\n      .toLocaleLowerCase();" in app_js
    assert "return _cleanLocationEntityLabel(raw).toLocaleLowerCase();" in app_js
