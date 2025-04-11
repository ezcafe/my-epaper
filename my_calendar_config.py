#  CHANGE THESE VALUES TO YOUR OWN

WEATHER_API_KEY = 'bd7687c19648b628d77527713a59bc47'
WEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_LATITUDE = '10.7863809'  # Latitude
WEATHER_LONGITUDE = '106.7781079'  # Longitude
WEATHER_UNITS = 'metric' # imperial or metric

TODOIST_API_KEY = ''

UI_MODE = 'normal'  # 'compact' or 'normal'

# DO NOT CHANGE THE FOLLOWING

FILL_BLACK = 0
FILL_WHITE = 1

CONFIG = {
    'compact': {
        'appBarHeight': 56,
        'appBarTitleOffset': 16,
        'taskItemCount': 5,
        'listItemHeight': 48,
        'listItemTitleOffset': 16,
    },
    'normal': {
        'appBarHeight': 64,
        'appBarTitleOffset': 20,
        'taskItemCount': 4,
        'listItemHeight': 56,
        'listItemTitleOffset': 20,
    },
}[UI_MODE]

from PIL import ImageFont
FONTS = {
    'headline': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22),
    'body': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16),
    'support_text': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14),
    'title': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24),
    'weather': ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 24)
}