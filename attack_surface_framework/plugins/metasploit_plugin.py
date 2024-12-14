import subprocess

class MetasploitPlugin:
    """
    Uses Metasploit for penetration testing of discovered assets.
    """

    def run(self, target_ip):
        print(f"Running Metasploit scan on: {target_ip}")
        try:
            result = subprocess.run(
                ["msfconsole", "-q", "-x", f"db_nmap {target_ip}; exit"],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            print(f"Error running Metasploit: {e}")
            return "Error"
