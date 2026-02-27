Feature: End-to-end shopping journey
  As a customer
  I want to purchase products end to end
  So that checkout can be completed without errors

  @smoke @ui
  Scenario: Full e2e flow with two products
    Given the user is logged in as "standard_user"
    When the user adds product "Sauce Labs Backpack" to cart
    And the user adds product "Sauce Labs Bolt T-Shirt" to cart
    Then cart badge count should be 2
    When the user opens the cart page
    Then cart should contain 2 items
    When the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    And the user finishes checkout
    Then checkout complete header should be "Thank you for your order!"
    When the user clicks back home on complete page
    Then the products page is displayed
