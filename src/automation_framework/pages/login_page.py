"""Login page actions and assertions."""

from selenium.webdriver.common.by import By

from automation_framework.pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "index.html"
    HEADING = (By.CSS_SELECTOR, "[data-testid='login-heading']")
    EMAIL = (By.CSS_SELECTOR, "[data-testid='email']")
    PASSWORD = (By.CSS_SELECTOR, "[data-testid='password']")
    SUBMIT = (By.CSS_SELECTOR, "[data-testid='login-submit']")
    ERROR = (By.CSS_SELECTOR, "[data-testid='login-error']")

    def load(self) -> None:
        self.open(self.PATH)
        self.visible(self.HEADING)

    def sign_in(self, email: str, password: str) -> None:
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)

    @property
    def error_message(self) -> str:
        return self.text(self.ERROR)
