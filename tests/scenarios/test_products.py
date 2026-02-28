from pytest_bdd import scenario


@scenario("../features/products.feature", "Validate inventory components")
def test_inventory_components():
    pass


@scenario("../features/products.feature", "Add and remove product from inventory page")
def test_add_remove_from_inventory_page():
    pass


@scenario("../features/products.feature", "Open product details and navigate back")
def test_open_product_details_and_back():
    pass


@scenario("../features/products.feature", "Validate product sorting for all 4 options")
def test_validate_product_sorting_for_all_4_options():
    pass


@scenario("../features/products.feature", "Reset app state clears cart badge")
def test_reset_app_state_clears_cart_badge():
    pass


@scenario("../features/products.feature", "Validate dynamic product details from inventory to details and cart")
def test_validate_dynamic_product_details_from_inventory_to_details_and_cart():
    pass

