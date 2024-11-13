import yaml
import requests
import time
from urllib.parse import urlparse

# Function to parse YAML configuration file
def parse_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform an HTTP request and determine if it is UP or DOWN
def check_endpoint(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=5)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=5)
        else:
            response = requests.request(method, url, headers=headers, data=body, timeout=5)

        latency = response.elapsed.total_seconds() * 1000  # Convert to ms
        is_up = response.status_code in range(200, 300) and latency < 500
        return is_up

    except requests.exceptions.RequestException:
        return False

# Function to track and log availability percentages
def log_availability(stats):
    
    for domain, (successes, total) in stats.items():
        percentage = (successes / total) * 100 if total > 0 else 0
        print(f"{domain} has {round(percentage)}% availability percentage")

# Main function to run health checks in cycles
def monitor_endpoints(file_path):
    endpoints = parse_yaml_file(file_path)
    domain_stats = {}

    while True:
        for endpoint in endpoints:
            url = endpoint['url']
            domain = urlparse(url).netloc
            is_up = check_endpoint(endpoint)

            # Initialize stats if first time encountering domain
            if domain not in domain_stats:
                domain_stats[domain] = [0, 0]  # [successes, total checks]

            # Update stats
            domain_stats[domain][1] += 1  # Increment total checks
            if is_up:
                domain_stats[domain][0] += 1  # Increment successes

        # Log availability after each cycle
        log_availability(domain_stats)
        
        # Wait for 15 seconds before the next cycle
        time.sleep(15)

# Run the program
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 monitor.py <path_to_yaml_file>")
    else:
        monitor_endpoints(sys.argv[1])
