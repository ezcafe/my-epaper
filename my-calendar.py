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

import math

from my_calendar_config import CONFIG, FILL_BLACK, WEATHER_LATITUDE, WEATHER_LONGITUDE, WEATHER_UNITS
from my_calendar_ui import renderAppBar, renderItemDetails, renderOneLineList, renderTwoLinesList
from my_calendar_apple import fetch_apple_calendar_events, process_apple_calendar_events
from my_calendar_weather import get_weather_data

# ======= Utils

def init():
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

def renderWeatherAndDate(draw):
    # get weather
    weather_data = get_weather_data()

    # get date
    currentDate = datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    renderAppBar(draw, weather_data, date)

def select_events(events):
    selected_event = None
    remaining_events = []
    for event in events:
        if event['timeStart'] is None or event['timeStart'].strftime('%H:%M') != '00:00' or event['timeEnd'] is None or event['timeEnd'].strftime('%H:%M') != '00:00':
            selected_event = event
        else:
            remaining_events.append(event)

    if selected_event is None:
        selected_event = events[0]
        remaining_events.pop(0)

    return (selected_event, remaining_events)

def renderEvents(mainDraw, eventDetailsDraw, eventListDraw):
    # get events
    calendar_events = fetch_apple_calendar_events()
    processed_events = process_apple_calendar_events(calendar_events)
    remaining_events = select_events(processed_events)

    # render events
    viewport = {'width': 400, 'height': 300}

    selected_event = remaining_events[0]
    if selected_event is not None:
        mainDraw.line((viewport['width'] / 2, CONFIG['appBar']['height'], viewport['width'] / 2, viewport['height']), fill = FILL_BLACK)
        renderItemDetails(eventDetailsDraw, selected_event)

    remaining_events = remaining_events[1]
    eventCount = len(remaining_events)
    logging.debug(f"Event count: {eventCount}")
    if eventCount > 0:
        displayCount = min(eventCount, CONFIG['visibleItemCount'])
        logging.debug(f"Display count: {displayCount}")
        renderOneLineList(eventListDraw, remaining_events, displayCount)
        # renderTwoLinesList(eventListDraw, remaining_events, displayCount)

def fetch_data():
    current_date = datetime.now()

    # Fetch calendar events
    calendar_events = fetch_apple_calendar_events(current_date)
    processed_events = process_apple_calendar_events(calendar_events)
    selected_event, remaining_events = select_events(processed_events)

    # Fetch weather data
    weather_data = get_weather_data()

    return current_date, selected_event, remaining_events, weather_data

def renderUI(mainDraw, eventDetailsDraw, eventListDraw):
    data = fetch_data()
    current_date, selected_event, remaining_events, weather_data = data

    renderWeatherAndDate(mainDraw)
    renderEvents(mainDraw, eventDetailsDraw, eventListDraw)

def mergeImages(mainImage, eventDetailsImage, eventListImage):
    mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))
    mainImage.paste(eventListImage, (math.ceil(epd.width / 2) + 1, CONFIG['appBar']['height'] + 1))

try:
    logging.debug("Starting...")
    epd = init()

    mainImage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    mainDraw = ImageDraw.Draw(mainImage)

    eventDetailsImage = Image.new('1', (math.ceil(epd.width / 2), epd.height - CONFIG['appBar']['height'] - 1), 255)
    eventDetailsDraw = ImageDraw.Draw(eventDetailsImage)

    eventListImage = Image.new('1', (math.ceil(epd.width / 2), epd.height - CONFIG['appBar']['height'] - 1), 255)
    eventListDraw = ImageDraw.Draw(eventListImage)

    if 0:
        logging.debug("E-paper refresh")
        epd.init()
        renderUI(mainDraw, eventDetailsDraw, eventListDraw)
        mergeImages(mainImage, eventDetailsImage, eventListImage)
        epd.display(epd.getbuffer(mainImage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)
        renderUI(mainDraw, eventDetailsDraw, eventListDraw)
        mergeImages(mainImage, eventDetailsImage, eventListImage)
        epd.display_Fast(epd.getbuffer(mainImage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()