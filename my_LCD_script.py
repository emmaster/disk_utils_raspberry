#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet

import os
import sys 
import time
import logging
import spidev as SPI

sys.path.append("/home/klsnkv/LCD_1.5_Code/RaspberryPi/python")
from lib import LCD_1inch5
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

####### resolution of the display 240 [width] x 280 [height]

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch5.LCD_1inch5(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch5.LCD_1inch5()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)

    logging.info("draw point")
    draw.rectangle((15,10,6,11), fill = "BLACK")

    logging.info("draw rectangle")
    draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")

    logging.info("draw text")
    Font1 = ImageFont.truetype("./Font/SuisseIntl-Medium-WebM.ttf",25)

    draw.text((20, 70), "HI CHIZHIK!", font = Font1, fill = (0,0,0))

    image1=image1.rotate(0)
    disp.ShowImage(image1)
    time.sleep(3)
    disp.clear()

    image = Image.open('./assets/img_for_display.jpg')
    image = image.rotate(0)
    disp.ShowImage(image)
    time.sleep(3)
    
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()



