print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess

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
    else:
        print("Unmounted partitions:")
        for dev in unmntd:
            print(dev)