#!/usr/bin/env python3

import logging
from flask import Flask, render_template
import urllib
import json
from datetime import date

# Sucky FTP server XML data method
# from lxml import etree
# xml = etree.parse('ftp://ftp.bom.gov.au/anon/gen/fwo/IDV10751.xml')

# API and data formatting stuff
API_URLs = {
    'obs': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/observations',
    'daily': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/daily',
    'hourly': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/hourly'
}

def load_data(URL):
    try:
        with urllib.request.urlopen(URL) as JSON_data:
            return json.load(JSON_data)['data']
    except urllib.error.HTTPError as error:
        logging.error(f'Failed to load data from URL: {URL}', error)

# Flask app
app = Flask(__name__)
if not app.debug:
    logging.basicConfig(filename='debug.log', format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)

@app.route('/')
def index():
    # Load data
    data = {}
    for data_category in API_URLs:
        data[data_category] = load_data(API_URLs[data_category])

    today = date.today()
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # Render and load HTML template!
    try:
        return render_template('index.html', data=data, today=today, weekdays=weekdays)
    except Exception as error:
        logging.error(error)
        return render_template('error.html', error=error)
