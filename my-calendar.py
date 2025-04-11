#!/usr/bin/python
# -*- coding:utf-8 -*-

# ======= Config

WEATHER_API_KEY = 'bd7687c19648b628d77527713a59bc47'
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_LATITUDE = '10.7863809'  # Latitude
WEATHER_LONGITUDE = '106.7781079'  # Longitude
WEATHER_UNITS = 'metric' # imperial or metric

TODOIST_API_KEY = ''

UI_MODE = 'normal'  # 'compact' or 'normal'
UI_MODES = {
    'compact': {
        'appBarHeight': 56,
        'appBarTitleOffset': 20,
        'taskItemHeight': 48,
        'taskItemTitleOffset': 20,
    },
    'normal': {
        'appBarHeight': 64,
        'appBarTitleOffset': 20,
        'taskItemHeight': 56,
        'taskItemTitleOffset': 20,
    },
}


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

import datetime
import requests
from weather_icons import weatherIdToIcon
from weather_icon_mapping import weatherIconToText

# ======= Utils

black = 0
white = 1
uiConfig = UI_MODES[UI_MODE]

fontHeadline = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
fontBody = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
fontSupportText = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
fontTitle = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
fontWeather = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 24)

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
    logging.debug(e)

def go_to_sleep(epd):
    # logging.debug("Clear...")
    # epd.init()
    # epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

# ======= Render

def renderDate(draw):
    # get date
    currentDate = datetime.datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    draw.text((48, uiConfig['appBarTitleOffset']), date, font = fontHeadline, fill = black)
    draw.rectangle((48, 0, 150, uiConfig['appBarHeight']), outline = 0)
    draw.rectangle((56, 20, 142, 44), outline = 0)

# Fetch weather data
def fetch_weather_data():
    url = f"{WEATHER_BASE_URL}?lat={WEATHER_LATITUDE}&lon={WEATHER_LONGITUDE}&units={WEATHER_UNITS}&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug("Weather data fetched successfully.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise

# Process weather data
def process_weather_data(data):
    try:
        logging.debug(data)
        current = data['main']

        weatherId = data['weather'][0]['id']

        weatherIcon = weatherIdToIcon[str(weatherId)]
        # If we are not in the ranges mentioned above, add a day/night prefix.
        if not(weatherId > 699 and weatherId < 800) and not(weatherId > 899 and weatherId < 1000):
            weatherIcon = 'day-' + weatherIcon

        # https://openweathermap.org/current
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "report": data['weather'][0]['description'],
            "icon_code": weatherIconToText[weatherIcon],
            "temp_max": current['temp_max'],
            "temp_min": current['temp_min'],
        }
        logging.debug("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def renderWeather(draw):
    # get weather
    data = fetch_weather_data()
    weather_data = process_weather_data(data)

    # render date
    draw.text((11, 15), weather_data['icon_code'], font = fontWeather, fill = black)
    draw.rectangle((0, 0, 48, uiConfig['appBarHeight']), outline = 0)
    draw.rectangle((12, 20, 36, 44), outline = 0)

def renderTasks(draw):
    # get tasks
    tasks = ["Prepare runsheet", "Approve TSR", "Ask for conflict approvals", 'IIIIIIIIIIIII']

    # render tasks
    for j in range(0, len(tasks)):
        itemPosition = j * uiConfig['taskItemHeight'] + uiConfig['appBarHeight']
        draw.text((16, itemPosition + uiConfig['taskItemTitleOffset']), tasks[j], font = fontBody, fill = black)
        draw.line((0, itemPosition + 56, 150, itemPosition + 56), fill = 0)
        draw.rectangle((16, itemPosition + 16, 134, itemPosition + 40), outline = 0)



try:
    logging.debug("Starting...")
    epd = init()

    if 0:
        logging.debug("E-paper refresh")
        epd.init()
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        renderDate(draw)
        renderWeather(draw)
        renderTasks(draw)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        renderDate(draw)
        renderWeather(draw)
        renderTasks(draw)
        epd.display_Fast(epd.getbuffer(Himage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()