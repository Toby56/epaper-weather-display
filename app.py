#!/usr/bin/env python3

import logging
from flask import Flask, render_template, send_file
import urllib
import json
import os
from dateutil.parser import isoparse
from datetime import date, timezone
from io import BytesIO

# Sucky FTP server XML data method
# from lxml import etree
# xml = etree.parse('ftp://ftp.bom.gov.au/anon/gen/fwo/IDV10751.xml')

# Paths and URLs
hourly_temps_log_path = "../weather-data-logs/hourly-temps.json"

API_URLs = {
    'observations': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/observations',
    'forecast-daily': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/daily',
    'forecast-hourly': 'https://api.weather.bom.gov.au/v1/locations/r1r0z4/forecasts/hourly'
}

# Load data from APIs
def load_API_data(URL):
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
    data['obs'] = load_API_data(API_URLs['observations'])
    data['daily'] = load_API_data(API_URLs['forecast-daily'])

    # Some utility variables
    today = date.today()
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Render and load HTML template!
    try:
        return render_template('index.html', data=data, today=today, weekdays=weekdays)
    except Exception as error:
        logging.error(error)
        return render_template('error.html', error=error)

@app.route('/todays-hourly-temps')
def todays_hourly_temps():
    # Maintain a JSON log file of the hourly forecast temperatures
    hourly_temps = {}
    if os.path.exists(hourly_temps_log_path):
        with open(hourly_temps_log_path, 'r') as hourly_temps_log:
            try:
                hourly_temps = json.load(hourly_temps_log)
            except:
                pass
        os.remove(hourly_temps_log_path)

    for hour in load_API_data(API_URLs['forecast-hourly']):
        hour_time = isoparse(hour['time']).replace(tzinfo=timezone.utc).astimezone(tz=None)
        iso_date = hour_time.date().isoformat()
        if iso_date not in hourly_temps.keys():
            hourly_temps[iso_date] = {}
        hourly_temps[iso_date][str(hour_time.hour)] = hour['temp']

    with open(hourly_temps_log_path, 'x') as hourly_temps_log:
        json.dump(hourly_temps, hourly_temps_log)

    # Compile an array of todays' hourly temperatures
    todays_hourly_temps = []
    for hour in range(24):
        hour = str(hour)
        if hour in hourly_temps[date.today().isoformat()].keys():
            todays_hourly_temps.append(hourly_temps[date.today().isoformat()][hour])
        # else:
        #     todays_hourly_temps.append(0)

    return send_file(BytesIO(json.dumps(todays_hourly_temps).encode()), 'application/json')

