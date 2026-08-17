"""Checkout page behaviours."""

from selenium.webdriver.common.by import By

from automation_framework.pages.base_page import BasePage


class CheckoutPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "[data-testid='checkout-heading']")
    FIRST_NAME = (By.CSS_SELECTOR, "[data-testid='first-name']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-testid='last-name']")
    POSTCODE = (By.CSS_SELECTOR, "[data-testid='postcode']")
    COMPLETE = (By.CSS_SELECTOR, "[data-testid='complete-order']")
    SUCCESS = (By.CSS_SELECTOR, "[data-testid='success-heading']")
    ORDER_NUMBER = (By.CSS_SELECTOR, "[data-testid='order-number']")

    def wait_until_loaded(self) -> None:
        self.visible(self.HEADING)

    def complete_order(self, first_name: str, last_name: str, postcode: str) -> None:
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTCODE, postcode)
        self.click(self.COMPLETE)

    @property
    def success_heading(self) -> str:
        return self.text(self.SUCCESS)

    @property
    def order_number(self) -> str:
        return self.text(self.ORDER_NUMBER)
