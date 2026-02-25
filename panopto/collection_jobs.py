"""Background collection job orchestration for progressive UI updates."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import threading
import uuid
from typing import Any

from panopto.collection_service import InvalidRequestError, collect_for_targets
from panopto.post_query import parse_day

_LOCK = threading.Lock()
_JOBS: dict[str, dict[str, Any]] = {}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _snapshot(job: dict[str, Any]) -> dict[str, Any]:
    snap: dict[str, Any] = {
        "job_id": job["job_id"],
        "status": job["status"],
        "phase": job["phase"],
        "current_stage": job["current_stage"],
        "total_stages": job["total_stages"],
        "progress": job["progress"],
        "targets": job["targets"],
        "start_date": job["start_date"],
        "end_date": job["end_date"],
        "case_id": job.get("case_id", ""),
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
    }
    if "snapshot" in job:
        snap["snapshot"] = job["snapshot"]
    if "result" in job:
        snap["result"] = job["result"]
    if "error" in job:
        snap["error"] = job["error"]
    return snap


def _update_job(job_id: str, **changes: Any) -> None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        job.update(changes)
        job["updated_at"] = _utc_now_iso()


def _date_stages(start_date: str, end_date: str) -> list[tuple[str, str, str]]:
    start_day = parse_day(start_date)
    end_day = parse_day(end_date)
    if not start_day or not end_day:
        raise InvalidRequestError("start_date and end_date must be valid dates (YYYY-MM-DD or MM/DD/YYYY)")
    if end_day < start_day:
        raise InvalidRequestError("end_date must be on/after start_date")

    quick_start = max(start_day, end_day - timedelta(days=6))
    quick_stage = (quick_start.isoformat(), end_day.isoformat(), "quick_window")
    if quick_start <= start_day:
        return [quick_stage]
    backfill_stage = (start_day.isoformat(), end_day.isoformat(), "backfill")
    return [quick_stage, backfill_stage]


def _run_job(job_id: str) -> None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return
        targets = list(job["targets"])
        start_date = str(job["start_date"])
        end_date = str(job["end_date"])
        case_id = str(job.get("case_id") or "")
        db_path = Path(str(job["db_path"]))
        stages = list(job["stages"])
        total_stages = int(job["total_stages"])

    _update_job(job_id, status="running", phase="quick_window", current_stage=0, progress=0.0)

    final_result: dict[str, Any] | None = None
    try:
        for index, (stage_start, stage_end, phase) in enumerate(stages, start=1):
            _update_job(
                job_id,
                status="running",
                phase=phase,
                current_stage=index,
                progress=round((index - 1) / max(total_stages, 1), 3),
            )
            stage_result = collect_for_targets(
                targets=targets,
                start_date=stage_start,
                end_date=stage_end,
                db_path=db_path,
                case_id=case_id or None,
                fail_on_total_failure=False,
            )
            stage_result["stage"] = phase
            _update_job(
                job_id,
                snapshot=stage_result,
                progress=round(index / max(total_stages, 1), 3),
            )
            final_result = stage_result

        _update_job(
            job_id,
            status="completed",
            phase="completed",
            current_stage=total_stages,
            progress=1.0,
            result=final_result or {},
        )
    except Exception as exc:
        _update_job(
            job_id,
            status="failed",
            phase="failed",
            error={"code": "collection_error", "message": str(exc)},
        )


def start_collection_job(
    *,
    targets: list[dict[str, str]],
    start_date: str,
    end_date: str,
    db_path: Path,
    case_id: str | None = None,
) -> dict[str, Any]:
    if not targets:
        raise InvalidRequestError("at least one target is required")

    stages = _date_stages(start_date=start_date, end_date=end_date)
    job_id = uuid.uuid4().hex
    now = _utc_now_iso()
    job: dict[str, Any] = {
        "job_id": job_id,
        "status": "queued",
        "phase": "queued",
        "current_stage": 0,
        "total_stages": len(stages),
        "progress": 0.0,
        "targets": targets,
        "start_date": start_date,
        "end_date": end_date,
        "case_id": str(case_id or ""),
        "db_path": str(db_path),
        "stages": stages,
        "created_at": now,
        "updated_at": now,
    }
    with _LOCK:
        _JOBS[job_id] = job

    threading.Thread(target=_run_job, args=(job_id,), daemon=True).start()
    with _LOCK:
        return _snapshot(_JOBS[job_id])


def get_collection_job_status(job_id: str) -> dict[str, Any] | None:
    with _LOCK:
        job = _JOBS.get(job_id)
        if not job:
            return None
        return _snapshot(job)
