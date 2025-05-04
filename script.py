print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess
# from my_LCD_utils import print_txt_on_LCD
from my_LCD_utils2 import print_txt_on_LCD2
import sys
import time
from pathlib import Path
import shutil

#### PATHES of NAS #####
##### CHICAGO #####
pi_nas_path_chi = "/home/klsnkv/mounted_media/chinas"
pi_nas_path_videos_chi = "/home/klsnkv/mounted_media/chinas/My videos"
pi_nas_path_photos_chi = "/home/klsnkv/mounted_media/chinas/Photo library ALL/Photos a New Era"

##### LISBON #####

###### PATHES of SD CARD #####
pi_sd_card_path = "/home/klsnkv/python_cron/mnt/sdcard"


def get_unmounted_partitions():
    output = subprocess.check_output(['lsblk', '-o', 'NAME,MOUNTPOINT,TYPE', '-nr']).decode()
    output_list = output.strip().split('\n')
    unmounted = []

    for item in output_list:
        new_list = item.split()
        if len(new_list) <= 2 and new_list[1] == 'part':
            unmounted.append(f"/dev/{new_list[0]}")
    
    return unmounted

if __name__ == "__main__":
    mount_point = "./mnt/sdcard"
    subprocess.run(['sudo', 'umount', mount_point])
    unmntd = get_unmounted_partitions()
    if len(unmntd) == 0:
        print("No unmounted partitions found.")
        print_txt_on_LCD2("No unmonted partitions found",color="RED")
        sys.exit()
    else:
        print("Unmounted partitions:")
        print_txt_on_LCD2(f"Found unmounted partitions: {len(unmntd)} !")
        for dev in unmntd:
            print(dev)

    if len(unmntd) > 0:
        print("Mounting all unmounted partitions...")
        for dev in unmntd:
            try:
                subprocess.run(['sudo','mount', dev, mount_point], check=True)
                print(f"Mounted {dev} to {mount_point}")
                print_txt_on_LCD2(f"Mounted {dev} to {mount_point}")
            except subprocess.CalledProcessError as e:
                print(f"Error mounting {dev}: {e}")

    

    print_txt_on_LCD2("Reached end of\nscript",color="GREEN")
        

    
