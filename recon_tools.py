import subprocess

def nmap_scan(target):
    try:
        command = f"nmap -sS -sV {target}"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode == 0 and process.stdout:
            return process.stdout
        else:
            return "Nmap scan failed or returned no output."
    except Exception as e:
        return f"Error running Nmap: {str(e)}"


def find_subdomains(target):
    try:
        result = subprocess.run(["subfinder", "-d", target], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            return "Subfinder command failed or returned no output."
    except FileNotFoundError:
        return "Subfinder is not installed. Install it using: sudo apt install subfinder"

def whois_lookup(target):
    try:
        result = subprocess.run(["whois", target], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            return "WHOIS command failed or returned no output."
    except FileNotFoundError:
        return "WHOIS is not installed. Install it using: sudo apt install whois"




def scan_vulnerabilities(target):
    print(f"Scanning {target} for web vulnerabilities using Nikto...\n")

    try:
        result = subprocess.run(
            ["nikto", "-h", target],
            capture_output=True,
            text=True
        )

        scan_results = result.stdout.strip()
        error_results = result.stderr.strip()

        print("Raw Nikto Output:", scan_results)
        print("Raw Nikto Error Output:", error_results)

        if scan_results:
            fixes = suggest_fixes(scan_results)
            return scan_results + "\n\n💡 Suggested Fixes:\n" + fixes
        elif error_results:
            return f"Error during scan: {error_results}"
        else:
            return "Nikto scan returned no output."

    except FileNotFoundError:
        return "Nikto is not installed. Install it using: sudo apt install nikto"

def suggest_fixes(scan_results):
    """Analyzes scan results and suggests security fixes."""
    fixes = {
        "X-Frame-Options header is not present": 
            "Fix: Add 'X-Frame-Options: DENY' in server config to prevent clickjacking.",

        "X-Content-Type-Options header is not set": 
            "Fix: Add 'X-Content-Type-Options: nosniff' to prevent MIME-based attacks.",

        "clientaccesspolicy.xml contains a full wildcard entry": 
            "Fix: Restrict '*' in 'clientaccesspolicy.xml' to prevent unauthorized cross-domain access.",

        "crossdomain.xml contains a full wildcard entry": 
            "Fix: Restrict '*' in 'crossdomain.xml' to prevent cross-origin attacks.",

        "Retrieved x-powered-by header": 
            "Fix: Remove 'X-Powered-By' header to prevent information disclosure.",

        "Allowed HTTP Methods": 
            "Fix: Disable unused HTTP methods (e.g., PUT, DELETE) in the server configuration.",

        "Unencrypted login forms detected": 
            "Fix: Use HTTPS and secure cookies to protect login credentials."
    }

    found_fixes = False
    fixes_list = ""
    for issue, fix in fixes.items():
        if issue in scan_results:
            fixes_list += f"- {fix}\n"
            found_fixes = True

    if not found_fixes:
        fixes_list += "✅ No critical misconfigurations detected!"
    else:
        fixes_list = "🚨 Vulnerabilities Detected:\n" + fixes_list

    return fixes_list


