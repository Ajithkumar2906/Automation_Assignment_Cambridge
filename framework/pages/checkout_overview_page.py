"""Checkout overview page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    QTY_HEADER = (By.CSS_SELECTOR, ".cart_quantity_label")
    DESC_HEADER = (By.CSS_SELECTOR, ".cart_desc_label")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity")
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

    def items_data(self) -> list[dict]:
        names = [el.text.strip() for el in self.wait.present_all(self.ITEM_NAMES)]
        descriptions = [el.text.strip() for el in self.wait.present_all(self.ITEM_DESCRIPTIONS)]
        prices = [float(el.text.replace("$", "").strip()) for el in self.wait.present_all(self.ITEM_PRICES)]
        quantities = [int(el.text.strip()) for el in self.wait.present_all(self.ITEM_QUANTITIES)]

        items = []
        for idx, name in enumerate(names):
            items.append(
                {
                    "name": name,
                    "description": descriptions[idx] if idx < len(descriptions) else "",
                    "price": prices[idx] if idx < len(prices) else None,
                    "quantity": quantities[idx] if idx < len(quantities) else 0,
                }
            )
        return items

    def cancel(self) -> None:
        self.click(self.CANCEL)

    def finish(self) -> None:
        self.click(self.FINISH)
