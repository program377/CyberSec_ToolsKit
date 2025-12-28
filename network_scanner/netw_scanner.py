from os import *
import sys
from tabnanny import verbose
from hamcrest import none
from scapy.all import Ether, ARP, srp
import re
from nmap import PortScanner



def arp_scan(ip):
    root_priv()
    if "/" not in ip:
        print('[-] ARP scan: use a CIDR range, not a single host [-]')
        sys.exit(0)
    mac_ip_list = []
    targets = {}
    arp_req_broad = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    answers = srp(arp_req_broad, timeout=2, verbose=False)[0]
    print("-------------------------------------------")
    print('IP Adresses\t\tMACs Adresses')
    print("-------------------------------------------") 
    for elt in answers:
        mac_ip_list.append(elt[1].psrc)
        print(elt[1].psrc,"  \t", elt[1].hwsrc)
    print("-------------------------------------------")
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
    

def nmap_engine(targets_ip):
    scanner = PortScanner()
    for ip in targets_ip:
        scanner.scan(ip, arguments='-sC -Pn -T3 -sV --min-rate 1000 -p-')
        print(f"[+] Scan result for {ip} [+]")
        if 'tcp' in scanner[ip]:
            for port in scanner[ip]['tcp']:
                state = scanner[ip]['tcp'][port]['state']
                service = scanner[ip]['tcp'][port]['name']
                version = scanner[ip]['tcp'][port]['version']
                print(f"{port}/tcp  {state} - {service} - {version}")




    















































































































