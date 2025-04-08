#!/usr/bin/python
# -*- coding:utf-8 -*-

# ======= Config

WEATHER_API_KEY = '50a816e10ff54f5dbff234827220106'
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall'
WEATHER_LATITUDE = '10.7863809'  # Latitude
WEATHER_LONGITUDE = '106.7781079'  # Longitude
WEATHER_UNITS = 'metric' # imperial or metric

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

import datetime
import requests

# ======= Utils

black = 0
white = 1

fontBody = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
fontTitle = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
fontHeadline = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
fontWeather = ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 32)

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
    currentDate = datetime.datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    draw.text((0, 0), date, font = fontTitle, fill = black)

# Fetch weather data
def fetch_weather_data():
    url = f"{WEATHER_BASE_URL}?lat={WEATHER_LATITUDE}&lon={WEATHER_LONGITUDE}&units={WEATHER_UNITS}&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Weather data fetched successfully.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise

# Process weather data
def process_weather_data(data):
    try:
        current = data['current']
        daily = data['daily'][0]
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "wind": current['wind_speed'],
            "report": current['weather'][0]['description'].title(),
            "icon_code": current['weather'][0]['icon'],
            "temp_max": daily['temp']['max'],
            "temp_min": daily['temp']['min'],
            "precip_percent": daily['pop'] * 100,
        }
        logging.info("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def renderWeather(draw):
    # get weather
    data = fetch_weather_data()
    weather_data = process_weather_data(data)

    # render date https://erikflowers.github.io/weather-icons/
    draw.text((200, 0), weather_data['icon_code'], font = fontWeather, fill = black)
    logging.info(weather_data['icon_code'])

def renderTasks(draw):
    # get tasks
    tasks = ["Ford", "Volvo", "BMW"]

    # render tasks
    for j in range(0, len(tasks)):
        draw.text((0, j * 16 + 32), tasks[j], font = fontBody, fill = black)

try:
    logging.info("Starting...")
    epd = init()

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
        renderDate(draw)
        renderWeather(draw)
        renderTasks(draw)
        epd.display_Fast(epd.getbuffer(Himage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.info("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.info("Ctrl + c:")
    on_exit()