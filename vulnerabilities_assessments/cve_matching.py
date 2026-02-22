from unittest.loader import VALID_MODULE_NAME

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
        cve_item = item["cve"]  # full dictionary
        cve_id = cve_item['id']

        # Default values in case CVSS data is missing
        base_score = "N/A"
        severity = "N/A"

        metrics = cve_item.get('metrics', {})
        if 'cvssMetricV2' in metrics:
            cvss = metrics['cvssMetricV2'][0]
            base_score = cvss['cvssData']['baseScore']
            severity = cvss.get('baseSeverity', 'N/A')
        elif 'cvssMetricV3' in metrics:
            cvss = metrics['cvssMetricV3'][0]
            base_score = cvss['cvssData']['baseScore']
            severity = cvss.get('baseSeverity', 'N/A')

    print(f"{cve_id} (CVSS {base_score} – {severity})")
    
    return vulnerabilities