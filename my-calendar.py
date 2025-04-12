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

from datetime import datetime, timedelta
import requests
import math

from openweathermap_to_weathericons import convert_icon_to_weathericon
from my_calendar_config import CONFIG, FILL_BLACK, WEATHER_API_KEY, WEATHER_BASE_URL, WEATHER_LATITUDE, WEATHER_LONGITUDE, WEATHER_UNITS, TODOIST_API_KEY
from my_calendar_ui import renderAppBar, renderItemDetails, renderOneLineList, renderTwoLinesList
from my_calendar_apple import get_apple_calendar_events

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
    currentDate = datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    renderAppBar(draw, weather_data['icon_code'], date)

def fetch_events():
    calendar_name = "QQ Home"
    calendar_start_date = datetime.now()
    calendar_end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1,microseconds=-1)
    return get_apple_calendar_events(calendar_name, calendar_start_date, calendar_end_date)

def process_events(calendar_events):
    processed_events = []
    if calendar_events:
        for calendar_event in calendar_events:
            for component in calendar_event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                processed_events.append({
                    "title": component.get("summary"),
                    "subtitle": component.get("description"),
                    "timeStart": component.get("dtstart").dt,
                    "timeEnd": component.get("dtend").dt,
                    "location": component.get("location")
                })
    return processed_events

def normalize_events(events):
    selected_event = None
    normalized_events = []
    for event in events:
        if event['timeStart'] is None or event['timeStart'].strftime('%H:%M') != '00:00' or event['timeEnd'] is None or event['timeEnd'].strftime('%H:%M') != '00:00':
            selected_event = event
        else:
            normalized_events.append(event)

    if selected_event is None:
        selected_event = events[0]
        normalized_events.pop(0)

    return (selected_event, normalized_events)

def renderEvents(eventDetailsDraw, mainDraw):
    # get events
    calendar_events = fetch_events()
    processed_events = process_events(calendar_events)
    normalized_events = normalize_events(processed_events)

    # render events
    viewport = {'width': 400, 'height': 300}

    selected_event = normalized_events[0]
    if selected_event is not None:
        mainDraw.line((viewport['width'] / 2, CONFIG['appBar']['height'], viewport['width'] / 2, viewport['height']), fill = FILL_BLACK)
        # renderItemDetails(eventDetailsDraw, selected_event)

    remaining_events = normalized_events[1]
    eventCount = len(remaining_events)
    if eventCount > 1:
        displayCount = min(eventCount, CONFIG['taskItemCount'])
        # renderOneLineList(mainDraw, remaining_events, displayCount)
        renderTwoLinesList(mainDraw, remaining_events, displayCount, viewport['width'] / 2)

try:
    logging.debug("Starting...")
    epd = init()

    mainImage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    mainDraw = ImageDraw.Draw(mainImage)

    eventDetailsImage = Image.new('1', (math.ceil(epd.width / 2) - 1, epd.height - CONFIG['appBar']['height'] - 1), 255)
    eventDetailsDraw = ImageDraw.Draw(eventDetailsImage)

    if 0:
        logging.debug("E-paper refresh")
        epd.init()

        renderWeatherAndDate(mainDraw)
        renderEvents(eventDetailsDraw, mainDraw)
        mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))
        epd.display(epd.getbuffer(mainImage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)

        renderWeatherAndDate(mainDraw)
        renderEvents(eventDetailsDraw, mainDraw)
        mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))
        epd.display_Fast(epd.getbuffer(mainImage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()