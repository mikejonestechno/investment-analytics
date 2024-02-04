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
    When today is 31 Jan 2024
    Then last_publish date is 1 Nov 2023

  Scenario: File does not exist 
    Given the local file does not exist
    Then is_file_stale returns True

  Scenario: Existing file is stale
    Given the local file does exist
    And local file is older than given date
    Then is_file_stale returns True

  Scenario: Existing file is not stale
    Given the local file does exist
    And local file is newer than given date
    Then is_file_stale returns False
