"""Cart page object for cart content and navigation operations."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    QTY_HEADER = (By.CSS_SELECTOR, ".cart_quantity_label")
    DESC_HEADER = (By.CSS_SELECTOR, ".cart_desc_label")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CHECKOUT = (By.ID, "checkout")

    def title(self) -> str:
        return self.text(self.TITLE)

    def quantity_header(self) -> str:
        return self.text(self.QTY_HEADER)

    def description_header(self) -> str:
        return self.text(self.DESC_HEADER)

    def item_count(self) -> int:
        return len(self.wait.present_all(self.CART_ITEMS))

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

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING)

    def checkout(self) -> None:
        self.click(self.CHECKOUT)
        try:
            self.wait.url_contains("checkout-step-one.html")
        except TimeoutException as exc:
            raise AssertionError("Failed to navigate to checkout step one from cart page") from exc
