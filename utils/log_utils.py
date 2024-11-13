import logging

def setup_logging():
    """Sets up the logging configuration for the application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_start_monitoring():
    """Logs the start of the monitoring process."""
    logging.info("Starting endpoint monitoring... Press CTRL+C to stop.")

def log_stop_monitoring():
    """Logs when the monitoring process is stopped by the user."""
    logging.info("Monitoring stopped by user. Exiting...")

def log_invalid_usage():
    """Logs an error message for incorrect usage."""
    logging.error("Usage: python3 monitor.py <path_to_yaml_file>")

def log_endpoint_status(name, url, status, latency_str):
    """
    Logs the status and latency of an endpoint.

    Args:
        name (str): The name of the endpoint.
        url (str): The URL of the endpoint.
        status (str): The status of the endpoint ('UP' or 'DOWN').
        latency_str (str): The formatted latency string or 'N/A'.
    """
    logging.info(f"{name} ({url}) is {status}, latency: {latency_str}")

def log_availability(stats):
    """
    Logs the availability percentage of each domain.

    Args:
        stats (dict): A dictionary where the key is the domain and the value is a tuple
                      (number of successful checks, total number of checks).
    """
    for domain, (successes, total) in stats.items():
        percentage = (successes / total) * 100 if total > 0 else 0
        logging.info(f"{domain} has {round(percentage)}% availability percentage")