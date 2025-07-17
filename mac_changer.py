import os
import subprocess
import re
import sys
import json
import random

from django.template.defaultfilters import upper
from wtforms.validators import length


def get_mac():
    """Returns a dictionary {interface: mac_address}"""
    mac_iface_dict = {}
    try:
        output = subprocess.check_output(['ip', '-o', 'link'], text=True) # This command display both the interface & mac on the same line
        pattern = re.compile(r"^\d+: ([\w@.\-]+):.*link/ether ([0-9a-f:]{17})", re.MULTILINE) # Pattern to find entry like 01: ... link/ether

        for line in output.splitlines():
            match = pattern.match(line)
            if match:
                iface = match.group(1)
                mac = match.group(2)
                mac_iface_dict[iface] = mac # Add interface and mac to a dictionary
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to retrieve interface information.")
    return mac_iface_dict

def manual_mac(iface, new_mac):

    if os.geteuid() != 0:
        print("Root privilege required")
        return
    try:
        subprocess.run(['ip','link', 'set',iface, 'down'], text=True)
        subprocess.run(['ip', 'link', 'set', iface, 'address', new_mac], check=True)
        pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$") # Regex for MAC address
        if pattern.match(new_mac):
            subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
            print(f"[+] The new MAC of {iface} is {new_mac} [+]")
        else:
            print("[!] Invalid MAC address [!]")
    except subprocess.CalledProcessError as e:
        print("[!] Command failed [!]")

def ifaces_checking(ifaces, mac_ifaces_dict):
    list_ifaces = list(mac_ifaces_dict.keys())
    print(f"[!] Failed to retrieve interface {ifaces} [!]")
    print(f"[i] Available interfaces: {list_ifaces} [i]")
    sys.exit(1)

def auto_mac():

    with open('mac-vendors.json', "r") as file:
        mac_vendors = json.load(file) # Convert json into dictionary
    # Get the lists of vendor and convert mac_vendors.keys to list then pass it to random.choice which accept only list
    rand_vendors = random.choice(list(mac_vendors.keys()))

    if len(set(mac_vendors[rand_vendors])) >= 2: # Remove duplicate values and test if we have more than 1 value
        rand_first_half_mac = str(random.choice(mac_vendors[rand_vendors]))
    else:
        first_half_mac = mac_vendors[rand_vendors][0]
        first_raw_mac = first_half_mac.zfill(6).upper() # Select random first half MAC address
        print(first_raw_mac)
        new_rand_mac = ':'.join(first_raw_mac[i:i+2] for i in range(0, 6, 2))
        #new_mac_result = ":".join(new_rand_mac).upper()
        print(new_rand_mac)
        #






