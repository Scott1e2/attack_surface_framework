import nmap


def discover_network_assets(ip_range="192.168.1.0/24"):
    """
    Discovers network assets using Nmap with detailed port and service scanning.
    """
    print(f"Scanning network range: {ip_range}")
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments="-sS -T4")  # SYN scan

    assets = []
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            open_ports = nm[host].all_tcp()
            services = {port: nm[host]["tcp"][port]["name"] for port in open_ports}
            assets.append({
                "ip": host,
                "hostname": nm[host].hostname(),
                "state": nm[host].state(),
                "open_ports": open_ports,
                "services": services,
            })
    print(f"Discovered {len(assets)} network assets.")
    return assets
