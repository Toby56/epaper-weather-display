#!/usr/bin/env python3

from PIL import Image
from inky.auto import auto
import sys
from subprocess import Popen, TimeoutExpired
import shlex
import time
import logging

logging.basicConfig(filename='debug.log', format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.DEBUG)
logfile = open('debug.log', 'a')

start_time = time.time()
def time_elapsed():
    return f'{round(start_time - time.time(), 2)}s'

logging.info('\n\n\nStarting gunicorn server')

gunicorn_process = Popen(shlex.split(f'{sys.executable} -m gunicorn --access-logfile=- \'app:app\''),
    stdout=logfile, stderr=logfile)

time.sleep(2)

logging.info('Rendering screenshot with Chromium')

chromium_command = 'chromium-browser --headless --window-size=640,400 --screenshot="./screenshot.png" "http://127.0.0.1:8000"'
chromium_process = Popen(shlex.split(chromium_command), stdout=logfile, stderr=logfile)

try:
    chromium_process.communicate(timeout=10)
    logging.info('Chromium done, stopping gunicorn server')
except TimeoutExpired:
    logging.warn('Chromium did not quit, killing and stopping gunicorn server')
    chromium_process.kill()

gunicorn_process.terminate()

try:
    gunicorn_process.communicate(timeout=10)
except TimeoutExpired:
    logging.warn('Gunicorn did not quit, killing 💀')
    gunicorn_process.kill()


logging.info(f'Finished rendering image in {time_elapsed()}, writing to display! ✍️')

inky = auto(ask_user=True, verbose=True)
image = Image.open('./screenshot.png')
resizedimage = image.resize(inky.resolution)
inky.set_image(resizedimage, saturation=0)
inky.show()

logfile.close()
logging.info(f'Done in {time_elapsed}, BYE!')

# Ping method
# ping = tcping.Ping('127.0.0.1', 8000)
# for tries in range(5):
#     try:
#         ping.ping(1)
#     except ConnectionRefusedError as error:
#         if tries == 4:
#             raise error
#         print('Ping failed, retrying')
#         time.sleep(0.5)
#         pass
#     else:
#         print('Ping connection sucessful')
#         break

# python3 -m gunicorn -w 4 --access-logfile=- 'app:app'