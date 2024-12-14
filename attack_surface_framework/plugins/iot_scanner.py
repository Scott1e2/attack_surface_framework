class IoTScannerPlugin:
    """
    Plug-in for scanning IoT devices for misconfigurations.
    """

    def run(self, assets):
        """
        Scan IoT devices.
        """
        print("IoTScannerPlugin: Scanning IoT devices...")
        results = []
        for asset in assets:
            if asset.get("type") == "iot":
                # Simulated IoT misconfiguration detection
                results.append({
                    "ip": asset["ip"],
                    "issue": "Default credentials detected"
                })
        return results
