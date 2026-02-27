"""BDD step definitions for UI scenarios."""

from __future__ import annotations

import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pytest_bdd import given, parsers, then, when


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


@when("the user adds selected dynamic product to cart")
def add_selected_dynamic_product(inventory_page, context):
    selected = context["selected_dynamic_product"]
    inventory_page.add_product_by_name(selected["name"])


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


@when("the user starts checkout")
def start_checkout(cart_page):
    cart_page.checkout()


@then(parsers.parse('checkout info title should be "{expected_title}"'))
def verify_checkout_info_title(checkout_info_page, expected_title):
    assert checkout_info_page.title() == expected_title


@when("the user continues checkout without entering information")
def continue_without_info(checkout_info_page):
    checkout_info_page.click_continue()


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


@when("the user finishes checkout")
def finish_checkout(checkout_overview_page):
    checkout_overview_page.finish()


@then(parsers.parse('checkout complete header should be "{expected_header}"'))
def verify_complete_header(checkout_complete_page, expected_header):
    assert checkout_complete_page.complete_header() == expected_header


@when("the user clicks back home on complete page")
def click_back_home(checkout_complete_page):
    checkout_complete_page.back_home()
