"""Base page object with robust interaction helpers."""

from __future__ import annotations

import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.logger import get_logger
from framework.core.settings import settings
from framework.utils.waits import WaitUtils


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitUtils(driver, settings.explicit_wait)
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url: str) -> None:
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)
        self._action_delay()

    def click(self, locator: tuple[str, str]) -> None:
        self.logger.info("Clicking element: %s", locator)
        element = self.wait.clickable(locator)
        # SauceDemo can intermittently ignore native Selenium click events.
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)
        self._action_delay()

    def type(self, locator: tuple[str, str], value: str) -> None:
        self.logger.info("Typing into element: %s", locator)
        element = self.wait.visible(locator)
        element.clear()
        element.send_keys(value)
        self._action_delay()

    def text(self, locator: tuple[str, str]) -> str:
        return self.wait.visible(locator).text.strip()

    def is_visible(self, locator: tuple[str, str]) -> bool:
        return self.wait.try_visible(locator) is not None

    def current_url(self) -> str:
        return self.driver.current_url

    def safe_click(self, locator: tuple[str, str]) -> bool:
        try:
            self.click(locator)
            return True
        except WebDriverException as exc:
            self.logger.warning("Click failed for %s: %s", locator, exc)
            return False

    @staticmethod
    def _action_delay() -> None:
        if settings.action_delay_seconds > 0:
            time.sleep(settings.action_delay_seconds)
