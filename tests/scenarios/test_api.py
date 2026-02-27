from pytest_bdd import scenario


@scenario("../features/api.feature", "Login page is reachable")
def test_login_page_is_reachable():
    pass
