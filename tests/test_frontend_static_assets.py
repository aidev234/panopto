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
    assert "id=\"insightsTabOps\"" in html
    assert "id=\"insightsTabGeo\"" in html
    assert "id=\"insightsTabSignals\"" in html
    assert "id=\"insightsTabNotes\"" in html
    assert "id=\"clearSearchBtn\"" in html
    assert "id=\"collectionContext\"" in html
    assert "id=\"contextTargets\"" in html
    assert "id=\"contextRange\"" in html
    assert "id=\"postingTimezoneMap\"" in html


def test_collection_target_platform_options_include_instagram():
    app_js = Path("frontend/static/app.js").read_text(encoding="utf-8")

    assert "{ value: 'instagram', label: 'Instagram' }" in app_js
    assert "function renderCollectionStreams()" in app_js
    assert "function startBackgroundCollection(" in app_js
    assert "function setInsightsTab(" in app_js
    assert "function applyMixFilters(" in app_js
    assert "data-mix-filter" in app_js
    assert "data-assessment-toggle" in app_js
    assert "persistThreatAssessmentUpdate" in app_js
