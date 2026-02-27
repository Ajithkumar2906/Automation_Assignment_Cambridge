"""Reusable explicit-wait helpers for flaky-sensitive UI actions."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WaitUtils:
    def __init__(self, driver: WebDriver, timeout: int) -> None:
        self.driver = driver
        self.timeout = timeout

    def visible(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator))

    def present_all(self, locator: tuple[str, str]) -> list[WebElement]:
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(locator))

    def invisible(self, locator: tuple[str, str]) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(EC.invisibility_of_element_located(locator))

    def url_contains(self, value: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(EC.url_contains(value))

    def try_visible(self, locator: tuple[str, str]) -> WebElement | None:
        try:
            return self.visible(locator)
        except TimeoutException:
            return None
