import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

class BaseChart:
    def __init__(self, 
                 chart_title='', 
                 chart_source='', 
                 chart_author_location='right', 
                 y_label='',
                 x_label='Date', 
                 x_ticks=5,
                 start_year=None, 
                 data_column=''):
        self.chart_title = chart_title
        self.chart_source = chart_source
        self.chart_author_location = chart_author_location
        self.y_label = y_label
        self.x_label = x_label
        self.x_ticks = x_ticks
        self.start_year = start_year
        self.data_column = data_column

    def base_chart(self, df: pd.DataFrame):

        plt.figure(figsize=(10, 6))
        plt.title(self.chart_title)

        colors = list(plt.rcParams['axes.prop_cycle'])

        ax = plt.gca()  # Get the current Axes instance
        if self.start_year == None:
            self.start_year = (df.index[0].year // self.x_ticks) * self.x_ticks
        left_limit = pd.to_datetime(f'{self.start_year}-01-01')
        end_year = (df.index[-1].year // self.x_ticks) * self.x_ticks + self.x_ticks
        right_limit = pd.to_datetime(f'{end_year}-01-01')
        plt.xlim(left=left_limit, right=right_limit)    
        ax.xaxis.set_major_locator(mdates.YearLocator(self.x_ticks))  # Set major ticks every x years
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
        figtext_adjust = 0
        if len(ax.get_xticks()) > 15:
            plt.xticks(rotation=45)  # Rotate x-axis labels
            # Reset bottom boundary of the subplots after rotating text
            plt.subplots_adjust(bottom=0.13)
            figtext_adjust = 0.013
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(True)
        if self.chart_source:
            plt.figtext(1, 0.04 - figtext_adjust, self.chart_source, ha="right", fontsize=8)
            plt.subplots_adjust(right=1)  # Reset right boundary of the subplots after adding figtext
        if self.chart_author_location == 'right':
            plt.figtext(1.01, 0.15 + figtext_adjust, 'mikejonestechno', ha="right", fontsize=8, rotation=-90)

        return plt, colors

class LogChart(BaseChart):
    def __init__(self, y_ticks=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y_ticks = np.array(y_ticks)

    def base_chart(self, df: pd.DataFrame):
        plt, colors = super().base_chart(df)

        """ Logarithmic y-axis chart """
        y_ticks_labels = np.array([str(f'{ytick:.0f}') for ytick in self.y_ticks])
        bottom_limit = self.y_ticks[0]
        top_limit = self.y_ticks[-1]
        plt.yscale('log')
        plt.ylim(bottom_limit, top_limit)
        plt.yticks(self.y_ticks, y_ticks_labels)

        return plt, colors

class StandardChart(BaseChart):
    def __init__(self, top_limit=None, bottom_limit=None, y_ticks=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y_ticks = y_ticks
        self.top_limit = top_limit
        self.bottom_limit = bottom_limit


    def base_chart(self, df: pd.DataFrame):
        plt, colors = super().base_chart(df)
        
        """ Standard y-axis chart """
        if self.bottom_limit == None:
            if df[self.data_column].min() > 0:
                self.bottom_limit = 0
            else:
                self.bottom_limit = (df[self.data_column].min() // self.y_ticks) * self.y_ticks    
        if self.top_limit == None:
            self.top_limit = (df[self.data_column].max() // self.y_ticks) * self.y_ticks + self.y_ticks
        plt.yticks(np.arange(self.bottom_limit, self.top_limit + 1, self.y_ticks))
        plt.ylim(self.bottom_limit, self.top_limit)

        return plt, colors

class PercentileChart(StandardChart):
    def __init__(self, percentiles, multi_year, color_index, legend_location='best', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.percentiles = percentiles
        self.multi_year = multi_year
        self.color_index = color_index
        self.legend_location = legend_location

    def plot_percentiles(self, df: pd.DataFrame):
        plt, colors = self.base_chart(df)

        plt.plot(df.index, df[self.data_column], label='YoY Annual Price Change', color=colors[self.color_index]['color'], alpha=0.1)

        for i, percentile in enumerate(self.percentiles._fields):
            linestyle = '--' if i != 1 else '-'
            alpha = 0.7 if i != 1 else 1.0
            if i == 0:
                label = f'{str(self.percentiles[0]) + "th and " + str(self.percentiles[2]) + "th Percentile"}'
            elif i == 1:
                label = f'{self.multi_year} Year {percentile.capitalize()}'
            else:
                label = None
            plt.plot(df.index, df[f'rolling_{self.multi_year}_years_{percentile}'], color=colors[self.color_index]['color'], linestyle=linestyle, alpha=alpha, label=label)
        legend = plt.legend(loc=self.legend_location)
        legend.get_frame().set_alpha(0.98)
        plt.show()    