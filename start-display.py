#!/usr/bin/env python3

from PIL import Image
from inky.auto import auto
import sys
from subprocess import Popen, TimeoutExpired
import shlex
import shutil
import os.path
import time
import logging

logging.basicConfig(filename='debug.log', format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
logfile = open('debug.log', 'a')

def log(message):
    logging.info(message)
    print(message)

start_time = time.time()
def time_elapsed():
    return f'{round(time.time() - start_time, 2)}s'

print('\n\n\n', file=logfile)
log('Starting gunicorn server')

gunicorn_process = Popen(shlex.split(f'{sys.executable} -m gunicorn --access-logfile=- \'app:app\''),
    stdout=logfile, stderr=logfile)

time.sleep(2)

log('Rendering screenshot with Chromium')

chromium_command = 'chromium-browser --headless --window-size=640,400 --screenshot="./screenshot.png" "http://127.0.0.1:8000"'
chromium_process = Popen(shlex.split(chromium_command), stdout=logfile, stderr=logfile)

try:
    chromium_process.communicate(timeout=10)
    log('Chromium done, stopping gunicorn server')
except TimeoutExpired:
    logging.warn('Chromium did not quit, killing and stopping gunicorn server')
    chromium_process.kill()

gunicorn_process.terminate()

try:
    gunicorn_process.communicate(timeout=10)
except TimeoutExpired:
    logging.warn('Gunicorn did not quit, killing 💀')
    gunicorn_process.kill()


log(f'Finished rendering image in {time_elapsed()}, writing to display! ✍️')

inky = auto(ask_user=True, verbose=True)
image = Image.open('./screenshot.png')
resized_image = image.resize(inky.resolution)
inky.set_image(resized_image, saturation=0)
inky.show()

# OPTIONAL
log('Saving a copy of the image')
file_index = 1
path = f'../data/screenshots/'
while os.path.exists(f'{path}screenshot{file_index}.png'): file_index += 1
shutil.copyfile('./screenshot.png', f'{path}screenshot{file_index}.png')

logfile.close()
log(f'Done in {time_elapsed()}, BYE!')
