    Using local file





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
      <th>Change</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-12-27</th>
      <td>261.440002</td>
      <td>112.293949</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <td>253.179993</td>
      <td>132.062326</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <td>248.479996</td>
      <td>120.459585</td>
    </tr>
    <tr>
      <th>2024-01-02</th>
      <td>248.419998</td>
      <td>103.923820</td>
    </tr>
    <tr>
      <th>2024-01-03</th>
      <td>238.449997</td>
      <td>93.578501</td>
    </tr>
  </tbody>
</table>
</div>




    
![png](images/tsla-yoy_4_0.png)
    





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
      <th>Change</th>
      <th>3_yr_rolling</th>
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
      <th>2023-12-27</th>
      <td>261.440002</td>
      <td>112.293949</td>
      <td>90.177252</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <td>253.179993</td>
      <td>132.062326</td>
      <td>89.468576</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <td>248.479996</td>
      <td>120.459585</td>
      <td>88.740280</td>
    </tr>
    <tr>
      <th>2024-01-02</th>
      <td>248.419998</td>
      <td>103.923820</td>
      <td>87.947881</td>
    </tr>
    <tr>
      <th>2024-01-03</th>
      <td>238.449997</td>
      <td>93.578501</td>
      <td>87.105496</td>
    </tr>
  </tbody>
</table>
</div>




    
![png](images/tsla-yoy_6_0.png)
    


    /tmp/ipykernel_3839/2051860956.py:58: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      rolling_forecast['BearChange'] = rolling_forecast['Bear'].pct_change() * 100 # change since previous row
    /tmp/ipykernel_3839/2051860956.py:61: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      rolling_forecast['BaseChange'] = rolling_forecast['Base'].pct_change() * 100 # change since previous row


    InvestA uses mediumseagreen
    RandyKirk uses olivedrab
    SMR uses green



    
![png](images/tsla-yoy_11_2.png)
    

