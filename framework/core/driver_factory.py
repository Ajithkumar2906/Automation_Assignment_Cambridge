"""WebDriver factory with local/remote support and resilient defaults."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from framework.core.logger import get_logger
from framework.core.settings import settings

logger = get_logger(__name__)


class DriverFactory:
    """Creates browser drivers for local and Selenium Grid execution."""

    @staticmethod
    def create_driver() -> WebDriver:
        browser = settings.browser
        logger.info("Creating driver. browser=%s remote=%s", browser, settings.remote)

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            if settings.headless:
                options.add_argument("--headless=new")

            if settings.remote:
                return webdriver.Remote(command_executor=settings.selenium_grid_url, options=options)

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

            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)

        raise ValueError(f"Unsupported browser '{browser}'. Use chrome or firefox.")
