import logging
import math
import os

import requests
from my_calendar_config import WEATHER_LATITUDE, WEATHER_LONGITUDE, WEATHER_UNITS

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# https://erikflowers.github.io/weather-icons/
# Mapping OpenWeatherMap icon codes to weathericons-regular-webfont text
openweathermap_to_weathericons = {
    "01d": "\uf00d",  # Clear sky (day)
    "01n": "\uf02e",  # Clear sky (night)
    "02d": "\uf002",  # Few clouds (day)
    "02n": "\uf086",  # Few clouds (night)
    "03d": "\uf041",  # Scattered clouds
    "03n": "\uf041",  # Scattered clouds
    "04d": "\uf013",  # Broken clouds
    "04n": "\uf013",  # Broken clouds
    "09d": "\uf019",  # Shower rain
    "09n": "\uf019",  # Shower rain
    "10d": "\uf008",  # Rain (day)
    "10n": "\uf036",  # Rain (night)
    "11d": "\uf01e",  # Thunderstorm
    "11n": "\uf01e",  # Thunderstorm
    "13d": "\uf01b",  # Snow
    "13n": "\uf01b",  # Snow
    "50d": "\uf014",  # Mist
    "50n": "\uf014",  # Mist
}

# Fetch weather data
def fetch_weather_data():
    WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
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
        weather_icon_text = openweathermap_to_weathericons.get(weather_icon_code, "?")  # Default to "?" if not found

        weather_temp_unit = '°'
        if WEATHER_UNITS == "imperial":
            weather_temp_unit = "F"
        weather_temp = f"{math.floor(current['temp'])}{weather_temp_unit}"

        # https://openweathermap.org/current
        weather_data = {
            "temp_current": weather_temp,
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

def get_weather_data():
    try:
        weather_data = fetch_weather_data()
        processed_weather_data = process_weather_data(weather_data)
        return processed_weather_data
    except Exception as e:
        logging.error(f"Error getting weather data: {e}")
        return None