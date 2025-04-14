#  CHANGE THESE VALUES TO YOUR OWN

WEATHER_LATITUDE = '10.7863809'  # Latitude
WEATHER_LONGITUDE = '106.7781079'  # Longitude
WEATHER_UNITS = 'metric' # imperial or metric

UI_MODE = 'compact'  # 'compact' or 'normal'

# DO NOT CHANGE THE FOLLOWING

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

FILL_BLACK = 0
FILL_WHITE = 1

CONFIG = {
    'compact': {
        'appBar': {
            'height': 48,
            'iconSize': 24,
            'paddingLeft': 5,
            'paddingRight': 5,
        },
        'visibleItemCount': 6,
        'listItem': {
            'height': 36,
            'titleHeight': 16,
            'subtitleHeight': 14,
            'linesGap': 2,
            'paddingLeft': 5,
            'paddingRight': 5,
            'paddingTop': 5,
        },
        'calendar': {
            'dateHeight': 100,
            'monthHeight': 22,
            'linesGap': 4,
            'iconSize': 24,
            'paddingRight': 16,
            'paddingTop': 36,
            'specialDayCount': 3,
        },
    },
    'normal': {
        'appBar': {
            'height': 64,
            'iconSize': 24,
            'paddingLeft': 10,
            'paddingRight': 10,
        },
        'visibleItemCount': 4,
        'listItem': {
            'height': 56,
            'titleHeight': 16,
            'subtitleHeight': 14,
            'linesGap': 4,
            'paddingLeft': 16,
            'paddingRight': 16,
            'paddingTop': 16,
        },
        'calendar': {
            'dateHeight': 100,
            'monthHeight': 22,
            'linesGap': 4,
            'iconSize': 24,
            'paddingRight': 16,
            'paddingTop': 36,
            'specialDayCount': 3,
        },
    },
}[UI_MODE]

from PIL import ImageFont
FONTS = {
    'headline': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22),
    'body': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16),
    'support_text': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14),
    'calendar_date': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 100),
    'calendar_month': ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22),
    'weather': ImageFont.truetype(os.path.join(picdir, 'weathericons-regular-webfont.ttf'), 24)
}