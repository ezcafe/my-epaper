from my_calendar_config import CONFIG, FILL_BLACK, FONTS

def renderAppBar(draw, icon, text):
    draw.text((11, 15), icon, font = FONTS['weather'], fill = FILL_BLACK)
    draw.rectangle((0, 0, 48, CONFIG['appBarHeight']), outline = 0)
    draw.rectangle((12, (CONFIG['appBarHeight'] - 24) / 2, 36, ((CONFIG['appBarHeight'] - 24) / 2) + 24), outline = 0)

    draw.text((48, CONFIG['appBarTitleOffset']), text, font = FONTS['headline'], fill = FILL_BLACK)
    draw.rectangle((48, 0, 150, CONFIG['appBarHeight']), outline = 0)
    draw.rectangle((48 + 8, (CONFIG['appBarHeight'] - 24) / 2, 142, ((CONFIG['appBarHeight'] - 24) / 2) + 24), outline = 0)

def renderList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItemHeight'] + CONFIG['appBarHeight']
        itemValue = items[j]

        draw.text((16, itemPosition + CONFIG['listItemTitleOffset']), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK)
        draw.line((0, itemPosition + CONFIG['listItemHeight'], 150, itemPosition + CONFIG['listItemHeight']), fill = FILL_BLACK)
        draw.rectangle((16, itemPosition + (CONFIG['listItemHeight'] - 16) / 2, 134, itemPosition + ((CONFIG['listItemHeight'] - 16) / 2) + 16), outline = FILL_BLACK)

def renderTwoLinesList(draw, items, count):
    for j in range(0, count):
        itemPosition = j * CONFIG['listItemHeight'] + CONFIG['appBarHeight']
        itemValue = items[j]

        draw.text((16, itemPosition + CONFIG['listItemTitleWithSupportTextOffset']), itemValue['title'], font = FONTS['body'], fill = FILL_BLACK)
        draw.line((0, itemPosition + CONFIG['listItemHeight'], 150, itemPosition + CONFIG['listItemHeight']), fill = FILL_BLACK)
        draw.rectangle((16, itemPosition + (CONFIG['listItemHeight'] - 16 - 14 - 2) / 2, 134, itemPosition + ((CONFIG['listItemHeight'] - 16 - 14 - 2) / 2) + 16), outline = FILL_BLACK)

        draw.text((16, itemPosition + CONFIG['listItemSupportTextOffset']), itemValue['due'].strftime('%H:%M'), font = FONTS['support_text'], fill = FILL_BLACK)
        draw.rectangle((0, 0, 48, CONFIG['listItemHeight']), outline = 0)
        draw.rectangle((12, itemPosition + ((CONFIG['listItemHeight'] - 16 - 14 - 2) / 2) + 16 + 2, 134, itemPosition + ((CONFIG['listItemHeight'] - 16 - 14 - 2) / 2) + 16 + 2 + 14), outline = FILL_BLACK)