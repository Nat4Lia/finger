# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import math
import gauges

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.truetype('/etc/finger/Retron2000.ttf',14)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)



def drawPercentBar(max_progress, progress, text1, text2, text3, x=0, y=63, width=127, height=14 ) :
    text1_width, text1_height = draw.textsize(text1, font=font)
    text2_width, text2_height = draw.textsize(text2, font=font)
    text3_width, text3_height = draw.textsize(text3, font=font)
    x_text1 = ((disp.width-text1_width)/2)
    y_text1 = (disp.height-height-text1_height-3)
    x_text2 = (disp.width-text2_width)/2
    y_text2 = (disp.height-height-text1_height-text2_height)
    x_text3 = (disp.width-text3_width)/2
    y_text3 = (disp.height-height-text1_height-text2_height-text3_height+3)
    draw.text((x_text1, y_text1), str('{}'.format(text1)), font=font, fill=255)
    draw.text((x_text2, y_text2), str('{}'.format(text2)), font=font, fill=255)
    draw.text((x_text3, y_text3), str('{}'.format(text3)), font=font, fill=255)
    height = y - height
    bar = math.ceil((width*progress)/max_progress)
    percent = (progress*100)/max_progress
    r_up = int(percent)
    draw.rectangle((x, y, width, height), outline=255, fill=0)
    draw.rectangle((x, y, bar, height), outline=255, fill=255)
    if percent < 10 :
        draw.text(((width/2)-11, height-3), str('{}'.format(str(r_up)[:1])), font=font, fill=255)
        draw.text(((width/2), height-3), str('{}'.format(str(r_up)[1:])), font=font, fill=255)
        draw.text(((width/2), height-3), str('%'), font=font, fill=255)
    elif r_up >= 10 and r_up < 45 :
        draw.text(((width/2)-11, height-3), str('{}'.format(str(r_up)[:1])), font=font, fill=255)
        draw.text(((width/2), height-3), str('{}'.format(str(r_up)[1:])), font=font, fill=255)
        draw.text(((width/2)+11, height-3), str('%'), font=font, fill=255)
    elif r_up >=45 and r_up < 55:
        draw.text(((width/2)-11, height-3), str('{}'.format(str(r_up)[:1])), font=font, fill=0)
        draw.text(((width/2), height-3), str('{}'.format(str(r_up)[1:])), font=font, fill=255)
        draw.text(((width/2)+11, height-3), str('%'), font=font, fill=255)
    elif r_up >=55 and r_up < 60 :
        draw.text(((width/2)-11, height-3), str('{}'.format(str(r_up)[:1])), font=font, fill=0)
        draw.text(((width/2), height-3), str('{}'.format(str(r_up)[1:])), font=font, fill=0)
        draw.text(((width/2)+11, height-3), str('%'), font=font, fill=255)
    elif r_up >= 100 :
        draw.text(((width/2)-11, height-3), str('{}'.format(str(r_up)[:1])), font=font, fill=0)
        draw.text(((width/2), height-3), str('{}'.format(str(r_up)[1:])), font=font, fill=0)
        draw.text(((width/2)+22, height-3), str('%'), font=font, fill=0)

def drawGauges(value, message) :
    g = gauges.GaugeDraw(image, 0, 100, 180)
    message_width, message_height = draw.textsize(message, font=font)
    draw.text(((127/2)-14, 35), str('{}%'.format(value)), font=font, fill=255)
    g.add_needle(value, needle_fill_color=255)
    g.add_dial(major_ticks=1, minor_ticks=1, dial_format="%d")
    g.render()
    draw.text(((disp.width-message_width)/2, disp.height-message_height), str(message), font=font, fill=255)

def drawImage(image_name) :
    image = Image.open(image_name).resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
    return image

def drawText(text) :
    if text :
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        if len(text) == 1:
            text0_width, text0_height = draw.textsize(text[0], font=font)
            draw.text(((disp.width-text0_width)/2, (disp.height-text0_height)/2), str(text[0]), font=font, fill=255)
        elif len(text) == 2:
            text0_width, text0_height = draw.textsize(text[0], font=font)
            text1_width, text1_height = draw.textsize(text[1], font=font)
            draw.text(((disp.width-text1_width)/2, (disp.height-text1_height)/2), str(text[1]), font=font, fill=255)
            draw.text(((disp.width-text0_width)/2, ((disp.height-text1_height-text0_height)/2)-6), str(text[0]), font=font, fill=255)
        elif len(text) == 3:
            text0_width, text0_height = draw.textsize(text[0], font=font)
            text1_width, text1_height = draw.textsize(text[1], font=font)
            text2_width, text2_height = draw.textsize(text[2], font=font)
            draw.text(((disp.width-text2_width)/2, (disp.height-text2_height+20)/2), str(text[2]), font=font, fill=255)
            draw.text(((disp.width-text1_width)/2, ((disp.height-text0_height-text1_height)/2)), str(text[1]), font=font, fill=255)
            draw.text(((disp.width-text0_width)/2, ((disp.height-text0_height-text1_height-text2_height-16)/2)), str(text[0]), font=font, fill=255)
        elif len(text) == 4:
            text0_width, text0_height = draw.textsize(text[0], font=font)
            text1_width, text1_height = draw.textsize(text[1], font=font)
            text2_width, text2_height = draw.textsize(text[2], font=font)
            text3_width, text3_height = draw.textsize(text[3], font=font)
            draw.text(((disp.width-text3_width)/2, (disp.height-text3_height+40)/2), str(text[3]), font=font, fill=255)
            draw.text(((disp.width-text2_width)/2, ((disp.height-text2_height-text3_height+25)/2)), str(text[2]), font=font, fill=255)
            draw.text(((disp.width-text1_width)/2, ((disp.height-text1_height-text2_height-text3_height+10)/2)), str(text[1]), font=font, fill=255)
            draw.text(((disp.width-text0_width)/2, ((disp.height-text0_height-text1_height-text2_height-text3_height)/2)), str(text[0]), font=font, fill=255)

def tampil_teks(value=[]) :
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    drawText(value)
    disp.image(image)
    disp.display()

def tampil_gambar(file_gambar) :
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(drawImage(file_gambar))
    disp.display()

def tampil_gauges(value, message) :
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    drawGauges(value, message)
    disp.image(image)
    disp.display()

def tampil_progressbar(max_progress, progress, text1='', text2='', text3='') :
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    drawPercentBar(max_progress, progress, text1, text2, text3)
    disp.image(image)
    disp.display()

