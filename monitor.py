import asyncio
import sys
from urllib.parse import urlparse
from utils.http_utils import check_endpoints
from utils.yaml_parser import parse_yaml_file
from utils.log_utils import setup_logging, log_start_monitoring, log_stop_monitoring, log_invalid_usage, log_endpoint_status, log_availability

async def monitor_endpoints(file_path):
    """Main function to monitor endpoints and log their availability."""
    endpoints = parse_yaml_file(file_path)
    domain_stats = {}

    log_start_monitoring()
    
    try:
        while True:
            # Fetch endpoint results concurrently
            results = await check_endpoints(endpoints)
            for name, url, is_up, latency in results:
                domain = urlparse(url).netloc

                # Initialize stats if first time encountering domain
                if domain not in domain_stats:
                    domain_stats[domain] = [0, 0]  # [successes, total checks]

                # Update stats
                domain_stats[domain][1] += 1  # Increment total checks
                if is_up:
                    domain_stats[domain][0] += 1  # Increment successes if 'is_up' is True

                # Log individual endpoint status
                status = "UP" if is_up else "DOWN"
                latency_str = f"{latency:.2f} ms" if latency is not None else "N/A"
                log_endpoint_status(name, url, status, latency_str)

            # Log the availability after each cycle
            log_availability(domain_stats)
            await asyncio.sleep(15)

    except asyncio.CancelledError:
        # Raise the exception to signal proper cancellation
        raise

if __name__ == "__main__":
    setup_logging()
    if len(sys.argv) != 2:
        log_invalid_usage()
        sys.exit(1)

    try:
        asyncio.run(monitor_endpoints(sys.argv[1]))  # Run the main async function
    except KeyboardInterrupt:
        log_stop_monitoring()  # Logs the message when the program is interrupted
        # Exit cleanly without traceback
