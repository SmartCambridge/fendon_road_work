#!/usr/bin/env python3

import matplotlib.pyplot

from datetime import date

import numpy as np

import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

TO_MPH = 2.23694
GRAPHS_PER_ROW = 2
GRAPHS_PER_PAGE = GRAPHS_PER_ROW * 3
MM_TO_INCH = 0.0393701
A4P = (210*MM_TO_INCH, 297*MM_TO_INCH)
A3P = (297*MM_TO_INCH, 420*MM_TO_INCH)
A3L = (420*MM_TO_INCH, 297*MM_TO_INCH)
FIGSIZE = A3L

YMAX = 30

DATAFILE = 'bus-data.csv'


def label_event(ax, text, x, y):
    ax.annotate(text, xy=(x, y), xycoords=('data', 'data'),
                xytext=(-30, 0), textcoords='offset points',
                ha='right', arrowprops=dict(arrowstyle="->"))


def hilight_events(ax, y):

    ax.axvline(x='2019-08-24', linestyle='--')
    label_event(ax, 'Mill Road bridge reopened', '2019-08-24', y)

    ax.axvline(x='2019-09-04', linestyle='--')
    label_event(ax, 'School term starts', '2019-09-04', y)

    ax.axvline(x='2019-09-09', linestyle='--')
    label_event(ax, 'Fendon road work starts', '2019-09-09', y-5)


def day_scatter_graph(ax, df, zone, ymax):

    df2 = df[df.Zone == zone].copy()
    df2.index = df2.index.normalize()
    df2['minutes'] = df2['Duration']/60

    ax.plot(df2.index, df2['minutes'], '. b')

    df2 = df2.resample('D').median()

    ax.plot(df2.index, df2['minutes'], '_ k')

    hilight_events(ax, ymax-2.5)

    ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(1))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('\n%b\n%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(matplotlib.dates.MO))
    ax.xaxis.set_minor_formatter(matplotlib.dates.DateFormatter('%d'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='minor', zorder=2)


def hourly_average(ax, df, zone, ymax):

    df2 = df[df.Zone == zone]
    df2 = df2.groupby(df2.index.hour).mean()
    df2['minutes'] = df2['Duration']/60

    ax.bar(df2.index, df2['minutes'], align='edge')

    ax.set_xlim([0, 24])
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=4))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(base=1))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%02d:00'))

    ax.grid(axis='y', which='major', zorder=2)
    ax.grid(axis='x', which='major', zorder=2)


def setup_figure(title):

    fig, axs_list = matplotlib.pyplot.subplots(
        nrows=GRAPHS_PER_PAGE // GRAPHS_PER_ROW,
        ncols=GRAPHS_PER_ROW,
        sharex=True,
        sharey=True,
        figsize=FIGSIZE,
        squeeze=False)

    fig.suptitle(title, fontsize=13)

    return fig, axs_list


def setup_axies(ax, ymax):
    '''
    Common axis setup code
    '''

    if ymax:
        ax.set_ylim([0, ymax])

    ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))


def get_traffic_data():

    df = pd.read_csv(DATAFILE)
    df.index = pd.to_datetime(df['Date'], utc=True)
    df.drop('Date', axis=1, inplace=True)

    return df


def do_graph_set(pdf, df, graph_fn, zones, page_title, ymax):

    graph = 0
    fig = None

    for zone in zones:

        if graph % GRAPHS_PER_PAGE == 0:
            if graph > 0:
                fig.tight_layout(rect=[0, 0, 1, 0.96])
                pdf.savefig(fig)
                print('Page!')
            fig, axs_list = setup_figure(page_title)

        row = (graph % GRAPHS_PER_PAGE) // GRAPHS_PER_ROW
        col = graph % GRAPHS_PER_ROW
        print(f'Zone: {zone}, graph: {graph}, row: {row}, col: {col}')
        ax = axs_list[row, col]

        graph_fn(ax, df, zone, ymax)
        setup_axies(ax, ymax)
        ax.set_title(f'{zone}')

        if col == 0:
            axs_list[row, col].set(ylabel='Journey time (minutes)')

        graph += 1

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)
    print('Last page!')
