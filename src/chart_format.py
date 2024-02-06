import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pandas as pd


class Chart:
    def __init__(self, chart_title='', chart_source='', y_label='', x_label='Date', x_ticks=5):
        self.chart_title = chart_title
        self.chart_source = chart_source
        self.y_label = y_label
        self.x_label = x_label
        self.x_ticks = x_ticks

    def base_chart(self, df: pd.DataFrame):

        plt.figure(figsize=(10, 6))
        plt.title(self.chart_title)
        if self.chart_source:
            plt.figtext(1, 0.01, self.chart_source, ha="right", fontsize=8)
            plt.subplots_adjust(right=1)  # Reset right boundary of the subplots after adding figtext
        plt.grid(True)

        colors = list(plt.rcParams['axes.prop_cycle'])

        ax = plt.gca()  # Get the current Axes instance
        plt.xlabel(self.x_label)
        start_year = (df.index[0].year // self.x_ticks) * self.x_ticks
        end_year = (df.index[-1].year // self.x_ticks) * self.x_ticks + self.x_ticks
        left_limit = pd.to_datetime(f'{start_year}-01-01')
        right_limit = pd.to_datetime(f'{end_year}-01-01')
        plt.xlim(left=left_limit, right=right_limit)    
        ax.xaxis.set_major_locator(mdates.YearLocator(self.x_ticks))  # Set major ticks every x years
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years

        plt.ylabel(self.y_label)

        return plt, colors