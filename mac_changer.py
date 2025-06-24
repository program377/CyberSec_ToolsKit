import scapy
import subprocess
import re

def get_mac(interface = None):

    if interface:
        try:
            output = subprocess.check_output(['ip', 'link', 'show', interface], text=True)
            mac = re.search(r"link/ether ([0-9a-f:]{17})", output)
            if mac:
                print(f"{interface} => {mac.group(1)}")
            else:
                print(f"[!] MAC address for {interface} not found [!]")
        except subprocess.CalledProcessError:
            print(f"[!] Interface {interface} not found [!]")
    else:
        try:
            output = subprocess.check_output(['ip', '-o', 'link'], text=True)
            pattern = re.compile(r"^\d+: ([\w@.\-]+):.*link/ether ([0-9a-f:]{17})")
            for line in output.splitlines():
                match = pattern.match(line)
                if match:
                    iface, mac = match.groups()
                    print(f"Interface: {iface} -> MAC: {mac}")
        except subprocess.CalledProcessError:
            print("[!] Error has been encountered [!]")

