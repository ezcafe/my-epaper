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
            'paddingLeft': 10,
            'paddingRight': 10,
        },
        'visibleItemCount': 5,
        'listItem': {
            'height': 36,
            'titleHeight': 16,
            'subtitleHeight': 14,
            'linesGap': 2,
            'paddingLeft': 10,
            'paddingRight': 10,
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
        },
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