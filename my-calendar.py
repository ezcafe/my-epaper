#!/usr/bin/python
# -*- coding:utf-8 -*-

# ======= Import
import sys
import os
base_dir = os.path.dirname(os.path.realpath(__file__))
picdir = os.path.join(base_dir, 'pic')
libdir = os.path.join(base_dir, 'lib')
if os.path.isdir(libdir):
    sys.path.append(libdir)

from dotenv import dotenv_values
import logging
from waveshare_epd import epd4in2_V2
import time
import json
from PIL import Image
import traceback

logging.basicConfig(level=logging.DEBUG)

from datetime import datetime, timedelta

from my_calendar_config import CONFIG
from my_calendar_ui import renderEventUI, renderCalendarUI
from my_calendar_apple import fetch_apple_calendar_events, process_apple_calendar_events
from my_calendar_weather import get_weather_data

env_config = dotenv_values(".env")
SPECIAL_DAYS = env_config.get('SPECIAL_DAYS', '[]')

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

def get_time_difference(date1, date2):
    """
    Calculate the difference between two dates.
    If the difference is less than 1 day, return the difference in hours or minutes.
    """
    delta = date2 - date1
    days = delta.days
    seconds = delta.total_seconds()

    if days >= 1:
        return f"{days} day(s)"
    elif seconds >= 3600:
        hours = seconds // 3600
        return f"{int(hours)} hour(s)"
    else:
        minutes = seconds // 60
        return f"{int(minutes)} minute(s)"

def get_extra_text(current_date):
    extra_text = ""

    try:
        special_days = json.loads(SPECIAL_DAYS)
        sorted_days = []

        for name, date_str in special_days:
            # Handle day-only (e.g., "25") or full date (e.g., "22/12")
            if "/" in date_str:
                day, month = map(int, date_str.split("/"))
                special_date = datetime(current_date.year, month, day)
                # Adjust for past dates in the current year
                if special_date < current_date:
                    special_date = special_date.replace(year=current_date.year + 1)
            else:
                special_date = current_date.replace(day=int(date_str))
                if special_date < current_date:
                    special_date = special_date.replace(month=current_date.month + 1)

            sorted_days.append((name, special_date))

        # Sort special days by their time difference from the current date
        sorted_days.sort(key=lambda x: x[1] - current_date)

        # Generate the extra text for top 3 special days
        specialDayCount = CONFIG['calendar']['specialDayCount']
        for name, special_date in sorted_days[:specialDayCount]:  # Limit to top 3
            time_difference = get_time_difference(current_date, special_date)
            extra_text += f"{name} in {time_difference}\n"

    except Exception as e:
        logging.error(f"Error parsing SPECIAL_DAYS: {e}")

    return extra_text

def renderUI(mainImage):
    data = fetch_data()
    current_date, selected_event, remaining_events, weather_data = data

    logging.debug(f"selected_event: {selected_event}")
    if selected_event:
        logging.debug("Rendering Event UI")
        renderEventUI(mainImage, data)
    else:
        logging.debug("Rendering Calendar UI")
        extra_text = get_extra_text(current_date)
        renderCalendarUI(mainImage, current_date, extra_text, weather_data)

try:
    logging.debug("Starting...")
    epd = init()

    mainImage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

    if 0:
        logging.debug("E-paper refresh")
        epd.init()
        renderUI(mainImage)
        epd.display(epd.getbuffer(mainImage))
        time.sleep(2)
    else:
        logging.debug("E-paper refreshes quickly")
        epd.init_fast(epd.Seconds_1_5S)
        renderUI(mainImage)
        epd.display_Fast(epd.getbuffer(mainImage))
        time.sleep(2)

    go_to_sleep(epd)

except IOError as e:
    logging.debug("Error:")
    on_error(e)

except KeyboardInterrupt:
    logging.debug("Ctrl + c:")
    on_exit()