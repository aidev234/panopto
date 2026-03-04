from panopto.collection_jobs import _date_stages


def test_date_stages_single_stage_when_range_within_week():
    stages = _date_stages("2026-02-24", "2026-03-01")
    assert stages == [("2026-02-24", "2026-03-01", "quick_window")]


def test_date_stages_backfill_excludes_quick_window_overlap():
    stages = _date_stages("2026-01-01", "2026-03-01")
    assert stages == [
        ("2026-02-23", "2026-03-01", "quick_window"),
        ("2026-01-01", "2026-02-22", "backfill"),
    ]
