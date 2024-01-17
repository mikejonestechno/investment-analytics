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
    When today is Feb 1
    Then last_publish date is Dec 31
    When today is Jan 30
    Then last_publish date is Nov 31