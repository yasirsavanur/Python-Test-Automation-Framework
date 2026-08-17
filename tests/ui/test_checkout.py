"""Critical end-to-end purchase journey."""

from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from automation_framework.config import FrameworkConfig
from automation_framework.data import load_json
from automation_framework.pages import CartPage, CheckoutPage, InventoryPage, LoginPage

USERS = load_json(Path(__file__).parents[1] / "data" / "users.json")


@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_complete_checkout(
    driver: WebDriver,
    base_url: str,
    framework_config: FrameworkConfig,
) -> None:
    login = LoginPage(driver, base_url, framework_config.timeout)
    inventory = InventoryPage(driver, base_url, framework_config.timeout)
    cart = CartPage(driver, base_url, framework_config.timeout)
    checkout = CheckoutPage(driver, base_url, framework_config.timeout)

    login.load()
    login.sign_in(**USERS["valid"])
    inventory.wait_until_loaded()
    inventory.add_product("Grid Compass")
    inventory.add_product("Trace Vault")

    assert inventory.cart_count == 2

    inventory.open_cart()
    cart.wait_until_loaded()
    assert cart.item_names == ["Grid Compass", "Trace Vault"]

    cart.begin_checkout()
    checkout.wait_until_loaded()
    checkout.complete_order("Ada", "Lovelace", "QA1 2ST")

    assert checkout.success_heading == "Order confirmed"
    assert checkout.order_number == "QA-2026-001"
