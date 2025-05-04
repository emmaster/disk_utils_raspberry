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
                print_txt_on_LCD2(f"Mounted {dev} to {mount_point}", font_size=20, color="GREEN")
                time.sleep(1)
            except subprocess.CalledProcessError as e:
                print(f"Error mounting {dev}: {e}")
    

    print_txt_on_LCD2("lets do check of folders", color = "GREEN")

    nas_video_dir = Path(pi_nas_path_videos_chi)
    nas_photo_dir = Path(pi_nas_path_photos_chi)
    sd_card_dir = Path(pi_sd_card_path)
    
    all_is_mounted = False
    message = ""
    
    if nas_video_dir.is_dir() and any(nas_video_dir.iterdir()):
        all_is_mounted = True
        message += f"[CHECK] NAS video dir: is mounted <br> "
    else:
        all_is_mounted = False
        message += f"[ERROR] NAS video dir: is NOT mounted <br> "
    
    if nas_photo_dir.is_dir() and any(nas_photo_dir.iterdir()) and all_is_mounted:
        all_is_mounted = True
        message += f"[CHECK] NAS photo dir: is mounted <br> "
    else:
        all_is_mounted = False
        message += f"[ERROR] NAS photo dir: is NOT mounted <br> "

    if sd_card_dir.is_dir() and any(sd_card_dir.iterdir()) and all_is_mounted:
        all_is_mounted = True
        message += f"[CHECK] SD card dir: is mounted <br> "
    else:
        all_is_mounted = False
        message += f"[ERROR] SD card dir: is NOT mounted <br> "

    if all_is_mounted:
        print("All directories are mounted")
        print_txt_on_LCD2(message, font_size = 16, color="GREEN")
        time.sleep(1)
    else:
        print("Not all directories are mounted")
        print_txt_on_LCD2(message, font_size = 16, color="RED")
        time.sleep(1)
        sys.exit()





    

    # print_txt_on_LCD2("Reached end of <br> script",color="GREEN")
        

    
