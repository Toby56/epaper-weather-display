#!/usr/bin/env python3

import logging
from flask import Flask, render_template
import urllib
import json
import calendar
from datetime import date

# Sucky FTP server XML data method
# from lxml import etree
# xml = etree.parse('ftp://ftp.bom.gov.au/anon/gen/fwo/IDV10751.xml')

# API and data formatting stuff
API_URLs = {
    'observations': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/observations',
    'forecast_daily': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/daily',
    # 'forecast_3-hourly': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/3-hourly'
}

data_format = {
    'current_temp': lambda d : d['observations']['temp'],
    'today_is_raining': lambda d : True if d['forecast_daily'][0] == 1 else False
}


def load_data(URL):
    try:
        with urllib.request.urlopen(URL) as JSON_data:
            return json.load(JSON_data)['data']
    except urllib.error.HTTPError as error:
        logging.error(f'Failed to load data from URL: {URL}', error)

def format_data(data_name, data):
    try:
        return data_format[data_name](data)
    except KeyError as error:
        logging.error(f'Data not found: {data_name}', error)
        return "???"

# Flask app
app = Flask(__name__)
if not app.debug:
    logging.basicConfig(filename='debug.log', format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)

@app.route('/')
def hello():
    # Load data
    data = {}
    for data_category in API_URLs:
        data[data_category] = load_data(API_URLs[data_category])

    # Format data
    formatted_data = {}
    for data_name in data_format:
        formatted_data[data_name] = format_data(data_name, data)

    today = date.today()
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # Render and load HTML template!
    return render_template('index.html', data=data, today=today, weekdays=weekdays)
