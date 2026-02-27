"""Global pytest fixtures and hooks for browser lifecycle and shared test context."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest
from _pytest.nodes import Item
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.driver_factory import DriverFactory
from framework.core.settings import settings
from framework.pages.cart_page import CartPage
from framework.pages.checkout_complete_page import CheckoutCompletePage
from framework.pages.checkout_info_page import CheckoutInfoPage
from framework.pages.checkout_overview_page import CheckoutOverviewPage
from framework.pages.inventory_page import InventoryPage
from framework.pages.login_page import LoginPage
from framework.pages.product_details_page import ProductDetailsPage

pytest_plugins = ["tests.steps.ui_steps", "tests.steps.api_steps"]


@pytest.fixture(scope="session")
def users_data() -> dict[str, str]:
    return json.loads(Path("framework/data/users.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def checkout_data() -> dict:
    return json.loads(Path("framework/data/checkout_data.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="function")
def driver() -> WebDriver:
    browser = DriverFactory.create_driver()
    browser.implicitly_wait(settings.implicit_wait)
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def context() -> dict:
    """Shared mutable scenario context for step-level data passing."""
    return {}


@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture(scope="function")
def inventory_page(driver: WebDriver) -> InventoryPage:
    return InventoryPage(driver)


@pytest.fixture(scope="function")
def product_details_page(driver: WebDriver) -> ProductDetailsPage:
    return ProductDetailsPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: WebDriver) -> CartPage:
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_info_page(driver: WebDriver) -> CheckoutInfoPage:
    return CheckoutInfoPage(driver)


@pytest.fixture(scope="function")
def checkout_overview_page(driver: WebDriver) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(driver)


@pytest.fixture(scope="function")
def checkout_complete_page(driver: WebDriver) -> CheckoutCompletePage:
    return CheckoutCompletePage(driver)


def pytest_bdd_apply_tag(tag: str, function):
    """Map Gherkin tags to pytest markers automatically."""
    marker = getattr(pytest.mark, tag, None)
    if marker:
        marker(function)
    return True


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    print(f"[STEP-START] {step.keyword} {step.name}", flush=True)


def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print(f"[STEP-END] {step.keyword} {step.name}", flush=True)
    if settings.step_delay_seconds > 0:
        time.sleep(settings.step_delay_seconds)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def _capture_screenshot_on_failure(request):
    """Capture screenshots for failed UI tests to help interview debugging discussion."""
    yield
    if request.node.rep_call.failed and "ui" in request.node.keywords:
        driver: WebDriver | None = request.node.funcargs.get("driver")
        if driver is None:
            return
        reports_dir = Path("reports") / "screenshots"
        reports_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = reports_dir / f"{request.node.name}.png"
        driver.save_screenshot(str(screenshot_path))
