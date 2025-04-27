print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess

def get_unmounted_partitions():
    output = subprocess.check_output(['lsblk', '-o', 'NAME,MOUNTPOINT,TYPE', '-nr']).decode()
    unmounted = []

    for line in output.strip().split('\n'):
        parts = line.strip().split()
        name = parts[0]
        mountpoint = parts[1] if len(parts) > 1 else ''
        dev_type = parts[2]

        if dev_type == 'part' and not mountpoint:
            unmounted.append(f"/dev/{name}")

    return unmounted

if __name__ == "__main__":
    print("Unmounted partitions:")
    for dev in get_unmounted_partitions():
        print(dev)