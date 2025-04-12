import logging
from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = True

def renderAppBar(draw, weather_data, text):
    app_bar_config = CONFIG['appBar']
    draw_size = draw.im.size
    iconPosition = ((48 - app_bar_config['iconSize']) / 2 + app_bar_config['iconSize'] / 2, (app_bar_config['height'] - app_bar_config['iconSize']) / 2 + app_bar_config['iconSize'] / 2)
    titlePosition = app_bar_config['height'] / 2
    draw.text(iconPosition, weather_data['icon_code'], font = FONTS['weather'], fill = FILL_BLACK, anchor = 'mm')
    draw.text((48, titlePosition), text, font = FONTS['headline'], fill = FILL_BLACK, anchor = 'lm')
    draw.text((draw_size[0] - app_bar_config['marginRight'], titlePosition), weather_data['temp_current'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'rm')
    draw.line((0, app_bar_config['height'], draw_size[0], app_bar_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, app_bar_config['height'] / 2, draw_size[0], app_bar_config['height'] / 2), fill = FILL_BLACK)
        draw.line((iconPosition[0], 0, iconPosition[0], app_bar_config['height']), fill = FILL_BLACK)
        draw.line((48, 0, 48, app_bar_config['height']), fill = FILL_BLACK)
        draw.line((draw_size[0] - app_bar_config['marginRight'], 0, draw_size[0] - app_bar_config['marginRight'], app_bar_config['height']), fill = FILL_BLACK)

def renderOneLineListItem(draw, item, itemTopPosition):
    item_config = CONFIG['listItem']
    draw_size = draw.im.size

    draw.text((16, itemTopPosition + item_config['height'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((draw_size[0] - item_config['marginRight'], itemTopPosition + item_config['height'] / 2), formatListItemTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    draw.line((0, itemTopPosition + item_config['height'], draw_size[0], itemTopPosition + item_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, itemTopPosition + item_config['height'] / 2, draw_size[0], itemTopPosition + item_config['height'] / 2), fill = FILL_BLACK)
        draw.line((16, itemTopPosition, 16, itemTopPosition + item_config['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((draw_size[0] - item_config['marginRight'], itemTopPosition, draw_size[0] - item_config['marginRight'], itemTopPosition + item_config['height']), fill = FILL_BLACK)

def renderOneLineList(draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height']
        renderOneLineListItem(draw, items[j], itemTopPosition)

def renderTwoLinesListItem(draw, item, itemTopPosition ):
    item_config = CONFIG['listItem']
    draw_size = draw.im.size

    titlePosition = itemTopPosition + (item_config['height'] - item_config['titleHeight'] - item_config['linesGap'] - item_config['subtitleHeight']) / 2 + item_config['titleHeight']/2
    subtitlePosition = itemTopPosition + (item_config['height'] - item_config['titleHeight'] - item_config['linesGap'] - item_config['subtitleHeight']) / 2 + item_config['titleHeight'] + item_config['linesGap'] + item_config['subtitleHeight']/2
    draw.text((16, titlePosition), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((draw_size[0] - item_config['marginRight'], itemTopPosition + item_config['height'] / 2), formatListItemTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    if item['subtitle'] is not None:
        draw.text((16, subtitlePosition), item['subtitle'], font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((0, itemTopPosition + item_config['height'], draw_size[0], itemTopPosition + item_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, titlePosition, draw_size[0], titlePosition), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            draw.line((0, subtitlePosition, draw_size[0], subtitlePosition), fill = FILL_BLACK)
        draw.line((16, itemTopPosition, 16, itemTopPosition + item_config['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((draw_size[0] - 48, itemTopPosition + item_config['height'] / 2, draw_size[0] - item_config['marginRight'], itemTopPosition + item_config['height'] / 2), fill = FILL_BLACK)
            draw.line((draw_size[0] - item_config['marginRight'], itemTopPosition, draw_size[0] - item_config['marginRight'], itemTopPosition + item_config['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height']
        item = items[j]
        if item['subtitle'] is not None:
            renderTwoLinesListItem(draw, item, itemTopPosition)
        else:
            renderOneLineListItem(draw, item, itemTopPosition)

def formatListItemTime(timeStart, timeEnd):
    if timeStart is not None:
        timeText = timeStart.strftime('%H:%M')
        if timeEnd is not None:
            if f"{timeText} - {timeEnd.strftime('%H:%M')}" == '00:00 - 00:00':
                timeText = 'All Day'
    else:
        timeText = ''
    return timeText

def formatItemDetailsTime(timeStart, timeEnd):
    if timeStart is not None:
        timeText = timeStart.strftime('%H:%M')
        if timeEnd is not None:
            timeText += ' - ' + timeEnd.strftime('%H:%M')
            if timeText == '00:00 - 00:00':
                timeText = 'All Day'
    else:
        timeText = ''
    return timeText

def renderItemDetails(draw, item):
    item_config = CONFIG['listItem']
    draw_size = draw.im.size

    datePosition = 16
    if item['timeStart'] is not None:
        titlePosition = datePosition + item_config['subtitleHeight'] + item_config['linesGap']
        draw.text((16, datePosition + item_config['subtitleHeight'] / 2), formatItemDetailsTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        titlePosition = datePosition

    draw.text((16, titlePosition + item_config['titleHeight'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')

    subtitlePosition = titlePosition + item_config['titleHeight'] + item_config['linesGap'] *3
    subtitleText = ''
    if item['subtitle'] is not None:
        subtitleText += f"Note: '{item['subtitle']}'"
    if item['location'] is not None:
        subtitleText += f"\nLocation: '{item['location']}'"

    draw.multiline_text((16, subtitlePosition), subtitleText, font = FONTS['support_text'], fill = FILL_BLACK)

    if showBorder:
        draw.line((16, 0, 16, draw_size[1]), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((16, datePosition + item_config['subtitleHeight'] / 2, draw_size[0] / 2, datePosition + item_config['subtitleHeight'] / 2), fill = FILL_BLACK)
        draw.line((16, titlePosition + item_config['titleHeight'] / 2, draw_size[0] / 2, titlePosition + item_config['titleHeight'] / 2), fill = FILL_BLACK)
        if item['subtitle'] is not None or item['location'] is not None:
            draw.line((16, subtitlePosition + item_config['subtitleHeight'] / 2, draw_size[0] / 2, subtitlePosition + item_config['subtitleHeight'] / 2), fill = FILL_BLACK)
