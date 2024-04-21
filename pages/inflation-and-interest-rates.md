---
layout: page
title: Inflation and Interest Rates
---

## [Inflation](inflation.html)

The Consumer Price Index that the Reserve Bank of Australia use to index inflation is published quarterly, one month after the end of each quarter.

See [inflation](inflation.html) for inflation charts, trends and analysis.

## [Interest Rates](interest-rates.html)

The Housing Loan Lending Rates are set by the Reserve Bank of Australia and published monthly within five business days after month end.

See [interest rates](interest-rates.html) for interest rate charts, trends and analysis.

## Inflation and Interest Rates

    no stored variable or alias df_interest





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
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>






    RangeIndex(start=0, stop=0, step=1)



The Reserve Bank of Australia has often increased base interest rates alledging a high correlation between interest rates and inflation.

This appears a reasonable construct from basic supply and demand economics; when households have high disposable income, demand for non-essential goods and services increases, and if supply is limited, prices increase to meet demand, resulting in inflation. 

Increasing interest rates reduces disposable income (for those with borrowing debt), thus reducing some demand for non-essential goods and services, potentially resulting in some price reductions, and subsequently reducing inflation.

Is there really a high correlation, or is this over simplification? Do lower interest rates subsequently cause inflation to rise, and higher interest rates subsequently cause inflation to reduce?

Perhaps there are other external factors influencing inflation, such as global oil prices, foreign war, pandemic supply chains, that have nothing to do with household disposable income?

""" Prepare simple chart """

chart_params = {
    'chart_title': 'AU Inflation and Housing Loan Lending Rate as at ' + last_index.strftime('%d %b %Y'), 
    'chart_source': 'Source: www.rba.gov.au/statistics/tables', 
    'y_label': 'Rate %', 
    'y_ticks': 2,
    'x_label': 'Date', 
    'x_ticks': 5,
    'start_year': 1960,
    'data_column': inflation_column
}

standard_chart = StandardChart(**chart_params)
plt, colors = standard_chart.base_chart(df_inflation)

plt.plot(df_interest.index, df_interest[interest_column], color=colors[0]['color'], label='Housing Interest Rate')
plt.plot(df_inflation.index, df_inflation[inflation_column], color=colors[1]['color'], label='CPI Inflation Rate')
legend = plt.legend(loc='best')
legend.get_frame().set_alpha(0.98)

plt.show()
