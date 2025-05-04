#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet

##### THIS IS A UTILS TO WORK WITHOUT DISCONNECTING THE DISPLAY AFTER EACH USE ######

import os
import sys 
import time
import logging
import atexit
from my_LCD_utils import string_for_lcd

sys.path.append("/home/klsnkv/LCD_1.5_Code/RaspberryPi/python")


import spidev as SPI
from lib import LCD_1inch5
from PIL import Image,ImageDraw,ImageFont

RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)


#statusbar params
padding_left_right = 20
padding_top_bottom = 30
statusbar_height = 24

disp = None

try:
    # Create a new SPI object each time
    spi = SPI.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 10000000
    
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    # disp = LCD_1inch5.LCD_1inch5(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch5.LCD_1inch5(spi=spi,spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    # disp = LCD_1inch5.LCD_1inch5()
    # Initialize library.
    disp.Init()
    # Clear display.
    time.sleep(0.1)
    disp.clear()
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()



def print_txt_on_LCD2(text_param, font_size=25, color="WHITE", statusbar = None):
        
        # Create blank image for drawing.
        if color == "WHITE":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
        elif color == "GREEN":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "GREEN")
        elif color == "YELLOW":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "YELLOW")
        elif color == "RED":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "RED")
        else:
                 image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
        draw = ImageDraw.Draw(image1)

        cursor = [padding_left_right, padding_top_bottom]

        if statusbar:
            set_statusbar_on_LCD2(draw, statusbar, inner_color=color)
            cursor[1] += statusbar_height + padding_top_bottom + 30

        logging.info("draw text")
        Font1 = ImageFont.truetype("./Font/SuisseIntl-Medium-WebM.ttf",font_size)
        line_width = 14
        if font_size == 25:
            line_width = 15
        elif font_size <25 and font_size > 18:
            line_width = 20
        text_formatted = string_for_lcd(text_param, width=line_width)
        draw.text(cursor,text_formatted, font = Font1, fill = (0,0,0))

        image1=image1.rotate(0)
        disp.ShowImage(image1)

        # if spinner:
        #     Font2 = ImageFont.truetype("./Font/SuisseIntl-Medium-WebM.ttf", 20)
        #     spinner_txt = "|||||||||||"
        #     draw.text([0, display.height - 20], spinner_txt, font = Font2, fill = (0,0,0))
        #     image1=image1.rotate(0)
        #     disp.ShowImage(image1)

            
        print("print_txt_on_LCD2 worked")


def print_rectangle_on_LCD2(x1, y1, x2, y2, color="WHITE", outline="BLUE"):
    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), color)
    draw = ImageDraw.Draw(image1)

    logging.info("draw rectangle")
    draw.rectangle([(x1, y1), (x2, y2)], fill=color, outline=outline)

    image1 = image1.rotate(0)
    disp.ShowImage(image1)
    print("print_rectangle_on_LCD2 worked")

def set_statusbar_on_LCD2(img, percents=0, color="BLACK", inner_color="WHITE", border = 3):
    bar_height = statusbar_height
    img.rectangle([(padding_left_right, padding_top_bottom), (disp.width - padding_left_right, padding_top_bottom+bar_height)], fill=color)
    img.rectangle([(padding_left_right+border, padding_top_bottom+border), (disp.width - padding_left_right-border, padding_top_bottom+bar_height-border)], fill=inner_color)
    inner_padding = 2
    w = int((disp.width - padding_left_right*2 - border*2 - inner_padding*2) * percents / 100)
    img.rectangle([(padding_left_right+border+inner_padding,padding_top_bottom+border+inner_padding),(padding_left_right+border+inner_padding+w,padding_top_bottom+bar_height-border-inner_padding)], fill=color)

    


def cleanup():
    print("[my_LCD_utils2] Cleaning up before exit")
    if disp:
        disp.module_exit()

atexit.register(cleanup)
    


