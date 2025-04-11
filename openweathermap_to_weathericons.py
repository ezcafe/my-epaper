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

def convert_icon_to_weathericon(icon_code):
    """Convert OpenWeatherMap icon code to weathericons-regular-webfont text."""
    return openweathermap_to_weathericons.get(icon_code, "?")  # Default to "?" if not found