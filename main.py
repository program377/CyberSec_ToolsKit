import argparse
import sys
from mac_changer import get_mac

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interface")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    group.add_argument('-i', '--interface', dest='interface', help='Specify the interface name')
    args = parser.parse_args()

    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        all_macs = get_mac()
        for iface, mac in all_macs.items():
            print(f"Interface: {iface} -> MAC: {mac}")
    else:
        macs = get_mac()  # this no longer prints anything
        if args.interface not in macs:
            print(f"[!] Failed to retrieve interface {args.interface} [!]")
            print(f"[i] Available interfaces: {list(macs.keys())}")
            sys.exit(1)
        else:
            print(f"[+] Getting MAC of interface {args.interface} [+]")
            print(f"{args.interface} => {macs[args.interface]}")

if __name__ == '__main__':
    main()
