"""WebDriver factory with local/remote support and resilient defaults."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

from framework.core.logger import get_logger
from framework.core.settings import settings

logger = get_logger(__name__)


class DriverFactory:
    """Creates browser drivers for local and Selenium Grid execution."""

    @staticmethod
    def _remote_executor_url() -> str:
        if settings.browserstack_enabled:
            if not settings.browserstack_username or not settings.browserstack_access_key:
                raise RuntimeError(
                    "BrowserStack is enabled but credentials are missing. "
                    "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY."
                )
            return (
                f"https://{settings.browserstack_username}:{settings.browserstack_access_key}"
                "@hub-cloud.browserstack.com/wd/hub"
            )
        return settings.selenium_grid_url

    @staticmethod
    def _apply_remote_capabilities(options, browser: str) -> None:
        if not settings.browserstack_enabled:
            return
        bstack_options = {
            "projectName": settings.browserstack_project_name,
            "buildName": settings.browserstack_build_name,
            "sessionName": f"smoke-{browser}",
            "debug": settings.browserstack_debug,
            "networkLogs": settings.browserstack_network_logs,
        }
        if settings.browserstack_os:
            bstack_options["os"] = settings.browserstack_os
        if settings.browserstack_os_version:
            bstack_options["osVersion"] = settings.browserstack_os_version

        options.set_capability("bstack:options", bstack_options)
        options.set_capability("browserVersion", settings.browserstack_browser_version)

    @staticmethod
    def create_driver(browser_name: str | None = None) -> WebDriver:
        browser = (browser_name or settings.browser).lower().strip()
        use_remote = settings.remote or settings.browserstack_enabled
        logger.info(
            "Creating driver. browser=%s remote=%s browserstack=%s",
            browser,
            use_remote,
            settings.browserstack_enabled,
        )
        remote_executor = DriverFactory._remote_executor_url()

        try:
            if browser == "chrome":
                options = ChromeOptions()
                options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                if settings.headless:
                    options.add_argument("--headless=new")
                DriverFactory._apply_remote_capabilities(options, browser)

                if use_remote:
                    return webdriver.Remote(command_executor=remote_executor, options=options)

                try:
                    return webdriver.Chrome(options=options)
                except Exception:
                    service = ChromeService(ChromeDriverManager().install())
                    return webdriver.Chrome(service=service, options=options)

            if browser == "firefox":
                options = FirefoxOptions()
                options.add_argument(f"--width={settings.window_width}")
                options.add_argument(f"--height={settings.window_height}")
                if settings.headless:
                    options.add_argument("-headless")
                DriverFactory._apply_remote_capabilities(options, browser)

                if use_remote:
                    return webdriver.Remote(command_executor=remote_executor, options=options)

                try:
                    return webdriver.Firefox(options=options)
                except Exception:
                    service = FirefoxService(GeckoDriverManager().install())
                    return webdriver.Firefox(service=service, options=options)

            if browser in {"edge", "msedge"}:
                options = EdgeOptions()
                options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
                if settings.headless:
                    options.add_argument("--headless=new")
                DriverFactory._apply_remote_capabilities(options, browser)

                if use_remote:
                    return webdriver.Remote(command_executor=remote_executor, options=options)

                try:
                    return webdriver.Edge(options=options)
                except Exception:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    return webdriver.Edge(service=service, options=options)

            if browser == "safari":
                if settings.headless:
                    logger.warning("Headless mode is not supported for Safari; running headed.")
                options = SafariOptions()
                DriverFactory._apply_remote_capabilities(options, browser)
                if use_remote:
                    return webdriver.Remote(command_executor=remote_executor, options=options)
                return webdriver.Safari(options=options)
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize browser '{browser}': {exc}") from exc

        raise ValueError("Unsupported browser. Use one of: chrome, firefox, edge, safari.")
