# Assumptions and Limitations

## Assumptions
- AUT is `https://www.saucedemo.com/` and test users remain available (for example `standard_user`, `locked_out_user`, and other SauceDemo sample accounts).
- Inventory and checkout business behavior follow current SauceDemo behavior; known demo-user quirks are treated as expected where covered.
- Test execution environment has supported browser(s) installed and compatible drivers available (or webdriver-manager fallback can download them).
- `.env` is configured correctly for local, Grid, or BrowserStack execution.
- Network access is available during runs (especially for remote/cloud sessions and webdriver downloads).
- Product list/order may vary; tests avoid hardcoded product dependency where possible.

## Current Limitations
- This is a UI-first functional automation framework; it is not a load/performance benchmark framework.
- API coverage is intentionally lightweight and limited to currently running/passing API checks, not full backend contract validation.
- Visual validation is functional (UI presence/alignment checks in flows) and does not include dedicated visual-diff tooling.
- Accessibility checks (WCAG, keyboard-only navigation audits, screen-reader validation) are not fully automated yet.
- Browser matrix depth in local execution is sequential by command unless xdist or CI matrix is explicitly used.
- Safari execution is macOS-only and does not support headless mode.

## Data and State Constraints
- SauceDemo is a shared demo environment; occasional instability or timing variance can occur.
- `Reset App State` and session-specific state are managed through test flow, but external transient site issues can still impact reliability.
- Financial checks rely on displayed UI values (item prices, tax, total) and current currency format.

## Non-Goals in Current Scope
- Full mutation/fuzz testing of inputs.
- Security penetration testing.
- Contract-first service virtualization/mocking.
- Cross-device mobile-native automation.

## Risk Mitigations Implemented
- Explicit waits and robust interaction patterns reduce flaky timing failures.
- Failure screenshots and detailed reports improve triage speed.
- Marker-based execution (`smoke`, `regression`, `ui`, `api`, `e2e`) supports risk-based test selection.
- Adaptive E2E selection logic (up to two products) keeps core flow resilient if inventory size changes.
