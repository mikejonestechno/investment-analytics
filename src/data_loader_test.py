import datetime
import csv
from pandas import Timestamp

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from data_loader import get_csv_by_age, get_last_publish_date, is_file_stale


# Define the scenario
scenarios('data_loader.feature')

@pytest.fixture
def publish_date():
    return None

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


def mock_urlretrieve_csv_data_stub(filename, url, *args, **kwargs):
    # Create file with CSV data stub
    with open(filename, mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'price'])
        writer.writerow(['2024-01-01', '140'])
        writer.writerow(['2024-01-02', '150'])
    return (filename, None)

# Define the when step
@when('I call get_csv_by_age', target_fixture="call_get_csv_by_age")
def call_get_csv_by_age(mocker, local_file_path):
    csv_url = 'https://mock.test.com/data.csv'
    max_age_days = 1

    # mock urlretrieve to intercept the download and return the CSV data stub
    mock_urlretrieve = mocker.patch('urllib.request.urlretrieve', side_effect=lambda url, filename, *args, **kwargs: mock_urlretrieve_csv_data_stub(filename, url, *args, **kwargs))

    df = get_csv_by_age(local_file_path, csv_url, max_age_days)
    yield df, mock_urlretrieve

# Define the then step
@then('a new file is downloaded')
def new_file_is_downloaded(call_get_csv_by_age):
    # call_get_csv_by_age yeilds the dataframe and the mock_urlretrieve object, ignore df object using '_'
    _, mock_urlretrieve = call_get_csv_by_age
    mock_urlretrieve.assert_called_once()

@then('a new file is not downloaded')
def new_file_is_not_downloaded(call_get_csv_by_age):
    # call_get_csv_by_age yeilds the dataframe and the mock_urlretrieve object, ignore df object using '_'
    _, mock_urlretrieve = call_get_csv_by_age
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

@then(parsers.parse('is_file_stale returns {expected}'))
def is_file_stale_returns_expected(expected, local_file_path, publish_date):
    expected = expected == 'True'
    assert is_file_stale(local_file_path, publish_date) == expected


@given(parsers.parse('local file is {older} than given date'), target_fixture="publish_date")
def local_file_is_older_than_given_date(older):
    older = older == 'older'
    if older: # the file will be older than this date
        publish_date = datetime.datetime(2040, 1, 1)
    else: # the file will be newer than this date
        publish_date = datetime.datetime(2020, 1, 1)
    return publish_date
