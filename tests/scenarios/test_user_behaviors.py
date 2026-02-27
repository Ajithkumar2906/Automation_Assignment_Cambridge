from pytest_bdd import scenario


@scenario("../features/user_behaviors.feature", "performance_glitch_user login and page load")
def test_performance_glitch_user_login_and_page_load():
    pass


@scenario("../features/user_behaviors.feature", "problem_user add/remove behavior smoke check")
def test_problem_user_add_remove_behavior_smoke():
    pass


@scenario("../features/user_behaviors.feature", "visual_user basic layout smoke check")
def test_visual_user_basic_layout_smoke_check():
    pass
