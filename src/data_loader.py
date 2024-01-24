import os
import datetime
import pandas as pd
import urllib.request

from yfinance import download

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

def get_quarter_publish_date(quarter):
    """
    This function returns the publish date of a given quarter.
    The publish date is defined as the last day of the next month after the end of the quarter.

    Parameters:
    - quarter (pd.Period): The quarter for which to calculate the publish date.

    Returns:
    - pd.Timestamp: The publish date of the given quarter.
    """
    publish_date = quarter.start_time + pd.offsets.MonthEnd(1)
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
    current_quarter = pd.Period(date, freq='Q')
    publish_date = get_quarter_publish_date(current_quarter)
    if (get_quarter_publish_date(current_quarter) > date):
        #print("Data from " + str(current_quarter - 1) + " not yet published...")
        #print("Use last published data from " + str(current_quarter - 2) )
        publish_date = get_quarter_publish_date(current_quarter - 1)
    #else:
        #print("Data from " + str(current_quarter - 1) + " has been published...")
    return publish_date
