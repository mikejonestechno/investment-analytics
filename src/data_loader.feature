Feature: Load data

  Scenario: Download a new file
    Given the local file does not exist
    When I call load_data
    Then a new file is downloaded

  Scenario: Use existing file
    Given the local file does exist
    When I call load_data
    Then a new file is not downloaded    