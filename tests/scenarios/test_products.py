from pytest_bdd import scenario


@scenario("../features/products.feature", "Validate inventory components and sort options")
def test_inventory_components_and_sort_options():
    pass


@scenario("../features/products.feature", "Add and remove product from inventory page")
def test_add_remove_from_inventory_page():
    pass


@scenario("../features/products.feature", "Open product details and navigate back")
def test_open_product_details_and_back():
    pass
