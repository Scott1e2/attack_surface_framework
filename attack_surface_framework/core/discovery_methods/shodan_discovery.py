import requests

class ShodanDiscovery:
    """
    Integrates Shodan API to find publicly exposed assets.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"

    def search(self, query=""):
        """
        Searches Shodan for assets based on the query.
        """
        url = f"{self.base_url}/shodan/host/search"
        params = {"key": self.api_key, "query": query}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error in Shodan search: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error accessing Shodan API: {e}")
            return []

    def run(self, query=""):
        """
        High-level function to use Shodan for asset discovery.
        """
        print(f"Running Shodan discovery with query: {query}")
        results = self.search(query=query)
        assets = []
        for match in results.get("matches", []):
            assets.append({
                "ip": match.get("ip_str"),
                "port": match.get("port"),
                "hostnames": match.get("hostnames"),
                "org": match.get("org"),
                "isp": match.get("isp")
            })
        print(f"Discovered {len(assets)} assets using Shodan.")
        return assets
