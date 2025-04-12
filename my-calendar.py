#!/usr/bin/python
# -*- coding:utf-8 -*-

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
from PIL import Image, ImageDraw
import traceback

logging.basicConfig(level=logging.DEBUG)

import datetime
import requests

from openweathermap_to_weathericons import convert_icon_to_weathericon
from my_calendar_config import CONFIG, WEATHER_API_KEY, WEATHER_BASE_URL, WEATHER_LATITUDE, WEATHER_LONGITUDE, WEATHER_UNITS, TODOIST_API_KEY
from my_calendar_ui import renderAppBar, renderOneLineList, renderTwoLinesList
from my_calendar_apple import discover_caldav_calendars, list_calendars, get_apple_calendar_events, add_event_to_calendar

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
    logging.debug(e)

def go_to_sleep(epd):
    # logging.debug("Clear...")
    # epd.init()
    # epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

# ======= Render

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

        weather_icon_code = data['weather'][0]['icon']  # Get OpenWeatherMap icon code
        weather_icon_text = convert_icon_to_weathericon(weather_icon_code)

        # https://openweathermap.org/current
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "report": data['weather'][0]['description'],
            "icon_code": weather_icon_text,
            "temp_max": current['temp_max'],
            "temp_min": current['temp_min'],
        }
        logging.debug("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def renderWeatherAndDate(draw):
    # get weather
    data = fetch_weather_data()
    weather_data = process_weather_data(data)

    # get date
    currentDate = datetime.datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    renderAppBar(draw, weather_data['icon_code'], date)

def renderEvents(draw):
    events = []
    # get tasks
    calendar_name = "QQ Home"
    calendar_start_date = datetime.datetime.now()
    calendar_end_date = calendar_start_date + datetime.timedelta(days=1)
    calendar_events = get_apple_calendar_events(calendar_name, calendar_start_date, calendar_end_date)
    if calendar_events:
        logging.debug(f"\nEvents in '{calendar_name}' for the next 7 days:")
        for calendar_event in calendar_events:
            logging.debug(f"todos - {calendar_event.todos()}")
            logging.debug(f"vevent - {calendar_event.instance.vevent}")

            for component in calendar_event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append({
                    "title": component.get("summary"),
                    "subtitle": component.get("description"),
                    "date": component.get("dtstart").dt,
                    "dtend": component.get("dtend").dt,
                    "dtstamp": component.get("dtstamp").dt
                })

    # render events
    itemCount = min(len(events), CONFIG['taskItemCount'])
    # renderOneLineList(draw, events, itemCount)
    renderTwoLinesList(draw, events, itemCount)


try:
    logging.debug("Starting...")
    epd = init()

    if 0:
        logging.debug("E-paper refresh")
        epd.init()
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        renderWeatherAndDate(draw)
        renderEvents(draw)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        renderWeatherAndDate(draw)
        renderEvents(draw)
        epd.display_Fast(epd.getbuffer(Himage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()