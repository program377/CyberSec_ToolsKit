import subprocess
import re
import sys

def get_mac(interface=None):
    mac_iface_dict = {}
    try:
        output = subprocess.check_output(['ip', '-o', 'link'], text=True)
        pattern = re.compile(r"^\d+: ([\w@.\-]+):.*link/ether ([0-9a-f:]{17})", re.MULTILINE)

        for line in output.splitlines():
            match = pattern.match(line)
            if match:
                iface = match.group(1).split('@')[0]
                mac = match.group(2)
                mac_iface_dict[iface] = mac

        if interface:
            if interface in mac_iface_dict:
                print(f"{interface} => {mac_iface_dict[interface]}")
            else:
                print(f"[!] Interface '{interface}' not found. Available: {list(mac_iface_dict.keys())}")
                sys.exit(1)

    except subprocess.CalledProcessError:
        print("[!] Failed to retrieve interface information.")
        sys.exit(1)

    return mac_iface_dict
