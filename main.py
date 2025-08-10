import argparse
import sys
from mac_changer import *
from mac_changer import _1st_half_mac, _2nd_half_mac

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interface")
    parser.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    parser.add_argument('-i', '--interface', dest='interface', help='Specify the interface name')
    parser.add_argument('-m', '--manual', dest='manual', help='Manually change the MAC address. Root access needed')
    parser.add_argument('-a','--auto', dest='auto', help='Automatically change the MAC address')
    args = parser.parse_args()
    ifaces_macs = get_mac()
    if args.interface not in ifaces_macs.keys():
        ifaces_checking(args.interface, ifaces_macs)
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

    if args.auto:
        first_half =_1st_half_mac()
        sec_half = _2nd_half_mac
        auto_mac(first_half, sec_half)


if __name__ == '__main__':
    main()
