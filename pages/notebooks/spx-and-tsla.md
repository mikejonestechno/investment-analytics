---
layout: page
title: spx-and-tsla
permalink: /spx-and-tsla
---

```python
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
start_date = pd.to_datetime('2011-01-01')
end_date = pd.to_datetime('2025-01-01')
```

# SPX 500

```python
# S&P 500 SPX monthly index from 1959
#csv_file = 'https://finance.yahoo.com/quote/%5EGSPC/history?period1=1262304000&period2=1702771200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
# extracted table to html file
html_file = '../data/temp.html'
local_file = '../data/spx_HistoricalData2010.csv'
#max_age = datetime.timedelta(days=7)
#if not os.path.exists(local_file) or datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(local_file)) > max_age:
#    import urllib.request
#    urllib.request.urlretrieve(csv_file, local_file)
#dfSpx = pd.read_csv(local_file, encoding='cp1252')    
dfSpx = pd.read_html(html_file, encoding='cp1252')[0] 
dfSpx.to_csv(local_file, index=False)
dfSpx = dfSpx.drop(dfSpx.index[-1]) # drop the last row of disclaimers
```

```python
dfSpx.rename(columns={'Adj Close**': 'Price'}, inplace=True)
dfSpx['Price'] = pd.to_numeric(dfSpx['Price'], errors='coerce')
dfSpx['Date'] = pd.to_datetime(dfSpx['Date'], format='%b %d, %Y')
dfSpx.set_index('Date', inplace=True)
dfSpx.sort_values(by='Date', ascending=True, inplace=True)
dfSpx.head()
```



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close*</th>
      <th>Price</th>
      <th>Volume</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-01-04</th>
      <td>1116.56</td>
      <td>1133.87</td>
      <td>1116.56</td>
      <td>1132.99</td>
      <td>1132.99</td>
      <td>3991400000</td>
    </tr>
    <tr>
      <th>2010-01-05</th>
      <td>1132.66</td>
      <td>1136.63</td>
      <td>1129.66</td>
      <td>1136.52</td>
      <td>1136.52</td>
      <td>2491020000</td>
    </tr>
    <tr>
      <th>2010-01-06</th>
      <td>1135.71</td>
      <td>1139.19</td>
      <td>1133.95</td>
      <td>1137.14</td>
      <td>1137.14</td>
      <td>4972660000</td>
    </tr>
    <tr>
      <th>2010-01-07</th>
      <td>1136.27</td>
      <td>1142.46</td>
      <td>1131.32</td>
      <td>1141.69</td>
      <td>1141.69</td>
      <td>5270680000</td>
    </tr>
    <tr>
      <th>2010-01-08</th>
      <td>1140.52</td>
      <td>1145.39</td>
      <td>1136.22</td>
      <td>1144.98</td>
      <td>1144.98</td>
      <td>4389590000</td>
    </tr>
  </tbody>
</table>
</div>


```python
dfSpx['YoY Change'] = dfSpx['Price'].pct_change(periods=252) *100
dfSpx['3 Yr Rolling Avg'] = dfSpx['YoY Change'].rolling(window=(252*3), min_periods=1).mean()
dfSpx = dfSpx.loc[dfSpx.index >= start_date]
dfSpx.tail()
```



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close*</th>
      <th>Price</th>
      <th>Volume</th>
      <th>YoY Change</th>
      <th>3 Yr Rolling Avg</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-12-11</th>
      <td>4593.39</td>
      <td>4623.71</td>
      <td>4593.39</td>
      <td>4622.44</td>
      <td>4622.44</td>
      <td>3823210000</td>
      <td>16.624911</td>
      <td>11.804009</td>
    </tr>
    <tr>
      <th>2023-12-12</th>
      <td>4618.30</td>
      <td>4643.93</td>
      <td>4608.09</td>
      <td>4643.70</td>
      <td>4643.70</td>
      <td>3808380000</td>
      <td>18.028762</td>
      <td>11.805042</td>
    </tr>
    <tr>
      <th>2023-12-13</th>
      <td>4646.20</td>
      <td>4709.69</td>
      <td>4643.23</td>
      <td>4707.09</td>
      <td>4707.09</td>
      <td>5063650000</td>
      <td>17.955625</td>
      <td>11.806626</td>
    </tr>
    <tr>
      <th>2023-12-14</th>
      <td>4721.04</td>
      <td>4738.57</td>
      <td>4694.34</td>
      <td>4719.55</td>
      <td>4719.55</td>
      <td>6314040000</td>
      <td>17.411964</td>
      <td>11.808998</td>
    </tr>
    <tr>
      <th>2023-12-15</th>
      <td>4714.23</td>
      <td>4725.53</td>
      <td>4704.69</td>
      <td>4719.19</td>
      <td>4719.19</td>
      <td>8218980000</td>
      <td>18.117948</td>
      <td>11.812982</td>
    </tr>
  </tbody>
</table>
</div>


# TSLA

```python
# Daily TSLA index for 10 years from 2013
# https://www.nasdaq.com/market-activity/index/tsla/historical  < NO! DOES NOT INC SPLIT ADJUSTED CLOSE! USE YAHOO!
# https://finance.yahoo.com/quote/TSLA/history?period1=1277769600&period2=1701907200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true
# Select max date range and download csv file
csv_file = '../data/tsla_HistoricalData.csv'
dfTsla = pd.read_csv(csv_file, encoding='cp1252', usecols=['Date', 'Adj Close'])

```

```python
#dfTsla.rename(columns={'Price': 'Pre-split Price'}, inplace=True)
dfTsla.rename(columns={'Adj Close': 'Price'}, inplace=True)
dfTsla['Date'] = pd.to_datetime(dfTsla['Date'])
dfTsla.set_index('Date', inplace=True)
dfTsla.sort_values(by='Date', ascending=True, inplace=True)
dfTsla.head()
```



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Price</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2010-06-29</th>
      <td>1.592667</td>
    </tr>
    <tr>
      <th>2010-06-30</th>
      <td>1.588667</td>
    </tr>
    <tr>
      <th>2010-07-01</th>
      <td>1.464000</td>
    </tr>
    <tr>
      <th>2010-07-02</th>
      <td>1.280000</td>
    </tr>
    <tr>
      <th>2010-07-06</th>
      <td>1.074000</td>
    </tr>
  </tbody>
</table>
</div>


```python
# weekly change Year over Year
dfTsla['YoY Change'] = dfTsla['Price'].pct_change(periods=252) * 100
dfTsla['3 Yr Rolling Avg'] = dfTsla['YoY Change'].rolling(window=(252*3)).mean()
dfTsla = dfTsla.loc[dfTsla.index >= start_date]
dfTsla.head()
```



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Price</th>
      <th>YoY Change</th>
      <th>3 Yr Rolling Avg</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-01-03</th>
      <td>1.774667</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-01-04</th>
      <td>1.778000</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-01-05</th>
      <td>1.788667</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-01-06</th>
      <td>1.858667</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2011-01-07</th>
      <td>1.882667</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>


```python
plt.figure(figsize=(10, 6))
colors = list(plt.rcParams['axes.prop_cycle'])
plt.plot(dfTsla.index, dfTsla['YoY Change'], label='TSLA YOY', color=colors[1]['color'], alpha=0.1)
plt.plot(dfTsla.index, dfTsla['3 Yr Rolling Avg'], label='TSLA 3 Yr Rolling Average', color=colors[1]['color'])
plt.plot(dfSpx.index, dfSpx['YoY Change'], label='SPX YOY', color=colors[0]['color'], alpha=0.1)
plt.plot(dfSpx.index, dfSpx['3 Yr Rolling Avg'], label='SPX 3 Yr Rolling Average', color=colors[0]['color'])
plt.xlabel('Date')
plt.ylabel('Annual % Change')
plt.suptitle('www.nasdaq.com/market-activity')
plt.title('YoY Annual Price Change (excludes dividend yield and inflation)')
plt.grid(True)
plt.yticks(range(-100, 1000, 100))
plt.ylim(bottom=-100, top=1000)
plt.xlim(left=start_date, right=end_date)
#plt.axhline(y=0, color='darkred')  # Add horizontal line at y=0
legend = plt.legend(loc='best')
legend.get_frame().set_facecolor('white')
legend.get_frame().set_alpha(0.98)
plt.show()
```

![png]({{ site.baseurl }}/_pages/images/spx-and-tsla_9_0.png){: .center-image }
