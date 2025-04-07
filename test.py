# ======= Import

import sys, os, time, traceback
picdir = "/home/ezcafe/e-Paper/RaspberryPi_JetsonNano/python/resources"
libdir = "/home/ezcafe/e-Paper/RaspberryPi_JetsonNano/python/lib" # Set according to your git download
if os.path.exists(libdir): sys.path.append(libdir)
from waveshare_epd import epd4in2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

black = 0
white = 1

# ======= Utils

def clear_display(epd):
    global image, draw
    epd.Clear(0xFF)
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    epd.display(epd.getbuffer(image))

def img_convert(img_file,X_new,Y_new):
    img = Image.open(img_file)
    # increase contrast
    enhancer = ImageEnhance.Contrast(img)
    contrast = 5 #increase contrast. contrast = 1 means not performing manipulation
    img = enhancer.enhance(contrast)

    img = img.convert('1') # convert to black & white
    img = img.resize((X_new,Y_new), Image.LANCZOS) # resize to new X,Y
    return img

# ======= Render

try:
    epd = epd4in2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    time.sleep(2)

    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)


# Drawing text
    clear_display(epd)
    draw.text((0, 0), 'Test 1) Draw text', font = font15, fill = black)
    draw.text((10, 15), 'test 15', font = font15, fill = black)
    draw.text((10, 31), 'text 24', font = font24, fill = black)
    draw.text((10, 63), 'text 32', font = font32, fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Drawing Line
    clear_display(epd)
    draw.text((0, 0), 'Test 2) Draw line', font = font15, fill = black)
    draw.line([(0,20),(50,100)], fill = 0,width = 5)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw Rectangles
    clear_display(epd)
    draw.text((0, 0), 'Test 3) Draw Rectangles', font = font15, fill = black)
    draw.rectangle([(0,20),(50,60)],outline = black)
    draw.rectangle([(50,20),(100,60)],fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw Chords
    clear_display(epd)
    draw.text((0, 0), 'Test 4) Draw Chords', font = font15, fill = black)
    draw.chord((0, 20, 100, 70), 0, 360, fill = black)
    draw.ellipse((0, 70, 100, 120), outline = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw Pie Slices
    clear_display(epd)
    draw.text((0, 0), 'Test 4) Draw Pie Slices', font = font15, fill = black)
    draw.pieslice((0, 20, 100, 110), 90, 180, outline = black)
    draw.pieslice((0, 20, 100, 110), 180, 270, fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw Polygons
    clear_display(epd)
    draw.text((0, 0), 'Test 5) Draw Polygons', font = font15, fill = black)
    draw.polygon([(0,20),(110,60),(150,35)],outline = black)
    draw.polygon([(190,20),(190,60),(150,40)],fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw Bitmap
    clear_display(epd)
    image = Image.open(os.path.join(picdir, '4in2.bmp'))
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw smaller bitmap
    clear_display(epd)
    bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    image.paste(bmp, (20,20))
    draw.text((0, 0), 'Test 7) Smaller Bitmap', font = font15, fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw custom image
    clear_display(epd)
    img = img_convert("peppe8o-logo.jpg",64,64)
    image.paste(img, (20,20))
    draw.text((0, 0), 'Test 8) Custom image', font = font15, fill = black)
    epd.display(epd.getbuffer(image))
    time.sleep(2)

# Draw partial Updates
    clear_display(epd)
    draw.text((0, 0), 'Test 9) Partial Updates', font = font15, fill = black)
    epd.displayPartBaseImage(epd.getbuffer(image))
    epd.init(epd.PART_UPDATE)

    num = 0
    start_time=time.time()
    elapsed = time.time()-start_time
    while (time.time()-start_time) <= 10:
        elapsed=time.time()-start_time
        progress = int(220-int(elapsed*10))
        draw.rectangle((120, 70, progress, 75), fill = black)
        draw.rectangle((progress, 70, 220, 75), fill = white)
        draw.rectangle([(progress,70),(220,75)],outline = black)

        draw.rectangle((120, 80, 220, 105), fill = white)
        draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = black)
        epd.displayPartial(epd.getbuffer(image))
        time.sleep(0.2)
    epd.init(epd.FULL_UPDATE)
    time.sleep(2)

# Tests finished
    clear_display(epd)
    draw.text((0, 0), 'Tests finished', font = font15, fill = 0)
    draw.text((0, 15), 'Visit peppe8o.com for more tutorials', font = font15, fill = 0)
    epd.display(epd.getbuffer(image))
    time.sleep(5)

    clear_display(epd)
    print("Goto Sleep...")
    epd.sleep()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()