import requests


class ThreatIntelligence:
    """
    Integrates multiple threat intelligence sources.
    """

    @staticmethod
    def correlate_mitre(data):
        """
        Correlates findings with MITRE ATT&CK framework.
        """
        print("Correlating vulnerabilities with MITRE ATT&CK...")
        mitre_map = {
            "open_port": "T1049",
            "default_credentials": "T1078",
            "public_s3_bucket": "T1530",
            "insecure_api": "T1132",
        }
        for item in data:
            tactic = mitre_map.get(item.get("issue_type"), "Unknown")
            item["mitre_tactic"] = tactic
        return data

    @staticmethod
    def get_cve_details(cve_id):
        """
        Fetches details about a CVE from CVE Details API.
        """
        url = f"https://cve.circl.lu/api/cve/{cve_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch CVE details for {cve_id}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching CVE details for {cve_id}: {e}")
        return {}

    @staticmethod
    def match_cves(vulnerabilities):
        """
        Matches vulnerabilities with CVE details.
        """
        print("Matching vulnerabilities with CVEs...")
        for vuln in vulnerabilities:
            if "cve" in vuln:
                vuln["cve_details"] = ThreatIntelligence.get_cve_details(vuln["cve"])
        return vulnerabilities

    @staticmethod
    def get_exploit_info(cve_id):
        """
        Fetches available exploits for a given CVE from Exploit Database.
        """
        url = f"https://www.exploit-db.com/search?cve={cve_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch exploit info for {cve_id}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching exploit info for {cve_id}: {e}")
        return {}

    @staticmethod
    def correlate_with_exploit_db(vulnerabilities):
        """
        Correlates vulnerabilities with Exploit Database.
        """
        print("Correlating vulnerabilities with Exploit Database...")
        for vuln in vulnerabilities:
            if "cve" in vuln:
                vuln["exploit_info"] = ThreatIntelligence.get_exploit_info(vuln["cve"])
        return vulnerabilities

    @staticmethod
    def get_alienvault_iocs(ip):
        """
        Retrieves threat intelligence indicators from AlienVault OTX.
        """
        url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch AlienVault OTX IOCs for IP: {ip}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching AlienVault OTX IOCs for IP: {ip}: {e}")
        return {}

    @staticmethod
    def correlate_with_alienvault(assets):
        """
        Correlates assets with AlienVault Open Threat Exchange.
        """
        print("Correlating assets with AlienVault OTX...")
        for asset in assets:
            if "ip" in asset:
                asset["alienvault_iocs"] = ThreatIntelligence.get_alienvault_iocs(asset["ip"])
        return assets
