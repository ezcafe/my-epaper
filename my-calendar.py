#!/usr/bin/python
# -*- coding:utf-8 -*-

# ======= Config

WEATHER_API_KEY = 'bd7687c19648b628d77527713a59bc47'
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
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
    draw.text((48, 0), date, font = fontHeadline, fill = black)

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
        current = data['main']
        # https://openweathermap.org/current
        weather_data = {
            "temp_current": current['temp'],
            "feels_like": current['feels_like'],
            "humidity": current['humidity'],
            "report": data['weather'][0]['description'],
            "icon_code": data['weather'][0]['id'],
            "temp_max": current['temp_max'],
            "temp_min": current['temp_min'],
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
    logging.info(weather_data['icon_code'])

    weatherIdToIcon = {
        "200": {
            "label": "thunderstorm with light rain",
            "icon": "storm-showers"
        },

        "201": {
            "label": "thunderstorm with rain",
            "icon": "storm-showers"
        },

        "202": {
            "label": "thunderstorm with heavy rain",
            "icon": "storm-showers"
        },

        "210": {
            "label": "light thunderstorm",
            "icon": "storm-showers"
        },

        "211": {
            "label": "thunderstorm",
            "icon": "thunderstorm"
        },

        "212": {
            "label": "heavy thunderstorm",
            "icon": "thunderstorm"
        },

        "221": {
            "label": "ragged thunderstorm",
            "icon": "thunderstorm"
        },

        "230": {
            "label": "thunderstorm with light drizzle",
            "icon": "storm-showers"
        },

        "231": {
            "label": "thunderstorm with drizzle",
            "icon": "storm-showers"
        },

        "232": {
            "label": "thunderstorm with heavy drizzle",
            "icon": "storm-showers"
        },

        "300": {
            "label": "light intensity drizzle",
            "icon": "sprinkle"
        },

        "301": {
            "label": "drizzle",
            "icon": "sprinkle"
        },

        "302": {
            "label": "heavy intensity drizzle",
            "icon": "sprinkle"
        },

        "310": {
            "label": "light intensity drizzle rain",
            "icon": "sprinkle"
        },

        "311": {
            "label": "drizzle rain",
            "icon": "sprinkle"
        },

        "312": {
            "label": "heavy intensity drizzle rain",
            "icon": "sprinkle"
        },

        "313": {
            "label": "shower rain and drizzle",
            "icon": "sprinkle"
        },

        "314": {
            "label": "heavy shower rain and drizzle",
            "icon": "sprinkle"
        },

        "321": {
            "label": "shower drizzle",
            "icon": "sprinkle"
        },

        "500": {
            "label": "light rain",
            "icon": "rain"
        },

        "501": {
            "label": "moderate rain",
            "icon": "rain"
        },

        "502": {
            "label": "heavy intensity rain",
            "icon": "rain"
        },

        "503": {
            "label": "very heavy rain",
            "icon": "rain"
        },

        "504": {
            "label": "extreme rain",
            "icon": "rain"
        },

        "511": {
            "label": "freezing rain",
            "icon": "rain-mix"
        },

        "520": {
            "label": "light intensity shower rain",
            "icon": "showers"
        },

        "521": {
            "label": "shower rain",
            "icon": "showers"
        },

        "522": {
            "label": "heavy intensity shower rain",
            "icon": "showers"
        },

        "531": {
            "label": "ragged shower rain",
            "icon": "showers"
        },

        "600": {
            "label": "light snow",
            "icon": "snow"
        },

        "601": {
            "label": "snow",
            "icon": "snow"
        },

        "602": {
            "label": "heavy snow",
            "icon": "snow"
        },

        "611": {
            "label": "sleet",
            "icon": "sleet"
        },

        "612": {
            "label": "shower sleet",
            "icon": "sleet"
        },

        "615": {
            "label": "light rain and snow",
            "icon": "rain-mix"
        },

        "616": {
            "label": "rain and snow",
            "icon": "rain-mix"
        },

        "620": {
            "label": "light shower snow",
            "icon": "rain-mix"
        },

        "621": {
            "label": "shower snow",
            "icon": "rain-mix"
        },

        "622": {
            "label": "heavy shower snow",
            "icon": "rain-mix"
        },

        "701": {
            "label": "mist",
            "icon": "sprinkle"
        },

        "711": {
            "label": "smoke",
            "icon": "smoke"
        },

        "721": {
            "label": "haze",
            "icon": "day-haze"
        },

        "731": {
            "label": "sand, dust whirls",
            "icon": "cloudy-gusts"
        },

        "741": {
            "label": "fog",
            "icon": "fog"
        },

        "751": {
            "label": "sand",
            "icon": "cloudy-gusts"
        },

        "761": {
            "label": "dust",
            "icon": "dust"
        },

        "762": {
            "label": "volcanic ash",
            "icon": "smog"
        },

        "771": {
            "label": "squalls",
            "icon": "day-windy"
        },

        "781": {
            "label": "tornado",
            "icon": "tornado"
        },

        "800": {
            "label": "clear sky",
            "icon": "sunny"
        },

        "801": {
            "label": "few clouds",
            "icon": "cloudy"
        },

        "802": {
            "label": "scattered clouds",
            "icon": "cloudy"
        },

        "803": {
            "label": "broken clouds",
            "icon": "cloudy"
        },

        "804": {
            "label": "overcast clouds",
            "icon": "cloudy"
        },


        "900": {
            "label": "tornado",
            "icon": "tornado"
        },

        "901": {
            "label": "tropical storm",
            "icon": "hurricane"
        },

        "902": {
            "label": "hurricane",
            "icon": "hurricane"
        },

        "903": {
            "label": "cold",
            "icon": "snowflake-cold"
        },

        "904": {
            "label": "hot",
            "icon": "hot"
        },

        "905": {
            "label": "windy",
            "icon": "windy"
        },

        "906": {
            "label": "hail",
            "icon": "hail"
        },

        "951": {
            "label": "calm",
            "icon": "sunny"
        },

        "952": {
            "label": "light breeze",
            "icon": "cloudy-gusts"
        },

        "953": {
            "label": "gentle breeze",
            "icon": "cloudy-gusts"
        },

        "954": {
            "label": "moderate breeze",
            "icon": "cloudy-gusts"
        },

        "955": {
            "label": "fresh breeze",
            "icon": "cloudy-gusts"
        },

        "956": {
            "label": "strong breeze",
            "icon": "cloudy-gusts"
        },

        "957": {
            "label": "high wind, near gale",
            "icon": "cloudy-gusts"
        },

        "958": {
            "label": "gale",
            "icon": "cloudy-gusts"
        },

        "959": {
            "label": "severe gale",
            "icon": "cloudy-gusts"
        },

        "960": {
            "label": "storm",
            "icon": "thunderstorm"
        },

        "961": {
            "label": "violent storm",
            "icon": "thunderstorm"
        },

        "962": {
            "label": "hurricane",
            "icon": "cloudy-gusts"
        }
        }
    weatherIcon = weatherIdToIcon[weather_data['icon_code']]
    # If we are not in the ranges mentioned above, add a day/night prefix.
    if !(code > 699 && code < 800) && !(code > 899 && code < 1000):
        icon = 'day-' + icon
    weatherIconToText = {
        'day-sunny': "\f00d",
        'day-cloudy': "\f002",
        'day-cloudy-gusts': "\f000",
        'day-cloudy-windy': "\f001",
        'day-fog': "\f003",
        'day-hail': "\f004",
        'day-haze': "\f0b6",
        'day-lightning': "\f005",
        'day-rain': "\f008",
        'day-rain-mix': "\f006",
        'day-rain-wind': "\f007",
        'day-showers': "\f009",
        'day-sleet': "\f0b2",
        'day-sleet-storm': "\f068",
        'day-snow': "\f00a",
        'day-snow-thunderstorm': "\f06b",
        'day-snow-wind': "\f065",
        'day-sprinkle': "\f00b",
        'day-storm-showers': "\f00e",
        'day-sunny-overcast': "\f00c",
        'day-thunderstorm': "\f010",
        'day-windy': "\f085",
        'solar-eclipse': "\f06e",
        'hot': "\f072",
        'day-cloudy-high': "\f07d",
        'day-light-wind': "\f0c4",
        'night-clear': "\f02e",
        'night-alt-cloudy': "\f086",
        'night-alt-cloudy-gusts': "\f022",
        'night-alt-cloudy-windy': "\f023",
        'night-alt-hail': "\f024",
        'night-alt-lightning': "\f025",
        'night-alt-rain': "\f028",
        'night-alt-rain-mix': "\f026",
        'night-alt-rain-wind': "\f027",
        'night-alt-showers': "\f029",
        'night-alt-sleet': "\f0b4",
        'night-alt-sleet-storm': "\f06a",
        'night-alt-snow': "\f02a",
        'night-alt-snow-thunderstorm': "\f06d",
        'night-alt-snow-wind': "\f067",
        'night-alt-sprinkle': "\f02b",
        'night-alt-storm-showers': "\f02c",
        'night-alt-thunderstorm': "\f02d",
        'night-cloudy': "\f031",
        'night-cloudy-gusts': "\f02f",
        'night-cloudy-windy': "\f030",
        'night-fog': "\f04a",
        'night-hail': "\f032",
        'night-lightning': "\f033",
        'night-partly-cloudy': "\f083",
        'night-rain': "\f036",
        'night-rain-mix': "\f034",
        'night-rain-wind': "\f035",
        'night-showers': "\f037",
        'night-sleet': "\f0b3",
        'night-sleet-storm': "\f069",
        'night-snow': "\f038",
        'night-snow-thunderstorm': "\f06c",
        'night-snow-wind': "\f066",
        'night-sprinkle': "\f039",
        'night-storm-showers': "\f03a",
        'night-thunderstorm': "\f03b",
        'lunar-eclipse': "\f070",
        'stars': "\f077",
        'storm-showers': "\f01d",
        'thunderstorm': "\f01e",
        'night-alt-cloudy-high': "\f07e",
        'night-cloudy-high': "\f080",
        'night-alt-partly-cloudy': "\f081",
        'cloud': "\f041",
        'cloudy': "\f013",
        'cloudy-gusts': "\f011",
        'cloudy-windy': "\f012",
        'fog': "\f014",
        'hail': "\f015",
        'rain': "\f019",
        'rain-mix': "\f017",
        'rain-wind': "\f018",
        'showers': "\f01a",
        'sleet': "\f0b5",
        'snow': "\f01b",
        'sprinkle': "\f01c",
        'storm-showers': "\f01d",
        'thunderstorm': "\f01e",
        'snow-wind': "\f064",
        'snow': "\f01b",
        'smog': "\f074",
        'smoke': "\f062",
        'lightning': "\f016",
        'raindrops': "\f04e",
        'raindrop': "\f078",
        'dust': "\f063",
        'snowflake-cold': "\f076",
        'windy': "\f021",
        'strong-wind': "\f050",
        'sandstorm': "\f082",
        'earthquake': "\f0c6",
        'fire': "\f0c7",
        'flood': "\f07c",
        'meteor': "\f071",
        'tsunami': "\f0c5",
        'volcano': "\f0c8",
        'hurricane': "\f073",
        'tornado': "\f056",
        'small-craft-advisory': "\f0cc",
        'gale-warning': "\f0cd",
        'storm-warning': "\f0ce",
        'hurricane-warning': "\f0cf",
        'wind-direction': "\f0b1",
        'alien': "\f075",
        'celsius': "\f03c",
        'fahrenheit': "\f045",
        'degrees': "\f042",
        'thermometer': "\f055",
        'thermometer-exterior': "\f053",
        'thermometer-internal': "\f054",
        'cloud-down': "\f03d",
        'cloud-up': "\f040",
        'cloud-refresh': "\f03e",
        'horizon': "\f047",
        'horizon-alt': "\f046",
        'sunrise': "\f051",
        'sunset': "\f052",
        'moonrise': "\f0c9",
        'moonset': "\f0ca",
        'refresh': "\f04c",
        'refresh-alt': "\f04b",
        'umbrella': "\f084",
        'barometer': "\f079",
        'humidity': "\f07a",
        'na': "\f07b",
        'train': "\f0cb",
        'moon-new': "\f095",
        'moon-waxing-crescent-1': "\f096",
        'moon-waxing-crescent-2': "\f097",
        'moon-waxing-crescent-3': "\f098",
        'moon-waxing-crescent-4': "\f099",
        'moon-waxing-crescent-5': "\f09a",
        'moon-waxing-crescent-6': "\f09b",
        'moon-first-quarter': "\f09c",
        'moon-waxing-gibbous-1': "\f09d",
        'moon-waxing-gibbous-2': "\f09e",
        'moon-waxing-gibbous-3': "\f09f",
        'moon-waxing-gibbous-4': "\f0a0",
        'moon-waxing-gibbous-5': "\f0a1",
        'moon-waxing-gibbous-6': "\f0a2",
        'moon-full': "\f0a3",
        'moon-waning-gibbous-1': "\f0a4",
        'moon-waning-gibbous-2': "\f0a5",
        'moon-waning-gibbous-3': "\f0a6",
        'moon-waning-gibbous-4': "\f0a7",
        'moon-waning-gibbous-5': "\f0a8",
        'moon-waning-gibbous-6': "\f0a9",
        'moon-third-quarter': "\f0aa",
        'moon-waning-crescent-1': "\f0ab",
        'moon-waning-crescent-2': "\f0ac",
        'moon-waning-crescent-3': "\f0ad",
        'moon-waning-crescent-4': "\f0ae",
        'moon-waning-crescent-5': "\f0af",
        'moon-waning-crescent-6': "\f0b0",
        'moon-alt-new': "\f0eb",
        'moon-alt-waxing-crescent-1': "\f0d0",
        'moon-alt-waxing-crescent-2': "\f0d1",
        'moon-alt-waxing-crescent-3': "\f0d2",
        'moon-alt-waxing-crescent-4': "\f0d3",
        'moon-alt-waxing-crescent-5': "\f0d4",
        'moon-alt-waxing-crescent-6': "\f0d5",
        'moon-alt-first-quarter': "\f0d6",
        'moon-alt-waxing-gibbous-1': "\f0d7",
        'moon-alt-waxing-gibbous-2': "\f0d8",
        'moon-alt-waxing-gibbous-3': "\f0d9",
        'moon-alt-waxing-gibbous-4': "\f0da",
        'moon-alt-waxing-gibbous-5': "\f0db",
        'moon-alt-waxing-gibbous-6': "\f0dc",
        'moon-alt-full': "\f0dd",
        'moon-alt-waning-gibbous-1': "\f0de",
        'moon-alt-waning-gibbous-2': "\f0df",
        'moon-alt-waning-gibbous-3': "\f0e0",
        'moon-alt-waning-gibbous-4': "\f0e1",
        'moon-alt-waning-gibbous-5': "\f0e2",
        'moon-alt-waning-gibbous-6': "\f0e3",
        'moon-alt-third-quarter': "\f0e4",
        'moon-alt-waning-crescent-1': "\f0e5",
        'moon-alt-waning-crescent-2': "\f0e6",
        'moon-alt-waning-crescent-3': "\f0e7",
        'moon-alt-waning-crescent-4': "\f0e8",
        'moon-alt-waning-crescent-5': "\f0e9",
        'moon-alt-waning-crescent-6': "\f0ea",
        'moon-0': "\f095",
        'moon-1': "\f096",
        'moon-2': "\f097",
        'moon-3': "\f098",
        'moon-4': "\f099",
        'moon-5': "\f09a",
        'moon-6': "\f09b",
        'moon-7': "\f09c",
        'moon-8': "\f09d",
        'moon-9': "\f09e",
        'moon-10': "\f09f",
        'moon-11': "\f0a0",
        'moon-12': "\f0a1",
        'moon-13': "\f0a2",
        'moon-14': "\f0a3",
        'moon-15': "\f0a4",
        'moon-16': "\f0a5",
        'moon-17': "\f0a6",
        'moon-18': "\f0a7",
        'moon-19': "\f0a8",
        'moon-20': "\f0a9",
        'moon-21': "\f0aa",
        'moon-22': "\f0ab",
        'moon-23': "\f0ac",
        'moon-24': "\f0ad",
        'moon-25': "\f0ae",
        'moon-26': "\f0af",
        'moon-27': "\f0b0",
        'time-1': "\f08a",
        'time-2': "\f08b",
        'time-3': "\f08c",
        'time-4': "\f08d",
        'time-5': "\f08e",
        'time-6': "\f08f",
        'time-7': "\f090",
        'time-8': "\f091",
        'time-9': "\f092",
        'time-10': "\f093",
        'time-11': "\f094",
        'time-12': "\f089",
        'direction-up': "\f058",
        'direction-up-right': "\f057",
        'direction-right': "\f04d",
        'direction-down-right': "\f088",
        'direction-down': "\f044",
        'direction-down-left': "\f043",
        'direction-left': "\f048",
        'direction-up-left': "\f087",
        'wind-beaufort-0': "\f0b7",
        'wind-beaufort-1': "\f0b8",
        'wind-beaufort-2': "\f0b9",
        'wind-beaufort-3': "\f0ba",
        'wind-beaufort-4': "\f0bb",
        'wind-beaufort-5': "\f0bc",
        'wind-beaufort-6': "\f0bd",
        'wind-beaufort-7': "\f0be",
        'wind-beaufort-8': "\f0bf",
        'wind-beaufort-9': "\f0c0",
        'wind-beaufort-10': "\f0c1",
        'wind-beaufort-11': "\f0c2",
        'wind-beaufort-12': "\f0c3",
        'yahoo-0': "\f056",
        'yahoo-1': "\f00e",
        'yahoo-2': "\f073",
        'yahoo-3': "\f01e",
        'yahoo-4': "\f01e",
        'yahoo-5': "\f017",
        'yahoo-6': "\f017",
        'yahoo-7': "\f017",
        'yahoo-8': "\f015",
        'yahoo-9': "\f01a",
        'yahoo-10': "\f015",
        'yahoo-11': "\f01a",
        'yahoo-12': "\f01a",
        'yahoo-13': "\f01b",
        'yahoo-14': "\f00a",
        'yahoo-15': "\f064",
        'yahoo-16': "\f01b",
        'yahoo-17': "\f015",
        'yahoo-18': "\f017",
        'yahoo-19': "\f063",
        'yahoo-20': "\f014",
        'yahoo-21': "\f021",
        'yahoo-22': "\f062",
        'yahoo-23': "\f050",
        'yahoo-24': "\f050",
        'yahoo-25': "\f076",
        'yahoo-26': "\f013",
        'yahoo-27': "\f031",
        'yahoo-28': "\f002",
        'yahoo-29': "\f031",
        'yahoo-30': "\f002",
        'yahoo-31': "\f02e",
        'yahoo-32': "\f00d",
        'yahoo-33': "\f083",
        'yahoo-34': "\f00c",
        'yahoo-35': "\f017",
        'yahoo-36': "\f072",
        'yahoo-37': "\f00e",
        'yahoo-38': "\f00e",
        'yahoo-39': "\f00e",
        'yahoo-40': "\f01a",
        'yahoo-41': "\f064",
        'yahoo-42': "\f01b",
        'yahoo-43': "\f064",
        'yahoo-44': "\f00c",
        'yahoo-45': "\f00e",
        'yahoo-46': "\f01b",
        'yahoo-47': "\f00e",
        'yahoo-3200': "\f077",
        'forecast-io-clear-day': "\f00d",
        'forecast-io-clear-night': "\f02e",
        'forecast-io-rain': "\f019",
        'forecast-io-snow': "\f01b",
        'forecast-io-sleet': "\f0b5",
        'forecast-io-wind': "\f050",
        'forecast-io-fog': "\f014",
        'forecast-io-cloudy': "\f013",
        'forecast-io-partly-cloudy-day': "\f002",
        'forecast-io-partly-cloudy-night': "\f031",
        'forecast-io-hail': "\f015",
        'forecast-io-thunderstorm': "\f01e",
        'forecast-io-tornado': "\f056",
        'wmo4680-0': "\f055",
        'wmo4680-00': "\f055",
        'wmo4680-1': "\f013",
        'wmo4680-01': "\f013",
        'wmo4680-2': "\f055",
        'wmo4680-02': "\f055"
        'wmo4680-3': "\f013",
        'wmo4680-03': "\f013",
        'wmo4680-4': "\f014",
        'wmo4680-04': "\f014",
        'wmo4680-5': "\f014",
        'wmo4680-05': "\f014",
        'wmo4680-10': "\f014",
        'wmo4680-11': "\f014",
        'wmo4680-12': "\f016",
        'wmo4680-18': "\f050",
        'wmo4680-20': "\f014",
        'wmo4680-21': "\f017",
        'wmo4680-22': "\f017",
        'wmo4680-23': "\f019",
        'wmo4680-24': "\f01b",
        'wmo4680-25': "\f015",
        'wmo4680-26': "\f01e",
        'wmo4680-27': "\f063",
        'wmo4680-28': "\f063",
        'wmo4680-29': "\f063",
        'wmo4680-30': "\f014",
        'wmo4680-31': "\f014",
        'wmo4680-32': "\f014",
        'wmo4680-33': "\f014",
        'wmo4680-34': "\f014",
        'wmo4680-35': "\f014",
        'wmo4680-40': "\f017",
        'wmo4680-41': "\f01c",
        'wmo4680-42': "\f019",
        'wmo4680-43': "\f01c",
        'wmo4680-44': "\f019",
        'wmo4680-45': "\f015",
        'wmo4680-46': "\f015",
        'wmo4680-47': "\f01b",
        'wmo4680-48': "\f01b",
        'wmo4680-50': "\f01c",
        'wmo4680-51': "\f01c",
        'wmo4680-52': "\f019",
        'wmo4680-53': "\f019",
        'wmo4680-54': "\f076",
        'wmo4680-55': "\f076",
        'wmo4680-56': "\f076",
        'wmo4680-57': "\f01c",
        'wmo4680-58': "\f019",
        'wmo4680-60': "\f01c",
        'wmo4680-61': "\f01c",
        'wmo4680-62': "\f019",
        'wmo4680-63': "\f019",
        'wmo4680-64': "\f015",
        'wmo4680-65': "\f015",
        'wmo4680-66': "\f015",
        'wmo4680-67': "\f017",
        'wmo4680-68': "\f017",
        'wmo4680-70': "\f01b",
        'wmo4680-71': "\f01b",
        'wmo4680-72': "\f01b",
        'wmo4680-73': "\f01b",
        'wmo4680-74': "\f076",
        'wmo4680-75': "\f076",
        'wmo4680-76': "\f076",
        'wmo4680-77': "\f01b",
        'wmo4680-78': "\f076",
        'wmo4680-80': "\f019",
        'wmo4680-81': "\f01c",
        'wmo4680-82': "\f019",
        'wmo4680-83': "\f019",
        'wmo4680-84': "\f01d",
        'wmo4680-85': "\f017",
        'wmo4680-86': "\f017",
        'wmo4680-87': "\f017",
        'wmo4680-89': "\f015",
        'wmo4680-90': "\f016",
        'wmo4680-91': "\f01d",
        'wmo4680-92': "\f01e",
        'wmo4680-93': "\f01e",
        'wmo4680-94': "\f016",
        'wmo4680-95': "\f01e",
        'wmo4680-96': "\f01e",
        'wmo4680-99': "\f056",
        'owm-200': "\f01e",
        'owm-201': "\f01e",
        'owm-202': "\f01e",
        'owm-210': "\f016",
        'owm-211': "\f016",
        'owm-212': "\f016",
        'owm-221': "\f016",
        'owm-230': "\f01e",
        'owm-231': "\f01e",
        'owm-232': "\f01e",
        'owm-300': "\f01c",
        'owm-301': "\f01c",
        'owm-302': "\f019",
        'owm-310': "\f017",
        'owm-311': "\f019",
        'owm-312': "\f019",
        'owm-313': "\f01a",
        'owm-314': "\f019",
        'owm-321': "\f01c",
        'owm-500': "\f01c",
        'owm-501': "\f019",
        'owm-502': "\f019",
        'owm-503': "\f019",
        'owm-504': "\f019",
        'owm-511': "\f017",
        'owm-520': "\f01a",
        'owm-521': "\f01a",
        'owm-522': "\f01a",
        'owm-531': "\f01d",
        'owm-600': "\f01b",
        'owm-601': "\f01b",
        'owm-602': "\f0b5",
        'owm-611': "\f017",
        'owm-612': "\f017",
        'owm-615': "\f017",
        'owm-616': "\f017",
        'owm-620': "\f017",
        'owm-621': "\f01b",
        'owm-622': "\f01b",
        'owm-701': "\f014",
        'owm-711': "\f062",
        'owm-721': "\f0b6",
        'owm-731': "\f063",
        'owm-741': "\f014",
        'owm-761': "\f063",
        'owm-762': "\f063",
        'owm-771': "\f011",
        'owm-781': "\f056",
        'owm-800': "\f00d",
        'owm-801': "\f041",
        'owm-802': "\f041",
        'owm-803': "\f013",
        'owm-804': "\f013",
        'owm-900': "\f056",
        'owm-901': "\f01d",
        'owm-902': "\f073",
        'owm-903': "\f076",
        'owm-904': "\f072",
        'owm-905': "\f021",
        'owm-906': "\f015",
        'owm-957': "\f050",
        'owm-day-200': "\f010",
        'owm-day-201': "\f010",
        'owm-day-202': "\f010",
        'owm-day-210': "\f005",
        'owm-day-211': "\f005",
        'owm-day-212': "\f005",
        'owm-day-221': "\f005",
        'owm-day-230': "\f010",
        'owm-day-231': "\f010",
        'owm-day-232': "\f010",
        'owm-day-300': "\f00b",
        'owm-day-301': "\f00b",
        'owm-day-302': "\f008",
        'owm-day-310': "\f008",
        'owm-day-311': "\f008",
        'owm-day-312': "\f008",
        'owm-day-313': "\f008",
        'owm-day-314': "\f008",
        'owm-day-321': "\f00b",
        'owm-day-500': "\f00b",
        'owm-day-501': "\f008",
        'owm-day-502': "\f008",
        'owm-day-503': "\f008",
        'owm-day-504': "\f008",
        'owm-day-511': "\f006",
        'owm-day-520': "\f009",
        'owm-day-521': "\f009",
        'owm-day-522': "\f009",
        'owm-day-531': "\f00e",
        'owm-day-600': "\f00a",
        'owm-day-601': "\f0b2",
        'owm-day-602': "\f00a",
        'owm-day-611': "\f006",
        'owm-day-612': "\f006",
        'owm-day-615': "\f006",
        'owm-day-616': "\f006",
        'owm-day-620': "\f006",
        'owm-day-621': "\f00a",
        'owm-day-622': "\f00a",
        'owm-day-701': "\f003",
        'owm-day-711': "\f062",
        'owm-day-721': "\f0b6",
        'owm-day-731': "\f063",
        'owm-day-741': "\f003",
        'owm-day-761': "\f063",
        'owm-day-762': "\f063",
        'owm-day-781': "\f056",
        'owm-day-800': "\f00d",
        'owm-day-801': "\f002",
        'owm-day-802': "\f002",
        'owm-day-803': "\f013",
        'owm-day-804': "\f013",
        'owm-day-900': "\f056",
        'owm-day-902': "\f073",
        'owm-day-903': "\f076",
        'owm-day-904': "\f072",
        'owm-day-906': "\f004",
        'owm-day-957': "\f050",
        'owm-night-200': "\f02d",
        'owm-night-201': "\f02d",
        'owm-night-202': "\f02d",
        'owm-night-210': "\f025",
        'owm-night-211': "\f025",
        'owm-night-212': "\f025",
        'owm-night-221': "\f025",
        'owm-night-230': "\f02d",
        'owm-night-231': "\f02d",
        'owm-night-232': "\f02d",
        'owm-night-300': "\f02b",
        'owm-night-301': "\f02b",
        'owm-night-302': "\f028",
        'owm-night-310': "\f028",
        'owm-night-311': "\f028",
        'owm-night-312': "\f028",
        'owm-night-313': "\f028",
        'owm-night-314': "\f028",
        'owm-night-321': "\f02b",
        'owm-night-500': "\f02b",
        'owm-night-501': "\f028",
        'owm-night-502': "\f028",
        'owm-night-503': "\f028",
        'owm-night-504': "\f028",
        'owm-night-511': "\f026",
        'owm-night-520': "\f029",
        'owm-night-521': "\f029",
        'owm-night-522': "\f029",
        'owm-night-531': "\f02c",
        'owm-night-600': "\f02a",
        'owm-night-601': "\f0b4",
        'owm-night-602': "\f02a",
        'owm-night-611': "\f026",
        'owm-night-612': "\f026",
        'owm-night-615': "\f026",
        'owm-night-616': "\f026",
        'owm-night-620': "\f026",
        'owm-night-621': "\f02a",
        'owm-night-622': "\f02a",
        'owm-night-701': "\f04a",
        'owm-night-711': "\f062",
        'owm-night-721': "\f0b6",
        'owm-night-731': "\f063",
        'owm-night-741': "\f04a",
        'owm-night-761': "\f063",
        'owm-night-762': "\f063",
        'owm-night-781': "\f056",
        'owm-night-800': "\f02e",
        'owm-night-801': "\f081",
        'owm-night-802': "\f086",
        'owm-night-803': "\f013",
        'owm-night-804': "\f013",
        'owm-night-900': "\f056",
        'owm-night-902': "\f073",
        'owm-night-903': "\f076",
        'owm-night-904': "\f072",
        'owm-night-906': "\f024",
        'owm-night-957': "\f050",
        'wu-chanceflurries': "\f064",
        'wu-chancerain': "\f019",
        'wu-chancesleat': "\f0b5",
        'wu-chancesnow': "\f01b",
        'wu-chancetstorms': "\f01e",
        'wu-clear': "\f00d",
        'wu-cloudy': "\f002",
        'wu-flurries': "\f064",
        'wu-hazy': "\f0b6",
        'wu-mostlycloudy': "\f002",
        'wu-mostlysunny': "\f00d",
        'wu-partlycloudy': "\f002",
        'wu-partlysunny': "\f00d",
        'wu-rain': "\f01a",
        'wu-sleat': "\f0b5",
        'wu-snow': "\f01b",
        'wu-sunny': "\f00d",
        'wu-tstorms': "\f01e",
        'wu-unknown': "\f00d",
    }

    logging.info(weatherIcon)
    logging.info(weatherIconToText[weatherIcon])

    # render date https://erikflowers.github.io/weather-icons/
    draw.text((0, 0), weatherIconMapping[weather_data['icon_code']], font = fontWeather, fill = black)

def renderTasks(draw):
    # get tasks
    tasks = ["Ford", "Volvo", "BMW"]

    # render tasks
    for j in range(0, len(tasks)):
        draw.text((0, j * 16 + 64), tasks[j], font = fontBody, fill = black)

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