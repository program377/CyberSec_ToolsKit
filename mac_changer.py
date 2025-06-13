import scapy
import subprocess
import argparse


def get_cmd():
    cmd = ['ip', 'add', 'show']
    cmd_out= subprocess.run(cmd, capture_output=True)
    print(cmd_out)


parse= argparse.ArgumentParser(description="Get the MAC address of ")
