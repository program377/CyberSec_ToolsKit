import scapy
import subprocess
import re

def get_mac(interface = None):


        if interface:
            try:
                output = subprocess.check_output(['ip', 'link', 'show', interface], text=True)
                mac = re.search(r"link/ether ([0-9a-f:]{17})")
                if mac:
                    print(f"{interface} => {mac.group(1)}")
                else:
                    print(f"[!] MAC address for {interface} not found [!]")
            except subprocess.CalledProcessError:
                print(f"[!] Interface {interface} not found [!]")
        else:
            try:
                output = subprocess.check_output(['ip', 'link', 'show'], text=True)
                mac = re.search()
                print(f"")
            except subprocess.CalledProcessError:
                print("[!] Error has been encountered [!]")

