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
    draw.text((48, 18), date, font = fontHeadline, fill = black)
    draw.rectangle((48, 0, 150, 64), outline = 0)
    draw.rectangle((56, 8, 142, 56), outline = 0)
    draw.rectangle((0, 0, 48, 64), outline = 0)
    draw.rectangle((12, 20, 36, 44), outline = 0)

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

        weatherId = data['weather'][0]['id']
        weatherIdToIcon = {
            "200": "storm-showers",
            "201": "storm-showers",
            "202": "storm-showers",
            "210": "storm-showers",
            "211": "thunderstorm",
            "212": "thunderstorm",
            "221": "thunderstorm",
            "230": "storm-showers",
            "231": "storm-showers",
            "232": "storm-showers",
            "300": "sprinkle",
            "301": "sprinkle",
            "302": "sprinkle",
            "310": "sprinkle",
            "311": "sprinkle",
            "312": "sprinkle",
            "313": "sprinkle",
            "314": "sprinkle",
            "321": "sprinkle",
            "500": "rain",
            "501": "rain",
            "502": "rain",
            "503": "rain",
            "504": "rain",
            "511": "rain-mix",
            "520": "showers",
            "521": "showers",
            "522": "showers",
            "531": "showers",
            "600": "snow",
            "601": "snow",
            "602": "snow",
            "611": "sleet",
            "612": "sleet",
            "615": "rain-mix",
            "616": "rain-mix",
            "620": "rain-mix",
            "621": "rain-mix",
            "622": "rain-mix",
            "701": "sprinkle",
            "711": "smoke",
            "721": "day-haze",
            "731": "cloudy-gusts",
            "741": "fog",
            "751": "cloudy-gusts",
            "761": "dust",
            "762": "smog",
            "771": "day-windy",
            "781": "tornado",
            "800": "sunny",
            "801": "cloudy",
            "802": "cloudy",
            "803": "cloudy",
            "804": "cloudy",
            "900": "tornado",
            "901": "hurricane",
            "902": "hurricane",
            "903": "snowflake-cold",
            "904": "hot",
            "905": "windy",
            "906": "hail",
            "951": "sunny",
            "952": "cloudy-gusts",
            "953": "cloudy-gusts",
            "954": "cloudy-gusts",
            "955": "cloudy-gusts",
            "956": "cloudy-gusts",
            "957": "cloudy-gusts",
            "958": "cloudy-gusts",
            "959": "cloudy-gusts",
            "960": "thunderstorm",
            "961": "thunderstorm",
            "962": "cloudy-gusts",
        }
        weatherIcon = weatherIdToIcon[str(weatherId)]
        # If we are not in the ranges mentioned above, add a day/night prefix.
        if not(weatherId > 699 and weatherId < 800) and not(weatherId > 899 and weatherId < 1000):
            weatherIcon = 'day-' + weatherIcon
        # https://erikflowers.github.io/weather-icons/
        weatherIconToText = {
            'day-sunny': "\uf00d",
            'day-cloudy': "\uf002",
            'day-cloudy-gusts': "\uf000",
            'day-cloudy-windy': "\uf001",
            'day-fog': "\uf003",
            'day-hail': "\uf004",
            'day-haze': "\uf0b6",
            'day-lightning': "\uf005",
            'day-rain': "\uf008",
            'day-rain-mix': "\uf006",
            'day-rain-wind': "\uf007",
            'day-showers': "\uf009",
            'day-sleet': "\uf0b2",
            'day-sleet-storm': "\uf068",
            'day-snow': "\uf00a",
            'day-snow-thunderstorm': "\uf06b",
            'day-snow-wind': "\uf065",
            'day-sprinkle': "\uf00b",
            'day-storm-showers': "\uf00e",
            'day-sunny-overcast': "\uf00c",
            'day-thunderstorm': "\uf010",
            'day-windy': "\uf085",
            'solar-eclipse': "\uf06e",
            'hot': "\uf072",
            'day-cloudy-high': "\uf07d",
            'day-light-wind': "\uf0c4",
            'night-clear': "\uf02e",
            'night-alt-cloudy': "\uf086",
            'night-alt-cloudy-gusts': "\uf022",
            'night-alt-cloudy-windy': "\uf023",
            'night-alt-hail': "\uf024",
            'night-alt-lightning': "\uf025",
            'night-alt-rain': "\uf028",
            'night-alt-rain-mix': "\uf026",
            'night-alt-rain-wind': "\uf027",
            'night-alt-showers': "\uf029",
            'night-alt-sleet': "\uf0b4",
            'night-alt-sleet-storm': "\uf06a",
            'night-alt-snow': "\uf02a",
            'night-alt-snow-thunderstorm': "\uf06d",
            'night-alt-snow-wind': "\uf067",
            'night-alt-sprinkle': "\uf02b",
            'night-alt-storm-showers': "\uf02c",
            'night-alt-thunderstorm': "\uf02d",
            'night-cloudy': "\uf031",
            'night-cloudy-gusts': "\uf02f",
            'night-cloudy-windy': "\uf030",
            'night-fog': "\uf04a",
            'night-hail': "\uf032",
            'night-lightning': "\uf033",
            'night-partly-cloudy': "\uf083",
            'night-rain': "\uf036",
            'night-rain-mix': "\uf034",
            'night-rain-wind': "\uf035",
            'night-showers': "\uf037",
            'night-sleet': "\uf0b3",
            'night-sleet-storm': "\uf069",
            'night-snow': "\uf038",
            'night-snow-thunderstorm': "\uf06c",
            'night-snow-wind': "\uf066",
            'night-sprinkle': "\uf039",
            'night-storm-showers': "\uf03a",
            'night-thunderstorm': "\uf03b",
            'lunar-eclipse': "\uf070",
            'stars': "\uf077",
            'storm-showers': "\uf01d",
            'thunderstorm': "\uf01e",
            'night-alt-cloudy-high': "\uf07e",
            'night-cloudy-high': "\uf080",
            'night-alt-partly-cloudy': "\uf081",
            'cloud': "\uf041",
            'cloudy': "\uf013",
            'cloudy-gusts': "\uf011",
            'cloudy-windy': "\uf012",
            'fog': "\uf014",
            'hail': "\uf015",
            'rain': "\uf019",
            'rain-mix': "\uf017",
            'rain-wind': "\uf018",
            'showers': "\uf01a",
            'sleet': "\uf0b5",
            'snow': "\uf01b",
            'sprinkle': "\uf01c",
            'storm-showers': "\uf01d",
            'thunderstorm': "\uf01e",
            'snow-wind': "\uf064",
            'snow': "\uf01b",
            'smog': "\uf074",
            'smoke': "\uf062",
            'lightning': "\uf016",
            'raindrops': "\uf04e",
            'raindrop': "\uf078",
            'dust': "\uf063",
            'snowflake-cold': "\uf076",
            'windy': "\uf021",
            'strong-wind': "\uf050",
            'sandstorm': "\uf082",
            'earthquake': "\uf0c6",
            'fire': "\uf0c7",
            'flood': "\uf07c",
            'meteor': "\uf071",
            'tsunami': "\uf0c5",
            'volcano': "\uf0c8",
            'hurricane': "\uf073",
            'tornado': "\uf056",
            'small-craft-advisory': "\uf0cc",
            'gale-warning': "\uf0cd",
            'storm-warning': "\uf0ce",
            'hurricane-warning': "\uf0cf",
            'wind-direction': "\uf0b1",
            'alien': "\uf075",
            'celsius': "\uf03c",
            'fahrenheit': "\uf045",
            'degrees': "\uf042",
            'thermometer': "\uf055",
            'thermometer-exterior': "\uf053",
            'thermometer-internal': "\uf054",
            'cloud-down': "\uf03d",
            'cloud-up': "\uf040",
            'cloud-refresh': "\uf03e",
            'horizon': "\uf047",
            'horizon-alt': "\uf046",
            'sunrise': "\uf051",
            'sunset': "\uf052",
            'moonrise': "\uf0c9",
            'moonset': "\uf0ca",
            'refresh': "\uf04c",
            'refresh-alt': "\uf04b",
            'umbrella': "\uf084",
            'barometer': "\uf079",
            'humidity': "\uf07a",
            'na': "\uf07b",
            'train': "\uf0cb",
            'moon-new': "\uf095",
            'moon-waxing-crescent-1': "\uf096",
            'moon-waxing-crescent-2': "\uf097",
            'moon-waxing-crescent-3': "\uf098",
            'moon-waxing-crescent-4': "\uf099",
            'moon-waxing-crescent-5': "\uf09a",
            'moon-waxing-crescent-6': "\uf09b",
            'moon-first-quarter': "\uf09c",
            'moon-waxing-gibbous-1': "\uf09d",
            'moon-waxing-gibbous-2': "\uf09e",
            'moon-waxing-gibbous-3': "\uf09f",
            'moon-waxing-gibbous-4': "\uf0a0",
            'moon-waxing-gibbous-5': "\uf0a1",
            'moon-waxing-gibbous-6': "\uf0a2",
            'moon-full': "\uf0a3",
            'moon-waning-gibbous-1': "\uf0a4",
            'moon-waning-gibbous-2': "\uf0a5",
            'moon-waning-gibbous-3': "\uf0a6",
            'moon-waning-gibbous-4': "\uf0a7",
            'moon-waning-gibbous-5': "\uf0a8",
            'moon-waning-gibbous-6': "\uf0a9",
            'moon-third-quarter': "\uf0aa",
            'moon-waning-crescent-1': "\uf0ab",
            'moon-waning-crescent-2': "\uf0ac",
            'moon-waning-crescent-3': "\uf0ad",
            'moon-waning-crescent-4': "\uf0ae",
            'moon-waning-crescent-5': "\uf0af",
            'moon-waning-crescent-6': "\uf0b0",
            'moon-alt-new': "\uf0eb",
            'moon-alt-waxing-crescent-1': "\uf0d0",
            'moon-alt-waxing-crescent-2': "\uf0d1",
            'moon-alt-waxing-crescent-3': "\uf0d2",
            'moon-alt-waxing-crescent-4': "\uf0d3",
            'moon-alt-waxing-crescent-5': "\uf0d4",
            'moon-alt-waxing-crescent-6': "\uf0d5",
            'moon-alt-first-quarter': "\uf0d6",
            'moon-alt-waxing-gibbous-1': "\uf0d7",
            'moon-alt-waxing-gibbous-2': "\uf0d8",
            'moon-alt-waxing-gibbous-3': "\uf0d9",
            'moon-alt-waxing-gibbous-4': "\uf0da",
            'moon-alt-waxing-gibbous-5': "\uf0db",
            'moon-alt-waxing-gibbous-6': "\uf0dc",
            'moon-alt-full': "\uf0dd",
            'moon-alt-waning-gibbous-1': "\uf0de",
            'moon-alt-waning-gibbous-2': "\uf0df",
            'moon-alt-waning-gibbous-3': "\uf0e0",
            'moon-alt-waning-gibbous-4': "\uf0e1",
            'moon-alt-waning-gibbous-5': "\uf0e2",
            'moon-alt-waning-gibbous-6': "\uf0e3",
            'moon-alt-third-quarter': "\uf0e4",
            'moon-alt-waning-crescent-1': "\uf0e5",
            'moon-alt-waning-crescent-2': "\uf0e6",
            'moon-alt-waning-crescent-3': "\uf0e7",
            'moon-alt-waning-crescent-4': "\uf0e8",
            'moon-alt-waning-crescent-5': "\uf0e9",
            'moon-alt-waning-crescent-6': "\uf0ea",
            'moon-0': "\uf095",
            'moon-1': "\uf096",
            'moon-2': "\uf097",
            'moon-3': "\uf098",
            'moon-4': "\uf099",
            'moon-5': "\uf09a",
            'moon-6': "\uf09b",
            'moon-7': "\uf09c",
            'moon-8': "\uf09d",
            'moon-9': "\uf09e",
            'moon-10': "\uf09f",
            'moon-11': "\uf0a0",
            'moon-12': "\uf0a1",
            'moon-13': "\uf0a2",
            'moon-14': "\uf0a3",
            'moon-15': "\uf0a4",
            'moon-16': "\uf0a5",
            'moon-17': "\uf0a6",
            'moon-18': "\uf0a7",
            'moon-19': "\uf0a8",
            'moon-20': "\uf0a9",
            'moon-21': "\uf0aa",
            'moon-22': "\uf0ab",
            'moon-23': "\uf0ac",
            'moon-24': "\uf0ad",
            'moon-25': "\uf0ae",
            'moon-26': "\uf0af",
            'moon-27': "\uf0b0",
            'time-1': "\uf08a",
            'time-2': "\uf08b",
            'time-3': "\uf08c",
            'time-4': "\uf08d",
            'time-5': "\uf08e",
            'time-6': "\uf08f",
            'time-7': "\uf090",
            'time-8': "\uf091",
            'time-9': "\uf092",
            'time-10': "\uf093",
            'time-11': "\uf094",
            'time-12': "\uf089",
            'direction-up': "\uf058",
            'direction-up-right': "\uf057",
            'direction-right': "\uf04d",
            'direction-down-right': "\uf088",
            'direction-down': "\uf044",
            'direction-down-left': "\uf043",
            'direction-left': "\uf048",
            'direction-up-left': "\uf087",
            'wind-beaufort-0': "\uf0b7",
            'wind-beaufort-1': "\uf0b8",
            'wind-beaufort-2': "\uf0b9",
            'wind-beaufort-3': "\uf0ba",
            'wind-beaufort-4': "\uf0bb",
            'wind-beaufort-5': "\uf0bc",
            'wind-beaufort-6': "\uf0bd",
            'wind-beaufort-7': "\uf0be",
            'wind-beaufort-8': "\uf0bf",
            'wind-beaufort-9': "\uf0c0",
            'wind-beaufort-10': "\uf0c1",
            'wind-beaufort-11': "\uf0c2",
            'wind-beaufort-12': "\uf0c3",
            'yahoo-0': "\uf056",
            'yahoo-1': "\uf00e",
            'yahoo-2': "\uf073",
            'yahoo-3': "\uf01e",
            'yahoo-4': "\uf01e",
            'yahoo-5': "\uf017",
            'yahoo-6': "\uf017",
            'yahoo-7': "\uf017",
            'yahoo-8': "\uf015",
            'yahoo-9': "\uf01a",
            'yahoo-10': "\uf015",
            'yahoo-11': "\uf01a",
            'yahoo-12': "\uf01a",
            'yahoo-13': "\uf01b",
            'yahoo-14': "\uf00a",
            'yahoo-15': "\uf064",
            'yahoo-16': "\uf01b",
            'yahoo-17': "\uf015",
            'yahoo-18': "\uf017",
            'yahoo-19': "\uf063",
            'yahoo-20': "\uf014",
            'yahoo-21': "\uf021",
            'yahoo-22': "\uf062",
            'yahoo-23': "\uf050",
            'yahoo-24': "\uf050",
            'yahoo-25': "\uf076",
            'yahoo-26': "\uf013",
            'yahoo-27': "\uf031",
            'yahoo-28': "\uf002",
            'yahoo-29': "\uf031",
            'yahoo-30': "\uf002",
            'yahoo-31': "\uf02e",
            'yahoo-32': "\uf00d",
            'yahoo-33': "\uf083",
            'yahoo-34': "\uf00c",
            'yahoo-35': "\uf017",
            'yahoo-36': "\uf072",
            'yahoo-37': "\uf00e",
            'yahoo-38': "\uf00e",
            'yahoo-39': "\uf00e",
            'yahoo-40': "\uf01a",
            'yahoo-41': "\uf064",
            'yahoo-42': "\uf01b",
            'yahoo-43': "\uf064",
            'yahoo-44': "\uf00c",
            'yahoo-45': "\uf00e",
            'yahoo-46': "\uf01b",
            'yahoo-47': "\uf00e",
            'yahoo-3200': "\uf077",
            'forecast-io-clear-day': "\uf00d",
            'forecast-io-clear-night': "\uf02e",
            'forecast-io-rain': "\uf019",
            'forecast-io-snow': "\uf01b",
            'forecast-io-sleet': "\uf0b5",
            'forecast-io-wind': "\uf050",
            'forecast-io-fog': "\uf014",
            'forecast-io-cloudy': "\uf013",
            'forecast-io-partly-cloudy-day': "\uf002",
            'forecast-io-partly-cloudy-night': "\uf031",
            'forecast-io-hail': "\uf015",
            'forecast-io-thunderstorm': "\uf01e",
            'forecast-io-tornado': "\uf056",
            'wmo4680-0': "\uf055",
            'wmo4680-00': "\uf055",
            'wmo4680-1': "\uf013",
            'wmo4680-01': "\uf013",
            'wmo4680-2': "\uf055",
            'wmo4680-02': "\uf055",
            'wmo4680-3': "\uf013",
            'wmo4680-03': "\uf013",
            'wmo4680-4': "\uf014",
            'wmo4680-04': "\uf014",
            'wmo4680-5': "\uf014",
            'wmo4680-05': "\uf014",
            'wmo4680-10': "\uf014",
            'wmo4680-11': "\uf014",
            'wmo4680-12': "\uf016",
            'wmo4680-18': "\uf050",
            'wmo4680-20': "\uf014",
            'wmo4680-21': "\uf017",
            'wmo4680-22': "\uf017",
            'wmo4680-23': "\uf019",
            'wmo4680-24': "\uf01b",
            'wmo4680-25': "\uf015",
            'wmo4680-26': "\uf01e",
            'wmo4680-27': "\uf063",
            'wmo4680-28': "\uf063",
            'wmo4680-29': "\uf063",
            'wmo4680-30': "\uf014",
            'wmo4680-31': "\uf014",
            'wmo4680-32': "\uf014",
            'wmo4680-33': "\uf014",
            'wmo4680-34': "\uf014",
            'wmo4680-35': "\uf014",
            'wmo4680-40': "\uf017",
            'wmo4680-41': "\uf01c",
            'wmo4680-42': "\uf019",
            'wmo4680-43': "\uf01c",
            'wmo4680-44': "\uf019",
            'wmo4680-45': "\uf015",
            'wmo4680-46': "\uf015",
            'wmo4680-47': "\uf01b",
            'wmo4680-48': "\uf01b",
            'wmo4680-50': "\uf01c",
            'wmo4680-51': "\uf01c",
            'wmo4680-52': "\uf019",
            'wmo4680-53': "\uf019",
            'wmo4680-54': "\uf076",
            'wmo4680-55': "\uf076",
            'wmo4680-56': "\uf076",
            'wmo4680-57': "\uf01c",
            'wmo4680-58': "\uf019",
            'wmo4680-60': "\uf01c",
            'wmo4680-61': "\uf01c",
            'wmo4680-62': "\uf019",
            'wmo4680-63': "\uf019",
            'wmo4680-64': "\uf015",
            'wmo4680-65': "\uf015",
            'wmo4680-66': "\uf015",
            'wmo4680-67': "\uf017",
            'wmo4680-68': "\uf017",
            'wmo4680-70': "\uf01b",
            'wmo4680-71': "\uf01b",
            'wmo4680-72': "\uf01b",
            'wmo4680-73': "\uf01b",
            'wmo4680-74': "\uf076",
            'wmo4680-75': "\uf076",
            'wmo4680-76': "\uf076",
            'wmo4680-77': "\uf01b",
            'wmo4680-78': "\uf076",
            'wmo4680-80': "\uf019",
            'wmo4680-81': "\uf01c",
            'wmo4680-82': "\uf019",
            'wmo4680-83': "\uf019",
            'wmo4680-84': "\uf01d",
            'wmo4680-85': "\uf017",
            'wmo4680-86': "\uf017",
            'wmo4680-87': "\uf017",
            'wmo4680-89': "\uf015",
            'wmo4680-90': "\uf016",
            'wmo4680-91': "\uf01d",
            'wmo4680-92': "\uf01e",
            'wmo4680-93': "\uf01e",
            'wmo4680-94': "\uf016",
            'wmo4680-95': "\uf01e",
            'wmo4680-96': "\uf01e",
            'wmo4680-99': "\uf056",
            'owm-200': "\uf01e",
            'owm-201': "\uf01e",
            'owm-202': "\uf01e",
            'owm-210': "\uf016",
            'owm-211': "\uf016",
            'owm-212': "\uf016",
            'owm-221': "\uf016",
            'owm-230': "\uf01e",
            'owm-231': "\uf01e",
            'owm-232': "\uf01e",
            'owm-300': "\uf01c",
            'owm-301': "\uf01c",
            'owm-302': "\uf019",
            'owm-310': "\uf017",
            'owm-311': "\uf019",
            'owm-312': "\uf019",
            'owm-313': "\uf01a",
            'owm-314': "\uf019",
            'owm-321': "\uf01c",
            'owm-500': "\uf01c",
            'owm-501': "\uf019",
            'owm-502': "\uf019",
            'owm-503': "\uf019",
            'owm-504': "\uf019",
            'owm-511': "\uf017",
            'owm-520': "\uf01a",
            'owm-521': "\uf01a",
            'owm-522': "\uf01a",
            'owm-531': "\uf01d",
            'owm-600': "\uf01b",
            'owm-601': "\uf01b",
            'owm-602': "\uf0b5",
            'owm-611': "\uf017",
            'owm-612': "\uf017",
            'owm-615': "\uf017",
            'owm-616': "\uf017",
            'owm-620': "\uf017",
            'owm-621': "\uf01b",
            'owm-622': "\uf01b",
            'owm-701': "\uf014",
            'owm-711': "\uf062",
            'owm-721': "\uf0b6",
            'owm-731': "\uf063",
            'owm-741': "\uf014",
            'owm-761': "\uf063",
            'owm-762': "\uf063",
            'owm-771': "\uf011",
            'owm-781': "\uf056",
            'owm-800': "\uf00d",
            'owm-801': "\uf041",
            'owm-802': "\uf041",
            'owm-803': "\uf013",
            'owm-804': "\uf013",
            'owm-900': "\uf056",
            'owm-901': "\uf01d",
            'owm-902': "\uf073",
            'owm-903': "\uf076",
            'owm-904': "\uf072",
            'owm-905': "\uf021",
            'owm-906': "\uf015",
            'owm-957': "\uf050",
            'owm-day-200': "\uf010",
            'owm-day-201': "\uf010",
            'owm-day-202': "\uf010",
            'owm-day-210': "\uf005",
            'owm-day-211': "\uf005",
            'owm-day-212': "\uf005",
            'owm-day-221': "\uf005",
            'owm-day-230': "\uf010",
            'owm-day-231': "\uf010",
            'owm-day-232': "\uf010",
            'owm-day-300': "\uf00b",
            'owm-day-301': "\uf00b",
            'owm-day-302': "\uf008",
            'owm-day-310': "\uf008",
            'owm-day-311': "\uf008",
            'owm-day-312': "\uf008",
            'owm-day-313': "\uf008",
            'owm-day-314': "\uf008",
            'owm-day-321': "\uf00b",
            'owm-day-500': "\uf00b",
            'owm-day-501': "\uf008",
            'owm-day-502': "\uf008",
            'owm-day-503': "\uf008",
            'owm-day-504': "\uf008",
            'owm-day-511': "\uf006",
            'owm-day-520': "\uf009",
            'owm-day-521': "\uf009",
            'owm-day-522': "\uf009",
            'owm-day-531': "\uf00e",
            'owm-day-600': "\uf00a",
            'owm-day-601': "\uf0b2",
            'owm-day-602': "\uf00a",
            'owm-day-611': "\uf006",
            'owm-day-612': "\uf006",
            'owm-day-615': "\uf006",
            'owm-day-616': "\uf006",
            'owm-day-620': "\uf006",
            'owm-day-621': "\uf00a",
            'owm-day-622': "\uf00a",
            'owm-day-701': "\uf003",
            'owm-day-711': "\uf062",
            'owm-day-721': "\uf0b6",
            'owm-day-731': "\uf063",
            'owm-day-741': "\uf003",
            'owm-day-761': "\uf063",
            'owm-day-762': "\uf063",
            'owm-day-781': "\uf056",
            'owm-day-800': "\uf00d",
            'owm-day-801': "\uf002",
            'owm-day-802': "\uf002",
            'owm-day-803': "\uf013",
            'owm-day-804': "\uf013",
            'owm-day-900': "\uf056",
            'owm-day-902': "\uf073",
            'owm-day-903': "\uf076",
            'owm-day-904': "\uf072",
            'owm-day-906': "\uf004",
            'owm-day-957': "\uf050",
            'owm-night-200': "\uf02d",
            'owm-night-201': "\uf02d",
            'owm-night-202': "\uf02d",
            'owm-night-210': "\uf025",
            'owm-night-211': "\uf025",
            'owm-night-212': "\uf025",
            'owm-night-221': "\uf025",
            'owm-night-230': "\uf02d",
            'owm-night-231': "\uf02d",
            'owm-night-232': "\uf02d",
            'owm-night-300': "\uf02b",
            'owm-night-301': "\uf02b",
            'owm-night-302': "\uf028",
            'owm-night-310': "\uf028",
            'owm-night-311': "\uf028",
            'owm-night-312': "\uf028",
            'owm-night-313': "\uf028",
            'owm-night-314': "\uf028",
            'owm-night-321': "\uf02b",
            'owm-night-500': "\uf02b",
            'owm-night-501': "\uf028",
            'owm-night-502': "\uf028",
            'owm-night-503': "\uf028",
            'owm-night-504': "\uf028",
            'owm-night-511': "\uf026",
            'owm-night-520': "\uf029",
            'owm-night-521': "\uf029",
            'owm-night-522': "\uf029",
            'owm-night-531': "\uf02c",
            'owm-night-600': "\uf02a",
            'owm-night-601': "\uf0b4",
            'owm-night-602': "\uf02a",
            'owm-night-611': "\uf026",
            'owm-night-612': "\uf026",
            'owm-night-615': "\uf026",
            'owm-night-616': "\uf026",
            'owm-night-620': "\uf026",
            'owm-night-621': "\uf02a",
            'owm-night-622': "\uf02a",
            'owm-night-701': "\uf04a",
            'owm-night-711': "\uf062",
            'owm-night-721': "\uf0b6",
            'owm-night-731': "\uf063",
            'owm-night-741': "\uf04a",
            'owm-night-761': "\uf063",
            'owm-night-762': "\uf063",
            'owm-night-781': "\uf056",
            'owm-night-800': "\uf02e",
            'owm-night-801': "\uf081",
            'owm-night-802': "\uf086",
            'owm-night-803': "\uf013",
            'owm-night-804': "\uf013",
            'owm-night-900': "\uf056",
            'owm-night-902': "\uf073",
            'owm-night-903': "\uf076",
            'owm-night-904': "\uf072",
            'owm-night-906': "\uf024",
            'owm-night-957': "\uf050",
            'wu-chanceflurries': "\uf064",
            'wu-chancerain': "\uf019",
            'wu-chancesleat': "\uf0b5",
            'wu-chancesnow': "\uf01b",
            'wu-chancetstorms': "\uf01e",
            'wu-clear': "\uf00d",
            'wu-cloudy': "\uf002",
            'wu-flurries': "\uf064",
            'wu-hazy': "\uf0b6",
            'wu-mostlycloudy': "\uf002",
            'wu-mostlysunny': "\uf00d",
            'wu-partlycloudy': "\uf002",
            'wu-partlysunny': "\uf00d",
            'wu-rain': "\uf01a",
            'wu-sleat': "\uf0b5",
            'wu-snow': "\uf01b",
            'wu-sunny': "\uf00d",
            'wu-tstorms': "\uf01e",
            'wu-unknown': "\uf00d",
        }

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
        logging.info("Weather data processed successfully.")
        return weather_data
    except KeyError as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def renderWeather(draw):
    # get weather
    data = fetch_weather_data()
    weather_data = process_weather_data(data)

    # render date
    draw.text((12, 18), weather_data['icon_code'], font = fontWeather, fill = black)
    # draw.line((12, 0, 12, 100), fill = 0)

def renderTasks(draw):
    # get tasks
    tasks = ["Prepare runsheet", "Approve TSR", "Ask for conflict approvals"]

    # render tasks
    for j in range(0, len(tasks)):
        draw.text((0, j * 56 + 64 + 15), tasks[j], font = fontBody, fill = black)
        draw.line((0, j * 56 + 64, 150, j * 56 + 64), fill = 0)
        draw.rectangle((8, j * 56 + 64 + 8, 142, j * 56 + 64 + 48), outline = 0)



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