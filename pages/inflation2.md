---
layout: page
title: Inflation
---

    /tmp/ipykernel_2149/1253525750.py:4: DeprecationWarning: 
    Pyarrow will become a required dependency of pandas in the next major release of pandas (pandas 3.0),
    (to allow more performant data types, such as the Arrow string type, and better interoperability with other libraries)
    but was not found to be installed on your system.
    If this would cause problems for you,
    please provide us feedback at https://github.com/pandas-dev/pandas/issues/54466
            
      import pandas as pd


    publish_date: 2023-10-31 00:00:00 was 85 days ago.


The Consumer Price Index that the Reserve Bank of Australia use to index inflation rocketed through the roof in the 1970s peaking at 18% in 1975. 

Inflation stablized through the late 1990s, trending slightly down until the sharp rise in 2021.


    
![png](images/inflation2_6_0.png)
    


Calculating the 25th and 75th percentile over multi-year time horizon helps visualize long term trends.



Over the last 10 years the median change is 1.9%:
- 25th percentile YoY change is 1.5%
- 50th percentile YoY change is 1.9%
- 75th percentile YoY change is 3.0%

Over the last 30 years:
- 25th percentile YoY change is 1.7%
- 50th percentile YoY change is 2.4%
- 75th percentile YoY change is 3.12%



The chart shows inflation stayed close to the RBA target inflation rate of 2 to 3 percent for over twenty five years.

> ℹ The data suggests reasonable confidence using a baseline inflation of 2% to 2.5% with some uncertainty or risk that inflation could peak higher.


    
![png](images/inflation2_10_0.png)
    


    Stored 'df_inflation' (DataFrame)


    /opt/hostedtoolcache/Python/3.11.7/x64/lib/python3.11/site-packages/IPython/extensions/storemagic.py:229: UserWarning: using autorestore/df_inflation requires you to install the `pickleshare` library.
      db[ 'autorestore/' + arg ] = obj

