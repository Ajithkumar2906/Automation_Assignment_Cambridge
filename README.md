# UI Test Automation Framework

A robust, scalable UI automation framework for [SauceDemo](https://www.saucedemo.com/) using:

- `Python`
- `pytest`
- `pytest-bdd` (Cucumber-style BDD)
- `Selenium WebDriver`
- `POM` (Page Object Model)
- `pytest-html` and `Allure` reporting
- lightweight API availability check for login page
- Local and Selenium Grid execution (Docker)
- BrowserStack cloud execution for cross-browser CI/CD

## Project Structure

```text
project-root/
├── framework/
│   ├── api/                # API validations used alongside UI tests
│   ├── core/               # Config, driver factory, logging
│   ├── data/               # Test data files
│   ├── pages/              # Page Object classes
│   └── utils/              # Wait and helper utilities
├── tests/
│   ├── features/           # Gherkin feature files
│   ├── scenarios/          # pytest-bdd scenario bindings
│   └── steps/              # Step definitions
├── conftest.py             # Shared fixtures and hooks
├── docker-compose.yml      # Selenium Grid
├── pytest.ini
└── requirements.txt
```

## Setup

1. Create and activate venv.
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Create env file:

```bash
cp .env.example .env
```

## Run Tests

```bash
pytest -m smoke --browser chrome
pytest -m regression --browser firefox
pytest -m ui --browser edge
pytest -m e2e --browser chrome
pytest -m api
```

Run full suite in a single browser:

```bash
pytest --browser chrome
```

Run full suite across local browsers (run separately for each browser):

```bash
pytest --browser chrome
pytest --browser firefox
pytest --browser edge
```

Parallel execution (xdist):

```bash
pytest -m ui -n auto --dist loadscope --browser chrome
```

Safari notes (macOS only):
- Enable `Allow Remote Automation` in Safari Develop menu.
- Headless is not supported for Safari.

## Run With Selenium Grid

1. Start grid:

```bash
docker compose up -d
```

2. Set in `.env`:

```env
REMOTE=true
SELENIUM_GRID_URL=http://localhost:4444/wd/hub
```

3. Execute tests:

```bash
pytest -m ui
```

## Run With BrowserStack

1. Set in `.env`:

```env
BROWSERSTACK_ENABLED=true
REMOTE=true
BROWSERSTACK_USERNAME=<your-browserstack-username>
BROWSERSTACK_ACCESS_KEY=<your-browserstack-access-key>
BROWSERSTACK_PROJECT_NAME=UI_Automation_Framework
BROWSERSTACK_BUILD_NAME=Local Build
BROWSERSTACK_BROWSER_VERSION=latest
BROWSERSTACK_OS=
BROWSERSTACK_OS_VERSION=
BROWSERSTACK_DEBUG=true
BROWSERSTACK_NETWORK_LOGS=false
```

2. Execute smoke suite on BrowserStack:

```bash
pytest -m "smoke and ui" --browser chrome
pytest -m "smoke and ui" --browser firefox
pytest -m "smoke and ui" --browser edge
```

3. For GitHub Actions, add repository secrets:
- `BROWSERSTACK_USERNAME`
- `BROWSERSTACK_ACCESS_KEY`

Then the `browserstack-smoke` job runs automatically on push/PR.

## Reports

- HTML: `reports/html/report.html`
- Allure raw: `reports/allure-results/`

Generate allure report:

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## GitLab Workflow Suggestions

- Commit frequently with meaningful messages.
- Protect `main` branch.
- Add project collaborators as `Developer` access.
- Run `@smoke` on each push/merge request.
- Run full `@regression` suite on a schedule (for example nightly).
- Keep BrowserStack CI matrix focused to representative coverage (for example Chrome/Firefox/Edge latest).

## Coverage Included

- API: login page reachability/status + content smoke check.
- Login positive and negative paths.
- Product listing validations and sort checks.
- Add/Remove cart flows.
- Cart page and checkout info validations.
- Checkout overview and finish flow.
- Loaded product flow: inventory -> details -> cart -> checkout overview.
- Product details data consistency against inventory: image, name, description, and price.
- Financial assertions in checkout overview:
  - `Item total = sum(price * quantity)`
  - `Total = Item total + Tax`
- E2E scalability behavior:
  - Selects up to two products.
  - If only one product is available, flow continues with one product.

## Requirement Traceability Matrix

|  Requirement  | Feature File | Representative Scenarios Covered |
| --- | --- | --- |
| Login page validation (positive/negative/error handling) | `tests/features/login.feature` | valid login, invalid credentials, empty fields, locked-out user, error message close, header checks |
| Product/inventory checks after login | `tests/features/products.feature` | inventory components visibility, product card data checks, add/remove cart, sort options and order checks |
| Product details and navigation behavior | `tests/features/products.feature` | open details page, data consistency (image/name/description/price), add/remove from details, back to products |
| Cart page validations | `tests/features/cart_checkout.feature` | cart header/columns, quantity-description checks, remove, continue shopping, checkout navigation |
| Checkout information page validations | `tests/features/cart_checkout.feature` | valid entry flow, mandatory field validation errors, cancel/continue behavior |
| Checkout overview and completion | `tests/features/cart_checkout.feature`, `tests/features/e2e.feature` | payment/shipping checks, item total and grand total assertions, finish flow, thank-you and back-home checks |
| End-to-end user journey | `tests/features/e2e.feature` | login -> add products -> cart -> checkout -> finish, adaptive product selection for resilience |
| API smoke validation (running checks only) | `tests/features/api.feature` | login page availability/status and content smoke validation |
| Cross-browser/parallel execution capability | `conftest.py`, `framework/core/driver_factory.py` | local Chrome/Firefox/Edge/Safari runs, Selenium Grid remote runs, BrowserStack smoke matrix, xdist parallel support |
| Reporting, evidence, and diagnostics | `conftest.py`, `pytest.ini` | screenshot-on-failure, pytest-html reports, Allure raw results, step-level execution logs |

## Test Design Notes

- Selector strategy:
  - Prefer `id` and `data-test` attributes.
  - Use scoped CSS selectors when stable test attributes are unavailable.
  - Use XPath only for text-based fallback paths.
- For known SauceDemo input instability in checkout/login edge cases, JS-assisted value setting is used in selected steps to reduce flakiness.
