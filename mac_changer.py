import subprocess
import re

def get_mac():
    """Returns a dictionary {interface: mac_address}"""
    mac_iface_dict = {}
    try:
        output = subprocess.check_output(['ip', '-o', 'link'], text=True)
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
