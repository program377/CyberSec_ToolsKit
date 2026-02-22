from os import *
import sys
from tabnanny import verbose
from hamcrest import none
from prompt_toolkit import print_formatted_text
from scapy.all import Ether, ARP, srp
import re
from nmap import PortScanner
from vulnerabilities_assessments.cve_matching import query_nvd




def arp_scan(ip):
    root_priv()
    if "/" not in ip:
        print('[-] ARP scan: use a CIDR range, not a single host [-]')
        sys.exit(0)
    mac_ip_list = []
    targets = {}
    arp_req_broad = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    answers = srp(arp_req_broad, timeout=2, verbose=False)[0]
    print("-" * 43)
    print('IP Adresses\t\tMACs Adresses')
    print("-" * 43) 
    for elt in answers:
        mac_ip_list.append(elt[1].psrc)
        print(elt[1].psrc,"  \t", elt[1].hwsrc)
    print("-" * 43)
    #print(mac_ip_list)
    #scapy.ls(scapy.ARP)
    return mac_ip_list


def get_network(ip):
    #Checking network input
    ip_regex = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:/(?:[0-9]|[12]\d|3[0-2]))?\b")
    if not ip_regex.fullmatch(ip):
        print("[-] Invalid IP Address ! [-]")
        sys.exit(0)
    return ip

    
def root_priv():
    if getuid() != 0:
        raise PermissionError("[-] Root privilege required [-]")
        sys.exit(1)
    
def nmap_engine(targets_ip):
    scanner = PortScanner()

    tcp_scan(scanner, targets_ip)
    display_scan_results(scanner, 'tcp')
    

    # udp_scan(scanner, targets_ip)
    # display_scan_results(scanner, 'udp')


def tcp_scan(scanner, targets_ip):
    tcp_args = '-sC -Pn -T4 -sV -sS --min-rate 1000 -p-'
    run_scan(scanner, targets_ip, tcp_args)

# def udp_scan(scanner, targets_ip):
#     print_formatted_text(color_depth=10)
#     udp_args = '-sC -Pn -T3 -sV -sU --min-rate 1000 -p-'
#     run_scan(scanner, targets_ip, udp_args)

def run_scan(scanner, targets_ip, scan_args):
    for ip in targets_ip:
        scanner.scan(ip, arguments=scan_args)



def display_scan_results(scanner, proto):
    
    for host in scanner.all_hosts():
        if proto not in scanner[host]:
            continue
        print("=" * 100)    
        title = f"Scan results for {host} ({proto.upper()})"
        print(title.center(100))
        print("=" * 100)
        print(f"{'PORT':<12}{'STATE':<12}{'SERVICE':<15} VERSION")

        # Collect vulnerabilities for this host
        vuln_results = set()

        # Loop through each port
        for port, data in scanner[host][proto].items():
            state = data.get('state', '')
            service = data.get('name', '')
            product = data.get('product', '')
            version = data.get('version', '')
            
            version_info = f"{product} {version} ".strip()
            port_proto = f"{port}/{proto}"
            print(f"{port_proto:<12}{state:<12}{service:<15}{version_info}")

            # Query NVD/CVEs for this service/version
            cves = query_nvd(service, version)
            if cves:
                service_key = f"{service} {version}".strip()
                vuln_results.add(
                f"{service_key}\n  - " + "\n  - ".join(sorted(cves))
                )

        # Print vulnerabilities once per host
        if vuln_results:
            print("-" * 50)
            print("[+] Vulnerabilities Assessment Results [+]")
            print("-" * 50)
            for v in vuln_results:
                print(v)

    return















































































































