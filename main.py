import argparse
import sys
from mac_changer import *

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interface")
    parser.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    parser.add_argument('-i', '--interface', dest='interface', help='Specify the interface name')
    parser.add_argument('-m', '--manual', dest='manual', help='Manually change the MAC address. Root access needed')
    args = parser.parse_args()
    ifaces_macs = get_mac()

    if args.manual and not args.interface:
        ifaces_checking(ifaces_macs, args.interface)
        sys.exit(1)
    if args.manual and args.interface:
        manual_mac(args.interface, args.manual)
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        ifaces_macs = get_mac()
        for iface, mac in ifaces_macs.items():
            print(f"Interface: {iface} -> MAC: {mac}")

    if args.interface in ifaces_macs:
        print(f"[+] Getting MAC of interface {args.interface} [+]")
        print(f"{args.interface} => {ifaces_macs[args.interface]}")

    # if args.manual and not args.interface:
    #     ifaces_checking(ifaces_macs, args.interface)
    #     pass
    #     #manual_mac(args.interface)
    #     #ifaces_checking(ifaces_macs, args.interface)
    #     # manual_mac(args.interface)
    #     # if args.interface not in ifaces_macs:
    #     #     ifaces_checking(ifaces_macs, args.interface)
    #
    # #else:
    #     #ifaces_checking(ifaces_macs, args.interface)


if __name__ == '__main__':
    main()
