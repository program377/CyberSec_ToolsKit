import argparse
from mac_changer import get_mac

def main():
    parser = argparse.ArgumentParser(description="Get the MAC address of any interfaces")
    parser.add_argument(required=False, help='Display all interfaces MAC')
    parser.add_argument('-i', '--interface', dest='interface', required=True, help='Specify the interface')
    args = parser.parse_args()
    if args.interface:
        get_mac(args.interface)


if __name__ == '__main__':
    main()


