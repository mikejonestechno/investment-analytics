import os
import datetime

import urllib.request
import hashlib

import pandas as pd

def load_data(csv_url, local_file, max_age_days, skip_rows=0):
    """
    Load data from a CSV file, refresh if older than max_age_days.
    """
    publish_date = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
    return load_csv_data(local_file, csv_url, publish_date, skip_rows)

"""
If local_file is older than specifed date, then download to latest_file.

Sometimes the data is still old e.g. downloaded early before last publish date.
So only replace the local_file if the latest_file actually has newer data.

If latest_file hash is different to local_file then replace the local_file.
"""

def load_csv_data(local_file, csv_url, publish_date, skip_rows=0):
    """
    Loads CSV data from a local file or updates it from a given URL if the file is stale.

    Args:
        local_file (str): The path to the local CSV file.
        csv_url (str): The URL of the CSV file to download if the local file is stale.
        publish_date (str): The publish date of the CSV file.

    Returns:
        pandas.DataFrame: The loaded CSV data as a pandas DataFrame.
    """
    if is_file_stale(local_file, publish_date):
        update_file(local_file, csv_url)
    return load_csv_file(local_file, skip_rows)

def load_csv_file(local_file, skip_rows=0):
    """
    Load a CSV file into a pandas DataFrame.

    Args:
    local_file (str): The path to the local CSV file.
    skip_rows (int, optional): The number of rows to skip at the beginning of the file. Default is 0.

    Returns:
    pandas.DataFrame: The loaded CSV data as a DataFrame.
    """
    return pd.read_csv(local_file, encoding='cp1252', skiprows=skip_rows)

def is_file_cache_stale(local_file):
    """
    TODO: is local_file hash different to the cached file hash.txt?
    """

def get_file_hash(local_file):
    """
    Calculate the MD5 hash of a file.

    Args:
        local_file (str): The path to the local file.

    Returns:
        str: The MD5 hash of the file.
    """
    h = hashlib.md5()
    with open(local_file, "rb") as f:
        while chunk := f.read(128*h.block_size): 
            h.update(chunk)
    return h.hexdigest()

def is_file_stale(local_file, specified_date):
    """
    Check if a file is stale based on the specified date.

    Args:
        local_file (str): The path to the local file.
        specified_date (datetime.datetime): The specified date to compare against.

    Returns:
        bool: True if the file is stale, False otherwise.
    """
    if not os.path.exists(local_file):
        return True
    if specified_date is None:
        raise ValueError('specified_date value is None')
    return os.path.getmtime(local_file) < specified_date.timestamp()

import urllib.request
import os

def update_file(local_file, csv_url):
    """
    Downloads a CSV file from the given URL and updates the local file if the content has changed.

    Args:
        local_file (str): The path to the local file.
        csv_url (str): The URL of the CSV file to download.

    Returns:
        None
    """    
    temp_file = local_file + '.tmp'
    urllib.request.urlretrieve(csv_url, temp_file) 
    if (not os.path.exists(local_file)) or (get_file_hash(temp_file) != get_file_hash(local_file)):
        os.replace(temp_file, local_file)

def get_quarter_publish_date(quarter):
    """
    This function returns the publish date of a given quarter.
    The publish date is defined as the last day of the next month after the end of the quarter.

    Args:
        quarter (pd.Period): The quarter for which to calculate the publish date.

    Returns:
        pd.Timestamp: The publish date of the given quarter.
    """
    publish_date = quarter.start_time + pd.DateOffset(months=1)
    return publish_date

def get_last_publish_date(date=None):
    """
    Get the last publish date for the given date or the current date.

    Args:
        date: Optional. The date for which to get the last publish date. If not provided, the current date is used.

    Returns:
        pd.Timestamp: The last publish date.
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