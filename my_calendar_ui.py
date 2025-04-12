from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = True
viewport = {'width': 400, 'height': 300}

def renderAppBar(draw, icon, text):
    draw.text((11, 15), icon, font = FONTS['weather'], fill = FILL_BLACK)
    draw.line((0, CONFIG['appBar']['height'], viewport['width'], CONFIG['appBar']['height']), fill = FILL_BLACK)
    if showBorder:
        draw.rectangle((0, 0, 48, CONFIG['appBar']['height']), outline = 0)
        draw.rectangle((12, (CONFIG['appBar']['height'] - 24) / 2, 36, ((CONFIG['appBar']['height'] - 24) / 2) + 24), outline = 0)

    draw.text((48, CONFIG['appBar']['titleOffset']), text, font = FONTS['headline'], fill = FILL_BLACK)
    if showBorder:
        draw.rectangle((48, 0, 150, CONFIG['appBar']['height']), outline = 0)
        draw.rectangle((48 + 8, (CONFIG['appBar']['height'] - 24) / 2, 142, ((CONFIG['appBar']['height'] - 24) / 2) + 24), outline = 0)

def renderOneLineList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        draw.text((16, itemPosition + CONFIG['listItem']['height'] / 2), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK, anchor = 'lm')
        draw.text((viewport['width'] - 48/2, itemPosition + CONFIG['listItem']['height'] / 2), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK, anchor = 'mm')
        draw.line((0, itemPosition + CONFIG['listItem']['height'], viewport['width'], itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
        if showBorder:
            draw.line((0, itemPosition + CONFIG['listItem']['height'] / 2, viewport['width'], itemPosition + CONFIG['listItem']['height'] / 2), fill = FILL_BLACK)
            draw.line((16, itemPosition, 16, itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
            draw.line((viewport['width'] - 48 / 2, itemPosition, viewport['width'] - 48 / 2, itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        draw.text((16, itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK)
        draw.text((16, itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2 + 16 + CONFIG['listItem']['linesGap']), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK)
        draw.line((0, itemPosition + CONFIG['listItem']['height'], viewport['width'], itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
        if showBorder:
            draw.line((0, itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2, viewport['width'], itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2), fill = FILL_BLACK)
            draw.line((0, itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2 + 16 + CONFIG['listItem']['linesGap'], viewport['width'], itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2  + 16 + CONFIG['listItem']['linesGap']), fill = FILL_BLACK)
            draw.line((16, itemPosition, 16, itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
