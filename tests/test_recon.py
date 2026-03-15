from __future__ import annotations

from unittest.mock import patch

from panopto.recon import (
    _check_linkedin,
    _check_twitter,
    _decode_google_polyline,
    _fetch_osint_profiles,
    _osint_coordinate_pair,
    _shape_person_data_profile,
    normalize_recon_selectors,
    run_recon,
    run_username_recon,
)


def test_check_twitter_uses_x_fallback_when_primary_unknown():
    def _fake_check(*, site, profile_url, not_found_tokens, timeout=12):
        _ = (site, not_found_tokens, timeout)
        if profile_url.endswith("/AOC"):
            return {"site": "twitter", "status": "unknown", "profile_url": profile_url, "reason": "http_503"}
        return {"site": "twitter", "status": "present", "profile_url": profile_url, "reason": ""}

    with patch("panopto.recon._check_html_profile", side_effect=_fake_check):
        result = _check_twitter("AOC")

    assert result["status"] == "present"
    assert result["profile_url"] == "https://x.com/aoc"


def test_check_twitter_marks_inconclusive_as_unknown_not_absent():
    calls = []

    def _fake_check(*, site, profile_url, not_found_tokens, timeout=12):
        _ = (site, not_found_tokens, timeout)
        calls.append(profile_url)
        if profile_url.endswith("/AOC"):
            return {"site": "twitter", "status": "unknown", "profile_url": profile_url, "reason": "http_503"}
        return {"site": "twitter", "status": "absent", "profile_url": profile_url, "reason": "not_found_marker"}

    with patch("panopto.recon._check_html_profile", side_effect=_fake_check):
        result = _check_twitter("AOC")

    assert any("https://x.com/AOC" == call for call in calls)
    assert any("https://x.com/aoc" == call for call in calls)
    assert result["status"] == "unknown"


def test_run_username_recon_includes_twitter_collection_target_when_present():
    with patch("panopto.recon._check_twitter", return_value={"site": "twitter", "status": "present", "profile_url": "https://x.com/aoc", "reason": ""}):
        with patch("panopto.recon._check_reddit", return_value={"site": "reddit", "status": "absent", "profile_url": "", "reason": "http_404"}):
            with patch("panopto.recon._check_tiktok", return_value={"site": "tiktok", "status": "absent", "profile_url": "", "reason": "http_404"}):
                with patch("panopto.recon._check_bluesky", return_value={"site": "bluesky", "status": "absent", "profile_url": "", "reason": "http_404"}):
                    with patch("panopto.recon._check_instagram", return_value={"site": "instagram", "status": "absent", "profile_url": "", "reason": "http_404"}):
                        with patch("panopto.recon._check_youtube", return_value={"site": "youtube", "status": "absent", "profile_url": "", "reason": "http_404"}):
                            with patch("panopto.recon._check_facebook", return_value={"site": "facebook", "status": "absent", "profile_url": "", "reason": "http_404"}):
                                with patch("panopto.recon._check_generic", return_value={"status": "absent", "profile_url": "", "reason": "http_404"}):
                                    payload = run_username_recon("@AOC")

    assert payload["collection_targets"] == [{"platform": "twitter", "username": "AOC"}]


def test_run_username_recon_attaches_screenshot_urls_for_present_profiles():
    present = {"status": "present", "reason": ""}
    absent = {"status": "absent", "profile_url": "", "reason": "http_404"}

    with patch("panopto.recon._check_twitter", return_value={"site": "twitter", "profile_url": "https://x.com/aoc", **present}):
        with patch("panopto.recon._check_reddit", return_value={"site": "reddit", **absent}):
            with patch("panopto.recon._check_tiktok", return_value={"site": "tiktok", **absent}):
                with patch("panopto.recon._check_bluesky", return_value={"site": "bluesky", **absent}):
                    with patch("panopto.recon._check_instagram", return_value={"site": "instagram", **absent}):
                        with patch("panopto.recon._check_youtube", return_value={"site": "youtube", **absent}):
                            with patch("panopto.recon._check_facebook", return_value={"site": "facebook", **absent}):
                                with patch(
                                    "panopto.recon._check_generic",
                                    return_value={"site": "github", "status": "present", "profile_url": "https://github.com/aoc", "reason": ""},
                                ):
                                    with patch("panopto.recon._capture_profile_screenshot", return_value="/recon_shots/test.png?v=1"):
                                        payload = run_username_recon("@AOC")

    twitter_row = next((row for row in payload["results"] if row.get("site") == "twitter"), {})
    assert twitter_row.get("screenshot_url") == "/recon_shots/test.png?v=1"
    assert any(lead.get("site") == "github" and lead.get("screenshot_url") == "/recon_shots/test.png?v=1" for lead in payload["leads"])


def test_run_username_recon_uses_x_dot_com_for_twitter_screenshot_target():
    present = {"status": "present", "reason": ""}
    absent = {"status": "absent", "profile_url": "", "reason": "http_404"}
    capture_calls: list[tuple[str, str]] = []

    def _fake_capture(*, site: str, profile_url: str, timeout: int = 24):
        _ = timeout
        capture_calls.append((site, profile_url))
        return "/recon_shots/test.png?v=1"

    with patch(
        "panopto.recon._check_twitter",
        return_value={"site": "twitter", "profile_url": "https://x.com/AOC", **present},
    ):
        with patch("panopto.recon._check_reddit", return_value={"site": "reddit", **absent}):
            with patch("panopto.recon._check_tiktok", return_value={"site": "tiktok", **absent}):
                with patch("panopto.recon._check_bluesky", return_value={"site": "bluesky", **absent}):
                    with patch("panopto.recon._check_instagram", return_value={"site": "instagram", **absent}):
                        with patch("panopto.recon._check_youtube", return_value={"site": "youtube", **absent}):
                            with patch("panopto.recon._check_facebook", return_value={"site": "facebook", **absent}):
                                with patch("panopto.recon._check_generic", return_value={"status": "absent", "profile_url": "", "reason": "http_404"}):
                                    with patch("panopto.recon._capture_profile_screenshot", side_effect=_fake_capture):
                                        run_username_recon("@AOC")

    assert ("twitter", "https://x.com/AOC") in capture_calls


def test_check_linkedin_treats_sign_in_wall_as_present():
    class _FakeResponse:
        status_code = 200
        text = "<html><body>Sign in to view profile</body></html>"

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        result = _check_linkedin("mattcampbellca")

    assert result["site"] == "linkedin"
    assert result["status"] == "present"
    assert result["profile_url"] == "https://www.linkedin.com/in/mattcampbellca"


def test_normalize_recon_selectors_supports_multi_selector_types():
    selectors = normalize_recon_selectors(
        [
            {"type": "username", "value": "@AOC"},
            {"type": "email", "value": "PERSON@example.com"},
            {"type": "phone", "value": "+1 (202) 555-0199"},
            {"type": "name", "value": "Jane Doe"},
            {"type": "wallet", "value": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"},
            {"type": "email", "value": "PERSON@example.com"},
            {"type": "unknown", "value": "x"},
        ]
    )

    assert selectors == [
        {"type": "username", "value": "AOC"},
        {"type": "email", "value": "person@example.com"},
        {"type": "phone", "value": "+12025550199"},
        {"type": "name", "value": "Jane Doe"},
        {"type": "wallet", "value": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"},
    ]


def test_normalize_recon_selectors_extracts_username_from_profile_urls():
    selectors = normalize_recon_selectors(
        [
            {"type": "username", "value": "https://x.com/Sama/status/12345"},
            {"type": "username", "value": "https://www.reddit.com/user/Cautious_Dirt8409/"},
            {"type": "username", "value": "https://www.youtube.com/@CSPAN/videos"},
            {"type": "username", "value": "https://bsky.app/profile/aoc.bsky.social"},
        ]
    )

    assert selectors == [
        {"type": "username", "value": "Sama"},
        {"type": "username", "value": "Cautious_Dirt8409"},
        {"type": "username", "value": "CSPAN"},
        {"type": "username", "value": "aoc"},
    ]


def test_run_recon_categorizes_supported_unsupported_and_no_url():
    fake_rows = [
        {"site_name": "X (Twitter)", "status": "Found", "url": "https://x.com"},
        {"site_name": "Github", "status": "Found", "url": "https://github.com"},
        {"site_name": "Discord", "status": "Found", "url": ""},
        {"site_name": "Gitlab", "status": "Not Found", "url": "https://gitlab.com"},
    ]
    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon._capture_profile_screenshot", return_value=""):
            payload = run_recon([{"type": "username", "value": "@aoc"}])

    assert payload["collection_targets"] == [{"platform": "twitter", "username": "aoc"}]
    assert any(row.get("site_key") == "github" for row in payload["unsupported_profiles_with_url"])
    assert any(row.get("site_key") == "discord" for row in payload["known_present_without_url"])


def test_run_recon_includes_linkedin_screenshot_when_present():
    fake_rows = [
        {"site_name": "Linkedin", "status": "Found", "url": "https://www.linkedin.com"},
    ]
    capture_calls = []

    def _fake_capture(*, site: str, profile_url: str, timeout: int = 24):
        _ = timeout
        capture_calls.append((site, profile_url))
        return "/recon_shots/linkedin-test.png?v=1"

    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon._capture_profile_screenshot", side_effect=_fake_capture):
            payload = run_recon([{"type": "username", "value": "mattcampbellca"}])

    row = payload["results"][0]
    assert row["site_key"] == "linkedin"
    assert row["profile_url"] == "https://www.linkedin.com/in/mattcampbellca"
    assert row["screenshot_url"] == "/recon_shots/linkedin-test.png?v=1"
    assert ("linkedin", "https://www.linkedin.com/in/mattcampbellca") in capture_calls


def test_run_recon_enriches_with_pdl_profile_and_adds_social_leads():
    fake_rows = [
        {"site_name": "Linkedin", "status": "Found", "url": "https://www.linkedin.com"},
        {"site_name": "Github", "status": "Not Found", "url": "https://github.com"},
    ]
    pdl_data = {
        "id": "pdl-123",
        "full_name": "John Smith",
        "job_title": "Engineer",
        "job_company_name": "Acme",
        "location_name": "New York, NY",
        "profiles": [
            "https://www.facebook.com/john.smith",
            "https://x.com/johnsmith",
            "https://www.reddit.com/user/johnsmith",
        ],
        "linkedin_url": "https://www.linkedin.com/in/john-smith",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon._capture_profile_screenshot", return_value=""):
            with patch("panopto.recon.load_config", return_value={"pdl_api_key": "pdl_test_key"}):
                with patch("panopto.recon._fetch_pdl_profile", return_value=pdl_data):
                    payload = run_recon([{"type": "username", "value": "johnsmith"}])

    profile = payload.get("person_data_profile") or {}
    assert profile.get("full_name") == "John Smith"
    assert profile.get("job_company_name") == "Acme"
    assert any(lead.get("site") == "facebook" for lead in payload.get("leads", []))
    assert {"platform": "twitter", "username": "johnsmith"} in payload.get("collection_targets", [])
    assert {"platform": "reddit", "username": "johnsmith"} in payload.get("collection_targets", [])


def test_run_recon_uses_pdl_email_query_for_email_selector():
    def _fake_fetch(*, api_key: str, email: str = "", profile_url: str = "", timeout: int = 16):
        _ = (api_key, timeout)
        assert email == "person@example.com"
        assert profile_url == ""
        return {"id": "pdl-email-1", "full_name": "Person Example", "profiles": ["https://x.com/personexample"]}

    with patch("panopto.recon._run_user_scanner_selector", return_value=[]):
        with patch("panopto.recon.load_config", return_value={"pdl_api_key": "pdl_test_key"}):
            with patch("panopto.recon._fetch_pdl_profile", side_effect=_fake_fetch):
                with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                    payload = run_recon([{"type": "email", "value": "person@example.com"}])

    assert payload.get("person_data_profile", {}).get("full_name") == "Person Example"
    assert {"platform": "twitter", "username": "personexample"} in payload.get("collection_targets", [])
    assert any(row.get("source") == "pdl" for row in payload.get("results", []))


def test_run_recon_marks_rows_as_pdl_source_when_profile_also_found_by_scanner():
    fake_rows = [
        {"site_name": "X (Twitter)", "status": "Found", "url": "https://x.com"},
    ]
    pdl_data = {
        "id": "pdl-42",
        "full_name": "AOC",
        "profiles": ["https://x.com/aoc", "https://github.com/aoc"],
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon.load_config", return_value={"pdl_api_key": "pdl_test_key"}):
            with patch("panopto.recon._fetch_pdl_profile", return_value=pdl_data):
                with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                    payload = run_recon([{"type": "username", "value": "aoc"}])

    supported = payload.get("collection_ready_profiles", [])
    unsupported = payload.get("unsupported_profiles_with_url", [])
    assert any(row.get("site_key") == "twitter" and row.get("source") == "pdl" for row in supported)
    assert any(row.get("site_key") == "github" and row.get("source") == "pdl" for row in unsupported)
    assert {"platform": "twitter", "username": "aoc"} in payload.get("collection_targets", [])


def test_run_recon_promotes_existing_scanner_row_to_present_when_pdl_confirms_profile():
    fake_rows = [
        {"site_name": "Linkedin", "status": "Error", "url": "https://www.linkedin.com/in/linked-person"},
    ]
    pdl_data = {
        "id": "pdl-999",
        "full_name": "Linked Person",
        "linkedin_url": "https://www.linkedin.com/in/linked-person",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon.load_config", return_value={"pdl_api_key": "pdl_test_key"}):
            with patch("panopto.recon._fetch_pdl_profile", return_value=pdl_data):
                with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                    payload = run_recon(
                        [
                            {"type": "username", "value": "linked-person"},
                            {"type": "email", "value": "linked-person@example.com"},
                        ]
                    )

    unsupported = payload.get("unsupported_profiles_with_url", [])
    assert any(row.get("site_key") == "linkedin" and row.get("source") == "pdl" for row in unsupported)


def test_shape_person_data_profile_includes_expanded_phone_and_email_fields():
    shaped = _shape_person_data_profile(
        {
            "full_name": "Person Example",
            "job_title": "Analyst",
            "location_name": "Boston",
            "work_email": "work@example.com",
            "emails": ["person@example.com", "person@example.com"],
            "phone_numbers": [
                {"type": "work", "number": "+1 555 1000"},
                {"type": "mobile", "number": "+1 555 2000"},
                {"type": "home", "number": "+1 555 3000"},
            ],
            "business_phone": "+1 555 4000",
            "home_phone": "+1 555 5000",
        },
        query_type="email",
        query_value="person@example.com",
    )

    assert shaped["professional_email"] == "work@example.com"
    assert "person@example.com" in shaped["personal_emails"]
    assert shaped["mobile_phone"] == "+1 555 2000"
    assert "+1 555 1000" in shaped["professional_phones"]
    assert "+1 555 4000" in shaped["professional_phones"]
    assert "+1 555 3000" in shaped["personal_phones"]
    assert "+1 555 5000" in shaped["personal_phones"]


def test_shape_person_data_profile_extracts_email_address_from_dict_values():
    shaped = _shape_person_data_profile(
        {
            "full_name": "Person Example",
            "emails": [{"address": "person@example.com"}],
        },
        query_type="email",
        query_value="person@example.com",
    )

    assert shaped["personal_emails"] == ["person@example.com"]


def test_run_recon_builds_facebook_profile_url_for_username_scan():
    fake_rows = [
        {"site_name": "Facebook", "status": "Found", "url": "https://www.facebook.com"},
    ]
    with patch("panopto.recon._run_user_scanner_selector", return_value=fake_rows):
        with patch("panopto.recon._capture_profile_screenshot", return_value=""):
            payload = run_recon([{"type": "username", "value": "MattCampbellca"}])

    row = payload["results"][0]
    assert row["site_key"] == "facebook"
    assert row["profile_url"] == "https://www.facebook.com/MattCampbellca/"
    assert row["category"] == "unsupported_with_url"


def test_run_recon_includes_osint_profiles_and_spec_results():
    osint_profile = {
        "title": "Jane Doe",
        "name": "Jane Doe",
        "first_name": "Jane",
        "last_name": "Doe",
        "username": "janedoe",
        "email": "jane@example.com",
        "profile_url": "https://x.com/janedoe",
        "website": "https://janedoe.example.com",
        "picture_url": "https://cdn.example.com/jane.jpg",
        "bio": "Open source investigator",
        "source": "osint_industries",
    }
    osint_spec = {
        "query_type": "username",
        "query_value": "janedoe",
        "title": "Jane Doe",
        "spec": {"title": "Jane Doe", "username": "janedoe"},
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=[]):
        with patch(
            "panopto.recon.load_config",
            return_value={
                "pdl_api_key": "",
                "osint_industries_api_key": "oi_test_key",
            },
        ):
            with patch("panopto.recon._fetch_osint_profiles", return_value=([osint_profile], [osint_spec], True)):
                with patch("panopto.recon._capture_profile_screenshot", return_value="/recon_shots/osint-test.png?v=1"):
                    payload = run_recon([{"type": "username", "value": "janedoe"}])

    assert payload["osint_profiles"] == [osint_profile]
    assert payload["osint_spec_results"] == [osint_spec]
    assert any(item.get("module") == "osint_industries" for item in payload.get("api_modules_queried", []))
    assert any(row.get("source") == "osint_industries" for row in payload.get("results", []))
    assert any(row.get("screenshot_url") == "/recon_shots/osint-test.png?v=1" for row in payload.get("results", []))
    assert {"platform": "twitter", "username": "janedoe"} in payload.get("collection_targets", [])


def test_run_recon_email_merges_scanner_and_osint_results():
    scanner_rows = [
        {"site_name": "Github", "status": "Found", "url": "https://github.com"},
        {"site_name": "Reddit", "status": "Not Found", "url": "https://reddit.com"},
    ]
    osint_profile = {
        "title": "Matt Campbell",
        "name": "Matt Campbell",
        "module": "strava",
        "profile_url": "https://www.strava.com/athletes/11713407",
        "source": "osint_industries",
        "query_type": "email",
        "query_value": "mattcampbell@gmail.com",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=scanner_rows):
        with patch("panopto.recon.load_config", return_value={"pdl_api_key": "", "osint_industries_api_key": "oi_test_key"}):
            with patch("panopto.recon._fetch_osint_profiles", return_value=([osint_profile], [], True)):
                with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                    payload = run_recon([{"type": "email", "value": "mattcampbell@gmail.com"}])

    assert len(payload.get("osint_profiles") or []) == 1
    assert any(row.get("source") == "osint_industries" for row in payload.get("results", []))
    assert any(
        row.get("source") == "scanner"
        and row.get("selector_type") == "email"
        and row.get("site_key") == "github"
        for row in payload.get("results", [])
    )
    assert any(item.get("module") == "osint_industries" for item in payload.get("api_modules_queried", []))


def test_run_recon_osint_website_only_does_not_emit_account_profile_url():
    osint_profile = {
        "title": "Example Listing",
        "name": "Example Listing",
        "module": "airbnb",
        "website": "https://www.airbnb.com/users/show/12345",
        "source": "osint_industries",
        "query_type": "email",
        "query_value": "mattcampbell@gmail.com",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=[]):
        with patch("panopto.recon.load_config", return_value={"pdl_api_key": "", "osint_industries_api_key": "oi_test_key"}):
            with patch("panopto.recon._fetch_osint_profiles", return_value=([osint_profile], [], True)):
                with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                    payload = run_recon([{"type": "email", "value": "mattcampbell@gmail.com"}])

    osint_rows = [row for row in payload.get("results", []) if row.get("source") == "osint_industries"]
    assert len(osint_rows) == 1
    row = osint_rows[0]
    assert row["profile_url"] == ""
    assert row["has_direct_profile_url"] is False
    assert row["category"] == "known_without_url"
    assert row["site_url"] == "https://www.airbnb.com/users/show/12345"


def test_fetch_osint_profiles_maps_spec_format_fields_into_osint_profile():
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def iter_lines(decode_unicode=True):
            _ = decode_unicode
            yield '{"data":[{"module":"chess","status":"found","reliable_source":true,"front_schemas":[{"image":"https://cdn.example.com/avatar.jpg","timeline":{"registered_date":"2016-08-17T18:28:32","last_seen_date":"2026-03-03T17:18:53"}}],"spec_format":[{"registered":{"type":"bool","proper_key":"Registered","value":true},"id":{"type":"int","proper_key":"Id","value":29522958},"name":{"type":"str","proper_key":"Name","value":"Matt C"},"picture_url":{"type":"str","proper_key":"Picture Url","value":"https://images.example.com/matt.jpg"},"location":{"type":"str","proper_key":"Location","value":"Country: CA"},"username":{"type":"str","proper_key":"Username","value":"mattcampbellca"},"profile_url":{"type":"str","proper_key":"Profile Url","value":"https://www.chess.com/member/mattcampbellca"},"followers":{"type":"int","proper_key":"Followers","value":2},"following":{"type":"int","proper_key":"Following","value":0},"verified":{"type":"bool","proper_key":"Verified","value":false},"private":{"type":"bool","proper_key":"Private","value":false},"creation_date":{"type":"datetime","proper_key":"Creation Date","value":"2016-08-17T18:28:32"},"last_seen":{"type":"datetime","proper_key":"Last Seen","value":"2026-03-03T17:18:53"}}]}]}'

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        profiles, spec_rows, query_succeeded = _fetch_osint_profiles(
            selector_type="username",
            selector_value="mattcampbellca",
            api_key="oi_test_key",
        )

    assert query_succeeded is True
    assert len(profiles) == 1
    profile = profiles[0]
    assert profile["registered"] == "True"
    assert profile["id"] == "29522958"
    assert profile["followers"] == "2"
    assert profile["following"] == "0"
    assert profile["verified"] == "False"
    assert profile["private"] == "False"
    assert profile["creation_date"] == "2016-08-17T18:28:32"
    assert profile["last_seen"] == "2026-03-03T17:18:53"
    assert profile["profile_url"] == "https://www.chess.com/member/mattcampbellca"
    assert len(spec_rows) == 1


def test_fetch_osint_profiles_treats_root_domain_profile_url_as_website_only():
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def iter_lines(decode_unicode=True):
            _ = decode_unicode
            yield '{"data":[{"module":"strava","status":"found","reliable_source":true,"spec_format":[{"name":{"proper_key":"Name","value":"Matt C"},"profile_url":{"proper_key":"Profile Url","value":"https://www.strava.com"},"username":{"proper_key":"Username","value":"mattcampbellca"}}]}]}'

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        profiles, spec_rows, query_succeeded = _fetch_osint_profiles(
            selector_type="username",
            selector_value="mattcampbellca",
            api_key="oi_test_key",
        )

    assert query_succeeded is True
    assert len(spec_rows) == 1
    assert len(profiles) == 1
    profile = profiles[0]
    assert profile["module"] == "strava"
    assert profile["profile_url"] == ""
    assert profile["website"] == "https://www.strava.com"


def test_fetch_osint_profiles_accepts_direct_profile_fields_without_spec_format():
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def iter_lines(decode_unicode=True):
            _ = decode_unicode
            yield '{"data":[{"module":"x","status":"found","username":"janedoe","name":"Jane Doe","profile_url":"https://x.com/janedoe","bio":"OSINT analyst"}]}'

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        profiles, spec_rows, query_succeeded = _fetch_osint_profiles(
            selector_type="username",
            selector_value="janedoe",
            api_key="oi_test_key",
        )

    assert query_succeeded is True
    assert len(profiles) == 1
    assert profiles[0]["profile_url"] == "https://x.com/janedoe"
    assert profiles[0]["username"] == "janedoe"
    assert len(spec_rows) == 1


def test_fetch_osint_profiles_keeps_biolocation_and_uses_location_fallback():
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def iter_lines(decode_unicode=True):
            _ = decode_unicode
            yield (
                '{"data":[{"module":"forum","status":"found","reliable_source":true,'
                '"spec_format":[{"username":{"proper_key":"Username","value":"geo_user"},'
                '"profile_url":{"proper_key":"Profile Url","value":"https://example.com/u/geo_user"},'
                '"biolocation":{"proper_key":"Biolocation","value":"Country: CA"}'
                '}]}]}'
            )

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        profiles, _, query_succeeded = _fetch_osint_profiles(
            selector_type="username",
            selector_value="geo_user",
            api_key="oi_test_key",
        )

    assert query_succeeded is True
    assert len(profiles) == 1
    profile = profiles[0]
    assert profile["biolocation"] == "Country: CA"
    assert profile["location"] == "Country: CA"


def test_decode_google_polyline_decodes_lat_lon_pairs():
    points = _decode_google_polyline("_p~iF~ps|U_ulLnnqC_mqNvxq`@")
    assert len(points) == 3
    assert points[0] == {"lat": 38.5, "lon": -120.2}
    assert points[-1] == {"lat": 43.252, "lon": -126.453}


def test_osint_coordinate_pair_swaps_lon_lat_when_inverted():
    pair = _osint_coordinate_pair([-122.3321, 47.6062])
    assert pair == (47.6062, -122.3321)


def test_fetch_osint_profiles_extracts_geo_signals_from_points_and_polylines():
    class _FakeResponse:
        status_code = 200

        @staticmethod
        def iter_lines(decode_unicode=True):
            _ = decode_unicode
            yield (
                '{"data":[{"module":"strava","status":"found","reliable_source":true,'
                '"spec_format":[{"name":{"proper_key":"Name","value":"Matt Route"},'
                '"profile_url":{"proper_key":"Profile Url","value":"https://www.strava.com/athletes/matt"},'
                '"review_text":{"proper_key":"Review Text","value":"Great ride around Seattle"},'
                '"review_location":{"lat":47.6062,"lon":-122.3321},'
                '"route_polyline":"_p~iF~ps|U_ulLnnqC_mqNvxq`@"}]}]}'
            )

    with patch("panopto.recon.requests.get", return_value=_FakeResponse()):
        profiles, _, query_succeeded = _fetch_osint_profiles(
            selector_type="email",
            selector_value="matt@example.com",
            api_key="oi_test_key",
        )

    assert query_succeeded is True
    assert len(profiles) == 1
    geo_signals = profiles[0].get("geo_signals") or []
    point_signals = [item for item in geo_signals if item.get("kind") == "point"]
    route_signals = [item for item in geo_signals if item.get("kind") == "polyline"]
    assert any(abs(float(item.get("lat") or 0) - 47.6062) < 0.0001 for item in point_signals)
    assert route_signals
    assert len(route_signals[0].get("coordinates") or []) >= 3


def test_run_recon_includes_numverify_phone_results():
    numverify_payload = {
        "valid": True,
        "number": "+12025550199",
        "international_format": "+1 202-555-0199",
        "country_name": "United States of America",
        "location": "Washington",
        "carrier": "Verizon",
        "line_type": "mobile",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=[]):
        with patch(
            "panopto.recon.load_config",
            return_value={
                "pdl_api_key": "",
                "osint_industries_api_key": "",
                "numverify_api_key": "numverify_test_key",
            },
        ):
            with patch("panopto.recon._fetch_numverify_profile", return_value=numverify_payload):
                payload = run_recon([{"type": "phone", "value": "+1 (202) 555-0199"}])

    assert len(payload["numverify_profiles"]) == 1
    profile = payload["numverify_profiles"][0]
    assert profile["country_name"] == "United States of America"
    assert profile["carrier"] == "Verizon"
    assert any(
        row.get("source") == "numverify"
        and row.get("site_key") == "numverify"
        and row.get("status") == "present"
        for row in payload.get("results", [])
    )
    assert any(item.get("module") == "numverify" for item in payload.get("api_modules_queried", []))


def test_run_recon_reports_all_successfully_queried_api_modules():
    pdl_data = {
        "id": "pdl-123",
        "full_name": "John Smith",
        "profiles": ["https://x.com/johnsmith"],
    }
    osint_profile = {
        "title": "John Smith",
        "name": "John Smith",
        "username": "johnsmith",
        "profile_url": "https://x.com/johnsmith",
        "source": "osint_industries",
    }
    numverify_payload = {
        "valid": True,
        "number": "+12025550199",
        "country_name": "United States of America",
    }

    with patch("panopto.recon._run_user_scanner_selector", return_value=[]):
        with patch(
            "panopto.recon.load_config",
            return_value={
                "pdl_api_key": "pdl_test_key",
                "osint_industries_api_key": "oi_test_key",
                "numverify_api_key": "numverify_test_key",
            },
        ):
            with patch("panopto.recon._fetch_pdl_profile", return_value=pdl_data):
                with patch("panopto.recon._fetch_osint_profiles", return_value=([osint_profile], [], True)):
                    with patch("panopto.recon._fetch_numverify_profile", return_value=numverify_payload):
                        with patch("panopto.recon._capture_profile_screenshot", return_value=""):
                            payload = run_recon(
                                [
                                    {"type": "email", "value": "person@example.com"},
                                    {"type": "username", "value": "johnsmith"},
                                    {"type": "phone", "value": "+1 (202) 555-0199"},
                                ]
                            )

    modules = {item.get("module") for item in payload.get("api_modules_queried", [])}
    assert "people_data_labs" in modules
    assert "osint_industries" in modules
    assert "numverify" in modules
