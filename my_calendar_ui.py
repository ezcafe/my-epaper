from my_calendar_config import CONFIG, FILL_BLACK, FONTS

showBorder = False
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

def renderList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        draw.text((0, itemPosition + CONFIG['listItem']['titleOffset']), itemValue['due'].strftime('%H:%M'), font = FONTS['body'], fill = FILL_BLACK)
        draw.text((48, itemPosition + CONFIG['listItem']['titleOffset']), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK)
        draw.line((0, itemPosition + CONFIG['listItem']['height'], viewport['width'], itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
        if showBorder:
            draw.rectangle((16, itemPosition + (CONFIG['listItem']['height'] - 16) / 2, 134, itemPosition + ((CONFIG['listItem']['height'] - 16) / 2) + 16), outline = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItem']['height'] + CONFIG['appBar']['height']
        itemValue = items[j]

        draw.text((16, itemPosition + CONFIG['listItem']['2LinesTitleOffset']), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK)
        draw.line((0, itemPosition + CONFIG['listItem']['height'], viewport['width'], itemPosition + CONFIG['listItem']['height']), fill = FILL_BLACK)
        if showBorder:
            draw.rectangle((16, itemPosition + (CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2, 134, itemPosition + ((CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2) + 16), outline = FILL_BLACK)

        draw.text((16, itemPosition + CONFIG['listItem']['2LinesSupportTextOffset']), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK)
        if showBorder:
            draw.rectangle((0, 0, 48, CONFIG['listItem']['height']), outline = 0)
            draw.rectangle((16, itemPosition + ((CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2) + 16 + CONFIG['listItem']['linesGap'], 134, itemPosition + ((CONFIG['listItem']['height'] - 16 - 14 - CONFIG['listItem']['linesGap']) / 2) + 16 + CONFIG['listItem']['linesGap'] + 14), outline = FILL_BLACK)