import argparse
from netw_scanner import all, get_network


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--network', help='Specify the network')
    parser.add_argument('-n', '--network', dest='network', help='Specify the network')
    args = parser.parse_args()

    get_network()


if __name__ == '__main__':
    main()

