from __future__ import annotations

from unittest.mock import patch

from panopto.recon import _check_twitter, run_username_recon


def test_check_twitter_uses_x_fallback_when_primary_unknown():
    def _fake_check(*, site, profile_url, not_found_tokens, timeout=12):
        _ = (site, not_found_tokens, timeout)
        if "twitterwebviewer.com" in profile_url:
            return {"site": "twitter", "status": "unknown", "profile_url": profile_url, "reason": "http_503"}
        return {"site": "twitter", "status": "present", "profile_url": profile_url, "reason": ""}

    with patch("panopto.recon._check_html_profile", side_effect=_fake_check):
        result = _check_twitter("AOC")

    assert result["status"] == "present"
    assert result["profile_url"] == "https://twitterwebviewer.com/@AOC"


def test_check_twitter_marks_inconclusive_as_unknown_not_absent():
    calls = []

    def _fake_check(*, site, profile_url, not_found_tokens, timeout=12):
        _ = (site, not_found_tokens, timeout)
        calls.append(profile_url)
        if "twitterwebviewer.com" in profile_url:
            return {"site": "twitter", "status": "unknown", "profile_url": profile_url, "reason": "http_503"}
        return {"site": "twitter", "status": "absent", "profile_url": profile_url, "reason": "not_found_marker"}

    with patch("panopto.recon._check_html_profile", side_effect=_fake_check):
        result = _check_twitter("AOC")

    assert any("twitterwebviewer.com/@AOC" in call for call in calls)
    assert any("twitterwebviewer.com/@aoc" in call for call in calls)
    assert result["status"] == "unknown"


def test_run_username_recon_includes_twitter_collection_target_when_present():
    with patch("panopto.recon._check_twitter", return_value={"site": "twitter", "status": "present", "profile_url": "https://x.com/aoc", "reason": ""}):
        with patch("panopto.recon._check_reddit", return_value={"site": "reddit", "status": "absent", "profile_url": "", "reason": "http_404"}):
            with patch("panopto.recon._check_tiktok", return_value={"site": "tiktok", "status": "absent", "profile_url": "", "reason": "http_404"}):
                with patch("panopto.recon._check_bluesky", return_value={"site": "bluesky", "status": "absent", "profile_url": "", "reason": "http_404"}):
                    with patch("panopto.recon._check_instagram", return_value={"site": "instagram", "status": "absent", "profile_url": "", "reason": "http_404"}):
                        with patch("panopto.recon._check_youtube", return_value={"site": "youtube", "status": "absent", "profile_url": "", "reason": "http_404"}):
                            with patch("panopto.recon._check_generic", return_value={"status": "absent", "profile_url": "", "reason": "http_404"}):
                                payload = run_username_recon("@AOC")

    assert payload["collection_targets"] == [{"platform": "twitter", "username": "AOC"}]
