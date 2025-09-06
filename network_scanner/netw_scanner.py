from scapy.all import Ether, ARP, srp


def arp_scan(ip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
    ans = srp(packet, timeout=2)[0]
    print("-------------------------------------------")
    print('MACs Adresses\t\tIP Adresses')
    print("-------------------------------------------")
    for elt in ans:
        print(elt[1].hwsrc,"\t", elt[1].psrc)
    print("-------------------------------------------")
    #print(ans.summary())
    #scapy.ls(scapy.ARP)


def get_ip(ip):
    pass


arp_scan("192.168.192.0/24")













































































































