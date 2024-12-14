import requests


class APISecurityTesterPlugin:
    """
    Plug-in for testing API endpoints for security vulnerabilities.
    """

    def run(self, assets):
        """
        Test API endpoints.
        """
        print("APISecurityTesterPlugin: Testing API endpoints...")
        results = []
        for asset in assets:
            if "api_url" in asset:
                url = asset["api_url"]
                try:
                    response = requests.get(url)
                    results.append({
                        "url": url,
                        "status_code": response.status_code,
                        "content_length": len(response.content)
                    })
                except Exception as e:
                    results.append({
                        "url": url,
                        "error": str(e)
                    })
        return results
