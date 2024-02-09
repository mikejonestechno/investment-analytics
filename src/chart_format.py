import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

class BaseChart:
    def __init__(self, chart_title='', chart_source='', chart_author='right', y_label='', y_ticks=0, y_log=False, y_log_ticks=None, x_label='Date', x_ticks=5, data_column='column_name'):
        self.chart_title = chart_title
        self.chart_source = chart_source
        self.chart_author = chart_author
        self.y_label = y_label
        self.y_ticks = y_ticks
        if y_log_ticks:
            self.y_log_ticks = np.array(y_log_ticks)
        self.y_log = y_log
        self.x_label = x_label
        self.x_ticks = x_ticks
        self.data_column = data_column

    def base_chart(self, df: pd.DataFrame):

        plt.figure(figsize=(10, 6))
        plt.title(self.chart_title)
        if self.chart_source:
            plt.figtext(1, 0.04, self.chart_source, ha="right", fontsize=8)
            plt.subplots_adjust(right=1)  # Reset right boundary of the subplots after adding figtext
        plt.grid(True)

        if self.chart_author == 'right':
            plt.figtext(1.01, 0.15, 'mikejonestechno', ha="right", fontsize=8, rotation=-90)

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
    

class LogChart(BaseChart):
    def __init__(self, y_log_ticks=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y_log_ticks = np.array(y_log_ticks)

    def base_chart(self, df: pd.DataFrame):
        plt, colors = super().base_chart(df)

        """ Logarithmic y-axis chart """
        y_ticks_labels = np.array([str(f'{ytick:.0f}') for ytick in self.y_log_ticks])
        bottom_limit = self.y_log_ticks[0]
        top_limit = self.y_log_ticks[-1]
        plt.yscale('log')
        plt.ylim(bottom_limit, top_limit)
        plt.yticks(self.y_log_ticks, y_ticks_labels)

        return plt, colors

class StandardChart(BaseChart):
    def __init__(self, y_ticks=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y_ticks = y_ticks

    def base_chart(self, df: pd.DataFrame):
        plt, colors = super().base_chart(df)
        
        """ Standard y-axis chart """
        self.y_ticks = self.y_ticks if self.y_ticks else 100
        if df[self.data_column].min() > 0:
            bottom_limit = 0
        else:
            bottom_limit = (df[self.data_column].min() // self.y_ticks) * self.y_ticks    
        top_limit = (df[self.data_column].max() // self.y_ticks) * self.y_ticks + self.y_ticks
        plt.yticks(np.arange(bottom_limit, top_limit + 1, self.y_ticks))
        plt.ylim(bottom_limit, top_limit)

        return plt, colors