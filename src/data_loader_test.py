from math import exp
import os
import datetime
from pandas import Timestamp
from pytest_bdd import scenarios, given, when, then, parsers
from data_loader import load_data, get_last_publish_date
from tempfile import NamedTemporaryFile
import csv

# Define the scenario
scenarios('data_loader.feature')

# Define the given step
@given('the local file does not exist', target_fixture="local_file_path")
def local_file_path(tmp_path):
    # pytest tmp_path is unique for each test run, file guranteed to not exist
    temp_file = tmp_path / "pytest.csv"
    return str(temp_file)

# Define the given step
@given('the local file does exist', target_fixture="local_file_path")
def local_file(tmp_path):
    # create a CSV data stub
    csv_file = local_file_path(tmp_path)
    mock_urlretrieve_csv_data_stub('', csv_file)
    return csv_file


def mock_urlretrieve_csv_data_stub(url, filename, *args, **kwargs):
    # Create file with CSV data stub
    with open(filename, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'price'])
        writer.writerow(['2024-01-01', '140'])
        writer.writerow(['2024-01-02', '150'])
    return (filename, None)

# Define the when step
@when('I call load_data', target_fixture="call_load_data")
def call_load_data(mocker, local_file_path):
    csv_url = 'https://mock.test.com/data.csv'
    max_age_days = 1

    # mock urlretrieve to intercept the download and return the CSV data stub
    mock_urlretrieve = mocker.patch('urllib.request.urlretrieve', side_effect=mock_urlretrieve_csv_data_stub)

    df = load_data(csv_url, local_file_path, max_age_days)
    yield df, mock_urlretrieve

# Define the then step
@then('a new file is downloaded')
def new_file_is_downloaded(call_load_data):
    # call_load_data yeilds the dataframe and the mock_urlretrieve object, ignore df object using '_'
    _, mock_urlretrieve = call_load_data
    mock_urlretrieve.assert_called_once()

@then('a new file is not downloaded')
def new_file_is_not_downloaded(call_load_data):
    # call_load_data yeilds the dataframe and the mock_urlretrieve object, ignore df object using '_'
    _, mock_urlretrieve = call_load_data
    mock_urlretrieve.assert_not_called()

@when(parsers.re('today is (?P<date>.+)'), target_fixture="today")
def today_is(date):
    today = datetime.datetime.strptime(date, '%d %b %Y')
    return today

@then(parsers.re('last_publish date is (?P<expected_date>.+)'))
def last_publish_date_is(expected_date, today):
    publish_date = get_last_publish_date(today)
    expected_publish_date = Timestamp(expected_date)
    assert publish_date == expected_publish_date