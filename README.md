# 🛡️ CyberSecurity Toolkit

⚠️ Public repository for demonstration and learning purposes only.  
Copying is allowed, but modification, redistribution, or commercial use is strictly prohibited.

> A unified, modular Python-based cybersecurity toolkit built for network reconnaissance, vulnerability scanning, MAC spoofing, and web attack detection — all from a single CLI interface.

---

## 📌 Overview

Most security tools do one thing. This toolkit does many — designed to support a full recon-to-exploitation workflow from a single entry point.

Built from scratch as a hands-on project to understand offensive security concepts at a deeper level, with real-world applicability to penetration testing engagements.

---

## ⚡ Features

| Module | Flag | Description |
|--------|------|-------------|
| **ARP Scan** | `-p <network/cidr>` | Host discovery via ARP — maps live devices on a subnet |
| **TCP Scan** | `-t` | Nmap-powered TCP port scanner with service detection |
| **MAC Spoofer (Manual)** | `-i <iface> -m <mac>` | Change MAC address to a custom value |
| **MAC Spoofer (Auto)** | `-i <iface> -a` | Randomize MAC address automatically |
| **Interface Listing** | `--all` | Display all network interfaces and their MAC addresses |
| **LFI Scanner** | `--lfi <url>` | Detect Local File Inclusion vulnerabilities on a target URL |
| **CVE Detection** | built-in | Nmap scan results enriched with live CVE data via NVD API |

---

## 🚀 Usage

```bash
# Discover live hosts on a network
python3 main.py -p 192.168.1.0/24

# Run a TCP scan
python3 main.py -t 192.168.192.129

# List all interfaces and MACs
python3 main.py --all

# Change MAC address manually
python3 main.py -i eth0 -m 00:11:22:33:44:55

# Randomize MAC address
python3 main.py -i wlan0 -a

# Scan a URL for LFI vulnerabilities
python3 main.py --lfi http://target.com/page?file=test

# Full help
python3 main.py -h
```

---

## 🖥️ Demo

### TCP Scan + Live CVE Detection
```
$ python3 main.py -t 192.168.192.129

================================================================
         Scan results for 192.168.192.129 (TCP)
================================================================
PORT        STATE    SERVICE        VERSION
22/tcp      open     ssh            OpenSSH 5.3p1 Debian 3ubuntu4
80/tcp      open     http           Apache httpd 2.2.14
139/tcp     open     netbios-ssn    Samba smbd 3.X - 4.X
143/tcp     open     imap           Courier Imapd
443/tcp     open     http           Apache httpd 2.2.14
445/tcp     open     netbios-ssn    Samba smbd 3.X - 4.X
5001/tcp    open     java-object    Java Object Serialization
8080/tcp    open     http           Apache Tomcat/Coyote JSP engine 1.1
8081/tcp    open     http           Jetty 6.1.25
------------------------------------------------
[+] Vulnerabilities Assessment Results [+]
------------------------------------------------
http 6.1.25
  - CVE-2023-53231
http 2.2.14
  - CVE-2009-2699
  - CVE-2009-3555
  - CVE-2010-0425
  - CVE-2022-22344
  - CVE-2022-22354
```

> Real CVEs fetched live from the **NIST NVD API** and matched against detected service versions — giving instant vulnerability context per open port.

---

## 🛠️ Tech Stack

| Tool / Library | Purpose |
|----------------|---------|
| Python 3 | Core language |
| `argparse` | Unified CLI interface |
| `scapy` | ARP scanning and packet crafting |
| `python-nmap` | TCP/UDP port scanning engine |
| `requests` | NVD CVE API integration & LFI detection |
| `subprocess` / `re` | MAC address manipulation |

---

## 🔍 CVE Detection — How It Works

After a port/service scan, the toolkit queries the **NIST NVD API** in real time to fetch known CVEs matching the detected service versions. This means you get:

- Live vulnerability intelligence alongside your scan results
- CVE IDs, severity scores (CVSS), and descriptions
- Direct mapping from open ports → known exploits

---

## 🧠 MITRE ATT&CK Mapping

| Technique | ID | Module |
|-----------|----|--------|
| Network Service Discovery | T1046 | TCP/UDP Scan |
| Remote System Discovery | T1018 | ARP Scan |
| Defense Evasion via MAC Spoofing | T1564 | MAC Changer |
| Exploit Public-Facing Application (LFI) | T1190 | LFI Scanner |

---

## 📋 Installation

```bash
git clone https://github.com/yourusername/cybersec-toolkit.git
cd cybersec-toolkit
pip install -r requirements.txt

# Run with sudo (required for ARP and MAC operations)
sudo python3 main.py -h
```

---

## 🧠 What I Learned

- Designing a modular, extensible CLI architecture in Python
- Network reconnaissance at Layer 2 (ARP) and Layer 4 (TCP/UDP)
- Integrating live threat intelligence via the NVD CVE REST API
- Web vulnerability detection logic for LFI attack vectors
- Mapping real attack techniques to the MITRE ATT&CK framework

---

## 🗺️ Roadmap

- [ ] Advanced LFI/RFI detection RCE
- [ ] Add SQL injection scanner module
- [ ] Export scan results to JSON/HTML report
- [ ] Add IDOR detection to web scanner
- [ ] Integrate Shodan API for passive recon

---

## ⚠️ Disclaimer

This toolkit is built for **educational purposes and authorized penetration testing only**. Only use it on systems and networks you own or have explicit written permission to test. Unauthorized use is illegal.

---

## 👤 Author

**[xploitDev]** — CEH | Penetration Testing & Web Security  
🔗 [LinkedIn](https://www.linkedin.com/in/vanie-chadwick-eloge-133842146) · [HackTheBox](https://app.hackthebox.com/users/1668666)
