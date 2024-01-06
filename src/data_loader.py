import os
import datetime
import pandas as pd
import urllib.request

def load_data(csv_url, local_file, max_age_days):
    max_age = datetime.timedelta(days=max_age_days)
    if os.path.exists(local_file) and today - datetime.datetime.fromtimestamp(os.path.getmtime(local_file)) <= max_age:
        print('Using local file')
    else:
        print('Downloading file')
        urllib.request.urlretrieve(csv_url, local_file)
    df = pd.read_csv(local_file, encoding='cp1252')
    return df