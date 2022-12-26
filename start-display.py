#!/usr/bin/env python3

import logging

from inky.auto import auto
from inky.inky_uc8159 import CLEAN
from PIL import Image

import sys
import os.path
from subprocess import Popen, TimeoutExpired
import shlex
import shutil

import time
from datetime import datetime

# Paths
dirname = os.path.dirname(os.path.abspath(__file__))
screenshot_path = os.path.join(dirname, 'screenshot.png')

# Set up logging
logging.basicConfig(filename='debug.log', format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
logfile = open('debug.log', 'a')

def log(message):
    logging.info(message)
    print(message)

log('-- DISPLAY SCRIPT START --')

start_time = time.time()
def time_elapsed():
    return f'{round(time.time() - start_time, 2)}s'

# Start Gunicorn process and wait for server to start
log('Starting gunicorn server')

gunicorn_command = f'{sys.executable} -m gunicorn --access-logfile=- --chdir=\'{dirname}\' \'app:app\''
gunicorn_process = Popen(shlex.split(gunicorn_command),
    stdout=logfile, stderr=logfile)

time.sleep(2)

# Start Chromium process
log(f'Rendering display to an image with Chromium')

chromium_command = f'chromium-browser --headless --window-size=640,400 --screenshot="{screenshot_path}" "http://127.0.0.1:8000"'
chromium_process = Popen(shlex.split(chromium_command), stdout=logfile, stderr=logfile)

# Wait for Chromium process to finish or kill it
try:
    chromium_process.communicate(timeout=10)
    log('Chromium done, stopping gunicorn server')
except TimeoutExpired:
    logging.warn('Chromium did not quit, killing and stopping gunicorn server')
    chromium_process.kill()

# Send terminate signal to Gunicorm process or kill it
gunicorn_process.terminate()
try:
    gunicorn_process.communicate(timeout=10)
except TimeoutExpired:
    logging.warn('Gunicorn did not quit, killing 💀')
    gunicorn_process.kill()

log(f'Finished rendering image in {time_elapsed()}, writing to display! ✍️')

# Inky display instance
inky = auto(ask_user=True, verbose=True)

# Clean display if it is midnight
if datetime.now().hour == 0:
    log('It\'s midnight! Cleaning display first')
    for y in range(inky.height - 1):
        for x in range(inky.width - 1):
            inky.set_pixel(x, y, CLEAN)

    inky.show()
    time.sleep(1.0)

# Write screenshot to display
image = Image.open(screenshot_path)
resized_image = image.resize(inky.resolution)
inky.set_image(resized_image, saturation=0)
inky.show()

# Optionally, save a copy of each image
log('Saving a copy of the image')
file_index = 1
screenshot_log_path = os.path.join(dirname, '..', 'data', 'screenshots')
while os.path.exists(os.path.join(screenshot_log_path, f'screenshot{file_index}.png')): file_index += 1
shutil.copyfile(screenshot_path, f'{screenshot_log_path}screenshot{file_index}.png')

# Finish up
logfile.close()
log(f'Done in {time_elapsed()}, BYE!')
log('-- DISPLAY SCRIPT END --')
