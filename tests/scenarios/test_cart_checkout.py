from pytest_bdd import scenario


@scenario("../features/cart_checkout.feature", "Validate cart headers and item count")
def test_validate_cart_headers_and_item_count():
    pass


@scenario("../features/cart_checkout.feature", "Checkout info validation with empty fields then cancel")
def test_checkout_info_validation_then_cancel():
    pass


@scenario("../features/cart_checkout.feature", "Checkout overview payment shipping and totals validation")
def test_checkout_overview_payment_shipping_and_totals_validation():
    pass
