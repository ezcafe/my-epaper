from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = True
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

def renderOneLineList(draw, items, count):
    itemConfig = CONFIG['listItem']
    for j in range(0, count):
        itemPosition = j * itemConfig['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        draw.text((16, itemPosition + itemConfig['height'] / 2), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
        draw.text((viewport['width'] - 48/2, itemPosition + itemConfig['height'] / 2), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
        draw.line((0, itemPosition + itemConfig['height'], viewport['width'], itemPosition + itemConfig['height']), fill = FILL_BLACK)
        if showBorder:
            draw.line((0, itemPosition + itemConfig['height'] / 2, viewport['width'], itemPosition + itemConfig['height'] / 2), fill = FILL_BLACK)
            draw.line((16, itemPosition, 16, itemPosition + itemConfig['height']), fill = FILL_BLACK)
            draw.line((viewport['width'] - 48 / 2, itemPosition, viewport['width'] - 48 / 2, itemPosition + itemConfig['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    itemConfig = CONFIG['listItem']
    for j in range(0, count):
        itemPosition = j * itemConfig['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        titlePosition = itemPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['supportTextHeight']) / 2 + itemConfig['titleHeight']/2
        supportTextPosition = itemPosition + (itemConfig['height'] - itemConfig['titleHeight'] - itemConfig['linesGap'] - itemConfig['supportTextHeight']) / 2 + itemConfig['titleHeight'] + itemConfig['linesGap'] + itemConfig['supportTextHeight']/2
        draw.text((16, titlePosition), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
        draw.text((16, supportTextPosition), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'lm')
        draw.line((0, itemPosition + itemConfig['height'], viewport['width'], itemPosition + itemConfig['height']), fill = FILL_BLACK)
        if showBorder:
            draw.line((0, titlePosition, viewport['width'], titlePosition), fill = FILL_BLACK)
            draw.line((0, supportTextPosition, viewport['width'], supportTextPosition), fill = FILL_BLACK)
            draw.line((16, itemPosition, 16, itemPosition + itemConfig['height']), fill = FILL_BLACK)
