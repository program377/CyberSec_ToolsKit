import scapy
import subprocess

def get_mac(interface = None):
    if interface:
        cmd = ['ip', 'link', 'show', interface]
    else:
        cmd = ['ip', 'link', 'show']
    cmd_out= subprocess.run(cmd, capture_output=True, text=True)
    print(cmd_out.stdout)


