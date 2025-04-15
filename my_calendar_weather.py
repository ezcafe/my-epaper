import logging
import math
import os

from dotenv import dotenv_values
import requests
from my_calendar_config import WEATHER_LATITUDE, WEATHER_LONGITUDE, WEATHER_UNITS

base_dir = os.path.dirname(os.path.realpath(__file__))
env_file = os.path.join(base_dir, '.env')
env_config = dotenv_values(env_file)

WEATHER_API_KEY = env_config.get('WEATHER_API_KEY', '')

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
    try:
        WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
        url = f"{WEATHER_BASE_URL}?lat={WEATHER_LATITUDE}&lon={WEATHER_LONGITUDE}&units={WEATHER_UNITS}&appid={WEATHER_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.debug("Weather data fetched successfully.")
        return response.json()
    except requests.Timeout:
        logging.error("Request timed out while fetching weather data.")
        raise
    except requests.RequestException as e:
        logging.error(f"Failed to fetch weather data: {e}")
        raise

# Process weather data
def process_weather_data(data):
    try:
        logging.debug(data)
        weather = data.get('weather', [{}])[0]
        current = data.get('main', {})

        weather_icon_code = weather.get('icon', '')
        weather_icon_text = openweathermap_to_weathericons.get(weather_icon_code, "?")

        temp_unit = "F" if WEATHER_UNITS == "imperial" else "°"
        temp_current = f"{math.floor(current.get('temp', 0))}{temp_unit}"
        feels_like = f"{math.floor(current.get('feels_like', 0))}{temp_unit}"
        temp_max = f"{math.floor(current.get('temp_max', 0))}{temp_unit}"
        temp_min = f"{math.floor(current.get('temp_min', 0))}{temp_unit}"

        weather_data = {
            "temp_current": temp_current,
            "feels_like": feels_like,
            "humidity": current.get('humidity', 0),
            "report": weather.get('description', 'N/A'),
            "icon_code": weather_icon_text,
            "temp_max": temp_max,
            "temp_min": temp_min,
        }
        logging.debug("Weather data processed successfully.")
        return weather_data
    except Exception as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def get_weather_data():
    try:
        return process_weather_data(fetch_weather_data())
    except Exception as e:
        logging.error(f"Error getting weather data: {e}")
        return None
