import logging
from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = False

def renderAppBar(draw, icon, text):
    drawSize = draw.im.size
    iconPosition = ((48 - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2, (CONFIG['appBar']['height'] - CONFIG['appBar']['iconSize']) / 2 + CONFIG['appBar']['iconSize'] / 2)
    titlePosition = CONFIG['appBar']['height'] / 2
    draw.text(iconPosition, icon, font = FONTS['weather'], fill = FILL_BLACK, anchor = 'mm')
    draw.text((48, titlePosition), text, font = FONTS['headline'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((0, CONFIG['appBar']['height'], drawSize[0], CONFIG['appBar']['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, CONFIG['appBar']['height'] / 2, drawSize[0], CONFIG['appBar']['height'] / 2), fill = FILL_BLACK)
        draw.line((iconPosition[0], 0, iconPosition[0], CONFIG['appBar']['height']), fill = FILL_BLACK)
        draw.line((48, 0, 48, CONFIG['appBar']['height']), fill = FILL_BLACK)

def renderOneLineListItem(draw, item, itemTopPosition):
    itemConfig = CONFIG['listItem']
    drawSize = draw.im.size

    draw.text((16, itemTopPosition + itemConfig['height'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((drawSize[0] - 16, itemTopPosition + itemConfig['height'] / 2), item['timeStart'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'rm')
    draw.line((0, itemTopPosition + itemConfig['height'], drawSize[0], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, itemTopPosition + itemConfig['height'] / 2, drawSize[0], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
        draw.line((16, itemTopPosition, 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((drawSize[0] - 16, itemTopPosition, drawSize[0] - 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderOneLineList(draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        renderOneLineListItem(draw, items[j], itemTopPosition)

def renderTwoLinesListItem(draw, item, itemTopPosition ):
    itemConfig = CONFIG['listItem']
    drawSize = draw.im.size

    titlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight']/2
    subtitlePosition = itemTopPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['subtitleHeight']) / 2 + itemConfig['titleHeight'] + itemConfig['linesGap'] + itemConfig['subtitleHeight']/2
    draw.text((16, titlePosition), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
    if item['timeStart'] is not None:
        draw.text((drawSize[0] - 48/2, itemTopPosition + itemConfig['height'] / 2), formatTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
    if item['subtitle'] is not None:
        draw.text((16, subtitlePosition), item['subtitle'], font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    draw.line((0, itemTopPosition + itemConfig['height'], drawSize[0], itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
    if showBorder:
        draw.line((0, titlePosition, drawSize[0], titlePosition), fill = FILL_BLACK)
        if item['subtitle'] is not None:
            draw.line((0, subtitlePosition, drawSize[0], subtitlePosition), fill = FILL_BLACK)
        draw.line((16, itemTopPosition, 16, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((drawSize[0] - 48, itemTopPosition + itemConfig['height'] / 2, drawSize[0], itemTopPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
            draw.line((drawSize[0] - 48 / 2, itemTopPosition, drawSize[0] - 48 / 2, itemTopPosition + itemConfig['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    for j in range(0, count):
        itemTopPosition = j * CONFIG['listItem']['height']
        item = items[j]
        if item['subtitle'] is not None:
            renderTwoLinesListItem(draw, item, itemTopPosition)
        else:
            renderOneLineListItem(draw, item, itemTopPosition)

def formatTime(timeStart, timeEnd):
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
    itemConfig = CONFIG['listItem']
    drawSize = draw.im.size

    datePosition = 16
    if item['timeStart'] is not None:
        titlePosition = datePosition + itemConfig['subtitleHeight'] + itemConfig['linesGap']
        draw.text((16, datePosition + itemConfig['subtitleHeight'] / 2), formatTime(item['timeStart'], item['timeEnd']), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
    else:
        titlePosition = datePosition

    draw.text((16, titlePosition + itemConfig['titleHeight'] / 2), item['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')

    subtitlePosition = titlePosition + itemConfig['titleHeight'] + itemConfig['linesGap'] *3
    subtitleText = ''
    if item['subtitle'] is not None:
        subtitleText += f"Note: '{item['subtitle']}'"
    if item['location'] is not None:
        subtitleText += f"\nLocation: '{item['location']}'"

    draw.multiline_text((16, subtitlePosition), subtitleText, font = FONTS['support_text'], fill = FILL_BLACK)

    if showBorder:
        draw.line((16, 0, 16, drawSize[1]), fill = FILL_BLACK)
        if item['timeStart'] is not None:
            draw.line((16, datePosition + itemConfig['subtitleHeight'] / 2, drawSize[0] / 2, datePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
        draw.line((16, titlePosition + itemConfig['titleHeight'] / 2, drawSize[0] / 2, titlePosition + itemConfig['titleHeight'] / 2), fill = FILL_BLACK)
        if item['subtitle'] is not None or item['location'] is not None:
            draw.line((16, subtitlePosition + itemConfig['subtitleHeight'] / 2, drawSize[0] / 2, subtitlePosition + itemConfig['subtitleHeight'] / 2), fill = FILL_BLACK)
