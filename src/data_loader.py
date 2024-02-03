import os
import datetime
import pandas as pd
import urllib.request

def load_data(csv_url, local_file, max_age_days, skip_rows=0):
    """
    Load data from a CSV file.

    Parameters:
    csv_url (str): The URL of the CSV file to download.
    local_file (str): The local file path to save the downloaded CSV file.
    max_age_days (int): The maximum age of the local file in days. If the local file is older than this, it will be re-downloaded.

    Returns:
    pandas.DataFrame: The loaded data as a pandas DataFrame.
    """
    max_age = datetime.timedelta(days=max_age_days)
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    download = False
    if os.path.exists(local_file) and today - datetime.datetime.fromtimestamp(os.path.getmtime(local_file)) <= max_age:
        download = False
        #print('Using local file')
    else:
        download = True
        #print('Downloading file')
        urllib.request.urlretrieve(csv_url, local_file)
    df = pd.read_csv(local_file, encoding='cp1252', skiprows=skip_rows)
    return df

"""
If local_file is older than specifed date, then download to latest_file.

Sometimes the data is still old e.g. downloaded early before last publish date.
So only replace the local_file if the latest_file actually has newer data.

If latest_file hash is different to local_file then replace the local_file.
"""
def is_file_cache_stale(local_file):
    """
    is local_file hash different to the cached file hash.txt?
    """

def is_file_stale(local_file, date):
    """
    is local_file older than the specified date?
    """

def update_file(local_file, csv_url):
    """
    Download the latest data to a temporary file and replace the local_file if the data is newer.
    """


def get_quarter_publish_date(quarter):
    """
    This function returns the publish date of a given quarter.
    The publish date is defined as the last day of the next month after the end of the quarter.

    Parameters:
    - quarter (pd.Period): The quarter for which to calculate the publish date.

    Returns:
    - pd.Timestamp: The publish date of the given quarter.
    """
    publish_date = quarter.start_time + pd.DateOffset(months=1)
    return publish_date

def get_last_publish_date(date=None):
    """
    Get the last publish date for the given date or the current date.

    Parameters:
    - date: Optional. The date for which to get the last publish date. If not provided, the current date is used.

    Returns:
    - pd.Timestamp: The last publish date.
    """
    if date is None:
        date = pd.Timestamp.now()
    quarter = pd.Period(date, freq='Q')
    publish_date = get_quarter_publish_date(quarter)
    if (publish_date > date):
        publish_date = get_quarter_publish_date(quarter - 1)
    return publish_date

""" 
NOTE that data may be published on the last or second last Wednesday before that month end
so I could look to get new data between the early publish date and the last publish date.
"""