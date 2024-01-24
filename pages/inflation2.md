---
layout: page
title: Inflation
---

    Data from 2023Q4 not yet published...
    Use last published data from 2023Q3
    publish_date: 2023-10-31 00:00:00 was 84 days ago.
    Using local file


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


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[1], line 2
          1 # Rolling average chart
    ----> 2 plt.figure(figsize=(10, 6))
          3 plt.plot(df_inflation.index, df_inflation['GCPIAGYP'], label='Annual CPI Rate', color=colors[1]['color'], alpha=0.1)
          4 quantile_label = str(int(quantile_lower*100)) + 'th and ' + str(int(quantile_upper*100)) + 'th Percentiles'


    NameError: name 'plt' is not defined


    Stored 'df_inflation' (DataFrame)

