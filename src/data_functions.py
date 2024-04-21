from collections import namedtuple
from IPython.display import display, Markdown

class Percentiles:
    def __init__(self, 
                df,
                data_column = '', 
                periods_per_year = 12,
                multi_years = [5, 10, 20, 30]             
                 ):
        self.data_column = data_column
        self.periods_per_year = periods_per_year
        self.multi_years = multi_years

        # Define the percentiles
        percentiles_tuple = namedtuple('Percentiles', ['lower', 'median', 'upper'])
        self.percentiles = percentiles_tuple(25, 50, 75)

        # Generate the window_periods array using a for loop
        self.window_periods = [self.periods_per_year * years for years in self.multi_years]
        self.window_periods.insert(0, self.periods_per_year)

    def add_percentiles(self, df, column, window, prefix):
        """Calculate and add percentiles to the DataFrame for a given window size."""
        for percentile_name, percentile in zip(self.percentiles._fields, self.percentiles):
            df[f'{prefix}_{percentile_name}'] = df[column].rolling(window=window, min_periods=1, center=True).quantile(percentile/100)
        return df

    def calculate_percentiles(self, df):
        """ Calculate median 50th and lower, upper percentiles over multiple years """

        # Calculate and add the percentiles for each window size
        for window in self.window_periods:
            years = window // self.periods_per_year
            name = f'rolling_{years}_years'
            df = self.add_percentiles(df, self.data_column, window, name)

        return df
    

# Write table to file
#
#   with open('../data/inflation_percentiles.md', 'w') as f:
#       f.write(table)
#       f.close()

    def percentile_table(self,df):
        """ Create a markdown data table of the multi year percentiles to reuse in other notebooks """

        # Create the header rows of the table
        table = "| Years |   " + " |   ".join(f'{str(percentile)}th percentile' for percentile in self.percentiles) + " |\n"
        table += "|-------" + "|-----:" * len(self.percentiles._fields) + "|\n"

        # Add the percentile values for each window period
        for window in self.window_periods:
            years = window // self.periods_per_year
            name = f'rolling_{years}_years'
            table += f"| {str(years).ljust(5)} | " + " | ".join("{:,.2f}".format(df[f'{name}_{percentile_name}'].iloc[-1]) for percentile_name in self.percentiles._fields) + " |\n"
        
        return table

    def display_percentile_table(self,df):
        display(Markdown(self.percentile_table(df)))

    """
    Markdown must not have indented whitespace. Indented markdown is rendered as code monospace font.
    """

    def display_percentile_intro(self):
        display(Markdown(f"""
Calculating the {self.percentiles[0]}th and {self.percentiles[2]}th percentile over a multi year time horizon helps smooth out the anomolies and visualize the {self.percentiles._fields[0]} and {self.percentiles._fields[2]} long term trends.
    """))
        
    def display_percentile_summary(self, df, metric_name='change'):
        display(Markdown(f"""
Over the last {self.multi_years[0]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { "{:,.2f}".format(df[f'rolling_{self.multi_years[0]}_years_{self.percentiles._fields[1]}'].iloc[-1])  }%.

Over the last {self.multi_years[-1]} years the {self.percentiles._fields[1]} ({self.percentiles[1]}th percetile) {metric_name} is { "{:,.2f}".format(df[f'rolling_{self.multi_years[-1]}_years_{self.percentiles._fields[1]}'].iloc[-1])  }%.
    """))