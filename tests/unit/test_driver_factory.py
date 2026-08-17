"""Driver construction tests that do not start a real browser."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from selenium import webdriver

from automation_framework.config import FrameworkConfig
from automation_framework.driver_factory import DriverFactory


@dataclass
class FakeDriver:
    window_size: tuple[int, int] | None = None
    page_load_timeout: int | None = None

    def set_window_size(self, width: int, height: int) -> None:
        self.window_size = (width, height)

    def set_page_load_timeout(self, timeout: int) -> None:
        self.page_load_timeout = timeout


@pytest.mark.unit
@pytest.mark.parametrize(
    ("browser", "constructor_name", "headless_argument"),
    [
        ("chrome", "Chrome", "--headless=new"),
        ("firefox", "Firefox", "-headless"),
    ],
)
def test_local_driver_uses_browser_options(
    monkeypatch: pytest.MonkeyPatch,
    browser: str,
    constructor_name: str,
    headless_argument: str,
) -> None:
    captured = {}
    fake_driver = FakeDriver()

    def create_driver(*, options):
        captured["options"] = options
        return fake_driver

    monkeypatch.setattr(webdriver, constructor_name, create_driver)

    driver = DriverFactory(FrameworkConfig(browser=browser)).create()

    assert driver is fake_driver
    assert headless_argument in captured["options"].arguments
    assert fake_driver.window_size == (1440, 1000)
    assert fake_driver.page_load_timeout == 30


@pytest.mark.unit
def test_remote_driver_receives_grid_url_and_options(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = {}
    fake_driver = FakeDriver()

    def create_remote_driver(*, command_executor, options):
        captured.update(command_executor=command_executor, options=options)
        return fake_driver

    monkeypatch.setattr(webdriver, "Remote", create_remote_driver)
    config = FrameworkConfig(browser="chrome", grid_url="http://grid.example/wd/hub")

    driver = DriverFactory(config).create()

    assert driver is fake_driver
    assert captured["command_executor"] == config.grid_url
    assert captured["options"].capabilities["acceptInsecureCerts"] is True
