import scapy
import subprocess
import re

def get_mac(interface = None):

    possible_interface_prefixes = [
        "eth",  # Legacy (eth0, eth1)
        "enp",  # Predictable (enp0s3, enp3s0)
        "ens",  # Predictable (ens33, ens1)
        "eno",  # Predictable (eno1, eno2)
        "wl",  # Wi-Fi (wlan0, wlp2s0)
        "wlan",  # Legacy Wi-Fi (wlan0, wlan1)
        "br",  # Bridges (br0)
        "virbr",  # Virtual bridges (virbr0)
        "tap",  # Tap devices (tap0)
        "tun",  # Tunnel interfaces (tun0)
        "vmnet",  # VMware interfaces
        "veth",  # Docker/Podman virtual Ethernet
        "docker",  # Docker bridge
    ]

    if interface:
        try:
            output = subprocess.check_output(['ip', 'link', 'show', interface], text=True)
            mac = re.search(r"link/ether ([0-9a-f:]{17})", output)
            if mac:
                print(f"\t{interface} => {mac.group(1)}")
            else:
                print(f"[!] MAC address for {interface} not found [!]")
        except subprocess.CalledProcessError:
            print(f"[!] Interface {interface} not found [!]")
    else:
        try:
            output = subprocess.check_output(['ip', 'link'], text=True)
            #  line starts with a number and capture group for the interface name (letters, numbers, underscores, dots, hyphens, or @
            iface_pattern = re.compile(r"^\d+: ([\w@.\-]+)")
            mac_pattern = re.compile(r"link/ether ([0-9a-f:]{17})")
            ifaces_list = []
            macs_list = []
            for lines in output.splitlines():
                ifaces_match = iface_pattern.match(lines)
                macs_match = mac_pattern.match(lines)
                if ifaces_match:
                    ifaces_list.append(ifaces_match.group(1))
                if macs_match:
                    macs_list.append(macs_match.group(1))
            pairing = list(zip(ifaces_list, macs_list))
            for interf, mac in pairing:
                print(f"Interface: {interf} -> MAC: {mac}")
        except subprocess.CalledProcessError:
            print("[!] Error has been encountered [!]")


