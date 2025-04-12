import logging
from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = False
viewport = {'width': 400, 'height': 300}

def renderAppBar(draw, icon, text):
    iconPosition = ((48 - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2, (CONFIG['appBar']['height'] - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2)
    titlePosition = CONFIG['appBar']['height'] / 2
    draw.text(iconPosition, icon, font = FONTS['weather'], fill = FILL_BLACK, anchor = 'mm')
    draw.text((48, titlePosition), text, font = FONTS['headline'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((0, CONFIG['appBar']['height'], viewport['width'], CONFIG['appBar']['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, CONFIG['appBar']['height'] / 2, viewport['width'], CONFIG['appBar']['height'] / 2), fill = FILL_BLACK)
        draw.line((iconPosition[0], 0, iconPosition[0], CONFIG['appBar']['height']), fill = FILL_BLACK)
        draw.line((48, 0, 48, CONFIG['appBar']['height']), fill = FILL_BLACK)

def renderOneLineListItem(draw, item, itemTopPosition, itemLeftPosition = 0):
    itemConfig = CONFIG['listItem']

    draw.text((itemLeftPosition + 16, itemTopPosition + itemConfig['height'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((viewport['width'] - 48/2, itemTopPosition + itemConfig['height'] / 2), item['timeStart'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
    draw.line((itemLeftPosition, itemTopPosition + itemConfig['height'], viewport['width'], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((itemLeftPosition, itemTopPosition + itemConfig['height'] / 2, viewport['width'], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
        draw.line((itemLeftPosition + 16, itemTopPosition, itemLeftPosition + 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((viewport['width'] - 48 / 2, itemTopPosition, viewport['width'] - 48 / 2, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderOneLineList(draw, items, count, listLeftPosition = 0):
    for j in range(1, count):
        itemTopPosition = (j - 1) * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        renderOneLineListItem(draw, items[j], itemTopPosition, listLeftPosition)

def renderTwoLinesListItem(draw, item, itemTopPosition, itemLeftPosition = 0):
    itemConfig = CONFIG['listItem']

    titlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight']/2
    subtitlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight'] + itemConfig['linesGap'] + itemConfig['subtitleHeight']/2
    draw.text((itemLeftPosition + 16, titlePosition), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((viewport['width'] - 48/2, itemTopPosition + itemConfig['height'] / 2), item['timeStart'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
    if item['subtitle'] is not None:
        draw.text((itemLeftPosition + 16, subtitlePosition), item['subtitle'], font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((itemLeftPosition, itemTopPosition + itemConfig['height'], viewport['width'], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((itemLeftPosition, titlePosition, viewport['width'], titlePosition), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            draw.line((itemLeftPosition, subtitlePosition, viewport['width'], subtitlePosition), fill = FILL_BLACK)
        draw.line((itemLeftPosition + 16, itemTopPosition, itemLeftPosition + 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((viewport['width'] - 48, itemTopPosition + itemConfig['height'] / 2, viewport['width'], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
            draw.line((viewport['width'] - 48 / 2, itemTopPosition, viewport['width'] - 48 / 2, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items, count, listLeftPosition = 0):
    for j in range(1, count):
        itemTopPosition = (j - 1) * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        item = items[j]
        if item['subtitle'] is not None:
            renderTwoLinesListItem(draw, item, itemTopPosition, listLeftPosition)
        else:
            renderOneLineListItem(draw, item, itemTopPosition, listLeftPosition)

def renderItemDetails(draw, item):
    appBarHeight = CONFIG['appBar']['height']
    itemConfig = CONFIG['listItem']

    datePosition = appBarHeight + 16
    if item['timeStart'] is not None:
        titlePosition = datePosition + itemConfig['subtitleHeight'] + itemConfig['linesGap'] * 2
        dateText = item['timeStart'].strftime('%H:%M')
        if item['timeEnd'] is not None:
            dateText += ' - ' + item['timeEnd'].strftime('%H:%M')
        if dateText == '00:00 - 00:00':
            dateText = 'All Day'
        draw.text((16, datePosition + itemConfig['subtitleHeight'] / 2), dateText, font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        titlePosition = appBarHeight + 16

    draw.text((16, titlePosition + itemConfig['titleHeight'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')

    subtitlePosition = titlePosition + itemConfig['titleHeight'] + itemConfig['linesGap'] * 2
    if item['subtitle'] is not None:
        locationPosition = subtitlePosition + itemConfig['subtitleHeight'] + itemConfig['linesGap'] * 2
        draw.text((16, subtitlePosition + itemConfig['subtitleHeight'] / 2), f"Note: '{item['subtitle']}'", font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        locationPosition = subtitlePosition

    if item['location'] is not None:
        draw.text((16, locationPosition + itemConfig['subtitleHeight'] / 2), f"Location: '{item['location']}'", font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')

    draw.line((viewport['width'] / 2, appBarHeight, viewport['width'] / 2, viewport['height']), fill = FILL_BLACK)

    if showBorder:
        draw.line((16, 0, 16, viewport['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((16, datePosition + itemConfig['subtitleHeight'] / 2, viewport['width'] / 2, datePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
        draw.line((16, titlePosition + itemConfig['titleHeight'] / 2, viewport['width'] / 2, titlePosition + itemConfig['titleHeight'] / 2), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            draw.line((16, subtitlePosition + itemConfig['subtitleHeight'] / 2, viewport['width'] / 2, subtitlePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
        if item['location'] is not None:
            draw.line((16, locationPosition + itemConfig['subtitleHeight'] / 2, viewport['width'] / 2, locationPosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
