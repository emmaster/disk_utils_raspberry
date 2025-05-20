# -*- coding:utf-8 -*-
import spidev as SPI
import logging
import sys
import time
import subprocess
import atexit
import random

sys.path.append("/home/klsnkv/1.3inch_LCD_HAT_code/1.3inch_LCD_HAT_code/python")

from my_LCD_utils3 import print_txt_on_LCD3
import script3

import ST7789
from PIL import Image,ImageDraw,ImageFont

# 240x240 display with hardware SPI:
disp = ST7789.ST7789()
disp.Init()

# Clear display.
disp.clear()

#Set the backlight to 100
disp.bl_DutyCycle(50)

Font1 = ImageFont.truetype("./Font/SuisseIntl-Medium-WebM.ttf", 22)


image = Image.open('./assets/greeting_image.jpg')
image = image.rotate(0)
disp.ShowImage(image)
time.sleep(3)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image1)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
disp.ShowImage(image1)

run_cycle = True
refresh_display = True

cycle_count = 0

try:
    while run_cycle:
        cycle_count += 1
        if cycle_count > 24:
            cycle_count = 0
            # Randomly change the background color
            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if refresh_display:
                image1 = Image.new("RGB", (disp.width, disp.height), random_color)
                draw = ImageDraw.Draw(image1)
                disp.ShowImage(image1)
        # with canvas(device) as draw:
        if disp.digital_read(disp.GPIO_KEY_UP_PIN ) == 0: # button is released
            ...
            # draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0xff00)  #Up        
        else: # button is pressed:
            refresh_display = True
            draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up filled
            print ("Up")
            
        if disp.digital_read(disp.GPIO_KEY_LEFT_PIN) == 0: # button is released
            ...
            # draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0xff00)  #left           
        else: # button is pressed:
            refresh_display = True
            draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left filled
            print ("left") 
            
        if disp.digital_read(disp.GPIO_KEY_RIGHT_PIN) == 0: # button is released
            ...
            # draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0xff00) #right        
        else: # button is pressed:
            refresh_display = True
            draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right filled
            print ("right")
            
        if disp.digital_read(disp.GPIO_KEY_DOWN_PIN) == 0: # button is released
            ...# draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0xff00) #down        
        else: # button is pressed:
            refresh_display = True
            draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down filled
            print ("down")
            
        if disp.digital_read(disp.GPIO_KEY_PRESS_PIN) == 0: # button is released
            ...# draw.rectangle((20, 22,40,40), outline=255, fill=0xff00) #center         
        else: # button is pressed:
            refresh_display = True
            draw.rectangle((20, 22,40,40), outline=255, fill=0) #center filled
            print ("center")
            
        if disp.digital_read(disp.GPIO_KEY1_PIN) == 0: # button is released
            ...# draw.ellipse((70,0,90,20), outline=255, fill=0xff00) #A button        
        else: # button is pressed:
            refresh_display = True
            draw.ellipse((70,0,90,20), outline=255, fill=0) #A button filled
            print ("KEY1")
            print_txt_on_LCD3(disp, "KEY1: launching copying", font_size=20, color="WHITE", statusbar=False, spinner_sec=1)
            try:
                script3.copying_files(disp)
                refresh_display = False
            except Exception as e:
                print_txt_on_LCD3(disp, f"Error during copying: {e}", font_size=20, color="RED", spinner_sec=3)
                print("Error during copying function: ", e)

            
        if disp.digital_read(disp.GPIO_KEY2_PIN) == 0: # button is released
            ...# draw.ellipse((100,20,120,40), outline=255, fill=0xff00) #B button]        
        else: # button is pressed:
            refresh_display = True
            draw.ellipse((100,20,120,40), outline=255, fill=0) #B button filled
            print_txt_on_LCD3(disp, "KEY2 pressed", font_size=20, color="WHITE", statusbar=False, spinner_sec=2)
            print ("KEY2")
            
        if disp.digital_read(disp.GPIO_KEY3_PIN) == 0: # button is released
            ...# draw.ellipse((70,40,90,60), outline=255, fill=0xff00) #A button        
        else: # button is pressed:
            refresh_display = True
            draw.ellipse((70,40,90,60), outline=255, fill=0) #A button filled
            draw.text([15, 90], 'KEY3 pressed = Exit', font=Font1, fill = (200,200,200))

            print ("KEY3")
            print ("Exit")
            run_cycle = False
        
        if refresh_display:
            disp.ShowImage(image1)
        
        if run_cycle == False:
            time.sleep(1)
except:
	print("except")
disp.module_exit()


#### MY CLEANUP FUNCTION ####
def cleanup():
    print("[LCD_w_keys_autorun] Cleaning up before exit")
    if disp:
        disp.module_exit()

atexit.register(cleanup)