Feature: Load data

  Scenario: Download a new file
    Given the local file does not exist
    When I call load_data
    Then a new file is downloaded

  Scenario: Use existing file
    Given the local file does exist
    When I call load_data
    Then a new file is not downloaded

  Scenario: Publish date is last day of month after quarter end
    When today is 2 Feb 2024
    Then last_publish date is 1 Feb 2024
    When today is 30 Jan 2024
    Then last_publish date is 1 Nov 2023