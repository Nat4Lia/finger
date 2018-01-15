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
font = ImageFont.load_default()

class printLCD:
    def __init__(self, text_1, text_2):
        self.text_1 = text_1
        self.text_2 = text_2

    def lcd_start():
    	draw.rectangle((0,0,width,height), outline=0, fill=0)
    	draw.text((40, 10), "Welcome",  font=font, fill=255)
    	disp.image(image)
    	disp.display()
    	time.sleep(1)
    	disp.clear()

    def lcd_status(self):
    	paddingX1 = (128 - (len(self.text_1)*6))/2
    	paddingX2 = (128 - (len(self.text_2)*6))/2
    	draw.rectangle((0,0,width,height), outline=0, fill=0)
    	draw.text((paddingX1, 0),str(self.text_1),  font=font, fill=255)
    	draw.text((paddingX2, 10),str(self.text_2),  font=font, fill=255)
    	disp.image(image)
    	disp.display()
    	time.sleep(1)
    	disp.clear()
