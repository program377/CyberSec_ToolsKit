import argparse
from paste.flup_session import store_cache
from mac_changer import get_mac

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interfaces")
    parser.add_argument('-all',action=store_cache, help='Display all interfaces MAC')
    parser.add_argument('-i', '--interface', dest='interface', required=True, help='Specify the interface')
    args = parser.parse_args()
    if args.all:
        print("[+] Showing all interfaces MACs [+]")
        get_mac()
    elif args.interface:
        print(f"[+] Geting MAC of interface {args.interaface} [+]")
        get_mac(args.interface)
    else:
        print('Wrong interface specify')



if __name__ == '__main__':
    main()


