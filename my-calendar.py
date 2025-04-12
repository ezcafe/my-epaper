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
from my_calendar_weather import fetch_weather_data, process_weather_data

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
    data = fetch_weather_data()
    weather_data = process_weather_data(data)

    # get date
    currentDate = datetime.now()
    date = currentDate.strftime('%A, %d/%m')

    # render date
    renderAppBar(draw, weather_data, date)

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

def renderEvents(mainDraw, eventDetailsDraw, eventListDraw):
    # get events
    calendar_events = fetch_apple_calendar_events()
    processed_events = process_apple_calendar_events(calendar_events)
    normalized_events = normalize_events(processed_events)

    # render events
    viewport = {'width': 400, 'height': 300}

    selected_event = normalized_events[0]
    if selected_event is not None:
        mainDraw.line((viewport['width'] / 2, CONFIG['appBar']['height'], viewport['width'] / 2, viewport['height']), fill = FILL_BLACK)
        renderItemDetails(eventDetailsDraw, selected_event)

    remaining_events = normalized_events[1]
    eventCount = len(remaining_events)
    logging.debug(f"Event count: {eventCount}")
    if eventCount > 0:
        displayCount = min(eventCount, CONFIG['visibleItemCount'])
        logging.debug(f"Display count: {displayCount}")
        renderOneLineList(eventListDraw, remaining_events, displayCount)
        # renderTwoLinesList(eventListDraw, remaining_events, displayCount)

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

        renderWeatherAndDate(mainDraw)
        renderEvents(mainDraw, eventDetailsDraw, eventListDraw)
        mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))
        mainImage.paste(eventListImage, (math.ceil(epd.width / 2) + 1, CONFIG['appBar']['height'] + 1))
        epd.display(epd.getbuffer(mainImage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)

        renderWeatherAndDate(mainDraw)
        renderEvents(mainDraw, eventDetailsDraw, eventListDraw)
        mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))
        mainImage.paste(eventListImage, (math.ceil(epd.width / 2) + 1, CONFIG['appBar']['height'] + 1))
        epd.display_Fast(epd.getbuffer(mainImage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()