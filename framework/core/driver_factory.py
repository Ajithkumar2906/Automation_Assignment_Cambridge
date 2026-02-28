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
    def create_driver(browser_name: str | None = None) -> WebDriver:
        browser = (browser_name or settings.browser).lower().strip()
        logger.info("Creating driver. browser=%s remote=%s", browser, settings.remote)

        try:
            if browser == "chrome":
                options = ChromeOptions()
                options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                if settings.headless:
                    options.add_argument("--headless=new")

                if settings.remote:
                    return webdriver.Remote(command_executor=settings.selenium_grid_url, options=options)

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

                if settings.remote:
                    return webdriver.Remote(command_executor=settings.selenium_grid_url, options=options)

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

                if settings.remote:
                    return webdriver.Remote(command_executor=settings.selenium_grid_url, options=options)

                try:
                    return webdriver.Edge(options=options)
                except Exception:
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    return webdriver.Edge(service=service, options=options)

            if browser == "safari":
                if settings.headless:
                    logger.warning("Headless mode is not supported for Safari; running headed.")
                options = SafariOptions()
                if settings.remote:
                    return webdriver.Remote(command_executor=settings.selenium_grid_url, options=options)
                return webdriver.Safari(options=options)
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize browser '{browser}': {exc}") from exc

        raise ValueError("Unsupported browser. Use one of: chrome, firefox, edge, safari.")
