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
    def add_percentiles(self, df, column, window, prefix):
        """Calculate and add percentiles to the DataFrame for a given window size."""
        for percentile_name, percentile in zip(self.percentiles._fields, self.percentiles):
            df[f'{prefix}_{percentile_name}'] = df[column].rolling(window=window, min_periods=1, center=True).quantile(percentile/100)
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
        df_last_percentiles = pd.DataFrame()
        for years in self.multi_years:
            rows = years * self.periods_per_year
            df_tail = df.tail(rows)
            data = {}
            for percentile in  self.percentiles:
                data[f"{percentile}th percentile"] = df_tail[self.data_column].quantile(percentile/100)
            df_temp = pd.DataFrame(data, index=[years])
            df_last_percentiles = pd.concat([df_last_percentiles, df_temp])
        df_last_percentiles.index.name = 'Years'
        return df_last_percentiles

# Write table to file
#
#   with open('../data/inflation_percentiles.md', 'w') as f:
#       f.write(table)
#       f.close()

    def display_dataframe_table(self, df):
        df.style.format(precision=2)
        df.tail(10)
        markdown_table = df.to_markdown()
        display(Markdown(markdown_table))


    """
    Markdown must not have indented whitespace. Indented markdown is rendered as code monospace font.
    """
    def display_percentile_intro(self):
        display(Markdown(f"""
Calculating the {self.percentiles[0]}th and {self.percentiles[2]}th percentile over a multi year time horizon helps smooth out the anomolies and visualize the {self.percentiles._fields[0]} and {self.percentiles._fields[2]} long term trends.
    """))
    def display_percentile_summary(self, df, metric_name='change'):
        display(Markdown(f"""
Over the last {self.multi_years[1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { df.loc[self.multi_years[1], f"{self.percentiles[1]}th percentile"] }%.

Over the last {self.multi_years[-1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { df.loc[self.multi_years[-1], f"{self.percentiles[1]}th percentile"] }%.
    """))
        
"""Over the last {self.multi_years[-1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { "{:,.2f}".format(df.loc[self.multi_years[-1], f"{self.percentiles[1]}th percentile"]) }%."""        