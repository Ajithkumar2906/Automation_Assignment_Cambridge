Feature: Cart and checkout validation

  Background:
    Given the user is logged in as "standard_user"

  @smoke @ui
  Scenario: Validate cart headers and item count
    When the user selects a loaded product from inventory
    And the user adds selected loaded product to cart
    And the user opens the cart page
    Then cart page title should be "Your Cart"
    And cart headers should be "QTY" and "Description"
    And cart should contain 1 items

  @regression @ui
  Scenario: Checkout info validation with empty fields then cancel
    When the user starts checkout
    Then checkout info title should be "Checkout: Your Information"
    When the user continues checkout without entering first name
    Then checkout info error should contain "First Name is required"
    When the user fills first name and continues checkout without entering last name
    Then checkout info error should contain "Last Name is required"
    When the user fills first name, last name and continues checkout without entering postal code
    Then checkout info error should contain "Postal code is required"
    When the user cancels checkout without continue
    Then cart page should be displayed
    When the user clicks continue shopping from cart page
    Then the products page is displayed

  @regression @ui
  Scenario: Checkout overview payment shipping and totals validation
    When the user selects a loaded product from inventory
    And the user adds selected loaded product to cart
    And the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    Then checkout overview title should be "Checkout: Overview"
    And checkout overview should show payment shipping and total information
    And checkout overview financial totals should be correct
    When the user clicks cancel from the overview page
    Then the products page is displayed
