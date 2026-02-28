from pytest_bdd import scenario


@scenario("../features/login.feature", "Successful login")
def test_successful_login():
    pass


@scenario("../features/login.feature", "Login with empty username and password")
def test_login_empty_username_password():
    pass


@scenario("../features/login.feature", "Login with locked out user")
def test_login_locked_out_user():
    pass


@scenario("../features/login.feature", "Invalid username and password")
def test_invalid_username_password():
    pass
