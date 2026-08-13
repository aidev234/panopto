from __future__ import annotations

import sys
import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


VENDOR_ROOT = Path(__file__).resolve().parents[1] / "panopto" / "_vendor"
if str(VENDOR_ROOT) not in sys.path:
    sys.path.insert(0, str(VENDOR_ROOT))

from user_scanner.core.helpers import ProxyManager, load_categories  # noqa: E402
from user_scanner.core import engine  # noqa: E402
from user_scanner.user_scan.email import protonmail  # noqa: E402
from user_scanner.user_scan.dev import boot_dev  # noqa: E402
from user_scanner.core.result import Result  # noqa: E402
from panopto.recon import _profile_record_from_scanner_row  # noqa: E402


def test_proxy_manager_preserves_explicit_proxy_scheme(tmp_path):
    proxy_file = tmp_path / "proxies.txt"
    proxy_file.write_text("socks5h://127.0.0.1:9050\n127.0.0.1:8080\n", encoding="utf-8")

    manager = ProxyManager(str(proxy_file))

    assert manager.proxies == [
        "socks5h://127.0.0.1:9050",
        "http://127.0.0.1:8080",
    ]


def test_load_categories_includes_new_username_email_category():
    categories = load_categories(is_email=False)

    assert "email" in categories


def test_new_modules_expose_expected_validate_functions():
    assert hasattr(protonmail, "validate_protonmail")
    assert hasattr(boot_dev, "validate_boot")


def test_engine_can_resolve_new_module_category():
    category = engine.find_category(protonmail)
    assert category == "Email"


def test_engine_stream_yields_each_completed_site_result():
    async def fake_check(module, target):
        _ = target
        await asyncio.sleep(module.delay)
        return Result.taken().update(site_name=module.name)

    modules = [SimpleNamespace(name="slow", delay=0.02), SimpleNamespace(name="fast", delay=0)]
    with patch.object(engine, "load_categories", return_value={"test": "test-path"}):
        with patch.object(engine, "load_modules", return_value=modules):
            with patch.object(engine, "check", side_effect=fake_check):
                async def collect():
                    return [item async for item in engine.check_all_stream("example", is_email=False)]
                results = asyncio.run(collect())

    assert [item.site_name for item in results] == ["fast", "slow"]


def test_result_and_profile_record_preserve_all_module_fields():
    result = Result.taken(
        extra={"display name": "Matt Campbell", "followers": 42},
        media={"avatar": "https://example.test/avatar.jpg"},
    ).update(site_name="Example", username="mattcampbellca")

    row = result.as_dict()
    profile = _profile_record_from_scanner_row(row, enrichment_status="complete")

    assert row["extra"] == {"display_name": "Matt Campbell", "followers": 42}
    assert row["media"] == {"avatar": "https://example.test/avatar.jpg"}
    assert profile["profile_record"]["fields"] == {
        "extra.display_name": "Matt Campbell",
        "extra.followers": 42,
        "media.avatar": "https://example.test/avatar.jpg",
    }
