Feature: Login behavior on SauceDemo
  Background:
   Given the user opens the SauceDemo login page

  @smoke @ui
  Scenario: Successful login
    When the user logs in with username "standard_user" and password "secret_sauce"
    Then the products page is displayed
    And the app header should be "Swag Labs"
    

  @regression @ui
  Scenario: Login with empty username and password
    When the user clicks login without entering credentials
    Then login error should contain "Username is required"
    When the user closes the login error
    Then login error should not be visible
    When the user logs in with username "standard_user" and password empty
    Then login error should contain "password is required"
    When the user logs in with username empty and password "secret_sauce"
    Then login error should contain "Username is required"


  @regression @ui
  Scenario: Login with locked out user
    When the user logs in with username "locked_out_user" and password "secret_sauce"
    Then login error should contain "locked out"
    When the user closes the login error
    Then login error should not be visible

  @regression @ui
  Scenario: Invalid username and password
    When the user logs in with username "invalid_user" and password "wrong_password"
    Then login error should contain "Username and password do not match"
    When the user closes the login error
    Then login error should not be visible
