# ======= Config

WEATHER_API_KEY = ''
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
WEATHER_LOCATION = 'XXXXXXXX'  # Name of location
WEATHER_LATITUDE = 'XXXXXXXX'  # Latitude
WEATHER_LONGITUDE = 'XXXXXXXX'  # Longitude
WEATHER_UNITS = 'imperial' # imperial or metric

TODOIST_API_KEY = ''

# ======= Import

import sys, os
picdir = "/home/ezcafe/e-Paper/RaspberryPi_JetsonNano/python/pic"
libdir = "/home/ezcafe/e-Paper/RaspberryPi_JetsonNano/python/lib"
# picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
# libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
# picdir = os.path.join(os.path.dirname(__file__), 'resources')
# libdir = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.exists(libdir): sys.path.append(libdir)

import datetime, time, traceback, logging
from waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

black = 0
white = 1

fontBody = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
fontTitle = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
fontHeadline = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
# fontWeather = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 32)

# ======= Utils

def init():
    logging.info("Init and Clear...")
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    return epd

def on_exit():
    logging.info("Exit...")
    epd4in2_V2.epdconfig.module_exit(cleanup=True)
    exit()

def on_error(e):
    logging.info(e)

def go_to_sleep(epd):
    logging.info("Sleep...")
    epd.sleep()

def get_draw():
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    return draw

def update_display(epd, image):
    epd.display_Fast(epd.getbuffer(image))

# ======= Render

def renderDate(epd):
    # get date
    date = datetime.datetime.now().strftime('%A, %d/%m')

    # render date
    draw = get_draw()
    draw.text((0, 0), date, font = fontBody, fill = black)
    update_display(epd, draw)

def renderWeather(epd):
    # get weather

    # render date
    draw = get_draw()
    draw.text((200, 0), '\uf095', font = fontBody, fill = black)
    update_display(epd, draw)

def renderTasks(epd):
    # get tasks
    tasks = ["Ford", "Volvo", "BMW"]

    # render tasks
    draw = get_draw()
    for j in range(0, len(tasks)):
        draw.text((0, j * 16), tasks(j), font = fontBody, fill = black)
    update_display(epd, draw)

try:
    logging.info("Starting...")
    epd = init()

    renderDate(epd)
    renderWeather(epd)
    renderTasks(epd)

    go_to_sleep(epd)

except IOError as e:
    logging.info("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.info("Ctrl + c:")
    on_exit()