class CloudSecurityPlugin:
    """
    Plug-in for evaluating cloud security configurations.
    """

    def run(self, assets):
        """
        Analyze cloud configurations.
        """
        print("CloudSecurityPlugin: Analyzing cloud configurations...")
        results = []
        for asset in assets:
            if "cloud_service" in asset:
                # Simulated cloud configuration analysis
                results.append({
                    "service": asset["cloud_service"],
                    "issue": "Public S3 bucket detected"
                })
        return results
