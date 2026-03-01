# Test Strategy

## Objective
- Validate critical user journeys on SauceDemo with reliable, maintainable automation.
- Provide fast feedback for build confidence (smoke) and deeper regression coverage.
- Keep tests readable for technical discussion and future extension.

## Scope
- Login page behavior:
  - successful login
  - empty credentials and validation messages
  - invalid credentials
  - locked-out user handling
- Post-login inventory behavior:
  - key UI components visibility
  - sort behavior (all 4 options)
  - add/remove product flows
  - product details navigation and data consistency checks
  - side menu operations (close/logout/reset app state)
- Cart and checkout:
  - cart headers and item count validation
  - checkout information validation and error flows
  - checkout overview content validation (payment/shipping/totals)
  - financial validations:
    - `item total = sum(price * quantity)`
    - `total = item total + tax`
- End-to-end flow:
  - inventory -> cart -> checkout -> complete order -> back home
  - adaptive selection (up to two products) to keep E2E robust with varying product availability
- API check:
  - lightweight login page availability/content check

## Test Levels
- UI functional tests:
  - primary coverage using Selenium + pytest-bdd
- API smoke check:
  - non-business API validation focused on page availability

## Test Design Approach
- BDD-first scenarios to keep business intent explicit.
- Page Object Model (POM) to centralize selectors and page behaviors.
- Explicit waits, retries, and robust click/type wrappers to reduce flakiness.
- Data-driven product selection from visible UI (avoid hardcoded product assumptions).
- Scenario tagging:
  - `@smoke`, `@regression`, `@e2e`, `@ui`, `@api`

## Execution Strategy
- Local:
  - targeted runs by marker and browser
  - full-suite browser-specific runs for release confidence
- CI:
  - API smoke + UI smoke in GitHub Actions
  - BrowserStack smoke matrix for cross-browser coverage
- Parallelization:
  - local xdist support (`-n auto`) for UI throughput
  - CI browser matrix for parallel cross-browser smoke

## Entry/Exit Criteria
- Entry:
  - AUT reachable
  - environment variables configured
  - browser drivers/grid available
- Exit:
  - all planned smoke tests pass
  - no unresolved blocker defects in critical paths
  - reports and screenshots available for review

## Defect Triage Inputs
- pytest HTML report
- step-level logs
- screenshot-on-failure artifacts
- scenario name and browser context

