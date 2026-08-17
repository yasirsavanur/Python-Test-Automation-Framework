"""Shopping cart page behaviours."""

from selenium.webdriver.common.by import By

from automation_framework.pages.base_page import BasePage


class CartPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "[data-testid='cart-heading']")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-testid='cart-item-name']")
    CHECKOUT = (By.CSS_SELECTOR, "[data-testid='checkout-link']")

    def wait_until_loaded(self) -> None:
        self.visible(self.HEADING)

    @property
    def item_names(self) -> list[str]:
        return [element.text.strip() for element in self.all_present(self.ITEM_NAME)]

    def begin_checkout(self) -> None:
        self.click(self.CHECKOUT)
