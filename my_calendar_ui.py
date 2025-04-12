import logging
from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = False
viewport = {'width': 400, 'height': 300}

def renderAppBar(_draw, icon, text):
    iconPosition = ((48 - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2, (CONFIG['appBar']['height'] - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2)
    titlePosition = CONFIG['appBar']['height'] / 2
    _draw.text(iconPosition, icon, font = FONTS['weather'], fill = FILL_BLACK, anchor = 'mm')
    _draw.text((48, titlePosition), text, font = FONTS['headline'], fill = FILL_BLACK, anchor = 'lm')
    _draw.line((0, CONFIG['appBar']['height'], viewport['width'], CONFIG['appBar']['height']), fill = FILL_BLACK)
    if showBorder:
        _draw.line((0, CONFIG['appBar']['height'] / 2, viewport['width'], CONFIG['appBar']['height'] / 2), fill = FILL_BLACK)
        _draw.line((iconPosition[0], 0, iconPosition[0], CONFIG['appBar']['height']), fill = FILL_BLACK)
        _draw.line((48, 0, 48, CONFIG['appBar']['height']), fill = FILL_BLACK)

def renderOneLineListItem(_draw, item, itemTopPosition):
    itemConfig = CONFIG['listItem']

    _draw.text((16, itemTopPosition + itemConfig['height'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        _draw.text((viewport['width'] - 16, itemTopPosition + itemConfig['height'] / 2), item['timeStart'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    _draw.line((0, itemTopPosition + itemConfig['height'], viewport['width'], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        _draw.line((0, itemTopPosition + itemConfig['height'] / 2, viewport['width'], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
        _draw.line((16, itemTopPosition, 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            _draw.line((viewport['width'] - 16, itemTopPosition, viewport['width'] - 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderOneLineList(_draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        renderOneLineListItem(_draw, items[j], itemTopPosition)

def renderTwoLinesListItem(_draw, item, itemTopPosition ):
    itemConfig = CONFIG['listItem']

    titlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight']/2
    subtitlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight'] + itemConfig['linesGap'] + itemConfig['subtitleHeight']/2
    _draw.text((16, titlePosition), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        _draw.text((viewport['width'] - 48/2, itemTopPosition + itemConfig['height'] / 2), item['timeStart'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
    if item['subtitle'] is not None:
        _draw.text((16, subtitlePosition), item['subtitle'], font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    _draw.line((0, itemTopPosition + itemConfig['height'], viewport['width'], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        _draw.line((0, titlePosition, viewport['width'], titlePosition), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            _draw.line((0, subtitlePosition, viewport['width'], subtitlePosition), fill = FILL_BLACK)
        _draw.line((16, itemTopPosition, 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            _draw.line((viewport['width'] - 48, itemTopPosition + itemConfig['height'] / 2, viewport['width'], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
            _draw.line((viewport['width'] - 48 / 2, itemTopPosition, viewport['width'] - 48 / 2, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderTwoLinesList(_draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        item = items[j]
        if item['subtitle'] is not None:
            renderTwoLinesListItem(_draw, item, itemTopPosition)
        else:
            renderOneLineListItem(_draw, item, itemTopPosition)

def renderItemDetails(_draw, item):
    itemConfig = CONFIG['listItem']

    datePosition = 16
    if item['timeStart'] is not None:
        titlePosition = datePosition + itemConfig['subtitleHeight'] + itemConfig['linesGap']
        dateText = item['timeStart'].strftime('%H:%M')
        if item['timeEnd'] is not None:
            dateText += ' - ' + item['timeEnd'].strftime('%H:%M')
        if dateText == '00:00 - 00:00':
            dateText = 'All Day'
        _draw.text((16, datePosition + itemConfig['subtitleHeight'] / 2), dateText, font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        titlePosition = datePosition

    _draw.text((16, titlePosition + itemConfig['titleHeight'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')

    subtitlePosition = titlePosition + itemConfig['titleHeight'] + itemConfig['linesGap'] *3
    subtitleText = ''
    if item['subtitle'] is not None:
        subtitleText += f"Note: '{item['subtitle']}'"
    if item['location'] is not None:
        subtitleText += f"\nLocation: '{item['location']}'"

    _draw.multiline_text((16, subtitlePosition), subtitleText, font = FONTS['support_text'], fill = FILL_BLACK)

    if showBorder:
        _draw.line((16, 0, 16, viewport['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            _draw.line((16, datePosition + itemConfig['subtitleHeight'] / 2, viewport['width'] / 2, datePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
        _draw.line((16, titlePosition + itemConfig['titleHeight'] / 2, viewport['width'] / 2, titlePosition + itemConfig['titleHeight'] / 2), fill = FILL_BLACK)
        if item['subtitle'] is not None or item['location'] is not None:
            _draw.line((16, subtitlePosition + itemConfig['subtitleHeight'] / 2, viewport['width'] / 2, subtitlePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
