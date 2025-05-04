#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet

import os
import sys 
import time
import logging

sys.path.append("/home/klsnkv/LCD_1.5_Code/RaspberryPi/python")

def string_for_lcd(text, width=14):
    words = text.split()
    if len(text) < width and not "<br>" in text:
        return text
    elif len(words[0]) > width:
        return words[0][:width]+"-" + "\n" + string_for_lcd(text[width:], width)
    else:
        line = ""
        rest = ""
        line_open = True
        for word in words:
            if word == "<br>":
                line_open = False
            elif len(line) + len(word) + 1 <= width and line_open:
                line += word + " "
            else:
                line_open = False
                rest += word + " "
        return line + "\n" + string_for_lcd(rest, width)


def print_txt_on_LCD(text_param, font_size=25, color="WHITE"):

    import spidev as SPI
    from lib import LCD_1inch5
    from PIL import Image,ImageDraw,ImageFont

    # Raspberry Pi pin configuration:
    RST = 27
    DC = 25
    BL = 18
    bus = 0 
    device = 0 
    logging.basicConfig(level=logging.DEBUG)

    try:
        # Create a new SPI object each time
        spi = SPI.SpiDev()
        spi.open(bus, device)
        spi.max_speed_hz = 10000000
        
        # display with hardware SPI:
        ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
        disp = LCD_1inch5.LCD_1inch5(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
        # disp = LCD_1inch5.LCD_1inch5()
        # Initialize library.
        disp.Init()
        # Clear display.
        time.sleep(0.1)
        disp.clear()

        # Create blank image for drawing.
        if color == "WHITE":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
        elif color == "GREEN":
                 image1 = Image.new("RGB", (disp.width,disp.height ), "GREEN")
        else:
                 image1 = Image.new("RGB", (disp.width,disp.height ), "RED")
        draw = ImageDraw.Draw(image1)

        logging.info("draw text")
        Font1 = ImageFont.truetype("./Font/SuisseIntl-Medium-WebM.ttf",font_size)
        text_formatted = string_for_lcd(text_param)
        draw.text((20, 70),text_formatted, font = Font1, fill = (0,0,0))

        image1=image1.rotate(0)
        disp.ShowImage(image1)
        
        time.sleep(0.1)
        disp.module_exit()
        logging.info("quit:")
    except IOError as e:
        logging.info(e)    
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()
