print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess
from my_LCD_utils import print_txt_on_LCD

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
    unmntd = get_unmounted_partitions()
    if len(unmntd) == 0:
        print("No unmounted partitions found.")
        print_txt_on_LCD("No unmonted\npartitions\nfound")
    else:
        print("Unmounted partitions:")
        print_txt_on_LCD(f"Found unmounted \npartitions:\n{len(unmntd)}!")
        for dev in unmntd:
            print(dev)

    if len(unmntd) > 0:
        print("Mounting all unmounted partitions...")
        mount_point = "./mnt/sdcard"
        for dev in unmntd:
            try:
                subprocess.run(['sudo','mount', dev, mount_point], check=True)
                print(f"Mounted {dev} to {mount_point}")
            except subprocess.CalledProcessError as e:
                print(f"Error mounting {dev}: {e}")
        

    
