print("Hello to the script of disk copy utils for raspberry")
# some comments

import subprocess

def get_unmounted_partitions():
    output = subprocess.check_output(['lsblk', '-o', 'NAME,MOUNTPOINT,TYPE', '-nr']).decode()
    unmounted = []

    for line in output.strip().split('\n'):
        parts = line.strip().split()

        # Skip if not enough fields
        if len(parts) < 3:
            continue

        name = parts[0]
        mountpoint = parts[1]
        dev_type = parts[2]

        if dev_type == 'part' and mountpoint == '':
            unmounted.append(f"/dev/{name}")

    return unmounted

if __name__ == "__main__":
    print("Unmounted partitions:")
    for dev in get_unmounted_partitions():
        print(dev)