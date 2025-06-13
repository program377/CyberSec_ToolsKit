import scapy
import subprocess
import argparse

def get_mac():
    cmd = ['ip', 'add', 'show']
    cmd_out= subprocess.run(cmd, capture_output=True)
    print(cmd_out)


parser= argparse.ArgumentParser(description="Get the MAC address of any interfaces")
parser.add_argument('-i', '--interface', required=True, help='Specify the interface')
args = parser.parse_args()
