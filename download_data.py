#!/usr/bin/env python3

import calendar
import csv
import logging
import os

import coreapi


logger = logging.getLogger('__name__')

API_SCHEMA = os.getenv('API_SCHEMA', 'https://tfc-app1.cl.cam.ac.uk/api/docs/')

API_TOKEN = os.getenv('API_TOKEN', None)
assert API_TOKEN, 'API_TOKEN environment variable not set'

zones = ['babraham_road_in', 'babraham_road_out',
         'hills_road_outer_in', 'hills_road_outer_out',
         'hills_road_inner_in', 'hills_road_inner_out',
         'cherry_hinton_road_in', 'cherry_hinton_road_out',
         'cherry_hinton_road_outer_in', 'cherry_hinton_road_outer_out',
         'perne_road_south', 'perne_road_north'
         ]
years = [2019]

# /api/v1/zone/history/a428_east/?start_date=2019-04-01&end_date=2019-04-30
# /api/v1/zone/history/a428_east/?start_date=2019-04-01&end_date=2019-04-30


def get_data():

    auth = coreapi.auth.TokenAuthentication(
        scheme='Token',
        token=API_TOKEN
    )
    client = coreapi.Client(auth=auth)

    schema = client.get(API_SCHEMA)

    action = ['zone', 'history', 'read']

    csv_filename = 'bus-data.csv'
    logger.info('Outputting CSV to %s', csv_filename)

    with open(csv_filename, 'w', newline='') as csvfile:

        output = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
        output.writerow(['Zone', 'Date', 'Duration', 'Distance'])

        for zone in zones:

            for year in years:

                ctr = 0

                for month in range(1, 13):

                    last_day = calendar.monthrange(year, month)[1]
                    start = '{:04d}-{:02d}-01'.format(year, month)
                    end = '{:04d}-{:02d}-{:02d}'.format(year, month, last_day)

                    params = {
                        'zone_id': zone,
                        'start_date': start,
                        'end_date': end
                    }
                    logger.debug("Getting transits, zone %s, start %s, end %s", zone, start, end)
                    api_results = client.action(schema, action, params=params)
                    for result in api_results['request_data']:
                        ctr += 1
                        output.writerow([
                            zone,
                            result['date'],
                            result['duration'],
                            result['distance']
                        ])

            logger.info('Retrieved %s transits.', ctr)


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    get_data()


if __name__ == "__main__":
    main()
