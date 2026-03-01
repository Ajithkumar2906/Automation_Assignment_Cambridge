"""Checkout information page object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    CANCEL = (By.ID, "cancel")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE = (By.CSS_SELECTOR, "button.error-button")

    def title(self) -> str:
        return self.text(self.TITLE)

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        # Retry field population because AUT can occasionally ignore first key events.
        for _ in range(3):
            self.type(self.FIRST_NAME, first_name)
            self.type(self.LAST_NAME, last_name)
            self.type(self.POSTAL_CODE, postal_code)
            # Always sync with JS setter to keep React-controlled state consistent.
            self.driver.execute_script(
                """
                const setValue = (id, value) => {
                  const el = document.getElementById(id);
                  if (!el) return;
                  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                  setter.call(el, value);
                  el.dispatchEvent(new Event('input', { bubbles: true }));
                  el.dispatchEvent(new Event('change', { bubbles: true }));
                };
                setValue('first-name', arguments[0]);
                setValue('last-name', arguments[1]);
                setValue('postal-code', arguments[2]);
                """,
                first_name,
                last_name,
                postal_code,
            )
            first = self.wait.visible(self.FIRST_NAME).get_attribute("value").strip()
            last = self.wait.visible(self.LAST_NAME).get_attribute("value").strip()
            zip_code = self.wait.visible(self.POSTAL_CODE).get_attribute("value").strip()
            if first == first_name.strip() and last == last_name.strip() and zip_code == postal_code.strip():
                return
        raise AssertionError("Failed to populate checkout information fields reliably")

    def click_continue(self) -> None:
        self.click(self.CONTINUE)

    def click_cancel(self) -> None:
        self.click(self.CANCEL)

    def error_text(self) -> str:
        return self.text(self.ERROR_MSG)

    def close_error(self) -> None:
        self.click(self.ERROR_CLOSE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MSG)
