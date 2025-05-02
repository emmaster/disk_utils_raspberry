from gpiozero import Button
from my_LCD_utils import print_txt_on_LCD

button = Button(2)
#GPIO number 2 was plugged

button.wait_for_press()
print("THE BUTTON WAS PRESSED")
print_txt_on_LCD("THE BUTTON\nWAS PRESSED!")

