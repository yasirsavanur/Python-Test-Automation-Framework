"""Shared explicit-wait actions used by all page objects."""

from __future__ import annotations

from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    """Expose intent-focused interactions without hiding Selenium failures."""

    def __init__(self, driver: WebDriver, base_url: str, timeout: float = 10.0) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path: str) -> None:
        self.driver.get(urljoin(self.base_url, path.lstrip("/")))

    def visible(self, locator: Locator) -> WebElement:
        return self.wait.until(conditions.visibility_of_element_located(locator))

    def all_present(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(conditions.presence_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(conditions.element_to_be_clickable(locator)).click()

    def fill(self, locator: Locator, value: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()
