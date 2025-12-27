import argparse
from netw_scanner import all, arp_scan, get_network


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--network', dest='network', help='Specify the network')
    args = parser.parse_args()

    if args.network:
        get_network(args.network)
        arp_scan(args.network)
        #


if __name__ == '__main__':
    main()

