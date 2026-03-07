from panopto.collectors import apify as apify_collector


class _FakeResponse:
    def __init__(self, status_code: int, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = str(payload)

    def json(self):
        return self._payload


def test_load_apify_token_prefers_panopto_env(monkeypatch):
    monkeypatch.setenv("PANOPTO_APIFY_API_TOKEN", "panopto-token")
    monkeypatch.setenv("APIFY_API_TOKEN", "fallback-token")

    token = apify_collector.load_apify_token()

    assert token == "panopto-token"


def test_load_apify_token_uses_standard_env_fallback(monkeypatch):
    monkeypatch.delenv("PANOPTO_APIFY_API_TOKEN", raising=False)
    monkeypatch.setenv("APIFY_API_TOKEN", "fallback-token")

    token = apify_collector.load_apify_token()

    assert token == "fallback-token"


def test_load_apify_token_uses_saved_config_when_env_missing(monkeypatch):
    monkeypatch.delenv("PANOPTO_APIFY_API_TOKEN", raising=False)
    monkeypatch.delenv("APIFY_API_TOKEN", raising=False)
    monkeypatch.setattr(apify_collector, "load_apify_token", apify_collector.load_apify_token)

    from panopto import config as config_module

    monkeypatch.setattr(config_module, "load_config", lambda: {"apify_api_token": "saved-config-token"})

    token = apify_collector.load_apify_token()

    assert token == "saved-config-token"


def test_run_actor_sync_get_items_returns_items_from_sync_endpoint(monkeypatch):
    monkeypatch.setenv("PANOPTO_APIFY_API_TOKEN", "token123")
    monkeypatch.setattr(
        apify_collector.requests,
        "post",
        lambda *args, **kwargs: _FakeResponse(200, [{"id": "p1"}, "skip", {"id": "p2"}]),
    )

    items = apify_collector.run_actor_sync_get_items(actor_id="apify/instagram-scraper", actor_input={"x": 1})

    assert items == [{"id": "p1"}, {"id": "p2"}]


def test_run_actor_sync_get_items_fetches_dataset_items_from_run_metadata(monkeypatch):
    monkeypatch.setenv("PANOPTO_APIFY_API_TOKEN", "token123")
    monkeypatch.setattr(
        apify_collector.requests,
        "post",
        lambda *args, **kwargs: _FakeResponse(
            200,
            {"data": {"id": "run-1", "status": "SUCCEEDED", "defaultDatasetId": "dataset-1"}},
        ),
    )

    def _fake_get(url, params=None, timeout=None):
        if "/datasets/dataset-1/items" in url:
            return _FakeResponse(200, [{"id": "d1"}, {"id": "d2"}])
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr(apify_collector.requests, "get", _fake_get)

    items = apify_collector.run_actor_sync_get_items(actor_id="apify/instagram-scraper", actor_input={"x": 1})

    assert items == [{"id": "d1"}, {"id": "d2"}]


def test_run_actor_sync_get_items_polls_run_then_fetches_dataset(monkeypatch):
    monkeypatch.setenv("PANOPTO_APIFY_API_TOKEN", "token123")
    monkeypatch.setattr(
        apify_collector.requests,
        "post",
        lambda *args, **kwargs: _FakeResponse(
            200,
            {"data": {"id": "run-2", "status": "RUNNING", "defaultDatasetId": ""}},
        ),
    )
    monkeypatch.setattr(apify_collector.time, "sleep", lambda _seconds: None)

    calls: list[str] = []

    def _fake_get(url, params=None, timeout=None):
        calls.append(url)
        if "/actor-runs/run-2" in url and len(calls) == 1:
            return _FakeResponse(
                200,
                {"data": {"id": "run-2", "status": "SUCCEEDED", "defaultDatasetId": "dataset-2"}},
            )
        if "/datasets/dataset-2/items" in url:
            return _FakeResponse(200, [{"id": "x1"}])
        raise AssertionError(f"unexpected url: {url}")

    monkeypatch.setattr(apify_collector.requests, "get", _fake_get)

    items = apify_collector.run_actor_sync_get_items(actor_id="apify/instagram-scraper", actor_input={"x": 1})

    assert items == [{"id": "x1"}]
