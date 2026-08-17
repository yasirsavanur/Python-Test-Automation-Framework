"""Data-driven authentication coverage."""

from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from automation_framework.config import FrameworkConfig
from automation_framework.data import load_cases
from automation_framework.pages import LoginPage

CASES = load_cases(Path(__file__).parents[1] / "data" / "users.json", "invalid")


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_invalid_login_explains_the_failure(
    driver: WebDriver,
    base_url: str,
    framework_config: FrameworkConfig,
    case: dict[str, str],
) -> None:
    login = LoginPage(driver, base_url, framework_config.timeout)

    login.load()
    login.sign_in(case["email"], case["password"])

    assert login.error_message == case["message"]
