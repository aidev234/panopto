from __future__ import annotations

import os
import shutil
import threading
from pathlib import Path
from unittest.mock import patch

import pytest
from http.server import ThreadingHTTPServer

selenium = pytest.importorskip("selenium")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait

from frontend.server import PostExplorerHandler
from panopto.storage.posts import create_case


def _resolve_geckodriver_path() -> str | None:
    configured = os.environ.get("GECKODRIVER", "").strip()
    if configured:
        return configured
    bundled = Path("/tmp/geckodriver")
    if bundled.exists():
        return str(bundled)
    return shutil.which("geckodriver")


pytestmark = pytest.mark.skipif(
    shutil.which("firefox") is None or _resolve_geckodriver_path() is None,
    reason="firefox + geckodriver are required for browser smoke tests",
)


@pytest.fixture
def frontend_live_server(tmp_path: Path):
    db_path = tmp_path / "browser-smoke.db"
    create_case(
        case_name="Browser Smoke Case",
        status="Open",
        threat_level="Low Threat",
        known_location="Boston",
        db_path=str(db_path),
    )

    with patch("frontend.server.DEFAULT_DB_PATH", db_path):
        server = ThreadingHTTPServer(("127.0.0.1", 0), PostExplorerHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


@pytest.fixture
def browser():
    options = FirefoxOptions()
    options.add_argument("-headless")
    service = FirefoxService(executable_path=_resolve_geckodriver_path(), log_output=os.devnull)
    driver = webdriver.Firefox(options=options, service=service)
    driver.set_window_size(1440, 1200)
    try:
        yield driver
    finally:
        driver.quit()


def _wait_visible(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        lambda current: _visible_or_false(current.find_element(by, value)),
    )


def _wait_hidden(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    wait.until(lambda current: "hidden" in current.find_element(by, value).get_attribute("class").split())


def element_is_visible(element) -> bool:
    return element.is_displayed() and "hidden" not in str(element.get_attribute("class") or "").split()


def _visible_or_false(element):
    return element if element_is_visible(element) else False


def test_workspace_settings_and_exit_buttons_open_modals(frontend_live_server: str, browser):
    browser.get(frontend_live_server)

    _wait_visible(browser, By.CSS_SELECTOR, '[data-case-open]')

    browser.find_element(By.ID, "openConfigBtn").click()
    _wait_visible(browser, By.ID, "configModal")
    browser.find_element(By.ID, "configCloseBtn").click()
    _wait_hidden(browser, By.ID, "configModal")

    browser.find_element(By.ID, "quitSessionCaseBtn").click()
    _wait_visible(browser, By.ID, "quitOptionsModal")
    browser.find_element(By.ID, "quitOptionsCancelBtn").click()
    _wait_hidden(browser, By.ID, "quitOptionsModal")


def test_dashboard_header_buttons_open_and_exit_cleanly(frontend_live_server: str, browser):
    browser.get(frontend_live_server)

    open_case_btn = _wait_visible(browser, By.CSS_SELECTOR, '[data-case-open]')
    open_case_btn.click()

    _wait_visible(browser, By.ID, "dashboardPanel")
    _wait_visible(browser, By.ID, "saveQuitCaseBtn")

    browser.find_element(By.ID, "saveQuitCaseBtn").click()
    _wait_visible(browser, By.ID, "caseSaveModal")
    browser.find_element(By.ID, "caseSaveCloseBtn").click()
    _wait_hidden(browser, By.ID, "caseSaveModal")

    browser.find_element(By.ID, "quitBtn").click()
    _wait_visible(browser, By.ID, "quitOptionsModal")
    browser.find_element(By.ID, "quitOptionsCancelBtn").click()
    _wait_hidden(browser, By.ID, "quitOptionsModal")

    browser.find_element(By.ID, "backToCasesBtn").click()
    _wait_visible(browser, By.ID, "caseWorkspace")
    _wait_hidden(browser, By.ID, "dashboardPanel")
