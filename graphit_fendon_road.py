#!/usr/bin/env python3

from matplotlib.backends.backend_pdf import PdfPages

from graphit_base import get_traffic_data, do_graph_set, day_scatter_graph, hourly_average

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

ZONES = [
         'babraham_road_in',
         'babraham_road_out',
         'cherry_hinton_road_in',
         'cherry_hinton_road_out',
         'cherry_hinton_road_outer_in',
         'cherry_hinton_road_outer_out',
         'hills_road_inner_in',
         'hills_road_inner_out',
         'hills_road_outer_in',
         'hills_road_outer_out',
         'perne_road_north',
         'perne_road_south',
         ]


def run():

    # Slurp the data

    df = get_traffic_data()
    df = df[df.index.dayofweek < 5]
    df = df['2019-08-01':]

    with PdfPages('journey_time_fendon_road_area_BUS.pdf') as pdf:

        for between in (('07:00', '09:00'), ('16:00', '18:00')):

            title = f'Journey Times, Mon-Fri, {between[0]}-{between[1]}'

            do_graph_set(pdf, df.between_time(*between).copy(), day_scatter_graph, ZONES, title, 40)

        title = 'Average journey times, Mon-Fri'
        do_graph_set(pdf, df, hourly_average, ZONES, title, 25)


if __name__ == '__main__':
    run()
