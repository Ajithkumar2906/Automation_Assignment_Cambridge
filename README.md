# Automation_Assignment_Cambridge

A robust, scalable UI automation framework for [SauceDemo](https://www.saucedemo.com/) using:

- `Python`
- `pytest`
- `pytest-bdd` (Cucumber-style BDD)
- `Selenium WebDriver`
- `POM` (Page Object Model)
- `pytest-html` and `Allure` reporting
- Local and Selenium Grid execution (Docker)

## Project Structure

```text
Automation_Assignment_Cambridge/
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
pytest -m smoke
pytest -m regression
pytest -n 2
```

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
- Add interviewers as `Developer` access.
- Configure CI job to run smoke suite on each push.

## Coverage Included

- Login positive and negative paths.
- Product listing validations and sort checks.
- Add/Remove cart flows.
- Cart page and checkout info validations.
- Checkout overview and finish flow.
- User-specific behavior checks (`standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user`).
- Lightweight API health validation.

