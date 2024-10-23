import subprocess
import sys
import requests
from bs4 import BeautifulSoup

# Function to install a package using pip
def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Function to check if a package is installed, if not, install it
def check_and_install(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
        print(f"'{package_name}' is already installed.")
    except ImportError:
        print(f"'{package_name}' not found. Installing...")
        install_package(package_name)

# Ensure required packages are installed
def setup():
    check_and_install('requests')
    check_and_install('bs4', 'bs4')
    
def get_ip_httpbin():
    response = requests.get('https://httpbin.org/ip')
    data = response.json()
    return data['origin']

# Function to get public IP and location details using ipinfo.io with a token
def get_ip_ipinfo():
    token = "3c9355c23d88d9"  # Your actual ipinfo.io token
    response = requests.get(f'https://ipinfo.io/json?token={token}')
    data = response.json()
    
    ip = data.get('ip', 'N/A')
    country = data.get('country', 'N/A')
    isp = data.get('org', 'N/A')
    timezone = data.get('timezone', 'N/A')
    loc = data.get('loc', 'N/A')
    
    # Check if 'loc' contains latitude and longitude
    if loc != 'N/A' and ',' in loc:
        latitude, longitude = loc.split(',')
        return ip, country, isp, timezone, latitude, longitude
    
    return ip, country, isp, timezone, 'N/A', 'N/A'

# Function to get public IP from ifconfig.me
def get_ip_ifconfigme():
    response = requests.get('https://ifconfig.me')
    return response.text.strip()

def main():
    ip_sources = {
        'httpbin': (get_ip_httpbin, False),
        'ipinfo': (get_ip_ipinfo, True),
        'ifconfigme': (get_ip_ifconfigme, False)
    }
    
    for name, (func, has_location) in ip_sources.items():
        try:
            if has_location:
                ip, country, isp, timezone, latitude, longitude = func()
                print(f"Your public IP address from {name}: {ip}")
                print(f"Country: {country}")
                print(f"ISP: {isp}")
                print(f"Timezone: {timezone}")
                print(f"Latitude: {latitude}, Longitude: {longitude}\n")
            else:
                ip = func()
                print(f"Your public IP address from {name}: {ip}\n")
        except Exception as e:
            print(f"Failed to get IP from {name}: {e}\n")

if __name__ == "__main__":
    main()