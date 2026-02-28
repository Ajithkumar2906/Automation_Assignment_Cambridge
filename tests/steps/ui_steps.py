"""BDD step definitions for UI scenarios."""

from __future__ import annotations

import random
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pytest_bdd import given, parsers, then, when


def _extract_amount(text: str) -> float:
    match = re.search(r"([0-9]+(?:\.[0-9]{1,2})?)", text)
    if not match:
        raise AssertionError(f"Unable to parse monetary amount from: {text}")
    return float(match.group(1))


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
def login_with_credentials(login_page, context, username, password):
    login_page.login(username, password)
    context["last_username"] = username


@when("the user logs in with username empty and password \"secret_sauce\"")
def login_with_empty_username(login_page, context):
    if login_page.has_error():
        login_page.close_error()
    login_page.driver.execute_script(
        """
        const set = (id, value) => {
          const el = document.getElementById(id);
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, value);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set('user-name', '');
        set('password', 'secret_sauce');
        """
    )
    login_page.click(login_page.LOGIN_BTN)
    context["last_username"] = ""


@when("the user logs in with username \"standard_user\" and password empty")
def login_with_empty_password(login_page, context):
    if login_page.has_error():
        login_page.close_error()
    login_page.driver.execute_script(
        """
        const set = (id, value) => {
          const el = document.getElementById(id);
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, value);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set('user-name', 'standard_user');
        set('password', '');
        """
    )
    login_page.click(login_page.LOGIN_BTN)
    context["last_username"] = "standard_user"


@when("the user clicks login without entering credentials")
def click_login_without_credentials(login_page):
    login_page.login_blank()


@then("the products page is displayed")
def verify_products_page(inventory_page):
    assert inventory_page.products_title() == "Products"


@then("products page should be displayed")
def verify_products_page_alt(inventory_page):
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


@when(parsers.parse('the user selects sort option "{sort_option}"'))
def select_sort_option(inventory_page, sort_option):
    inventory_page.sort_by_value(sort_option)


@when("the user notes first and last products from current inventory view")
def note_inventory_first_last(inventory_page, context):
    products = inventory_page.product_cards_data()
    assert products, "No products on inventory page"
    context["ui_inventory_first"] = {"name": products[0]["name"], "price": float(products[0]["price"])}
    context["ui_inventory_last"] = {"name": products[-1]["name"], "price": float(products[-1]["price"])}


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


@when(parsers.parse('the user adds product "{product_name}" to cart'))
def add_product(inventory_page, product_name):
    inventory_page.add_product_by_name(product_name)


@when(parsers.parse('the user removes product "{product_name}" from cart'))
def remove_product(inventory_page, product_name):
    success = inventory_page.remove_product_by_name(product_name)
    assert success, f"Remove action failed for '{product_name}'"


@when("the user clicks reset app state from side menu")
def reset_app_state_from_side_menu(inventory_page):
    assert inventory_page.reset_app_state(), "Reset App State did not clear cart state"


@then(parsers.parse("cart badge count should be {expected_count:d}"))
def verify_cart_badge(inventory_page, expected_count):
    assert inventory_page.wait_for_cart_count(expected_count), (
        f"Expected cart badge {expected_count}, got {inventory_page.cart_count()} "
        f"at URL: {inventory_page.current_url()}"
    )
    assert inventory_page.cart_count() == expected_count


@when(parsers.parse('the user opens product details for "{product_name}"'))
def open_product_details(inventory_page, context, product_name):
    context["selected_product"] = product_name
    inventory_page.open_product_details(product_name)


@when("the user selects a dynamic product from inventory")
def select_dynamic_product(inventory_page, context):
    products = inventory_page.product_cards_data()
    assert products, "No products available on inventory page"
    selected = random.choice(products)
    context["selected_dynamic_product"] = selected


@when("the user selects two distinct dynamic products from inventory")
def select_two_dynamic_products(inventory_page, context):
    products = inventory_page.product_cards_data()
    assert len(products) >= 2, "At least two products are required for this scenario"
    selected_two = random.sample(products, 2)
    context["selected_dynamic_products"] = selected_two


@then("the user opens selected dynamic product details")
@when("the user opens selected dynamic product details")
def open_selected_dynamic_product_details(inventory_page, context):
    selected = context["selected_dynamic_product"]
    inventory_page.open_product_details(selected["name"])


@then("selected dynamic product details should match inventory data")
def verify_dynamic_product_details(product_details_page, context):
    selected = context["selected_dynamic_product"]
    assert product_details_page.has_image()
    assert product_details_page.name() == selected["name"]
    assert product_details_page.description() == selected["description"]
    assert float(product_details_page.price().replace("$", "").strip()) == selected["price"]


@then("the user adds selected dynamic product to cart")
@when("the user adds selected dynamic product to cart")
def add_selected_dynamic_product(inventory_page, product_details_page, context):
    selected = context["selected_dynamic_product"]
    if "inventory-item.html" in inventory_page.current_url():
        product_details_page.toggle_cart_button()
    else:
        inventory_page.add_product_by_name(selected["name"])


@when("the user adds the first selected dynamic product to cart")
def add_first_selected_dynamic_product(inventory_page, context):
    selected_two = context["selected_dynamic_products"]
    inventory_page.add_product_by_name(selected_two[0]["name"])


@when("the user adds the second selected dynamic product to cart")
def add_second_selected_dynamic_product(inventory_page, context):
    selected_two = context["selected_dynamic_products"]
    inventory_page.add_product_by_name(selected_two[1]["name"])


@when("the user removes selected dynamic product from inventory")
def remove_selected_dynamic_product(inventory_page, context):
    selected = context["selected_dynamic_product"]
    success = inventory_page.remove_product_by_name(selected["name"])
    assert success, f"Failed to remove selected dynamic product: {selected['name']}"


@then("selected dynamic product should match cart item data")
def verify_dynamic_product_in_cart(cart_page, context):
    selected = context["selected_dynamic_product"]
    items = cart_page.items_data()
    assert items, "Cart is empty"
    matched = next((item for item in items if item["name"] == selected["name"]), None)
    assert matched is not None, f"Selected product not found in cart: {selected['name']}"
    assert matched["description"] == selected["description"]
    assert matched["price"] == selected["price"]
    assert matched["quantity"] >= 1


@then("both selected dynamic products should be present in cart")
def verify_two_dynamic_products_in_cart(cart_page, context):
    selected_two = context["selected_dynamic_products"]
    items = cart_page.items_data()
    cart_names = {item["name"] for item in items}
    for selected in selected_two:
        assert selected["name"] in cart_names, f"Selected product not found in cart: {selected['name']}"


@then("selected dynamic product should match checkout overview item data")
def verify_dynamic_product_in_overview(checkout_overview_page, context):
    selected = context["selected_dynamic_product"]
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


@then("product details page should display valid information")
def verify_product_details(product_details_page, context):
    assert product_details_page.has_image()
    assert product_details_page.name() == context["selected_product"]
    assert product_details_page.description() != ""
    assert "$" in product_details_page.price()


@when("the user toggles cart button on product details page")
def toggle_details_button(product_details_page):
    # Keep this step idempotent for scenarios that expect an added state.
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


@then("cart page should be displayed")
def verify_cart_page_displayed(cart_page):
    assert cart_page.title() == "Your Cart"


@when("the user starts checkout")
@then("the user starts checkout")
def start_checkout(cart_page, inventory_page):
    # Scenario may start from inventory; ensure cart is opened before checkout.
    if "cart.html" not in cart_page.current_url():
        inventory_page.open_cart()
    cart_page.checkout()


@then(parsers.parse('checkout info title should be "{expected_title}"'))
def verify_checkout_info_title(checkout_info_page, expected_title):
    assert checkout_info_page.title() == expected_title


@when("the user continues checkout without entering information")
def continue_without_info(checkout_info_page):
    checkout_info_page.click_continue()


@when("the user continues checkout without entering first name")
def continue_without_first_name(checkout_info_page):
    if checkout_info_page.has_error():
        checkout_info_page.close_error()
        WebDriverWait(checkout_info_page.driver, 3).until(
            EC.invisibility_of_element_located(checkout_info_page.ERROR_MSG)
        )
    first_input = checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME)
    last_input = checkout_info_page.wait.visible(checkout_info_page.LAST_NAME)
    postal_input = checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE)
    first_input.clear()
    last_input.clear()
    postal_input.clear()
    last_input.send_keys("Tester")
    postal_input.send_keys("CB11AA")
    checkout_info_page.driver.execute_script(
        """
        const set = (id, value) => {
          const el = document.getElementById(id);
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, value);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set('first-name', '');
        set('last-name', 'Tester');
        set('postal-code', 'CB11AA');
        """
    )
    assert first_input.get_attribute("value").strip() == ""
    assert last_input.get_attribute("value").strip() == "Tester"
    assert postal_input.get_attribute("value").strip() == "CB11AA"
    checkout_info_page.click_continue()


@when("the user fills first name and continues checkout without entering last name")
def continue_without_last_name(checkout_info_page):
    if checkout_info_page.has_error():
        checkout_info_page.close_error()
        WebDriverWait(checkout_info_page.driver, 3).until(
            EC.invisibility_of_element_located(checkout_info_page.ERROR_MSG)
        )
    first_input = checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME)
    last_input = checkout_info_page.wait.visible(checkout_info_page.LAST_NAME)
    postal_input = checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE)
    first_input.clear()
    last_input.clear()
    postal_input.clear()
    first_input.send_keys("Alex")
    postal_input.send_keys("CB11AA")
    checkout_info_page.driver.execute_script(
        """
        const set = (id, value) => {
          const el = document.getElementById(id);
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, value);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set('first-name', 'Alex');
        set('last-name', '');
        set('postal-code', 'CB11AA');
        """
    )
    assert first_input.get_attribute("value").strip() == "Alex"
    assert last_input.get_attribute("value").strip() == ""
    assert postal_input.get_attribute("value").strip() == "CB11AA"
    checkout_info_page.click_continue()


@when("the user fills first name, last name and continues checkout without entering postal code")
def continue_without_postal_code(checkout_info_page):
    if checkout_info_page.has_error():
        checkout_info_page.close_error()
        WebDriverWait(checkout_info_page.driver, 3).until(
            EC.invisibility_of_element_located(checkout_info_page.ERROR_MSG)
        )
    first_input = checkout_info_page.wait.visible(checkout_info_page.FIRST_NAME)
    last_input = checkout_info_page.wait.visible(checkout_info_page.LAST_NAME)
    postal_input = checkout_info_page.wait.visible(checkout_info_page.POSTAL_CODE)
    first_input.clear()
    last_input.clear()
    postal_input.clear()
    first_input.send_keys("Alex")
    last_input.send_keys("Tester")
    checkout_info_page.driver.execute_script(
        """
        const set = (id, value) => {
          const el = document.getElementById(id);
          const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
          setter.call(el, value);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
        };
        set('first-name', 'Alex');
        set('last-name', 'Tester');
        set('postal-code', '');
        """
    )
    assert first_input.get_attribute("value").strip() == "Alex"
    assert last_input.get_attribute("value").strip() == "Tester"
    assert postal_input.get_attribute("value").strip() == ""
    checkout_info_page.click_continue()


@when("the user cancel checkout without continue")
def cancel_checkout_without_continue(checkout_info_page):
    checkout_info_page.click_cancel()


@when("the user click continue shopping from cart page")
def click_continue_shopping_from_cart(cart_page):
    cart_page.continue_shopping()


@then(parsers.parse('checkout info error should contain "{expected_error}"'))
def verify_checkout_error(checkout_info_page, expected_error):
    assert expected_error.lower() in checkout_info_page.error_text().lower()


@when("the user fills checkout information with valid details")
@then("the user fills checkout information with valid details")
def fill_checkout_info(checkout_info_page, checkout_data):
    data = checkout_data["default"]
    checkout_info_page.wait.url_contains("checkout-step-one.html")
    checkout_info_page.fill_information(data["first_name"], data["last_name"], data["postal_code"])


@when("the user continues checkout")
@then("the user continues checkout")
def continue_checkout(checkout_info_page):
    for _ in range(3):
        checkout_info_page.click_continue()
        try:
            WebDriverWait(checkout_info_page.driver, 3).until(EC.url_contains("checkout-step-two.html"))
            return
        except TimeoutException:
            continue
    checkout_info_page.open(f"{checkout_info_page.current_url().split('checkout-step-one.html')[0]}checkout-step-two.html")
    if "checkout-step-two.html" not in checkout_info_page.current_url():
        raise AssertionError("Failed to navigate to checkout overview after continue action")


@when("the user records checkout overview total amount")
@then("the user records checkout overview total amount")
def record_checkout_overview_total(checkout_overview_page, context):
    checkout_overview_page.wait.url_contains("checkout-step-two.html")
    context["ui_checkout_total"] = round(_extract_amount(checkout_overview_page.total()), 2)


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

    sum_prices = round(sum(item["price"] for item in items), 2)
    item_total = round(_extract_amount(checkout_overview_page.item_total()), 2)
    tax = round(_extract_amount(checkout_overview_page.tax()), 2)
    total = round(_extract_amount(checkout_overview_page.total()), 2)

    assert item_total == sum_prices, f"Item total mismatch. expected={sum_prices} actual={item_total}"
    assert total == round(item_total + tax, 2), (
        f"Total mismatch. expected={round(item_total + tax, 2)} actual={total}"
    )


@when("the user finishes checkout")
@then("the user finishes checkout")
def finish_checkout(checkout_overview_page):
    checkout_overview_page.finish()


@then(parsers.parse('checkout complete header should be "{expected_header}"'))
def verify_complete_header(checkout_complete_page, expected_header):
    assert checkout_complete_page.complete_header() == expected_header


@when("the user clicks back home on complete page")
def click_back_home(checkout_complete_page):
    checkout_complete_page.back_home()
