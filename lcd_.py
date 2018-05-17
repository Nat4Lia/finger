import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import time

RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

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
font = ImageFont.truetype('/etc/finger/CALIBRI.TTF', 11)

# class printLCD:

def teks(text1='',text2='',text3=''):
	add_y = 0
	draw.rectangle((0,0,width,height), outline=0, fill=0)
	draw.text(((width - (len(text1)*6))/2, 0), str(text1),  font=font, fill=255)
	draw.text(((width - (len(text2)*6))/2, 10), str(text2),  font=font, fill=255)
	draw.text(((width - (len(text3)*6))/2, 20), str(text3),  font=font, fill=255)
	disp.image(image)
	disp.display()
	time.sleep(1)
	disp.clear()

def progress_bar(progress, total, x=0, y=40, width=127, height=27, decimals=1, length=100, text=''):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (progress / float(total)))
	filledLength = int(length * progress // total)
	bar = (float(width - 4) / 100) * filledLength
	draw.rectangle ((0, 0, disp.width, disp.height), outline=0, fill=0)
	draw.rectangle((x + 5, y + 2, bar, height - 4), fill=255)
	draw.text(((disp.width - (len(text) * 6)) / 2, 0), str(text), font=font, fill=255)
	draw.text(((disp.width - (len(percent) * 6)) / 2, 10), "%s" % percent + "%", font=font, fill=255)
	if progress == total:
		draw.rectangle ((0, 0, disp.width, disp.height), outline=0, fill=0)
		draw.text(((disp.width - (len('Complete') * 6)) / 2, 23/2), str('Complete'), font=font, fill=255)
		return

