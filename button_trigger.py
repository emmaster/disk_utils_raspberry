from gpiozero import Button
from my_LCD_utils import print_txt_on_LCD
import subprocess
import time

button = Button(2)
button2 = Button(21)
#GPIO number 2 was plugged

button2.wait_for_press()
print("THE BUTTON (key1 P21) WAS PRESSED")
## print_txt_on_LCD("THE BUTTON\nWAS PRESSED!")
time.sleep(0.2)

# subprocess.run(["./launcher.sh"], check=True)
