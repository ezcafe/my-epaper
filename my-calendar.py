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
from my_calendar_ui import renderAppBar, renderItemDetails, renderOneLineList, renderTwoLinesList, renderCalendar
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

def select_events(events):
    remaining_events = [event for event in events if not (
        event['timeStart'] and event['timeStart'].strftime('%H:%M') == '00:00' and
        event['timeEnd'] and event['timeEnd'].strftime('%H:%M') == '00:00'
    )]

    selected_event = remaining_events.pop(0) if remaining_events else (events[0] if events else None)

    return selected_event, remaining_events

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
    current_date, selected_event, remaining_events, weather_data = fetch_data()

    renderAppBar(mainDraw, current_date, weather_data)

    viewport_width, viewport_height = mainDraw.im.size
    mainDraw.line(
        (viewport_width / 2, CONFIG['appBar']['height'], viewport_width / 2, viewport_height),
        fill=FILL_BLACK
    )

    if selected_event:
        renderItemDetails(eventDetailsDraw, selected_event)
        renderOneLineList(eventListDraw, remaining_events)
        # renderTwoLinesList(eventListDraw, remaining_events)
    else:
        renderCalendar(mainDraw, current_date, 'TODO', weather_data)

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