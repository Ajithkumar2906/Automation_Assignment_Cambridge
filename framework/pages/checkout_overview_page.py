"""Checkout overview page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    QTY_HEADER = (By.CSS_SELECTOR, ".cart_quantity_label")
    DESC_HEADER = (By.CSS_SELECTOR, ".cart_desc_label")
    PAYMENT_INFO = (By.CSS_SELECTOR, "[data-test='payment-info-value']")
    SHIPPING_INFO = (By.CSS_SELECTOR, "[data-test='shipping-info-value']")
    ITEM_TOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL = (By.CSS_SELECTOR, ".summary_total_label")
    CANCEL = (By.ID, "cancel")
    FINISH = (By.ID, "finish")

    def title(self) -> str:
        return self.text(self.TITLE)

    def qty_header(self) -> str:
        return self.text(self.QTY_HEADER)

    def desc_header(self) -> str:
        return self.text(self.DESC_HEADER)

    def payment_info(self) -> str:
        return self.text(self.PAYMENT_INFO)

    def shipping_info(self) -> str:
        return self.text(self.SHIPPING_INFO)

    def item_total(self) -> str:
        return self.text(self.ITEM_TOTAL)

    def tax(self) -> str:
        return self.text(self.TAX)

    def total(self) -> str:
        return self.text(self.TOTAL)

    def cancel(self) -> None:
        self.click(self.CANCEL)

    def finish(self) -> None:
        self.click(self.FINISH)
