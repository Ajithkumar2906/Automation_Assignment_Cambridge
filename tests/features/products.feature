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

  @regression @ui
  Scenario: Validate product sorting for all 4 options
    When the user selects sort option "Name (A to Z)"
    Then products should be sorted by name ascending
    When the user selects sort option "Name (Z to A)"
    Then products should be sorted by name descending
    When the user selects sort option "Price (low to high)"
    Then products should be sorted by price ascending
    When the user selects sort option "Price (high to low)"
    Then products should be sorted by price descending

  @regression @ui
  Scenario: Reset app state clears cart badge
    When the user adds product "Sauce Labs Backpack" to cart
    Then cart badge count should be 1
    When the user clicks reset app state from side menu
    Then cart badge count should be 0

  @regression @ui
  Scenario: Validate dynamic product details from inventory to details and cart
    When the user selects a dynamic product from inventory
    And the user opens selected dynamic product details
    Then selected dynamic product details should match inventory data
    When the user toggles cart button on product details page
    Then cart badge count should be 1
    When the user opens the cart page
    Then selected dynamic product should match cart item data

  @regression @ui
  Scenario: Validate dynamic product consistency in checkout overview
    When the user selects a dynamic product from inventory
    And the user adds selected dynamic product to cart
    And the user opens the cart page
    And the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    Then selected dynamic product should match checkout overview item data

  @regression @ui
  Scenario: Validate all product images are loaded
    Then all inventory product images should be loaded

  @regression @ui
  Scenario: Validate cart badge increment and decrement for dynamic product
    When the user selects a dynamic product from inventory
    And the user notes the current cart badge count
    And the user adds selected dynamic product to cart
    Then the cart badge should increment by 1
    When the user removes selected dynamic product from inventory
    Then the cart badge should decrement by 1
