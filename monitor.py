import asyncio
import aiohttp
import yaml
import time
from urllib.parse import urlparse
import logging

# Function to parse YAML configuration file
def parse_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Functions to perform an HTTP request and determine if it is UP or DOWN
async def fetch(session, endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper() # Default to 'GET' if method is not specified
    headers = endpoint.get('headers', {}) # Default to an empty dictionary if headers are not provided
    body = endpoint.get('body', None) # Default to None if body is not provided

    try:
        start_time = time.time()  # Start time before the request
        async with session.request(method, url, headers=headers, data=body, timeout=5) as response:
            end_time = time.time()  # End time after the request
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            is_up = response.status in range(200, 300) and latency < 500
            return endpoint['name'], url, is_up, latency
    except Exception as e:
        logging.warning(f"Request failed for {url}: {e}")
        return endpoint['name'], url, False, None

async def check_endpoints(endpoints):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)
    
# Function to track and log availability percentages
def log_availability(stats):
    for domain, (successes, total) in stats.items():
        percentage = (successes / total) * 100 if total > 0 else 0
        logging.info(f"{domain} has {round(percentage)}% availability percentage")

# Main function to run health checks in cycles
async def monitor_endpoints(file_path):
    endpoints = parse_yaml_file(file_path)
    domain_stats = {}
    logging.info("Starting endpoint monitoring... Press CTRL+C to stop.")
    
    try:
        while True:
            results = await check_endpoints(endpoints)
            for name, url, is_up, latency in results:
                domain = urlparse(url).netloc

                # Initialize stats if first time encountering domain
                if domain not in domain_stats:
                    domain_stats[domain] = [0, 0]  # [successes, total checks]

                # Update stats
                domain_stats[domain][1] += 1  # Increment total checks
                if is_up:
                    domain_stats[domain][0] += 1  # Increment successes

                # Log individual endpoint status
                status = "UP" if is_up else "DOWN"
                latency_str = f"{latency:.2f} ms" if latency is not None else "N/A"
                logging.info(f"{name} ({url}) is {status}, latency: {latency_str}")

            # Log the availability after each cycle
            log_availability(domain_stats)

            # Wait for 15 seconds before the next cycle
            await asyncio.sleep(15)

    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user. Exiting...")

# Run the program
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    if len(sys.argv) != 2:
        logging.error("Usage: python3 monitor.py <path_to_yaml_file>")
        sys.exit(1)
    asyncio.run(monitor_endpoints(sys.argv[1]))
