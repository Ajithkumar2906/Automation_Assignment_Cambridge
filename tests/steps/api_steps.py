"""BDD step definitions for API validation scenarios."""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, then, when

from framework.api.sauce_api import ApiClientError, SauceApiClient
from framework.core.settings import settings


@given("an API client for SauceDemo")
def api_client(context):
    context["api_client"] = SauceApiClient()


@given("an API client for SauceDemo backend")
def api_client_backend(context):
    if not settings.api_enabled:
        pytest.skip("Hybrid API checks are disabled. Set API_ENABLED=true and configure API_* endpoints.")
    context["api_client"] = SauceApiClient()


@when("the API client requests the login page")
def request_login_page(context):
    context["status_code"] = context["api_client"].get_login_page_status()
    context["response_body"] = context["api_client"].get_login_page_text()


@then("the login page response status should be 200")
def verify_status_code(context):
    assert context["status_code"] == 200


@then('the response body should contain "Swag Labs"')
def verify_response_text(context):
    assert "Swag Labs" in context["response_body"]


@when(parsers.parse('the API client requests inventory sorted by "{sort_value}"'))
def request_inventory_sorted(context, sort_value):
    try:
        status_code, payload = context["api_client"].get_inventory(sort_value)
    except ApiClientError as exc:
        pytest.skip(f"Inventory API unavailable: {exc}")
    context["status_code"] = status_code
    context["api_inventory"] = payload


@when("the API client requests current cart")
def request_current_cart(context):
    try:
        status_code, payload = context["api_client"].get_cart()
    except ApiClientError as exc:
        pytest.skip(f"Cart API unavailable: {exc}")
    context["status_code"] = status_code
    context["api_cart"] = payload


@when("the API client requests latest order")
def request_latest_order(context):
    try:
        status_code, payload = context["api_client"].get_latest_order()
    except ApiClientError as exc:
        pytest.skip(f"Latest-order API unavailable: {exc}")
    context["status_code"] = status_code
    context["api_order"] = payload


@then("inventory API response status should be 200")
def verify_inventory_api_status(context):
    assert context["status_code"] == 200


@then("cart API response status should be 200")
def verify_cart_api_status(context):
    assert context["status_code"] == 200


@then("order API response status should be 200")
def verify_order_api_status(context):
    assert context["status_code"] == 200


@then("inventory API should be sorted by price descending")
def verify_inventory_sorted_desc(context):
    payload = context["api_inventory"]
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    prices = [float(item["price"]) for item in items]
    assert prices == sorted(prices, reverse=True), f"Inventory prices are not sorted desc: {prices}"


@then("inventory API first and last items should match current UI inventory view")
def verify_inventory_edges_match_ui(context):
    payload = context["api_inventory"]
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    assert items, "API inventory payload is empty"
    ui_first = context["ui_inventory_first"]
    ui_last = context["ui_inventory_last"]
    api_first = items[0]
    api_last = items[-1]

    assert api_first["name"] == ui_first["name"]
    assert float(api_first["price"]) == ui_first["price"]
    assert api_last["name"] == ui_last["name"]
    assert float(api_last["price"]) == ui_last["price"]


@then("cart API should contain selected dynamic product")
def verify_cart_contains_dynamic_product(context):
    selected = context["selected_dynamic_product"]
    payload = context["api_cart"]
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    assert any(item.get("name") == selected["name"] for item in items), (
        f"Selected product not found in API cart: {selected['name']}"
    )


@then(parsers.parse('latest order status should be "{expected_status}"'))
def verify_latest_order_status(context, expected_status):
    order = context["api_order"]
    assert isinstance(order, dict), f"Expected order object, got: {type(order)}"
    assert order.get("status") == expected_status


@then(parsers.parse("latest order item count should be {expected_count:d}"))
def verify_latest_order_item_count(context, expected_count):
    order = context["api_order"]
    assert isinstance(order, dict), f"Expected order object, got: {type(order)}"
    assert int(order.get("item_count", -1)) == expected_count


@then("latest order total should match recorded checkout overview total")
def verify_latest_order_total(context):
    order = context["api_order"]
    assert isinstance(order, dict), f"Expected order object, got: {type(order)}"
    api_total = float(order.get("total", -1))
    ui_total = float(context["ui_checkout_total"])
    assert round(api_total, 2) == round(ui_total, 2), f"Order total mismatch: api={api_total} ui={ui_total}"
