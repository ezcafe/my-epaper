#!/usr/bin/python
# -*- coding:utf-8 -*-

# ======= Config

WEATHER_API_KEY = ''
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
WEATHER_LOCATION = 'XXXXXXXX'  # Name of location
WEATHER_LATITUDE = 'XXXXXXXX'  # Latitude
WEATHER_LONGITUDE = 'XXXXXXXX'  # Longitude
WEATHER_UNITS = 'imperial' # imperial or metric

TODOIST_API_KEY = ''

# ======= Import

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

# ======= Utils

black = 0
white = 1

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
    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

# ======= Render

def renderDate(draw):
    # get date
    date = datetime.datetime.now().strftime('%A, %d/%m')

    # render date
    draw.text((0, 0), date, font = fontBody, fill = black)

def renderWeather(draw):
    # get weather

    # render date
    draw.text((200, 0), '\uf095', font = fontBody, fill = black)

def renderTasks(draw):
    # get tasks
    tasks = ["Ford", "Volvo", "BMW"]

    # render tasks
    for j in range(0, len(tasks)):
        draw.text((0, j * 16), tasks(j), font = fontBody, fill = black)

try:
    logging.info("Starting...")
    epd = init()

    fontBody = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    fontTitle = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    fontHeadline = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
    # fontWeather = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 32)

    if 0:
        logging.info("E-paper refresh")
        epd.init()
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        renderDate(draw)
        renderWeather(draw)
        renderTasks(draw)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)
    else:
        logging.info("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        # get date
        date = datetime.datetime.now().strftime('%A, %d/%m')
        # render date
        draw.text((0, 0), date, font = fontBody, fill = black)
        # renderDate(draw)
        # renderWeather(draw)
        # renderTasks(draw)
        epd.display_Fast(epd.getbuffer(Himage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.info("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.info("Ctrl + c:")
    on_exit()