import argparse

from tables import Description
from network_scanner.netw_scanner import *
from mac_changer.mac_changer import *
from mac_changer.mac_changer import _1st_half_mac, _2nd_half_mac


def main():
    parser = argparse.ArgumentParser(description="Cyber Security Toolkit")
    parser.add_argument('-p', '--arp-scan', metavar='', dest='arpscan', help='Hosts Discovery - Specify the network along with cidr(e.g:10.x.x.x/x)')
    parser.add_argument('-t', '--tcp-scan', dest='tcpscan', metavar='', help='TCP Nmap Engine scan')


    parser.add_argument('--all', action='store_true', help='Display all interfaces MACs')
    parser.add_argument('-i', '--interface', dest='interface', metavar='', help='Specify the interface name')
    parser.add_argument('-m', '--manual', dest='manual', metavar='', help='Manually change the MAC address')
    parser.add_argument('-a','--auto', action='store_true', help='Automatically change the MAC address')
    args = parser.parse_args()
    ifaces_macs = get_mac()
    
# -------- MAC CHANGER --------
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        ifaces_macs = get_mac()
        for iface, mac in ifaces_macs.items():
            print(f"Interface: {iface} -> MAC: {mac}")
        exit(0)

    if args.interface:
        if args.interface not in ifaces_macs:
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

# -------- NETWORK SCANNER --------
    if args.arpscan:
        ip = get_network(args.arpscan)
        try:
            targets_ip = arp_scan(ip)
        except PermissionError as e:
            print(e)
            exit(1)
    nmap_engine()


if __name__ == '__main__':
    main()

