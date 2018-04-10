#!/usr/bin/env python3
# Find Amazon Fire Sticks running ADB on network, requires arp-scan

import os
import sys
import socket
import subprocess
from contextlib import closing

# Port to use for ADB
adb_port = 5555

# Keyword to search MAC OUIs
arp_string = "Amazon"

# The code in this function will be executed when an ADB enabled device is found
# Any potentially harmful code added here is to be done so at your own risk
def payload(target_ip):
    print("Payload execute for %s" % target_ip)

# User must be root to run script
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script. Exiting.")

# Use arp-scan to get list of Amazon-made devices
print("Running arp-scan...")
try:
    amzdevices = subprocess.check_output("arp-scan --localnet | grep " + arp_string , shell=True).splitlines()
except subprocess.CalledProcessError:
    # Bail out if we didn't get any results
    print("No Amazon devices found!")
    exit()

# Check and display results
targetnumber = len(amzdevices)
if targetnumber > 0:
    print("Detected %i Amazon devices" % targetnumber)
else:
    # Bail out if we didn't get any results
    print("No Amazon devices found!")
    exit()

# Try to connect to ADB port on found devices
print("Scanning discovered Amazon devices...")
for target in amzdevices:
    target_ip = target.split()[0].decode('ascii').strip()
    print("%s:" % target_ip, end="")
    sys.stdout.flush()

    # Attempt to connect to ADB port
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        if sock.connect_ex((target_ip, adb_port)) == 0:
            print(" ADB Enabled")
            # Uncomment to enable payload function
            #payload(target_ip);
        else:
            print(" ADB Disabled")
