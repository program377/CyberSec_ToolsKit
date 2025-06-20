import argparse
from mac_changer import get_mac

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interfaces")
    group =parser.add_mutually_exclusive_group(required=True)  #Create a group of exclusive args to use one of them
    group.add_argument('-all', action='store_true', help='Display all interfaces MAC')
    group.add_argument('-i', '--interface', dest='interface', help='Specify the interface')
    args = parser.parse_args()
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        get_mac()
    elif args.interface:
        print(f"[+] Geting MAC of interface {args.interaface} [+]")
        get_mac(args.interface)
    else:
        print("[+] Device {args.interface} does not exist [+]")



if __name__ == '__main__':
    main()


