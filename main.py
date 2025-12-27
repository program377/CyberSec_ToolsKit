import argparse

from tables import Description
from network_scanner.netw_scanner import *
from mac_changer.mac_changer import *
from mac_changer.mac_changer import _1st_half_mac, _2nd_half_mac


def main():
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument('-n', '--network', dest='network', help='Specify the network')
   
    parser = argparse.ArgumentParser(description="Get the MAC address of any interfaces and modify MACs manually or automatically.")
    parser.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    parser.add_argument('-i', '--interface', dest='interface', help='Specify the interface name')
    parser.add_argument('-m', '--manual', dest='manual', help='Manually change the MAC address. Root access needed')
    parser.add_argument('-a','--auto', action='store_true', help='Automatically change the MAC address')
    args = parser.parse_args()
    ifaces_macs = get_mac()
#Mac_changer
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        ifaces_macs = get_mac()
        for iface, mac in ifaces_macs.items():
            print(f"Interface: {iface} -> MAC: {mac}")
        exit(0)
    if args.interface not in ifaces_macs.keys() or (args.manual and not args.interface):
        ifaces_checking(args.interface, ifaces_macs)
        sys.exit(1)
    if args.manual and args.interface:
        manual_mac(args.interface, args.manual)

    if args.interface in ifaces_macs:
        print(f"[+] Getting MAC of interface {args.interface} [+]")
        print(f"{args.interface} => {ifaces_macs[args.interface]}")

    if args.auto and args.interface:
        first_half =str(_1st_half_mac())
        sec_half = _2nd_half_mac()
        final_auto_mac =auto_mac(first_half, sec_half)
        manual_mac(args.interface, final_auto_mac)

#Network scan

    if args.network:
        ip = get_network(args.network)
        try:
            arp_scan(ip)
        except PermissionError as e:
            print(e)
            exit(1)


if __name__ == '__main__':
    main()

