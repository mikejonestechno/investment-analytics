from collections import namedtuple
from IPython.display import display, Markdown
import pandas as pd

class Percentiles:
    def __init__(self, 
                df,
                data_column = '', 
                periods_per_year = 12,
                multi_years = [1, 5, 10, 20, 30]             
                 ):
        self.data_column = data_column
        self.periods_per_year = periods_per_year
        self.multi_years = multi_years

        # Define the percentiles
        percentiles_tuple = namedtuple('Percentiles', ['lower', 'median', 'upper'])
        self.percentiles = percentiles_tuple(25, 50, 75)

        # Generate the window_periods array using a for loop
        self.window_periods = [self.periods_per_year * years for years in self.multi_years]

    # rolling window centered on current period - for charting
    def add_percentiles(self, df, column, window, prefix, center=False):
        """Calculate and add percentiles to the DataFrame for a given window size."""
        for percentile_name, percentile in zip(self.percentiles._fields, self.percentiles):
            df[f'{prefix}_{percentile_name}'] = df[column].rolling(window=window, min_periods=1, center=center).quantile(percentile/100)
        return df

    def calculate_percentiles(self, df):
        """ Calculate median 50th and lower, upper percentiles over multiple years """
        for window in self.window_periods:
            years = window // self.periods_per_year
            name = f'rolling_{years}_years'
            df = self.add_percentiles(df, self.data_column, window, name)
        return df
    
    def calculate_last_percentiles(self, df):
        """ Calculate the rolling percentiles for the last row in the DataFrame.
            Values do not need to be calculated for each row in DataFrame.
        """
        df_summary_percentiles = pd.DataFrame()
        for years in self.multi_years:
            rows = years * self.periods_per_year
            df_tail = df.tail(rows)
            data = {}
            for percentile in  self.percentiles:
                data[percentile] = df_tail[self.data_column].quantile(percentile/100)
            data['mean'] = df_tail[self.data_column].mean()
            df_temp = pd.DataFrame(data, index=[years])
            df_summary_percentiles = pd.concat([df_summary_percentiles, df_temp])
        df_summary_percentiles.index.name = 'Years'
        return df_summary_percentiles

    # calculate last means 
    def calculate_last_means(self, df):
        """ Calculate the rolling means for the last row in the DataFrame."""
        df_last_means = pd.DataFrame()
        for years in self.multi_years:
            rows = years * self.periods_per_year
            df_tail = df.tail(rows)
            data = {}
            data['mean'] = df_tail[self.data_column].mean()
            df_temp = pd.DataFrame(data, index=[years])
            df_last_means = pd.concat([df_last_means, df_temp])
        df_last_means.index.name = 'years'
        return df_last_means

    def calculate_last_cagr(self, df, data_column=None):
        """ Calculate the CAGR for the last periods in the DataFrame."""
        if data_column is None:
            data_column = self.data_column
        df_last_cagr = pd.DataFrame()
        last_date = df.index[-1]
        for years in self.multi_years:
            start_date = last_date - pd.DateOffset(years=years)
            idx = df.index.get_indexer([start_date], method='nearest')[0]
            if idx == -1:
                continue
            start_date_actual = df.index[idx]
            start_value = df.loc[start_date_actual, data_column]
            end_value = df.loc[last_date, data_column]
            if start_value == 0 or pd.isna(start_value) or pd.isna(end_value):
                cagr = float('nan')
                cumulative_return = float('nan')
            else:
                cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
                cumulative_return = (end_value - start_value) / start_value * 100
            data = {'cumulative return': cumulative_return, 'CAGR': cagr}
            df_temp = pd.DataFrame(data, index=[years])
            df_last_cagr = pd.concat([df_last_cagr, df_temp])
        df_last_cagr.index.name = 'years'
        return df_last_cagr

    def display_dataframe_table(self, df):
        # all columns have numeric label, rename them to a string in format 'xxth percentile'
        df_display = df.copy()
        rename_columns = [f'{percentile}th Percentile' for percentile in self.percentiles]
        additional_cols = df_display.columns[len(rename_columns):]
        # capitalize first letter of each word in the column name (but do not change acronyms)
        additional_cols = [col.title() if col.upper() != col else col for col in additional_cols]
        rename_columns += list(additional_cols)
        df_display.columns = rename_columns
        df_display = df_display.reset_index()
        format_dict = {'Years': '{0:,.0f}'}
        format_dict.update({col: '{0:,.2f}%' for col in df_display.columns if col != 'Years'})
        df_display = df_display.style.hide(axis="index").format(format_dict)
        display(df_display)


    """
    Markdown must not have indented whitespace. Indented markdown is rendered as code monospace font.
    """
    def display_percentile_intro(self):
        display(Markdown(f"""
Calculating the {self.percentiles[0]}th and {self.percentiles[2]}th percentile over a multi year time horizon helps smooth out the anomolies and visualize the {self.percentiles._fields[0]} and {self.percentiles._fields[2]} long term trends.
    """))
    def display_percentile_summary(self, df, metric_name='change'):
        display(Markdown(f"""
Over the last {self.multi_years[1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[1], self.percentiles[1]]) }%; The mean (average) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[1], 'mean']) }%.

Over the last {self.multi_years[-1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[-1], self.percentiles[1]]) }%; The mean (average) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[-1], 'mean']) }%.
    """))
    def display_cagr_summary(self, df, metric_name='CAGR'):
        display(Markdown(f"""
Over the last {self.multi_years[1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percentile) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[1], self.percentiles[1]]) }%; The Compound Annual Growth Rate CAGR is { "{:,.2f}".format(df.loc[self.multi_years[1], 'CAGR']) }%.

Over the last {self.multi_years[-1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percentile) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[-1], self.percentiles[1]]) }%; The Compound Annual Growth Rate CAGR is { "{:,.2f}".format(df.loc[self.multi_years[-1], 'CAGR']) }%.
    """))

    def display_summary(self, df, data_column):
        df_summary_percentiles = self.calculate_last_percentiles(df)
        df_last_cagr = self.calculate_last_cagr(df, data_column)
        df_summary_percentiles = df_summary_percentiles.join(df_last_cagr)
        df_summary_percentiles = df_summary_percentiles.drop(columns=['mean'])
        self.display_cagr_summary(df_summary_percentiles, 'YoY change')
        self.display_dataframe_table(df_summary_percentiles)
        return df_summary_percentiles