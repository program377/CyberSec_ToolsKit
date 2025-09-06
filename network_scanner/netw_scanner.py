from scapy.all import Ether, ARP, srp


def arp_scan(ip):
    mac_ip_list = []
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    ans = srp(packet, timeout=2)[0]
    print("-------------------------------------------")
    print('IP Adresses\t\tMACs Adresses')
    print("-------------------------------------------")
    for elt in ans:
        mac_ip_list.append(elt[1].psrc)
        print(elt[1].psrc,"  \t", elt[1].hwsrc)
    print("-------------------------------------------")
    print(mac_ip_list)
    #scapy.ls(scapy.ARP)
    return mac_ip_list


def get_network(ip):
    pass

def nmap_enum():
    pass


arp_scan("192.168.192.0/24")













































































































