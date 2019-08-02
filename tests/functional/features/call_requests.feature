Feature: call requests
    As a user,
    I want to make the HTTP requests provided by my API specification

    Scenario: API spec with only base_url and one request with name and method
        Given base_url is correct
        And HTTP method is GET
        Then the request should be made
