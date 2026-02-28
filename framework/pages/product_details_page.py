"""Product details page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    NAME = (By.CSS_SELECTOR, ".inventory_details_name")
    DESCRIPTION = (By.CSS_SELECTOR, ".inventory_details_desc")
    PRICE = (By.CSS_SELECTOR, ".inventory_details_price")
    IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    ADD_OR_REMOVE = (By.CSS_SELECTOR, ".btn_inventory")
    BACK = (By.ID, "back-to-products")

    def name(self) -> str:
        return self.text(self.NAME)

    def description(self) -> str:
        return self.text(self.DESCRIPTION)

    def price(self) -> str:
        return self.text(self.PRICE)

    def has_image(self) -> bool:
        return self.is_visible(self.IMAGE)

    def toggle_cart_button(self) -> None:
        self.click(self.ADD_OR_REMOVE)

    def cart_button_label(self) -> str:
        return self.text(self.ADD_OR_REMOVE)

    def back_to_products(self) -> None:
        self.click(self.BACK)
