import requests

class VirusTotalDiscovery:
    """
    Integrates VirusTotal API to gather threat intelligence on assets.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"

    def scan_ip(self, ip):
        """
        Retrieves VirusTotal analysis for an IP address.
        """
        url = f"{self.base_url}/ip_addresses/{ip}"
        headers = {"x-apikey": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error in VirusTotal scan: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Error accessing VirusTotal API: {e}")
            return {}

    def run(self, assets):
        """
        High-level function to scan IPs with VirusTotal.
        """
        print("Running VirusTotal discovery...")
        results = []
        for asset in assets:
            if "ip" in asset:
                ip = asset["ip"]
                print(f"Scanning IP: {ip}")
                analysis = self.scan_ip(ip)
                results.append({
                    "ip": ip,
                    "malicious_count": analysis.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0),
                    "harmless_count": analysis.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("harmless", 0),
                })
        return results
