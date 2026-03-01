"""Login page object for authentication and login error handling."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.core.settings import settings
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE = (By.CSS_SELECTOR, "button.error-button")

    def load(self) -> None:
        self.open(settings.base_url)

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def login_blank(self) -> None:
        self.click(self.LOGIN_BTN)

    def get_error(self) -> str:
        return self.text(self.ERROR_MSG)

    def close_error(self) -> None:
        self.click(self.ERROR_CLOSE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MSG)
