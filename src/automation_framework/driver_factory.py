"""Selenium 4 WebDriver creation for local browsers or a remote Grid."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from automation_framework.config import FrameworkConfig


class DriverFactory:
    """Create consistently configured, modern WebDriver sessions."""

    def __init__(self, config: FrameworkConfig) -> None:
        self.config = config

    def create(self) -> WebDriver:
        options = self._options()
        if self.config.grid_url:
            driver = webdriver.Remote(
                command_executor=self.config.grid_url,
                options=options,
            )
        elif self.config.browser == "chrome":
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Firefox(options=options)

        driver.set_window_size(1440, 1000)
        driver.set_page_load_timeout(30)
        return driver

    def _options(self) -> ChromeOptions | FirefoxOptions:
        if self.config.browser == "chrome":
            options = ChromeOptions()
            if self.config.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        else:
            options = FirefoxOptions()
            if self.config.headless:
                options.add_argument("-headless")

        options.set_capability("acceptInsecureCerts", True)
        return options
