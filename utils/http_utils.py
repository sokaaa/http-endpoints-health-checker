import asyncio
import aiohttp
import time
import logging

async def fetch(session, endpoint):
    """Asynchronously fetch an HTTP response for a given endpoint."""
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
    """Run multiple fetch calls concurrently and gather results."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)