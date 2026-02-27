Feature: API and page availability checks
  As a QA engineer
  I want lightweight API validation
  So that test failures can be triaged faster

  @api
  Scenario: Login page is reachable
    Given an API client for SauceDemo
    When the API client requests the login page
    Then the login page response status should be 200
    And the response body should contain "Swag Labs"
