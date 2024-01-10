Feature: Load data

  Scenario: Download a new file
    Given the local file does not exist
    When I call load_data
    Then a new file is downloaded