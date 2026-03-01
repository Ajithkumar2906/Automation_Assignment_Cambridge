# Framework Architecture

## Purpose
This framework automates SauceDemo UI flows with maintainable, reusable, and scalable design using Python, pytest, pytest-bdd, Selenium WebDriver, and POM.

## High-Level Design
- BDD layer: feature files define business-readable test behavior.
- Binding layer: scenario files bind feature scenarios to pytest-bdd execution.
- Step layer: step definitions orchestrate actions/assertions and pass shared state via `context`.
- Page layer (POM): page classes encapsulate selectors and UI interactions.
- Core layer: configuration, logging, and driver creation for local/remote/cloud runs.
- Data layer: user and checkout data from JSON files.

## Folder Responsibilities
- `tests/features/`: Gherkin scenarios (`login`, `products`, `cart_checkout`, `e2e`, `api`).
- `tests/scenarios/`: `@scenario` mappings for pytest collection.
- `tests/steps/`: reusable step implementations (`ui_steps.py`, `api_steps.py`).
- `framework/pages/`: page objects for login, inventory, details, cart, checkout info/overview/complete.
- `framework/core/`: runtime settings, driver factory, logger.
- `framework/api/`: lightweight API helper(s) used by running API checks.
- `framework/data/`: test datasets (`users.json`, `checkout_data.json`).
- `conftest.py`: fixtures, browser parametrization, BDD tag mapping, screenshot hook.

## Execution Flow
1. pytest collects scenarios from `tests/scenarios/`.
2. Browser matrix is created through `--browser` (single/multiple values).
3. `DriverFactory` creates local WebDriver or remote session (Selenium Grid / BrowserStack).
4. Step definitions call page objects for actions and validations.
5. On UI failure, screenshot is saved under `reports/screenshots/`.
6. Reports are generated via pytest-html and Allure outputs.

## Browser and Environment Model
- Local browsers: Chrome, Firefox, Edge, Safari.
- Remote modes:
  - Selenium Grid via `REMOTE=true` and `SELENIUM_GRID_URL`.
  - BrowserStack via `BROWSERSTACK_ENABLED=true` + credentials.
- Config is centralized in `framework/core/settings.py` using `.env`.

## Reliability Design
- Explicit wait utilities and robust element interaction wrappers.
- Controlled pacing through `ACTION_DELAY_SECONDS` and `STEP_DELAY_SECONDS`.
- Selector strategy prioritizes stable attributes (`id`, `data-test`) before fallback selectors.
- Adaptive E2E product selection (`up to two`) avoids brittle hardcoded assumptions.

## Parallelization and CI
- Local parallel support via `pytest-xdist` (`-n auto --dist loadscope`).
- CI parallelism through browser matrix jobs (GitHub Actions / BrowserStack smoke lanes).
- Selenium Grid and Docker allow isolated, reproducible remote browser nodes.

## Reporting and Diagnostics
- HTML report: `reports/html/report.html`
- Allure raw: `reports/allure-results/`
- Failure screenshots: `reports/screenshots/`
- Console step tracing via `pytest_bdd_before_step` and `pytest_bdd_after_step` hooks.
