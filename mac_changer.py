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
        pattern = re.compile(r"^\d+: ([\w@.\-]+):.*link/ether ([0-9a-f:]{17})", re.MULTILINE) # re.MULTILINE will match every lines after \n

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
    pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$") # Search for MAC address pattern 
    if os.geteuid() != 0:
        print("[!] Root privilege required [!]")
        exit(0)
    try:
        subprocess.run(['ip','link', 'set',iface, 'down'], text=True)
        cmd_outp = subprocess.run(['ip', 'link', 'set', iface, 'address', new_mac], check=True, capture_output=True, text=True)
        if pattern.match(new_mac):
            subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)
            print(f"[+] The new MAC of {iface} is {new_mac} [+]")
            exit(0)
    except subprocess.CalledProcessError as e:
        if "Invalid address length" in e.stderr:
            print("[!] System error :", e.stderr.strip(), "[!]")
        subprocess.run(['ip', 'link', 'set', iface, 'up'], check=True)

        exit(1)
    

def ifaces_checking(ifaces, mac_ifaces_dict):
    list_ifaces = list(mac_ifaces_dict.keys())
    print(f"[!] Failed to retrieve interface {ifaces} [!]")
    print(f"[i] Available interfaces: {list_ifaces} [i]")
    sys.exit(1)

def _1st_half_mac():
    """
    Gets all the keys of the dictionary (vendors) using .keys().
    Converts these keys to a list (because random.choice() requires a sequence).
    Selects one random vendor key from the list and stores it in rand_vendors.
    """
    with open('mac-vendors.json', "r") as file:
        mac_vendors = json.load(file) # Convert json into dictionary
    """
    Takes the list of MAC prefixes for the chosen vendor mac_vendors[rand_vendors].
    Converts the list to a set to remove duplicates.
    Checks if the vendor has 2 or more unique prefixes.
    Converts it to lowercase.
    """
    rand_vendors = random.choice(list(mac_vendors.keys()))
    if len(set(mac_vendors[rand_vendors])) >= 2: 
        first_raw_mac = str(random.choice(mac_vendors[rand_vendors])).lower()
    else:
        #Pads the prefix with leading zeros if it’s shorter than 6 characters (because MAC prefix is usually 6 hex digits).
        first_half_mac = mac_vendors[rand_vendors][0]
        first_raw_mac = first_half_mac.zfill(6).lower()
    """
    Splits the 6-character first_raw_mac string into 3 parts of 2 characters each.
    Joins these parts with a colon : separator to form a MAC-style prefix
    """
    first_half = ':'.join(first_raw_mac[i:i+2] for i in range(0, 6, 2))
    return first_half
    
def _2nd_half_mac():
    """
    Creates a list comprehension that runs random.randint(0x00, 0xff) 3 times.
    0x00 and 0xff are hexadecimal numbers (0 and 255 in decimal).
    Each call generates a random number between 0 and 255 (inclusive) — which is the valid range for a MAC address byte.
    """
    bytes = [random.randint(0x00, 0xff) for _ in range(3)]
    """
    Loops through each value b in the list bytes.
    f"{b:02x}" formats the number:
    02 → always 2 characters wide, padding with a leading zero if needed.
    x → format as lowercase hexadecimal (so 10 becomes "0a").
    Joins these formatted hex values with : separators to create a string
    """
    sec_half_mac = ':'.join(f"{b:02x}" for b in bytes) 
    return sec_half_mac


def auto_mac(first_half_mac, sec_half_mac):
    final_mac = f'{first_half_mac}:{sec_half_mac}'
    return final_mac






