Feature: Login behavior on SauceDemo
  As a QA engineer
  I want to validate authentication flows
  So that login behavior is reliable for all supported users

  @smoke @ui
  Scenario: Successful login with standard user
    Given the user opens the SauceDemo login page
    When the user logs in with username "standard_user" and password "secret_sauce"
    Then the products page is displayed
    And the app header should be "Swag Labs"

  @regression @ui
  Scenario: Login with empty username and password
    Given the user opens the SauceDemo login page
    When the user clicks login without entering credentials
    Then login error should contain "Username is required"
    When the user closes the login error
    Then login error should not be visible

  @regression @ui
  Scenario: Login with locked out user
    Given the user opens the SauceDemo login page
    When the user logs in with username "locked_out_user" and password "secret_sauce"
    Then login error should contain "locked out"

  @regression @ui
  Scenario: Invalid username and password
    Given the user opens the SauceDemo login page
    When the user logs in with username "invalid_user" and password "wrong_password"
    Then login error should contain "Username and password do not match"
