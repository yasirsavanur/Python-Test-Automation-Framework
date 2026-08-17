"""Shared pytest configuration, lifecycle fixtures, and failure evidence."""

from __future__ import annotations

import re
from collections.abc import Generator
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from automation_framework.api_client import ApiClient
from automation_framework.config import SUPPORTED_BROWSERS, FrameworkConfig
from automation_framework.driver_factory import DriverFactory
from tests.support.demo_server import RunningDemoServer, start_demo_server


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("orbit automation")
    group.addoption("--browser", choices=SUPPORTED_BROWSERS, default="chrome")
    group.addoption("--headed", action="store_true", help="Show the local browser window")
    group.addoption("--grid-url", help="Remote Selenium Grid endpoint")
    group.addoption("--base-url", help="Override the system-under-test URL")
    group.addoption("--timeout", type=float, default=10.0, help="Explicit wait timeout")
    group.addoption("--artifacts-dir", default="artifacts", help="Failure evidence directory")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"report_{report.when}", report)


@pytest.fixture(scope="session")
def framework_config(pytestconfig: pytest.Config) -> FrameworkConfig:
    return FrameworkConfig.from_pytest(pytestconfig)


@pytest.fixture(scope="session")
def demo_server() -> Generator[RunningDemoServer, None, None]:
    root = Path(__file__).resolve().parents[1] / "demo_app"
    server = start_demo_server(root)
    yield server
    server.close()


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config, request: pytest.FixtureRequest) -> str:
    override = pytestconfig.getoption("--base-url")
    if override:
        return override.rstrip("/")
    server = request.getfixturevalue("demo_server")
    return server.url


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    return ApiClient(base_url)


@pytest.fixture
def driver(
    request: pytest.FixtureRequest,
    framework_config: FrameworkConfig,
) -> Generator[WebDriver, None, None]:
    web_driver = DriverFactory(framework_config).create()
    yield web_driver

    report = getattr(request.node, "report_call", None)
    if report and report.failed:
        _save_failure_evidence(web_driver, request.node.nodeid, framework_config.artifacts_dir)
    web_driver.quit()


def _save_failure_evidence(driver: WebDriver, node_id: str, artifacts_dir: Path) -> None:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", node_id).strip("_")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(artifacts_dir / f"{safe_name}.png"))
    (artifacts_dir / f"{safe_name}.html").write_text(driver.page_source, encoding="utf-8")
