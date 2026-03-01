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
def test_sorting_all_options():
    pass


@scenario("../features/products.feature", "Sidemenu close and Logout from page")
def test_sidemenu_close_and_logout_from_page():
    pass


@scenario("../features/products.feature", "Reset app state clears cart badge")
def test_reset_clears_cart_badge():
    pass


@scenario("../features/products.feature", "Validate loaded product details from inventory to details and cart")
def test_loaded_product_details_flow():
    pass

