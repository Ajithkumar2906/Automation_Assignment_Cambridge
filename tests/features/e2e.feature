Feature: End-to-end shopping journey

  @smoke @e2e @ui
  Scenario: Full e2e flow with two products
    Given the user is logged in as "standard_user"
    When the user selects two distinct loaded products from inventory
    And the user adds the first selected loaded product to cart
    And the user adds the second selected loaded product to cart
    Then cart badge count should be 2
    When the user opens the cart page
    Then cart should contain 2 items
    And both selected loaded products should be present in cart
    When the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    Then checkout overview should show payment shipping and total information
    And checkout overview financial totals should be correct
    When the user records checkout overview total amount
    And the user finishes checkout
    Then checkout complete header should be "Thank you for your order!"
    When the user clicks back home on complete page
    Then the products page is displayed
