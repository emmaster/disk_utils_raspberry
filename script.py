print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess
# old import
# from my_LCD_utils import print_txt_on_LCD
from my_LCD_utils2 import print_txt_on_LCD2
from my_file_db_utils import put_status_in_db, get_status_from_db
import sys
import time
from pathlib import Path
import shutil
import datetime

#### PATHES of NAS #####
##### CHICAGO #####
pi_nas_path_chi = "/home/klsnkv/mounted_media/chinas"
pi_nas_path_videos_chi = "/home/klsnkv/mounted_media/chinas/My videos"
pi_nas_path_photos_chi = "/home/klsnkv/mounted_media/chinas/Photo library ALL/Photos a New Era"

##### LISBON #####

###### PATHES of SD CARD #####
pi_sd_card_path = "/home/klsnkv/python_cron/mnt/sdcard"


####### reading status from previous runs #########

STATUS_DB_FILE = "/home/klsnkv/python_cron/status_db"

# status_object = {
#     "time": datetime.datetime.now(),
#     "payload": "fucking amazing",

#     "photos_subfolder_path": "/Volumes/Untitled/",
#     "photos_finished": True,

#     "videos_subfolder_path": "/Volumes/Untitled/",
#     "videos_finished": False,

#     'path': Path(db_file_path),
#     "finished": True,
# }

status_obj = get_status_from_db(STATUS_DB_FILE)
need_to_continue = False

if status_obj == {}:
    print("No status from previous run")
    print_txt_on_LCD2("No status from previous run. Creating a new one.", color="YELLOW", spinner_sec=1)

    status_obj = {
        "time": datetime.datetime.now(),
        "payload": "just created a new status object",
        
        "photos_finished": False,
        "videos_finished": False,

        "finished": False,
    }
    put_status_in_db(status_obj, STATUS_DB_FILE)
    need_to_continue = False
else:
    from_previous_run_minutes = (datetime.datetime.now() - status_obj["time"]).total_seconds() // 60

    if status_obj["finished"]:
        print(f"Previous run was: {from_previous_run_minutes} minutes ago. And it was finished.")
        print_txt_on_LCD2(f"Previous run was: {from_previous_run_minutes} minutes ago. And it was finished", color="GREEN", spinner_sec=1)
        need_to_continue = False
    else:
        print(f"Previous run was: {from_previous_run_minutes} minutes ago. And it was finished.")
        need_to_continue = True
        print_txt_on_LCD2(f"Previous run was: {from_previous_run_minutes} minutes ago. And it was NOT finished. TRYING to continue", color="YELLOW",font_size=20, spinner_sec=1)

#### WE HAVE A FLAG need_to_continue



####### FUNCTIONS ########

def get_unmounted_partitions():
    output = subprocess.check_output(['lsblk', '-o', 'NAME,MOUNTPOINT,TYPE', '-nr']).decode()
    output_list = output.strip().split('\n')
    unmounted = []

    for item in output_list:
        new_list = item.split()
        if len(new_list) <= 2 and new_list[1] == 'part':
            unmounted.append(f"/dev/{new_list[0]}")
    
    return unmounted

def copy_files_w_status(src_list, target_subfolder, label ="", max_retries = 3, sleep_between_retries = 1):
    
    copied = 0
    to_copy = len(src_list)
    
    if len(src_list) == 0:
        print(f"No files to copy for {label}")
        print_txt_on_LCD2(f"{label} No files to copy", font_size = 25, color="YELLOW")
        return
    
    for f in src_list:
        
        for attempt in range(1, max_retries + 1):
            with open("/home/klsnkv/python_cron/heartbeat.txt", "w") as hb:
                hb.write(f"Last alive: {datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d %H:%M:%S')}")
            try:
                new_full_path = target_subfolder / f.name
                if new_full_path.exists() and new_full_path.stat().st_size == f.stat().st_size:
                    copied += 1
                    continue
                shutil.copy2(f, target_subfolder)
                copied += 1
                if copied % 10 == 1:
                    completion = int((copied / to_copy) * 100)
                    print(f"Copied {copied} files")
                    print_txt_on_LCD2(f"{label} Copied {copied}/{to_copy} files", font_size = 25, color="GREEN", statusbar = completion)
                break
            except Exception as e:
                print(f"[Attempt: {attempt}/{max_retries}]Error copying {f}: {e}")
                print_txt_on_LCD2(f"[Attempt: {attempt}/{max_retries}] {label} Error copying {f}", font_size = 25, color="RED")
                if attempt < max_retries:
                    print(f"Retrying in {sleep_between_retries} seconds...")
                    time.sleep(sleep_between_retries)
                    continue
                sys.exit()

##### MAIN SCRIPT #####

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
        print_txt_on_LCD2(message, font_size = 16, color="GREEN", spinner_sec = 1)
        time.sleep(1)
    else:
        print("Not all directories are mounted")
        print_txt_on_LCD2(message, font_size = 16, color="RED")
        time.sleep(1)
        sys.exit()

    try:
        jpg_files = list(sd_card_dir.rglob('*.JPG'))
        arw_files = list(sd_card_dir.rglob('*.ARW'))
        mp4_files = list(sd_card_dir.rglob('*.MP4'))

        # earliest_jpg_date = datetime.datetime.fromtimestamp(min(jpg_files, key = lambda f: f.stat().st_mtime).stat().st_mtime)
        # earliest_arw_date = datetime.datetime.fromtimestamp(min(arw_files, key = lambda f: f.stat().st_mtime).stat().st_mtime)
        # earliest_mp4_date = datetime.datetime.fromtimestamp(min(mp4_files, key = lambda f: f.stat().st_mtime).stat().st_mtime)

        now = datetime.datetime.now()
        target_folder_name = now.strftime("%Y_%b") + "_byscript"

        msg = f"Found <br> {len(jpg_files)+len(arw_files)} images, <br> {len(mp4_files)} videos (MP4) <br> on SD card. <br> target folder: {target_folder_name}"
        print_txt_on_LCD2(msg, font_size = 25, color="GREEN", spinner_sec = 1)

        if len(jpg_files) == 0 and len(arw_files) == 0 and len(mp4_files) == 0:
            print("No files to transfer")
            print_txt_on_LCD2("No files found", font_size = 25, color="YELLOW")
            sys.exit()
        
        

        #### photos #####

        target_subfolder = None

        if len(jpg_files) > 0 or len(arw_files) > 0:
            if (nas_photo_dir / target_folder_name).is_dir():
                print(f"Folder {target_folder_name} already exists")
                print_txt_on_LCD2(f"[PHOTOS] Folder {target_folder_name} already exists", font_size = 25, color="YELLOW", spinner_sec= 0.5)
            else:
                print(f"Creating folder {target_folder_name} for photos")
                (nas_photo_dir / target_folder_name).mkdir(parents=False, exist_ok=False)
                print_txt_on_LCD2(f"[PHOTOS] Created folder {target_folder_name}", font_size = 25, color="GREEN", spinner_sec= 0.5)

            ## creating subfolders for JPG and ARW
            if need_to_continue and not status_obj["photos_finished"]:
                target_subfolder = Path(status_obj["photos_subfolder_path"])
                print(f"[PHOTOS] Continuing from previous run. Using folder {target_subfolder}")
                print_txt_on_LCD2(f"[PHOTOS] Continuing from previous run. Using folder {target_subfolder}", font_size = 20, color="YELLOW", spinner_sec= 0.5)
            else:
                for i in range(100):
                    if not (nas_photo_dir / target_folder_name / f"{i+1:03d}").is_dir():
                        (nas_photo_dir / target_folder_name / f"{i+1:03d}").mkdir(parents=False, exist_ok=False)
                        target_subfolder = (nas_photo_dir / target_folder_name / f"{i+1:03d}")
                        
                        status_obj["photos_subfolder_path"] = target_subfolder
                        status_obj["payload"] = "new photos subfolder created"
                        put_status_in_db(status_obj, STATUS_DB_FILE)

                        print(f"Creating folder {target_folder_name}/{i+1:03d} for photos")
                        print_txt_on_LCD2(f"[PHOTOS] Created folder {target_folder_name}/{i+1:03d}", font_size = 20, color="GREEN", spinner_sec= 0.5)
                        break
            
            status_obj["payload"] = "starting copying images"
            put_status_in_db(status_obj, STATUS_DB_FILE)

            #copying jpg files:
            copy_files_w_status(jpg_files, target_subfolder, label="[PHOTOS JPF]")

            #copying arw files:
            copy_files_w_status(arw_files, target_subfolder, label="[PHOTOS ARW]")

            print_txt_on_LCD2(f"[PHOTOS] Copied {len(jpg_files) + len(arw_files)} files", font_size = 25, color="GREEN", spinner_sec= 0.5)
            status_obj["payload"] = "finished copying images"
            status_obj["photos_finished"] = True
            put_status_in_db(status_obj, STATUS_DB_FILE)
        elif len(jpg_files) == 0 and len(arw_files) == 0:
            status_obj["photos_finished"] = True
            put_status_in_db(status_obj, STATUS_DB_FILE)
                    

        
        #### VIDEOS #####
        if len(mp4_files) > 0:
            if (nas_video_dir / target_folder_name).is_dir():
                print(f"Folder {target_folder_name} already exists")
                print_txt_on_LCD2(f"[VIDEOS] Folder {target_folder_name} already exists", font_size = 25, color="YELLOW", spinner_sec= 0.5)
            else:
                print(f"Creating folder {target_folder_name} for videos")
                (nas_video_dir / target_folder_name).mkdir(parents=False, exist_ok=False)
                print_txt_on_LCD2(f"[VIDEOS] Created folder {target_folder_name}", font_size = 25, color="GREEN", spinner_sec= 0.5)
            
            ## creating subfolders for Videos
            if need_to_continue and not status_obj["videos_finished"]:
                target_subfolder = Path(status_obj["videos_subfolder_path"])
                print(f"[VIDEOS] Continuing from previous run. Using folder {target_subfolder}")
                print_txt_on_LCD2(f"[VIDEOS] Continuing from previous run. Using folder {target_subfolder}", font_size = 20, color="YELLOW", spinner_sec= 0.5)
            else:
                for i in range(100):
                    if not (nas_video_dir / target_folder_name / f"{i+1:03d}").is_dir():
                        (nas_video_dir / target_folder_name / f"{i+1:03d}").mkdir(parents=False, exist_ok=False)
                        target_subfolder = (nas_video_dir / target_folder_name / f"{i+1:03d}")

                        status_obj["videos_subfolder_path"] = target_subfolder
                        status_obj["payload"] = "new videos subfolder created"
                        put_status_in_db(status_obj, STATUS_DB_FILE)

                        print(f"Creating folder {target_folder_name}/{i+1:03d} for videos")
                        print_txt_on_LCD2(f"[VIDEOS] Created folder {target_folder_name}/{i+1:03d}", font_size = 25, color="GREEN", spinner_sec= 0.5)
                        break
            
            status_obj["payload"] = "starting copying videos"
            status_obj["videos_finished"] = False
            put_status_in_db(status_obj, STATUS_DB_FILE)

            #copying mp4 files:
            copy_files_w_status(mp4_files, target_subfolder, label="[VIDEOS MP4]")

            print_txt_on_LCD2(f"[VIDEOS] Successfuly Copied {len(mp4_files)} files", font_size = 25, color="GREEN", spinner_sec= 0.5)
            status_obj["payload"] = "finished copying videos"
            status_obj["videos_finished"] = True
            put_status_in_db(status_obj, STATUS_DB_FILE)
        else:
            status_obj["videos_finished"] = True
            put_status_in_db(status_obj, STATUS_DB_FILE)
        
        status_obj["finished"] = True
        status_obj["time"] = datetime.datetime.now()
        status_obj["payload"] = "finished copying all files"
        put_status_in_db(status_obj, STATUS_DB_FILE)


            


    except Exception as e:
        print(f"Error: {e}")
        print_txt_on_LCD2("Error: with finding video/audio files", font_size = 25, color="RED")
        sys.exit()

    






    

    # print_txt_on_LCD2("Reached end of <br> script",color="GREEN")
        

    
