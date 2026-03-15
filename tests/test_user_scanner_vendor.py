from __future__ import annotations

import sys
from pathlib import Path


VENDOR_ROOT = Path(__file__).resolve().parents[1] / "panopto" / "_vendor"
if str(VENDOR_ROOT) not in sys.path:
    sys.path.insert(0, str(VENDOR_ROOT))

from user_scanner.core.helpers import ProxyManager, load_categories  # noqa: E402
from user_scanner.core import engine  # noqa: E402
from user_scanner.user_scan.email import protonmail  # noqa: E402
from user_scanner.user_scan.dev import boot_dev  # noqa: E402


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
    assert hasattr(boot_dev, "validate_boot_dev")


def test_engine_can_resolve_new_module_category():
    category = engine.find_category(protonmail)
    assert category == "Email"
