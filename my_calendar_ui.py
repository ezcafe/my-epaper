import logging
import math
from PIL import Image, ImageDraw
from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = False

def renderAppBar(draw, current_date, weather_data):
    app_bar_config = CONFIG['appBar']
    viewport_width, viewport_height = draw.im.size
    iconPosition = ((48 - app_bar_config['iconSize']) / 2 + app_bar_config['iconSize'] / 2, (app_bar_config['height'] - app_bar_config['iconSize']) / 2 + app_bar_config['iconSize'] / 2)
    titlePosition = app_bar_config['height'] / 2
    draw.text(iconPosition, weather_data['icon_code'], font = FONTS['weather'], fill = FILL_BLACK, anchor = 'mm')
    draw.text((48, titlePosition), current_date.strftime('%A, %d/%m'), font = FONTS['headline'], fill = FILL_BLACK, anchor = 'lm')
    draw.text((viewport_width - app_bar_config['paddingRight'], titlePosition), weather_data['temp_current'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'rm')
    draw.line((0, app_bar_config['height'], viewport_width, app_bar_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, app_bar_config['height'] / 2, viewport_width, app_bar_config['height'] / 2), fill = FILL_BLACK)
        draw.line((iconPosition[0], 0, iconPosition[0], app_bar_config['height']), fill = FILL_BLACK)
        draw.line((48, 0, 48, app_bar_config['height']), fill = FILL_BLACK)
        draw.line((viewport_width - app_bar_config['paddingRight'], 0, viewport_width - app_bar_config['paddingRight'], app_bar_config['height']), fill = FILL_BLACK)

def renderOneLineListItem(draw, item, itemTopPosition):
    item_config = CONFIG['listItem']
    viewport_width, viewport_height = draw.im.size

    draw.text((item_config['paddingLeft'], itemTopPosition + item_config['height'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((viewport_width - item_config['paddingRight'], itemTopPosition + item_config['height'] / 2), formatListItemTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    draw.line((0, itemTopPosition + item_config['height'], viewport_width, itemTopPosition + item_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, itemTopPosition + item_config['height'] / 2, viewport_width, itemTopPosition + item_config['height'] / 2), fill = FILL_BLACK)
        draw.line((item_config['paddingLeft'], itemTopPosition, item_config['paddingLeft'], itemTopPosition + item_config['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((viewport_width - item_config['paddingRight'], itemTopPosition, viewport_width - item_config['paddingRight'], itemTopPosition + item_config['height']), fill = FILL_BLACK)

def renderOneLineList(draw, items):
    if len(items) == 0:
        return

    displayCount = min(len(items), CONFIG['visibleItemCount'])

    for j in range(0, displayCount):
        itemTopPosition = j * CONFIG['listItem']['height']
        renderOneLineListItem(draw, items[j], itemTopPosition)

def renderTwoLinesListItem(draw, item, itemTopPosition ):
    item_config = CONFIG['listItem']
    viewport_width, viewport_height = draw.im.size

    titlePosition = itemTopPosition + (item_config['height'] - item_config['titleHeight'] - item_config['linesGap'] - item_config['subtitleHeight']) / 2 + item_config['titleHeight']/2
    subtitlePosition = itemTopPosition + (item_config['height'] - item_config['titleHeight'] - item_config['linesGap'] - item_config['subtitleHeight']) / 2 + item_config['titleHeight'] + item_config['linesGap'] + item_config['subtitleHeight']/2
    draw.text((item_config['paddingLeft'], titlePosition), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((viewport_width - item_config['paddingRight'], itemTopPosition + item_config['height'] / 2), formatListItemTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    if item['subtitle'] is not None:
        draw.text((item_config['paddingLeft'], subtitlePosition), item['subtitle'], font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((0, itemTopPosition + item_config['height'], viewport_width, itemTopPosition + item_config['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, titlePosition, viewport_width, titlePosition), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            draw.line((0, subtitlePosition, viewport_width, subtitlePosition), fill = FILL_BLACK)
        draw.line((item_config['paddingLeft'], itemTopPosition, item_config['paddingLeft'], itemTopPosition + item_config['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((viewport_width - 48, itemTopPosition + item_config['height'] / 2, viewport_width - item_config['paddingRight'], itemTopPosition + item_config['height'] / 2), fill = FILL_BLACK)
            draw.line((viewport_width - item_config['paddingRight'], itemTopPosition, viewport_width - item_config['paddingRight'], itemTopPosition + item_config['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items):
    if len(items) == 0:
        return

    displayCount = min(len(items), CONFIG['visibleItemCount'])

    for j in range(0, displayCount):
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
    if item is None:
        return

    item_config = CONFIG['listItem']
    viewport_width, viewport_height = draw.im.size

    datePosition = item_config['paddingTop']
    if item['timeStart'] is not None:
        titlePosition = datePosition + item_config['subtitleHeight'] + item_config['linesGap']
        draw.text((item_config['paddingLeft'], datePosition + item_config['subtitleHeight'] / 2), formatItemDetailsTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        titlePosition = datePosition

    draw.text((item_config['paddingLeft'], titlePosition + item_config['titleHeight'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')

    subtitlePosition = titlePosition + item_config['titleHeight'] + item_config['linesGap'] *3
    subtitleText = ''
    if item['subtitle'] is not None:
        subtitleText += f"Note: '{item['subtitle']}'"
    if item['location'] is not None:
        subtitleText += f"\nLocation: '{item['location']}'"

    draw.multiline_text((item_config['paddingLeft'], subtitlePosition), subtitleText, font = FONTS['support_text'], fill = FILL_BLACK)

    if showBorder:
        draw.line((item_config['paddingLeft'], 0, item_config['paddingLeft'], viewport_height), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((item_config['paddingLeft'], datePosition + item_config['subtitleHeight'] / 2, viewport_width, datePosition + item_config['subtitleHeight'] / 2), fill = FILL_BLACK)
        draw.line((item_config['paddingLeft'], titlePosition + item_config['titleHeight'] / 2, viewport_width, titlePosition + item_config['titleHeight'] / 2), fill = FILL_BLACK)
        if item['subtitle'] is not None or item['location'] is not None:
            draw.line((item_config['paddingLeft'], subtitlePosition + item_config['subtitleHeight'] / 2, viewport_width, subtitlePosition + item_config['subtitleHeight'] / 2), fill = FILL_BLACK)

def renderEventUI(mainImage, data):
    mainDraw = ImageDraw.Draw(mainImage)
    current_date, selected_event, remaining_events, weather_data = data

    renderAppBar(mainDraw, current_date, weather_data)

    viewport_width, viewport_height = mainDraw.im.size
    mainDraw.line(
        (viewport_width / 2, CONFIG['appBar']['height'], viewport_width / 2, viewport_height),
        fill=FILL_BLACK
    )

    eventDetailsImage = Image.new('1', (math.ceil(viewport_width / 2), viewport_height - CONFIG['appBar']['height'] - 1), 255)
    eventDetailsDraw = ImageDraw.Draw(eventDetailsImage)
    renderItemDetails(eventDetailsDraw, selected_event)
    mainImage.paste(eventDetailsImage, (0, CONFIG['appBar']['height'] + 1))

    eventListImage = Image.new('1', (math.ceil(viewport_width / 2), viewport_height - CONFIG['appBar']['height'] - 1), 255)
    eventListDraw = ImageDraw.Draw(eventListImage)
    renderOneLineList(eventListDraw, remaining_events)
    # renderTwoLinesList(eventListDraw, remaining_events)
    mainImage.paste(eventListImage, (math.ceil(viewport_width / 2) + 1, CONFIG['appBar']['height'] + 1))

def renderCalendarWeatherUI(mainImage, weather_data):
    mainDraw = ImageDraw.Draw(mainImage)
    viewport_width, _ = mainDraw.im.size
    calendar_config = CONFIG['calendar']

    iconPosition = viewport_width - calendar_config['paddingRight']
    weatherText = weather_data['temp_current']
    weatherTextWidth = mainDraw.textlength(weatherText, font=FONTS['body'])

    # Draw weather icon and text
    mainDraw.text(
        (iconPosition - 3 - weatherTextWidth, calendar_config['paddingTop']),
        weather_data['icon_code'],
        font=FONTS['weather'],
        fill=FILL_BLACK,
        anchor='rm'
    )
    mainDraw.text(
        (iconPosition, calendar_config['paddingTop']),
        weatherText,
        font=FONTS['body'],
        fill=FILL_BLACK,
        anchor='rm'
    )

def renderCalendarUI(mainImage, current_date, extra_text):
    mainDraw = ImageDraw.Draw(mainImage)
    viewport_width, viewport_height = mainDraw.im.size
    middlePoint = viewport_width / 2
    calendar_config = CONFIG['calendar']

    positions = {
        "date": calendar_config['paddingTop'] + calendar_config['dateHeight'] / 2,
        "month": calendar_config['paddingTop'] + calendar_config['dateHeight'] + calendar_config['monthHeight'] / 2,
        "separator": calendar_config['paddingTop'] + calendar_config['dateHeight'] + calendar_config['monthHeight'] + calendar_config['linesGap'] * 3,
        "text": calendar_config['paddingTop'] + calendar_config['dateHeight'] + calendar_config['monthHeight'] + calendar_config['linesGap'] * 10,
    }

    mainDraw.text((middlePoint, positions["date"]), current_date.strftime('%d'), font=FONTS['calendar_date'], fill=FILL_BLACK, anchor='mm')
    mainDraw.text((middlePoint, positions["month"]), current_date.strftime('%A').upper(), font=FONTS['calendar_month'], fill=FILL_BLACK, anchor='mm')
    mainDraw.line((middlePoint - 30, positions["separator"], middlePoint + 30, positions["separator"]), fill=FILL_BLACK)
    mainDraw.multiline_text((middlePoint, positions["text"]), extra_text, font=FONTS['support_text'], fill=FILL_BLACK, anchor='ms', align='center')

    if showBorder:
        border_lines = [
            ((middlePoint, 0), (middlePoint, viewport_height)),
            ((viewport_width - calendar_config['paddingRight'], 0), (viewport_width - calendar_config['paddingRight'], viewport_height)),
            ((calendar_config['paddingTop'], 0), (calendar_config['paddingTop'], viewport_width)),
            ((0, positions["date"]), (viewport_width, positions["date"])),
            ((0, positions["month"]), (viewport_width, positions["month"])),
            ((0, positions["text"]), (viewport_width, positions["text"])),
        ]
        for start, end in border_lines:
            mainDraw.line((*start, *end), fill=FILL_BLACK)