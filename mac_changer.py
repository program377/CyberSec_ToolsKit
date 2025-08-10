import os
import subprocess
import re
import sys
import json
import random

from django.template.defaultfilters import upper
from numpy.ma.core import concatenate
from numpy.testing.overrides import allows_array_ufunc_override
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
        pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$") # Search for MAC address pattern 
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

def _1st_half_mac():
    with open('mac-vendors.json', "r") as file:
        mac_vendors = json.load(file) # Convert json into dictionary
    """
    Gets all the keys of the dictionary (vendors) using .keys().
    Converts these keys to a list (because random.choice() requires a sequence).
    Selects one random vendor key from the list and stores it in rand_vendors.
    """
    rand_vendors = random.choice(list(mac_vendors.keys()))
    """
    Takes the list of MAC prefixes for the chosen vendor mac_vendors[rand_vendors].
    Converts the list to a set to remove duplicates.
    Checks if the vendor has 2 or more unique prefixes.
    """
    if len(set(mac_vendors[rand_vendors])) >= 2: 
        first_raw_mac = str(random.choice(mac_vendors[rand_vendors])).lower()
    else:
        first_half_mac = mac_vendors[rand_vendors][0]  # Get the first string
        first_raw_mac = first_half_mac.zfill(6).lower() # Fill up with preceding zero until the num of character is 6
    first_half = ':'.join(first_raw_mac[i:i+2] for i in range(0, 6, 2))
    return first_half
    
def _2nd_half_mac():
    bytes = [random.randint(0x00, 0xff) for _ in range(3)]
    sec_half_mac = ':'.join(f"{b:02x}" for b in bytes)
    return sec_half_mac


def auto_mac(first_half, sec_half_mac):
    first_half_mac = _1st_half_mac()
    sec_half_mac = _2nd_half_mac()
    final_mac = concatenate(first_half_mac, sec_half_mac)






