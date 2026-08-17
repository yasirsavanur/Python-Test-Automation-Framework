"""Focused catalogue behaviour coverage."""

from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from automation_framework.config import FrameworkConfig
from automation_framework.data import load_json
from automation_framework.pages import InventoryPage, LoginPage

USERS = load_json(Path(__file__).parents[1] / "data" / "users.json")


@pytest.mark.ui
@pytest.mark.regression
def test_product_search_filters_the_catalogue(
    driver: WebDriver,
    base_url: str,
    framework_config: FrameworkConfig,
) -> None:
    login = LoginPage(driver, base_url, framework_config.timeout)
    inventory = InventoryPage(driver, base_url, framework_config.timeout)

    login.load()
    login.sign_in(**USERS["valid"])
    inventory.wait_until_loaded()
    inventory.search("selector")

    assert inventory.visible_product_names == ["Selector Studio"]
