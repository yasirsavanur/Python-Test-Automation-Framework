"""Fast validation of framework runtime settings."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from automation_framework.config import FrameworkConfig


@pytest.mark.unit
def test_config_normalises_browser_and_artifact_path() -> None:
    config = FrameworkConfig(browser="FIREFOX", artifacts_dir="test-output", timeout=2.5)

    assert config.browser == "firefox"
    assert config.artifacts_dir == Path("test-output")
    assert config.timeout == 2.5


@pytest.mark.unit
def test_config_reads_registered_pytest_options() -> None:
    values = {
        "--browser": "firefox",
        "--headed": True,
        "--grid-url": "http://grid.example/wd/hub",
        "--timeout": 7.5,
        "--artifacts-dir": "evidence",
    }
    pytest_config = SimpleNamespace(getoption=values.__getitem__)

    config = FrameworkConfig.from_pytest(pytest_config)

    assert config == FrameworkConfig(
        browser="firefox",
        headless=False,
        grid_url="http://grid.example/wd/hub",
        timeout=7.5,
        artifacts_dir=Path("evidence"),
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"browser": "safari"}, "Unsupported browser"),
        ({"timeout": 0}, "greater than zero"),
    ],
)
def test_config_rejects_invalid_values(overrides: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        FrameworkConfig(**overrides)
