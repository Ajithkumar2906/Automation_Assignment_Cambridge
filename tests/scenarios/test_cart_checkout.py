from pytest_bdd import scenario


@scenario("../features/cart_checkout.feature", "Validate cart headers and item count")
def test_validate_cart_headers_and_item_count():
    pass


@scenario("../features/cart_checkout.feature", "Checkout info validation with empty fields then success")
def test_checkout_info_validation_then_success():
    pass


@scenario("../features/cart_checkout.feature", "Complete checkout flow")
def test_complete_checkout_flow():
    pass
