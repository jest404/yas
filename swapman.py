#!/usr/bin/env python3

# GNU GPL 3.0, see license file for details
# Author: Lohrrrr, Jester404
# TODO replace all sudo calls with just hope of that user is running as su. This will allow users without SUDO use this script too. For example with doas.
import subprocess
import sys

def print_commands():
    print("Select something:")
    print(" [1] - Create a new swapfile and enable it (require sudo)")
    print(" [2] - Create a new swapfile")
    print(" [3] - Show UUID of swapfile (for fstab)")
    print(" [4] - Open fstab config (require sudo)")
    print(" [5] - Enable all (require sudo)")
    print(" [6] - Detect filesystem type")
    print(" [7] - List all swapfiles")
    print(" [8] - Disable all swaps (require sudo)")

def get_swap_size():
    while True:
        try:
            size = int(input("Enter swap size in GB (max 4): "))
            if 0 < size <= 4:
                return size
            print("Size must be between 1 and 4 GB")
        except ValueError:
            print("Invalid input, enter a number")

def get_swapfile_name():
    name = input("Enter swapfile name (default: swapfile): ").strip()
    return name if name else "swapfile"

def parse_size(size_str): # TODO add any other size detection, for example 512M or 1TB
    size_str = size_str.upper()
    if size_str.endswith("G"):
        return int(size_str[:-1])
    elif size_str.endswith("GB"):
        return int(size_str[:-2])
    else:
        return int(size_str)

def detect_filesystem():
    result = subprocess.run("df / | awk 'NR==2 {print $1}'", shell=True, capture_output=True, text=True)
    device = result.stdout.strip()
    result = subprocess.run(f"lsblk -no FSTYPE {device}", shell=True, capture_output=True, text=True)
    fstype = result.stdout.strip()
    return fstype

def create_swap(name=None, size=None, enable=False):
    if not name:
        name = get_swapfile_name()
    if not size:
        size = get_swap_size()
    
    fstype = detect_filesystem()
    path = f"/{name}"
    
    if fstype == "btrfs":
        subprocess.run(f"sudo touch {path}", shell=True)
        subprocess.run(f"sudo chattr +C {path}", shell=True)
    
    subprocess.run(f"sudo dd if=/dev/zero of={path} bs=1G count={size}", shell=True)
    subprocess.run(f"sudo chmod 600 {path}", shell=True)
    subprocess.run(f"sudo mkswap {path}", shell=True)
    
    if enable:
        subprocess.run(f"sudo swapon {path}", shell=True)
        print(f"Swapfile created and enabled: {name} ({size}G)")
    else:
        print(f"Swapfile created: {name} ({size}G)")

def show_uuid(name=None):
    if not name:
        name = get_swapfile_name()
    path = f"/{name}"
    result = subprocess.run(f"blkid {path}", shell=True, capture_output=True, text=True)
    print(result.stdout if result.stdout else f"Swapfile {name} not found")

def open_fstab():
    subprocess.run("sudo nano /etc/fstab", shell=True)

def enable_all():
    subprocess.run("sudo swapon -a", shell=True) #FIXME this should enable swapfiles
    print("All swaps enabled")

def list_swaps():
    result = subprocess.run("swapon --show", shell=True, capture_output=True, text=True)
    print(result.stdout if result.stdout else "No active swaps")

def disable_all():
    subprocess.run("sudo swapoff -a", shell=True)
    print("All swaps disabled")

def print_help():
    print("Usage: swapman <command> [options]")
    print("\nCommands:")
    print("  create <size> [--name NAME] [--now]  Create swapfile (size: 1G-4G), --now to enable")
    print("  uuid [--name NAME]                   Show UUID of swapfile")
    print("  fstab                                Open fstab config (require sudo)")
    print("  enable                               Enable all swaps (require sudo)")
    print("  fs                                   Detect filesystem type")
    print("  list                                 List all swapfiles")
    print("  disable                              Disable all swaps (require sudo)")
    print("  help                                 Show this help message")
    print("  interactive                          Start interactive mode")

def main():
    if len(sys.argv) < 2:
        interactive_mode()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    elif command == "interactive":
        interactive_mode()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Usage: yas create <size> [--name NAME] [--now]")
            return
        size = parse_size(sys.argv[2])
        name = "swapfile"
        enable_now = False
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == "--name" and i + 1 < len(sys.argv):
                name = sys.argv[i + 1]
            elif sys.argv[i] == "--now":
                enable_now = True
        
        create_swap(name, size, enable_now)
    elif command == "uuid":
        name = "swapfile"
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--name" and i + 1 < len(sys.argv):
                name = sys.argv[i + 1]
        show_uuid(name)
    elif command == "fstab":
        open_fstab()
    elif command == "enable":
        enable_all()
    elif command == "fs":
        fstype = detect_filesystem()
        print(f"Filesystem: {fstype}")
    elif command == "list":
        list_swaps()
    elif command == "disable":
        disable_all()
    else:
        print(f"Unknown command: {command}")
        print_help()

def interactive_mode():
    RUN = True
    print("'Let's download some ram' - Bringus Studios.")
    print("Basically just yet another swap manager...\n")
    
    while RUN:
        print_commands()
        cmd = input(":$/  ")
        if cmd == "1":
            create_swap(enable=True)
        elif cmd == "2":
            create_swap(enable=False)
        elif cmd == "3":
            show_uuid()
        elif cmd == "4":
            open_fstab()
        elif cmd == "5":
            enable_all()
        elif cmd == "6":
            fstype = detect_filesystem()
            print(f"Filesystem: {fstype}")
        elif cmd == "7":
            list_swaps()
        elif cmd == "8":
            disable_all()
        else:
            print("Invalid command\n")

if __name__ == "__main__":
    main()
