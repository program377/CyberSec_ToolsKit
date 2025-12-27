import argparse

from tables import Description
from netw_scanner import *


def main():
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument('-n', '--network', dest='network', help='Specify the network')
    args = parser.parse_args()

    if args.network:
        ip = get_network(args.network)
        arp_scan(ip)


if __name__ == '__main__':
    main()

