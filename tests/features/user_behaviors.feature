Feature: Special user behavior checks
  As a QA engineer
  I want to validate known persona-specific behavior
  So that defects are reproducible and documented

  @regression @ui
  Scenario: performance_glitch_user login and page load
    Given the user opens the SauceDemo login page
    When the user logs in with username "performance_glitch_user" and password "secret_sauce"
    Then the products page is displayed

  @regression @ui
  Scenario: problem_user add/remove behavior smoke check
    Given the user is logged in as "problem_user"
    When the user adds product "Sauce Labs Backpack" to cart
    Then cart badge count should be 1

  @regression @ui
  Scenario: visual_user basic layout smoke check
    Given the user is logged in as "visual_user"
    Then sort options should be available
