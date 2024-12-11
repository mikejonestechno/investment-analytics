# Python Jupyter Notebooks for Investment Retirement Data Analytics

These experimental jupyter notebooks plot inflation, interest rate and SPX 500 index to help visualize investment and retirement portfolios.

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/mikejonestechno/investment-analytics)

> If you already have VS Code and Docker installed, you can click the badge above to get started. Clicking this link will cause VS Code to automatically install the Dev Containers extension if needed, clone the source code into a container volume, and spin up a dev container for use.

[![CI](https://github.com/mikejonestechno/investment-analytics/actions/workflows/python.yaml/badge.svg)](https://github.com/mikejonestechno/investment-analytics/actions/workflows/python.yaml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mikejonestechno_investment-analytics&metric=alert_status)](https://sonarcloud.io/summary/overall?id=mikejonestechno_investment-analytics) [![Notebooks](https://github.com/mikejonestechno/investment-analytics/actions/workflows/notebooks.yml/badge.svg)](https://github.com/mikejonestechno/investment-analytics/actions/workflows/notebooks.yml) [![Deploy Pages](https://github.com/mikejonestechno/investment-analytics/actions/workflows/deploy-pages.yml/badge.svg)](https://mikejonestechno.github.io/investment-analytics/)

[GitHub Actions](https://github.com/mikejonestechno/investment-analytics/actions/workflows/python.yaml) trigger a devops CI pipeline on every PR and code quality is automatically scanned and published on [SonarCloud](https://sonarcloud.io/summary/overall?id=mikejonestechno_investment-analytics). Although SonarQube can scan python files for code quality, it does not currently support python code in Jupyter notebook files. Charts and documentation is deployed to [GitHub Pages](https://mikejonestechno.github.io/investment-analytics/).

## [Investment Analytics GitHub Pages](https://mikejonestechno.github.io/investment-analytics/)

View all the charts in this data-analytics project at 
[https://mikejonestechno.github.io/investment-analytics/](https://mikejonestechno.github.io/investment-analytics/)

### Examples

1. [Inflation and Interest Rates](https://mikejonestechno.github.io/investment-analytics/inflation-and-interest-rates.html) chart from Jupyter notebook. 

<img src="https://mikejonestechno.github.io/investment-analytics/images/inflation-and-interest-rates_7_0.png" alt="Inflation and Interest Rates" width="200"/>

2. [TSLA Prices](https://mikejonestechno.github.io/investment-analytics/tsla-and-targets.html) chart with ArkInvest four year targets from Jupyter notebook. 

<img src="https://mikejonestechno.github.io/investment-analytics/images/tsla-targets_10_0.png" alt="ArkInvest TSLA Price Targets" width="200"/>

View all the charts in this data-analytics project at 
[https://mikejonestechno.github.io/investment-analytics/](https://mikejonestechno.github.io/investment-analytics/)

### Disclaimer

Not financial advice: All content of this repository is for educational purposes only. No warranty or guarantee or forward looking statements of fit for purpose; do your own research, etc.

## Australian Index Data

The interest rates and inflation rates are obtained from [https://www.rba.gov.au/statistics/tables/](https://www.rba.gov.au/statistics/tables/).

The data for interest rates will be downloaded to `.\data\f5-data.csv`.

The data for inflation rates will be downloaded to `.\data\g1-data.csv`.

The notebooks automatically download new data after expected data publishing schedules and GitHub actions cache the data between runs.

## International Index Data

Historical prices (adjusted for splits and dividend and/or capital gain distributions) obtained from [https://finance.yahoo.com/quote/TSLA/history](https://finance.yahoo.com/quote/TSLA/history).

The data will be downloaded to `.\data\tsla_HistoricalData.csv`.