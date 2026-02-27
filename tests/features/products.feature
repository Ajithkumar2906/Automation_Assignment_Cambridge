Feature: Inventory and product operations
  As a QA engineer
  I want to validate products page elements and interactions
  So that core shopping functionality is robust

  Background:
    Given the user is logged in as "standard_user"

  @smoke @ui
  Scenario: Validate inventory components and sort options
    Then the products page is displayed
    And products section title should be "Products"
    And cart icon should be visible
    And sort options should be available

  @regression @ui
  Scenario: Add and remove product from inventory page
    When the user adds product "Sauce Labs Backpack" to cart
    Then cart badge count should be 1
    When the user removes product "Sauce Labs Backpack" from cart
    Then cart badge count should be 0

  @regression @ui
  Scenario: Open product details and navigate back
    When the user opens product details for "Sauce Labs Bike Light"
    Then product details page should display valid information
    When the user toggles cart button on product details page
    Then cart badge count should be 1
    When the user returns to products page
    Then the products page is displayed
