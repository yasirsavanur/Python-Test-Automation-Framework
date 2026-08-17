"""Runtime configuration shared by pytest fixtures and driver creation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

SUPPORTED_BROWSERS = ("chrome", "firefox")


@dataclass(frozen=True, slots=True)
class FrameworkConfig:
    """Validated settings for a single automation session."""

    browser: str = "chrome"
    headless: bool = True
    grid_url: str | None = None
    timeout: float = 10.0
    artifacts_dir: Path = Path("artifacts")

    def __post_init__(self) -> None:
        browser = self.browser.lower()
        if browser not in SUPPORTED_BROWSERS:
            choices = ", ".join(SUPPORTED_BROWSERS)
            raise ValueError(f"Unsupported browser '{self.browser}'. Choose one of: {choices}")
        if self.timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        object.__setattr__(self, "browser", browser)
        object.__setattr__(self, "artifacts_dir", Path(self.artifacts_dir))

    @classmethod
    def from_pytest(cls, pytest_config: Any) -> FrameworkConfig:
        """Build settings from the CLI options registered in ``tests/conftest.py``."""

        return cls(
            browser=pytest_config.getoption("--browser"),
            headless=not pytest_config.getoption("--headed"),
            grid_url=pytest_config.getoption("--grid-url") or None,
            timeout=pytest_config.getoption("--timeout"),
            artifacts_dir=Path(pytest_config.getoption("--artifacts-dir")),
        )
