"""Checkout complete page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    BACK_HOME = (By.ID, "back-to-products")

    def complete_header(self) -> str:
        return self.text(self.COMPLETE_HEADER)

    def back_home(self) -> None:
        self.click(self.BACK_HOME)
