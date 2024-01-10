import os
import pytest
from pytest_bdd import scenarios, given, when, then
from data_loader import load_data

# Define the scenario
scenarios('data_loader.feature')

# Define the given step
@given('the local file does not exist',target_fixture="local_file_name")
def local_file():
    local_file = 'test.csv'
    if os.path.exists(local_file):
        os.remove(local_file)
    return local_file

# Define the when step
@when('I call load_data')
def call_load_data(local_file_name):
    csv_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv'
    max_age_days = 1
    df = load_data(csv_url, local_file_name, max_age_days)
    return df

# Define the then step
@then('a new file is downloaded')
def new_file_is_downloaded(local_file_name):
    assert os.path.exists(local_file_name)