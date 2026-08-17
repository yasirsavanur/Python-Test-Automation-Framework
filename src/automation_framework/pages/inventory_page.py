"""Inventory page behaviours."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions

from automation_framework.pages.base_page import BasePage


class InventoryPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "[data-testid='inventory-heading']")
    PRODUCT_CARD = (By.CSS_SELECTOR, "[data-testid='product-card']")
    CART_COUNT = (By.CSS_SELECTOR, "[data-testid='cart-count']")
    CART_LINK = (By.CSS_SELECTOR, "[data-testid='cart-link']")
    SEARCH = (By.CSS_SELECTOR, "[data-testid='product-search']")

    def wait_until_loaded(self) -> None:
        self.visible(self.HEADING)

    def add_product(self, name: str) -> None:
        def matching_button(_driver):
            for card in self.driver.find_elements(*self.PRODUCT_CARD):
                if card.get_attribute("data-product-name") == name:
                    return card.find_element(By.CSS_SELECTOR, "[data-testid='add-product']")
            return False

        self.wait.until(matching_button).click()

    @property
    def cart_count(self) -> int:
        return int(self.text(self.CART_COUNT))

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def search(self, term: str) -> None:
        self.fill(self.SEARCH, term)

    @property
    def visible_product_names(self) -> list[str]:
        locator = (By.CSS_SELECTOR, "[data-testid='product-card']:not([hidden])")
        self.wait.until(conditions.presence_of_element_located(locator))
        return [
            card.get_attribute("data-product-name") for card in self.driver.find_elements(*locator)
        ]
