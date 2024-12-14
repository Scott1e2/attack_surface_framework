import requests


def discover_api_endpoints(openapi_url, zap_enabled=False, zap_url=None):
    """
    Discovers API endpoints using OpenAPI or OWASP ZAP if enabled.
    """
    print(f"Fetching OpenAPI specification from: {openapi_url}")
    response = requests.get(openapi_url)
    spec = response.json()

    endpoints = []
    for path, methods in spec["paths"].items():
        for method in methods:
            endpoints.append({
                "path": path,
                "method": method.upper()
            })

    if zap_enabled and zap_url:
        print("Using OWASP ZAP for API endpoint testing...")
        # Add OWASP ZAP integration logic here

    print(f"Discovered {len(endpoints)} API endpoints.")
    return endpoints
