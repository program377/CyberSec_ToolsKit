import subprocess
import re
import sys

def get_mac():
    """Returns a dictionary {interface: mac_address}"""
    mac_iface_dict = {}
    try:
        output = subprocess.check_output(['ip', '-o', 'link'], text=True) # This command display both the interface & mac on the same line
        pattern = re.compile(r"^\d+: ([\w@.\-]+):.*link/ether ([0-9a-f:]{17})", re.MULTILINE)

        for line in output.splitlines():
            match = pattern.match(line)
            if match:
                iface = match.group(1)
                mac = match.group(2)
                mac_iface_dict[iface] = mac
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to retrieve interface information.")
    return mac_iface_dict

def manual_mac(ifaces):
    try:
        output = subprocess.run(['ip','link', 'set', ifaces, 'down'], text=True)
    except subprocess.CalledProcessError:
        raise RuntimeError(f"Cannot find device {ifaces}")

def auto_mac():
    pass

def ifaces_checking(ifaces, iface_arg):
    if iface_arg not in ifaces:
        print(f"[!] Failed to retrieve interface {iface_arg} [!]")
        print(f"[i] Available interfaces: {list(ifaces.keys())}")
        sys.exit(1)




