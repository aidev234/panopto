import time

import panopto.collection_jobs as collection_jobs
from panopto.collection_jobs import _date_stages


def test_date_stages_single_stage_when_range_within_week():
    stages = _date_stages("2026-02-24", "2026-03-01")
    assert stages == [("2026-02-24", "2026-03-01", "full_range")]


def test_date_stages_single_stage_when_range_exceeds_week():
    stages = _date_stages("2026-01-01", "2026-03-01")
    assert stages == [("2026-01-01", "2026-03-01", "full_range")]


def test_run_job_marks_timeout_when_stage_exceeds_limit(monkeypatch, tmp_path):
    def _slow_collect(**_kwargs):
        time.sleep(0.05)
        return {"collected": 0, "inserted": 0, "count": 0, "posts": [], "per_target": [], "errors": []}

    monkeypatch.setattr(collection_jobs, "collect_for_targets", _slow_collect)
    monkeypatch.setattr(collection_jobs, "COLLECTION_STAGE_TIMEOUT_SECONDS", 0.01)

    job_id = "job-timeout-test"
    collection_jobs._JOBS[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "phase": "queued",
        "current_stage": 0,
        "total_stages": 1,
        "progress": 0.0,
        "targets": [{"platform": "twitter", "username": "aoc"}],
        "start_date": "2026-03-01",
        "end_date": "2026-03-05",
        "case_id": "",
        "db_path": str(tmp_path / "osint_data.db"),
        "stages": [("2026-03-01", "2026-03-05", "quick_window")],
        "created_at": collection_jobs._utc_now_iso(),
        "updated_at": collection_jobs._utc_now_iso(),
    }
    try:
        collection_jobs._run_job(job_id)
        payload = collection_jobs.get_collection_job_status(job_id)
        assert payload
        assert payload["status"] == "failed"
        assert payload["phase"] == "failed"
        assert payload["error"]["code"] == "collection_timeout"
    finally:
        collection_jobs._JOBS.pop(job_id, None)


def test_start_collection_job_reuses_inflight_identical_job(tmp_path):
    job_id = "job-inflight-1"
    collection_jobs._JOBS[job_id] = {
        "job_id": job_id,
        "status": "running",
        "phase": "full_range",
        "current_stage": 1,
        "total_stages": 1,
        "progress": 0.5,
        "targets": [{"platform": "tiktok", "username": "aoc"}],
        "targets_signature": (("tiktok", "aoc"),),
        "start_date": "2026-01-01",
        "end_date": "2026-03-01",
        "case_id": "",
        "db_path": str(tmp_path / "osint_data.db"),
        "stages": [("2026-01-01", "2026-03-01", "full_range")],
        "created_at": collection_jobs._utc_now_iso(),
        "updated_at": collection_jobs._utc_now_iso(),
    }
    try:
        payload = collection_jobs.start_collection_job(
            targets=[{"platform": "tiktok", "username": "aoc"}],
            start_date="2026-01-01",
            end_date="2026-03-01",
            db_path=tmp_path / "osint_data.db",
            case_id=None,
        )
        assert payload["job_id"] == job_id
    finally:
        collection_jobs._JOBS.pop(job_id, None)


def test_stage_timeout_seconds_extends_for_tiktok_instagram():
    fast = collection_jobs._stage_timeout_seconds([{"platform": "twitter", "username": "aoc"}])
    slow_tiktok = collection_jobs._stage_timeout_seconds([{"platform": "tiktok", "username": "aoc"}])
    slow_instagram = collection_jobs._stage_timeout_seconds([{"platform": "instagram", "username": "aoc"}])
    assert fast == float(collection_jobs.COLLECTION_STAGE_TIMEOUT_SECONDS)
    assert slow_tiktok == float(collection_jobs.SLOW_APIFY_STAGE_TIMEOUT_SECONDS)
    assert slow_instagram == float(collection_jobs.SLOW_APIFY_STAGE_TIMEOUT_SECONDS)
