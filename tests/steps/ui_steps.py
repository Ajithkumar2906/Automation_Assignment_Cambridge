"""BDD step definitions for UI scenarios."""

from __future__ import annotations

import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from framework.core.settings import settings
from pytest_bdd import given, parsers, then, when


def _extract_amount(text: str) -> float:
    match = re.search(r"([0-9]+(?:\.[0-9]{1,2})?)", text)
    if not match:
        raise AssertionError(f"Unable to parse monetary amount from: {text}")
    return float(match.group(1))


def _set_input_value_js(page, field_id: str, value: str) -> None:
    """Use the native input setter so React-controlled fields update consistently."""
    page.driver.execute_script(
        """
        const set = (id, val) => {
          const el = document.getElementById(id);
          if (!el) return;
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, val);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set(arguments[0], arguments[1]);
        """,
        field_id,
        value,
    )


def _set_checkout_fields(checkout_info_page, first_name: str, last_name: str, postal_code: str) -> None:
    """Set checkout fields in one place to avoid repeated JS and field-clear logic."""
    _set_input_value_js(checkout_info_page, "first-name", first_name)
    _set_input_value_js(checkout_info_page, "last-name", last_name)
    _set_input_value_js(checkout_info_page, "postal-code", postal_code)


def _close_checkout_error_if_visible(checkout_info_page) -> None:
    if checkout_info_page.has_error():
        checkout_info_page.close_error()
        WebDriverWait(checkout_info_page.driver, 3).until(
            EC.invisibility_of_element_located(checkout_info_page.ERROR_MSG)
        )


@given("the user opens the SauceDemo login page")
def open_login_page(login_page):
    login_page.load()


@given(parsers.parse('the user is logged in as "{username}"'))
def login_as_user(login_page, inventory_page, users_data, username):
    password = users_data.get(username, "secret_sauce")
    login_page.load()
    login_page.login(username, password)
    assert inventory_page.is_visible(inventory_page.PRODUCTS_TITLE), "Login did not reach inventory page"


@when(parsers.parse('the user logs in with username "{username}" and password "{password}"'))
def login_with_credentials(login_page, username, password):
    login_page.login(username, password)


@when("the user logs in with username empty and password \"secret_sauce\"")
def login_with_empty_username(login_page):
    if login_page.has_error():
        login_page.close_error()
    _set_input_value_js(login_page, "user-name", "")
    _set_input_value_js(login_page, "password", "secret_sauce")
    login_page.click(login_page.LOGIN_BTN)


@when("the user logs in with username \"standard_user\" and password empty")
def login_with_empty_password(login_page):
    if login_page.has_error():
        login_page.close_error()
    _set_input_value_js(login_page, "user-name", "standard_user")
    _set_input_value_js(login_page, "password", "")
    login_page.click(login_page.LOGIN_BTN)


@when("the user clicks login without entering credentials")
def click_login_without_credentials(login_page):
    login_page.login_blank()


@then("the products page is displayed")
def verify_products_page(inventory_page):
    assert inventory_page.products_title() == "Products"


@then(parsers.parse('the app header should be "{expected_header}"'))
def verify_header(inventory_page, expected_header):
    assert inventory_page.header_text() == expected_header


@then(parsers.parse('login error should contain "{expected_text}"'))
def verify_login_error(login_page, expected_text):
    assert expected_text.lower() in login_page.get_error().lower()


@when("the user closes the login error")
def close_login_error(login_page):
    login_page.close_error()


@then("login error should not be visible")
def verify_error_not_visible(login_page):
    assert not login_page.has_error()


@then(parsers.parse('products section title should be "{expected_title}"'))
def verify_products_title(inventory_page, expected_title):
    assert inventory_page.products_title() == expected_title


@then("cart icon should be visible")
def verify_cart_icon(inventory_page):
    assert inventory_page.is_visible(inventory_page.CART_ICON)


@then("sort options should be available")
def verify_sort_options(inventory_page):
    expected = {"Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"}
    actual = set(inventory_page.sort_option_labels())
    assert expected.issubset(actual)


@when("the user clicks sidemenu from inventory")
def click_inventory_sidemenu(inventory_page):
    inventory_page.open_menu()


@when("the user clicks close icon")
def click_inventory_menu_close(inventory_page):
    inventory_page.close_menu()


@then("the side menu should be closed")
def verify_inventory_menu_closed(inventory_page):
    # Confirm the menu fully closed before moving on.
    assert inventory_page.wait.invisible(inventory_page.MENU_CLOSE), "Side menu is still open"
    assert inventory_page.is_visible(inventory_page.MENU_BTN), "Menu button did not reappear after closing"


@when("the user clicks logout from inventory side menu")
def click_logout_from_inventory_menu(inventory_page):
    inventory_page.click_logout()


@then("the login page should be displayed")
def verify_login_page_displayed(login_page):
    assert login_page.is_visible(login_page.LOGIN_BTN), "Login button is not visible"


@when(parsers.parse('the user selects sort option "{sort_option}"'))
def select_sort_option(inventory_page, sort_option):
    inventory_page.sort_by_value(sort_option)


@then("products should be sorted by name ascending")
def verify_products_sorted_name_asc(inventory_page):
    actual = inventory_page.product_names()
    assert actual == sorted(actual), f"Name A-Z sort mismatch. Actual order: {actual}"


@then("products should be sorted by name descending")
def verify_products_sorted_name_desc(inventory_page):
    actual = inventory_page.product_names()
    assert actual == sorted(actual, reverse=True), f"Name Z-A sort mismatch. Actual order: {actual}"


@then("products should be sorted by price ascending")
def verify_products_sorted_price_asc(inventory_page):
    actual = inventory_page.product_prices()
    assert actual == sorted(actual), f"Price low-high sort mismatch. Actual order: {actual}"


@then("products should be sorted by price descending")
def verify_products_sorted_price_desc(inventory_page):
    actual = inventory_page.product_prices()
    assert actual == sorted(actual, reverse=True), f"Price high-low sort mismatch. Actual order: {actual}"


@when("the user clicks reset app state from side menu")
def reset_app_state_from_side_menu(inventory_page):
    assert inventory_page.reset_app_state(), "Reset App State did not clear cart state"


@then(parsers.parse("cart badge count should be {expected_count:d}"))
def verify_cart_badge(inventory_page, expected_count):
    assert inventory_page.wait_for_cart_count(expected_count), (
        f"Cart badge mismatch: expected {expected_count}, actual {inventory_page.cart_count()} "
        f"(url={inventory_page.current_url()})"
    )
    assert inventory_page.cart_count() == expected_count


@when("the user selects a loaded product from inventory")
def select_loaded_product(inventory_page, context):
    # Deterministic pick keeps this data-driven step reproducible.
    products = inventory_page.product_cards_data()
    assert products, "No products available on inventory page"
    selected = sorted(products, key=lambda item: item["name"])[0]
    context["selected_loaded_product"] = selected


@when("the user selects two distinct loaded products from inventory")
def select_two_loaded_products(inventory_page, context):
    products = inventory_page.product_cards_data()
    assert len(products) >= 2, "At least two products are required for this scenario"
    selected_two = sorted(products, key=lambda item: item["name"])[:2]
    context["selected_loaded_products"] = selected_two


@when("the user selects up to two loaded products from inventory")
def select_up_to_two_loaded_products(inventory_page, context):
    products = inventory_page.product_cards_data()
    assert products, "No products available on inventory page"
    context["selected_loaded_products"] = sorted(products, key=lambda item: item["name"])[:2]


@when("the user opens selected loaded product details")
def open_selected_loaded_product_details(inventory_page, context):
    selected = context["selected_loaded_product"]
    inventory_page.open_product_details(selected["name"])


@then("selected loaded product details should match inventory data")
def verify_loaded_product_details(product_details_page, context):
    selected = context["selected_loaded_product"]
    assert product_details_page.has_image()
    assert product_details_page.name() == selected["name"]
    assert product_details_page.description() == selected["description"]
    assert float(product_details_page.price().replace("$", "").strip()) == selected["price"]


@when("the user adds selected loaded product to cart")
def add_selected_loaded_product(inventory_page, product_details_page, context):
    selected = context["selected_loaded_product"]
    if "inventory-item.html" in inventory_page.current_url():
        product_details_page.toggle_cart_button()
    else:
        inventory_page.add_product_by_name(selected["name"])


@when("the user adds the first selected loaded product to cart")
def add_first_selected_loaded_product(inventory_page, context):
    selected_two = context["selected_loaded_products"]
    inventory_page.add_product_by_name(selected_two[0]["name"])


@when("the user adds the second selected loaded product to cart")
def add_second_selected_loaded_product(inventory_page, context):
    selected_two = context["selected_loaded_products"]
    inventory_page.add_product_by_name(selected_two[1]["name"])


@when("the user adds all selected loaded products to cart")
def add_all_selected_loaded_products(inventory_page, context):
    for product in context["selected_loaded_products"]:
        inventory_page.add_product_by_name(product["name"])


@when("the user removes selected loaded product from inventory")
def remove_selected_loaded_product(inventory_page, context):
    selected = context["selected_loaded_product"]
    success = inventory_page.remove_product_by_name(selected["name"])
    assert success, f"Failed to remove selected loaded product: {selected['name']}"


@then("selected loaded product should match cart item data")
def verify_loaded_product_in_cart(cart_page, context):
    selected = context["selected_loaded_product"]
    items = cart_page.items_data()
    assert items, "Cart is empty"
    matched = next((item for item in items if item["name"] == selected["name"]), None)
    assert matched is not None, f"Selected product not found in cart: {selected['name']}"
    assert matched["description"] == selected["description"]
    assert matched["price"] == selected["price"]
    assert matched["quantity"] >= 1


@then("both selected loaded products should be present in cart")
def verify_two_loaded_products_in_cart(cart_page, context):
    selected_two = context["selected_loaded_products"]
    items = cart_page.items_data()
    cart_names = {item["name"] for item in items}
    for selected in selected_two:
        assert selected["name"] in cart_names, f"Selected product not found in cart: {selected['name']}"


@then("selected loaded product should match checkout overview item data")
def verify_loaded_product_in_overview(checkout_overview_page, context):
    selected = context["selected_loaded_product"]
    items = checkout_overview_page.items_data()
    assert items, "No items in checkout overview"
    matched = next((item for item in items if item["name"] == selected["name"]), None)
    assert matched is not None, f"Selected product not found in checkout overview: {selected['name']}"
    assert matched["description"] == selected["description"]
    assert matched["price"] == selected["price"]
    assert matched["quantity"] >= 1


@then("all inventory product images should be loaded")
def verify_all_inventory_images_loaded(inventory_page):
    assert inventory_page.all_images_loaded(), "One or more inventory product images failed to load"


@when("the user notes the current cart badge count")
def note_current_cart_badge(inventory_page, context):
    context["cart_count_before"] = inventory_page.cart_count()


@then("the cart badge should increment by 1")
def verify_badge_increment(inventory_page, context):
    before = context.get("cart_count_before", 0)
    expected = before + 1
    assert inventory_page.wait_for_cart_count(expected), (
        f"Expected cart badge to increment from {before} to {expected}, got {inventory_page.cart_count()}"
    )


@then("the cart badge should decrement by 1")
def verify_badge_decrement(inventory_page, context):
    before = context.get("cart_count_before", 0)
    assert inventory_page.wait_for_cart_count(before), (
        f"Expected cart badge to decrement back to {before}, got {inventory_page.cart_count()}"
    )


@when("the user toggles cart button on product details page")
def toggle_details_button(product_details_page):
    # Only click when button is in "Add to cart" state.
    if "add to cart" in product_details_page.cart_button_label().lower():
        product_details_page.toggle_cart_button()


@when("the user returns to products page")
def go_back_products(product_details_page):
    product_details_page.back_to_products()


@when("the user opens the cart page")
def open_cart_page(inventory_page):
    inventory_page.open_cart()


@then(parsers.parse('cart page title should be "{expected_title}"'))
def verify_cart_page_title(cart_page, expected_title):
    assert cart_page.title() == expected_title


@then(parsers.parse('cart headers should be "{expected_qty}" and "{expected_desc}"'))
def verify_cart_headers(cart_page, expected_qty, expected_desc):
    assert cart_page.quantity_header() == expected_qty
    assert cart_page.description_header() == expected_desc


@then(parsers.parse("cart should contain {expected_items:d} items"))
def verify_cart_item_count(cart_page, expected_items):
    assert cart_page.item_count() == expected_items


@then("cart badge count should match selected loaded products")
def verify_cart_badge_matches_selected(inventory_page, context):
    expected = len(context["selected_loaded_products"])
    assert inventory_page.wait_for_cart_count(expected), (
        f"Cart badge mismatch: expected {expected}, actual {inventory_page.cart_count()}"
    )
    assert inventory_page.cart_count() == expected


@then("cart should contain selected loaded products count")
def verify_cart_item_count_matches_selected(cart_page, context):
    expected = len(context["selected_loaded_products"])
    assert cart_page.item_count() == expected


@then("cart page should be displayed")
def verify_cart_page_displayed(cart_page):
    assert cart_page.title() == "Your Cart"


@when("the user starts checkout")
def start_checkout(cart_page, inventory_page):
    # Some scenarios jump straight from inventory.
    if "cart.html" not in cart_page.current_url():
        inventory_page.open_cart()
    cart_page.checkout()


@then(parsers.parse('checkout info title should be "{expected_title}"'))
def verify_checkout_info_title(checkout_info_page, expected_title):
    assert checkout_info_page.title() == expected_title


@when("the user continues checkout without entering first name")
def continue_without_first_name(checkout_info_page):
    _close_checkout_error_if_visible(checkout_info_page)
    _set_checkout_fields(checkout_info_page, "", "Tester", "CB11AA")
    assert checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME).get_attribute("value").strip() == ""
    assert checkout_info_page.wait.visible(checkout_info_page.LAST_NAME).get_attribute("value").strip() == "Tester"
    assert checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE).get_attribute("value").strip() == "CB11AA"
    checkout_info_page.click_continue()


@when("the user fills first name and continues checkout without entering last name")
def continue_without_last_name(checkout_info_page):
    _close_checkout_error_if_visible(checkout_info_page)
    _set_checkout_fields(checkout_info_page, "Alex", "", "CB11AA")
    assert checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME).get_attribute("value").strip() == "Alex"
    assert checkout_info_page.wait.visible(checkout_info_page.LAST_NAME).get_attribute("value").strip() == ""
    assert checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE).get_attribute("value").strip() == "CB11AA"
    checkout_info_page.click_continue()


@when("the user fills first name, last name and continues checkout without entering postal code")
def continue_without_postal_code(checkout_info_page):
    _close_checkout_error_if_visible(checkout_info_page)
    _set_checkout_fields(checkout_info_page, "Alex", "Tester", "")
    assert checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME).get_attribute("value").strip() == "Alex"
    assert checkout_info_page.wait.visible(checkout_info_page.LAST_NAME).get_attribute("value").strip() == "Tester"
    assert checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE).get_attribute("value").strip() == ""
    checkout_info_page.click_continue()


@when("the user cancels checkout without continue")
def cancel_checkout_without_continue(checkout_info_page):
    checkout_info_page.click_cancel()


@when("the user clicks continue shopping from cart page")
def click_continue_shopping_from_cart(cart_page):
    cart_page.continue_shopping()


@then(parsers.parse('checkout info error should contain "{expected_error}"'))
def verify_checkout_error(checkout_info_page, expected_error):
    assert expected_error.lower() in checkout_info_page.error_text().lower()


@when("the user fills checkout information with valid details")
def fill_checkout_info(checkout_info_page, checkout_data):
    data = checkout_data["default"]
    checkout_info_page.wait.url_contains("checkout-step-one.html")
    checkout_info_page.fill_information(data["first_name"], data["last_name"], data["postal_code"])


@when("the user continues checkout")
def continue_checkout(checkout_info_page):
    # Retry click+wait because navigation can lag on remote browsers.
    for _ in range(3):
        checkout_info_page.click_continue()
        try:
            WebDriverWait(checkout_info_page.driver, settings.explicit_wait).until(
                EC.url_contains("checkout-step-two.html")
            )
            return
        except TimeoutException:
            continue
    error_text = checkout_info_page.error_text() if checkout_info_page.has_error() else "no form error shown"
    raise AssertionError(f"Checkout did not reach overview after continue; error={error_text}")


@when("the user records checkout overview total amount")
def record_checkout_overview_total(checkout_overview_page):
    checkout_overview_page.wait.url_contains("checkout-step-two.html")
    total = round(_extract_amount(checkout_overview_page.total()), 2)
    assert total > 0, f"Expected checkout total to be positive, got {total}"


@then(parsers.parse('checkout overview title should be "{expected_title}"'))
def verify_checkout_overview_title(checkout_overview_page, expected_title):
    assert checkout_overview_page.title() == expected_title


@then("checkout overview should show payment shipping and total information")
def verify_checkout_overview_fields(checkout_overview_page):
    checkout_overview_page.wait.url_contains("checkout-step-two.html")
    assert checkout_overview_page.qty_header() == "QTY"
    assert checkout_overview_page.desc_header() == "Description"
    assert checkout_overview_page.payment_info() != ""
    assert checkout_overview_page.shipping_info() != ""
    assert "Item total" in checkout_overview_page.item_total()
    assert "Tax" in checkout_overview_page.tax()
    assert "Total" in checkout_overview_page.total()


@then("checkout overview financial totals should be correct")
def verify_checkout_overview_totals(checkout_overview_page):
    checkout_overview_page.wait.url_contains("checkout-step-two.html")
    items = checkout_overview_page.items_data()
    assert items, "Expected at least one item in checkout overview"

    sum_prices = round(sum(item["price"] * item["quantity"] for item in items), 2)
    item_total = round(_extract_amount(checkout_overview_page.item_total()), 2)
    tax = round(_extract_amount(checkout_overview_page.tax()), 2)
    total = round(_extract_amount(checkout_overview_page.total()), 2)

    assert item_total == sum_prices, f"Item total mismatch. expected={sum_prices} actual={item_total}"
    assert total == round(item_total + tax, 2), (
        f"Total mismatch. expected={round(item_total + tax, 2)} actual={total}"
    )


@when("the user clicks cancel from the overview page")
def cancel_from_checkout_overview(checkout_overview_page):
    checkout_overview_page.cancel()


@when("the user finishes checkout")
def finish_checkout(checkout_overview_page):
    checkout_overview_page.finish()


@then(parsers.parse('checkout complete header should be "{expected_header}"'))
def verify_complete_header(checkout_complete_page, expected_header):
    assert checkout_complete_page.complete_header() == expected_header


@when("the user clicks back home on complete page")
def click_back_home(checkout_complete_page):
    checkout_complete_page.back_home()
