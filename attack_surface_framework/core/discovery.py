from core.discovery_methods.network_discovery import discover_network_assets
from core.discovery_methods.cloud_discovery import discover_aws_assets, discover_azure_assets, discover_gcp_assets
from core.discovery_methods.shodan_discovery import ShodanDiscovery
from core.discovery_methods.virustotal_discovery import VirusTotalDiscovery


def run_discovery(config):
    """
    Orchestrates all discovery methods based on configuration.
    """
    discovered_assets = []

    # Network Discovery
    if config.get("network_discovery", {}).get("enabled", False):
        print("Running Network Discovery...")
        ip_range = config["network_discovery"].get("ip_range", "192.168.0.0/24")
        discovered_assets.extend(discover_network_assets(ip_range))

    # Cloud Discovery
    if config.get("cloud_discovery", {}).get("aws", {}).get("enabled", False):
        print("Running AWS Discovery...")
        discovered_assets.extend(discover_aws_assets())
    if config.get("cloud_discovery", {}).get("azure", {}).get("enabled", False):
        print("Running Azure Discovery...")
        subscription_id = config["cloud_discovery"]["azure"].get("subscription_id")
        discovered_assets.extend(discover_azure_assets(subscription_id))
    if config.get("cloud_discovery", {}).get("gcp", {}).get("enabled", False):
        print("Running GCP Discovery...")
        discovered_assets.extend(discover_gcp_assets())

    # Shodan Integration
    if config.get("shodan", {}).get("enabled", False):
        print("Running Shodan Discovery...")
        api_key = config["shodan"].get("api_key")
        shodan = ShodanDiscovery(api_key)
        discovered_assets.extend(shodan.run(query=config["shodan"].get("query", "")))

    # VirusTotal Integration
    if config.get("virustotal", {}).get("enabled", False):
        print("Running VirusTotal Discovery...")
        api_key = config["virustotal"].get("api_key")
        virustotal = VirusTotalDiscovery(api_key)
        discovered_assets.extend(virustotal.run(discovered_assets))

    print(f"Total discovered assets: {len(discovered_assets)}")
    return discovered_assets
