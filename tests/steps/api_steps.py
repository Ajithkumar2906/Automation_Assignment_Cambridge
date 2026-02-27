"""BDD step definitions for API validation scenarios."""

from __future__ import annotations

from pytest_bdd import given, then, when

from framework.api.sauce_api import SauceApiClient


@given("an API client for SauceDemo")
def api_client(context):
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
