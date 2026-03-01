Feature: Inventory and product operations
 
  Background:
    Given the user is logged in as "standard_user"

  @smoke @ui
  Scenario: Validate inventory components 
    Then the products page is displayed
    And products section title should be "Products"
    And cart icon should be visible
    And sort options should be available

  @regression @ui
  Scenario: Add and remove product from inventory page
    When the user selects a loaded product from inventory
    And the user adds selected loaded product to cart
    Then cart badge count should be 1
    When the user removes selected loaded product from inventory
    Then cart badge count should be 0

  @regression @ui
  Scenario: Open product details and navigate back
    When the user selects a loaded product from inventory
    And the user opens selected loaded product details
    Then selected loaded product details should match inventory data
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

  @regression @ui @api
  Scenario: Validate sorting with API comparison
    Given an API client for SauceDemo backend
    When the user selects sort option "Price (high to low)"
    And the user notes first and last products from current inventory view
    And the API client requests inventory sorted by "price_desc"
    Then inventory API response status should be 200
    And inventory API should be sorted by price descending
    And inventory API first and last items should match current UI inventory view

  @regression @ui
  Scenario: Sidemenu close and Logout from page
    When the user clicks sidemenu from inventory
    And the user clicks close icon
    Then the side menu should be closed
    When the user clicks logout from inventory side menu
    Then the login page should be displayed

  @regression @ui
  Scenario: Reset app state clears cart badge
    When the user selects a loaded product from inventory
    And the user adds selected loaded product to cart
    Then cart badge count should be 1
    When the user clicks reset app state from side menu
    Then cart badge count should be 0

  @regression @ui
  Scenario: Validate loaded product details from inventory to details and cart
    Then all inventory product images should be loaded
    When the user selects a loaded product from inventory
    And the user notes the current cart badge count
    And the user adds selected loaded product to cart
    Then the cart badge should increment by 1
    When the user removes selected loaded product from inventory
    Then the cart badge should decrement by 1
    When the user opens selected loaded product details
    Then selected loaded product details should match inventory data
    When the user adds selected loaded product to cart
    When the user toggles cart button on product details page
    Then cart badge count should be 1
    When the user opens the cart page
    Then selected loaded product should match cart item data
    When the user starts checkout
    And the user fills checkout information with valid details
    And the user continues checkout
    Then selected loaded product should match checkout overview item data

  @regression @ui @api
  Scenario: Validate loaded cart state between UI and API
    Given an API client for SauceDemo backend
    When the user selects a loaded product from inventory
    And the user adds selected loaded product to cart
    And the API client requests current cart
    Then cart API response status should be 200
    And cart API should contain selected loaded product
