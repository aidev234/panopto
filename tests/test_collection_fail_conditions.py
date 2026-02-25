from pathlib import Path

import pytest

import panopto.collection_service as collection_service
from panopto.errors import SourceAccessBlockedError


def test_collect_for_targets_marks_blocked_source_as_failure(monkeypatch, tmp_path: Path):
    def _raise_blocked(**_kwargs):
        raise SourceAccessBlockedError(platform="tiktok", username="aoc")

    monkeypatch.setattr(collection_service, "collect_tiktok_posts", _raise_blocked)
    monkeypatch.setattr(collection_service, "save_posts", lambda posts, db_path: 0)
    monkeypatch.setattr(collection_service, "query_posts", lambda **kwargs: {"count": 0, "posts": []})

    payload = collection_service.collect_for_targets(
        targets=[{"platform": "tiktok", "username": "aoc"}],
        start_date="2026-02-01",
        end_date="2026-02-18",
        db_path=tmp_path / "osint_data.db",
        fail_on_total_failure=False,
    )

    assert payload["collected"] == 0
    assert payload["per_target"] == [
        {"platform": "tiktok", "username": "aoc", "status": "blocked", "collected": 0}
    ]
    assert payload["errors"]
    assert payload["errors"][0]["code"] == "blocked_by_protection"


def test_collect_for_targets_raises_on_total_blocked_failure(monkeypatch, tmp_path: Path):
    def _raise_blocked(**_kwargs):
        raise SourceAccessBlockedError(platform="tiktok", username="aoc")

    monkeypatch.setattr(collection_service, "collect_tiktok_posts", _raise_blocked)

    with pytest.raises(collection_service.InvalidRequestError):
        collection_service.collect_for_targets(
            targets=[{"platform": "tiktok", "username": "aoc"}],
            start_date="2026-02-01",
            end_date="2026-02-18",
            db_path=tmp_path / "osint_data.db",
            fail_on_total_failure=True,
        )
