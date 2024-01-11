import os
from pytest_bdd import scenarios, given, when, then
from data_loader import load_data
from tempfile import NamedTemporaryFile
import csv

# Define the scenario
scenarios('data_loader.feature')

# Define the given step
@given('the local file does not exist', target_fixture="local_file_name")
def local_file():
    local_file = 'test.csv'
    if os.path.exists(local_file):
        os.remove(local_file)
    return local_file


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
def call_load_data(mocker, local_file_name):
    csv_url = 'https://mock.test.com/data.csv'
    max_age_days = 1

    # mock urlretrieve to intercept the download and return the CSV data stub
    mock_urlretrieve = mocker.patch('urllib.request.urlretrieve', side_effect=mock_urlretrieve_csv_data_stub)

    df = load_data(csv_url, local_file_name, max_age_days)
    yield df, mock_urlretrieve

# Define the then step
@then('a new file is downloaded')
def new_file_is_downloaded(call_load_data):
    _, mock_urlretrieve = call_load_data
    mock_urlretrieve.assert_called_once()