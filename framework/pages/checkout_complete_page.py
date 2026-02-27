"""Checkout complete page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    BACK_HOME = (By.ID, "back-to-products")

    def title(self) -> str:
        return self.text(self.TITLE)

    def complete_header(self) -> str:
        return self.text(self.COMPLETE_HEADER)

    def complete_text(self) -> str:
        return self.text(self.COMPLETE_TEXT)

    def back_home(self) -> None:
        self.click(self.BACK_HOME)
