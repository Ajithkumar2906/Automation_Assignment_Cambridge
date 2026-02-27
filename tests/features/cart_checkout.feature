Feature: Cart and checkout validation
  As a QA engineer
  I want to verify cart and checkout workflows
  So that users can complete purchases successfully

  Background:
    Given the user is logged in as "standard_user"

  @smoke @ui
  Scenario: Validate cart headers and item count
    When the user adds product "Sauce Labs Backpack" to cart
    And the user opens the cart page
    Then cart page title should be "Your Cart"
    And cart headers should be "QTY" and "Description"
    And cart should contain 1 items

  @regression @ui
  Scenario: Checkout info validation with empty fields then success
    When the user adds product "Sauce Labs Backpack" to cart
    And the user opens the cart page
    And the user starts checkout
    Then checkout info title should be "Checkout: Your Information"
    When the user continues checkout without entering information
    Then checkout info error should contain "First Name is required"
    When the user fills checkout information with valid details
    And the user continues checkout
    Then checkout overview title should be "Checkout: Overview"

  @smoke @ui
  Scenario: Complete checkout flow
    When the user adds product "Sauce Labs Backpack" to cart
    And the user opens the cart page
    And the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    Then checkout overview should show payment shipping and total information
    When the user finishes checkout
    Then checkout complete header should be "Thank you for your order!"
