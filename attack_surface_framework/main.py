from core.threat_intelligence import ThreatIntelligence
from core.asset_discovery import discover_assets
from core.plugin_manager import PluginManager
from core.reporting import (
    save_to_csv,
    save_to_json,
    generate_pdf_report,
    send_to_splunk,
    send_to_elasticsearch,
    summarize_results
)
import json


def main():
    """
    Entry point for the Attack Surface Framework.
    """
    print("Starting the Attack Surface Framework...")

    # Step 1: Discover assets
    print("Discovering assets...")
    assets = discover_assets()
    print(f"Discovered assets: {json.dumps(assets, indent=4)}")

    # Step 2: Load and execute plug-ins
    print("Loading and executing plug-ins...")
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    results = plugin_manager.execute_plugins(assets)

    # Step 3: Correlate with threat intelligence
    print("Correlating vulnerabilities with threat intelligence...")
    results = ThreatIntelligence.correlate_mitre(results)
    results = ThreatIntelligence.match_cves(results)
    results = ThreatIntelligence.correlate_with_exploit_db(results)
    assets = ThreatIntelligence.correlate_with_alienvault(assets)

    # Step 4: Summarize and generate reports
    print("Summarizing and generating reports...")
    summary = summarize_results(results)
    save_to_csv(summary, "summary_report.csv")
    save_to_json(results, "detailed_report.json")
    generate_pdf_report(results, "detailed_report.pdf")

    # Step 5: Send reports to external platforms (if configured)
    config = load_config()
    splunk_config = config.get("splunk", {})
    elastic_config = config.get("elasticsearch", {})

    if splunk_config.get("enabled"):
        print("Sending data to Splunk...")
        send_to_splunk(results, splunk_config["url"], splunk_config["token"])

    if elastic_config.get("enabled"):
        print("Sending data to Elasticsearch...")
        send_to_elasticsearch(results, elastic_config["url"], elastic_config["index"])

    print("Framework execution completed.")


def load_config(config_file="config.json"):
    """
    Load the configuration file.
    """
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return {}


if __name__ == "__main__":
    main()
