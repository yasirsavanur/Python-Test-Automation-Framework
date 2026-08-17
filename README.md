# Orbit QA — Python Test Automation Framework

[![Quality gates](https://github.com/yasirsavanur/Python-Test-Automation-Framework/actions/workflows/quality-gates.yml/badge.svg)](https://github.com/yasirsavanur/Python-Test-Automation-Framework/actions/workflows/quality-gates.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium 4](https://img.shields.io/badge/Selenium-4-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)

A production-minded UI and API automation framework built with Python, pytest, and Selenium 4. It demonstrates maintainable page objects, data-driven testing, cross-browser execution, Grid support, failure diagnostics, contract testing, and CI quality gates—without depending on an unstable public demo site.

The repository includes **Orbit QA Store**, a small deterministic commerce system used as the test target. Clone the project and the whole suite is ready to run locally.

## What this project demonstrates

- Selenium 4 sessions for Chrome, Firefox, or a remote Grid
- explicit waits and stable `data-testid` selectors—no fixed sleeps or implicit waits
- focused page objects that model user intent instead of test mechanics
- pytest fixtures, custom CLI options, markers, and readable parametrized cases
- UI journeys and API contract tests against the same system under test
- automatic screenshot and page-source capture when a browser test fails
- self-contained HTML, JUnit XML, and coverage reports
- GitHub Actions matrices across Python 3.10/3.12 and Chrome/Firefox
- Ruff linting and an enforced 80% branch-coverage threshold

## Framework shape

```text
src/automation_framework/
├── api_client.py          # JSON API test client
├── config.py              # validated runtime settings
├── driver_factory.py      # local and remote WebDriver sessions
└── pages/                 # intent-focused page objects
demo_app/                  # deterministic UI + API test target
tests/
├── api/                   # service contract checks
├── data/                  # versioned, non-secret test data
├── support/               # ephemeral demo server
├── ui/                    # browser journeys
└── unit/                  # fast framework checks
```

The fixture layer owns infrastructure and lifecycle; tests own assertions; page objects own browser interactions. That separation keeps failures clear and makes a new environment or page straightforward to add.

## Quick start

Prerequisites: Python 3.10+ and Chrome or Firefox.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"

pytest -m smoke --browser chrome
```

Selenium Manager resolves the matching local driver, so no machine-specific driver path is required. Tests start the bundled application on an available local port and shut it down after the session.

## Useful test runs

```bash
# Fast feedback, no browser
pytest -m "unit or api"

# Full Chrome suite with a self-contained report
pytest --browser chrome --html=artifacts/report.html --self-contained-html

# Firefox regression suite with JUnit output
pytest -m regression --browser firefox --junitxml=artifacts/regression.xml

# Watch the test execute
pytest -m smoke --browser chrome --headed

# Run against a compatible remote environment
pytest -m ui --browser chrome \
  --grid-url http://localhost:4444/wd/hub \
  --base-url https://your-accessible-test-environment.example
```

### Runtime options

| Option | Default | Purpose |
|---|---:|---|
| `--browser` | `chrome` | Select `chrome` or `firefox` |
| `--headed` | off | Display a local browser instead of using headless mode |
| `--grid-url` | local | Send the session to Selenium Grid or a cloud provider |
| `--base-url` | bundled app | Target another compatible environment |
| `--timeout` | `10` | Set the explicit-wait timeout in seconds |
| `--artifacts-dir` | `artifacts` | Choose where failure evidence is written |

## Example test

```python
@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_complete_checkout(driver, base_url, framework_config):
    login = LoginPage(driver, base_url, framework_config.timeout)
    inventory = InventoryPage(driver, base_url, framework_config.timeout)

    login.load()
    login.sign_in("qa.engineer@example.com", "quality-first")
    inventory.wait_until_loaded()
    inventory.add_product("Grid Compass")

    assert inventory.cart_count == 1
```

The complete journey lives in [`tests/ui/test_checkout.py`](tests/ui/test_checkout.py).

## Failure diagnostics

If a browser test reaches its assertion and fails, the `driver` fixture writes two files to `artifacts/`:

- a PNG screenshot showing the rendered state
- the matching HTML source for DOM-level investigation

CI uploads these alongside the HTML and JUnit reports even when the test job fails.

## Continuous integration

The workflow separates fast framework feedback from browser compatibility:

| Job | Coverage |
|---|---|
| Framework | Ruff plus unit/API tests on Python 3.10 and 3.12 |
| Selenium / Chrome | complete suite, HTML/JUnit reports, branch coverage |
| Selenium / Firefox | complete suite, HTML/JUnit reports, branch coverage |

This keeps the signal specific: a Python compatibility problem, a browser-specific problem, and a product regression appear as different checks.

## Extending it

1. Add a page object under `src/automation_framework/pages/` with selectors and user-level actions.
2. Put reusable, non-secret cases under `tests/data/` and load them with `load_cases`.
3. Mark tests by intent (`smoke`, `regression`, `ui`, `api`, or `unit`).
4. Keep credentials outside the repository and inject them through your CI secret store.
5. Add provider-specific capabilities to `DriverFactory._options()` when connecting a cloud Grid.

## Design choices

- **A bundled test target:** public demo sites change or disappear; this repository remains repeatable and portfolio-friendly.
- **Explicit waits:** each synchronization point describes the condition the test actually needs.
- **Native Selenium Manager:** local setup stays portable and avoids checked-in browser binaries.
- **Small abstractions:** page objects remove repetition while Selenium exceptions retain useful stack traces.
- **No live TestRail coupling:** results are emitted in portable JUnit XML so CI or a test-management adapter can consume them without putting account configuration in the framework.

## License

MIT
