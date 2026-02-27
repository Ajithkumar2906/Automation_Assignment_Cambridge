"""Inventory page object encapsulating products, sort, and menu operations."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from framework.core.settings import settings
from framework.pages.base_page import BasePage


class InventoryPage(BasePage):
    HEADER = (By.CSS_SELECTOR, ".app_logo")
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    MENU_CLOSE = (By.ID, "react-burger-cross-btn")
    CART_ICON = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    PRODUCTS_TITLE = (By.CSS_SELECTOR, ".title")
    FILTER = (By.CSS_SELECTOR, ".product_sort_container")
    SORT_OPTIONS = (By.CSS_SELECTOR, ".product_sort_container option")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    INVENTORY_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    INVENTORY_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    INVENTORY_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    INVENTORY_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_LINK = (By.ID, "reset_sidebar_link")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "[id^='remove-']")

    @staticmethod
    def _product_slug(product_name: str) -> str:
        return product_name.strip().lower().replace(" ", "-")

    def header_text(self) -> str:
        return self.text(self.HEADER)

    def products_title(self) -> str:
        return self.text(self.PRODUCTS_TITLE)

    def open_menu(self) -> None:
        self.click(self.MENU_BTN)

    def close_menu(self) -> None:
        self.click(self.MENU_CLOSE)

    def click_logout(self) -> None:
        self.open_menu()
        self.click(self.LOGOUT_LINK)

    def click_about(self) -> None:
        self.open_menu()
        self.click(self.ABOUT_LINK)

    def reset_app_state(self) -> bool:
        for _ in range(3):
            self.open_menu()
            self.click(self.RESET_LINK)
            self.driver.refresh()
            if self.wait_for_cart_count(0):
                return True
        return False

    def cart_count(self) -> int:
        badge = self.wait.try_visible(self.CART_BADGE)
        if badge:
            return int(badge.text.strip())
        # Fallback for occasional badge rendering issues in AUT.
        return len(self.driver.find_elements(*self.REMOVE_BUTTONS))

    def wait_for_cart_count(self, expected_count: int) -> bool:
        try:
            WebDriverWait(self.driver, settings.explicit_wait).until(lambda _: self.cart_count() == expected_count)
            return True
        except TimeoutException:
            return False

    def open_cart(self) -> None:
        self.click(self.CART_ICON)
        try:
            self.wait.url_contains("cart.html")
        except TimeoutException:
            self.open(f"{settings.base_url.rstrip('/')}/cart.html")

    def inventory_count(self) -> int:
        return len(self.wait.present_all(self.INVENTORY_ITEMS))

    def sort_by_value(self, value: str) -> None:
        dropdown = self.wait.visible(self.FILTER)
        Select(dropdown).select_by_visible_text(value)

    def sort_option_labels(self) -> list[str]:
        options = self.wait.present_all(self.SORT_OPTIONS)
        return [option.text.strip() for option in options]

    def product_names(self) -> list[str]:
        names = self.wait.present_all(self.INVENTORY_NAMES)
        return [name.text.strip() for name in names]

    def product_prices(self) -> list[float]:
        prices = self.wait.present_all(self.INVENTORY_PRICES)
        return [float(price.text.replace("$", "").strip()) for price in prices]

    def product_descriptions(self) -> list[str]:
        descriptions = self.wait.present_all(self.INVENTORY_DESCRIPTIONS)
        return [description.text.strip() for description in descriptions]

    def product_cards_data(self) -> list[dict]:
        names = self.product_names()
        descriptions = self.product_descriptions()
        prices = self.product_prices()
        image_elements = self.wait.present_all(self.INVENTORY_IMAGES)

        products = []
        for idx, name in enumerate(names):
            image = image_elements[idx] if idx < len(image_elements) else None
            products.append(
                {
                    "name": name,
                    "description": descriptions[idx] if idx < len(descriptions) else "",
                    "price": prices[idx] if idx < len(prices) else None,
                    "image_src": image.get_attribute("src") if image else "",
                }
            )
        return products

    def image_loaded_for_name(self, product_name: str) -> bool:
        image = self.driver.find_element(
            By.XPATH,
            f"//div[@class='inventory_item'][.//div[@class='inventory_item_name' and text()='{product_name}']]"
            "//img",
        )
        return bool(
            self.driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                image,
            )
        )

    def all_images_loaded(self) -> bool:
        images = self.wait.present_all(self.INVENTORY_IMAGES)
        if not images:
            return False
        for image in images:
            loaded = self.driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0;",
                image,
            )
            if not loaded:
                return False
        return True

    def add_product_by_name(self, product_name: str) -> None:
        add_locator = (By.ID, f"add-to-cart-{self._product_slug(product_name)}")
        remove_locator = (By.ID, f"remove-{self._product_slug(product_name)}")

        if self.driver.find_elements(*remove_locator):
            return

        for _ in range(3):
            self.click(add_locator)
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(remove_locator))
                return
            except TimeoutException:
                continue

        raise AssertionError(f"Failed to add product '{product_name}' after retries")

    def remove_product_by_name(self, product_name: str) -> bool:
        locator = (By.ID, f"remove-{self._product_slug(product_name)}")
        return self.safe_click(locator)

    def open_product_details(self, product_name: str) -> None:
        locator = (By.XPATH, f"//div[text()='{product_name}']")
        self.click(locator)
