
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVD_API_KEY")
debug_mode = os.getenv("DEBUG", "False")

def query_nvd(service, version):
    keyword = f"{service} {version}"
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    params = {"keywordSearch": keyword, "resultsPerPage": 5}
    headers = {"apiKey": api_key}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    vulnerabilities = []
    for item in data.get("vulnerabilities", []):
        cve = item["cve"]["id"]
        vulnerabilities.append(cve)
        
    return vulnerabilities