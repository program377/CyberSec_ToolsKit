import argparse
import sys
from mac_changer import *

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interface")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    group.add_argument('-i', '--interface', dest='interface', help='Specify the interface name')
    group.add_argument('-m', '--manual', dest='manual', help='Manually change the MAC address')
    args = parser.parse_args()
    ifaces_macs = get_mac()
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        # ifaces_macs = get_mac()
        for iface, mac in ifaces_macs.items():
            print(f"Interface: {iface} -> MAC: {mac}")

    elif args.interface in ifaces_macs:
        print(f"[+] Getting MAC of interface {args.interface} [+]")
        print(f"{args.interface} => {ifaces_macs[args.interface]}")
    else:
        ifaces_checking(ifaces_macs, args.interface)


if __name__ == '__main__':
    main()
