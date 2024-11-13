import pytest
from utils.log_utils import setup_logging, log_availability, log_endpoint_status
import logging

@pytest.fixture(autouse=True)
def setup_logging_fixture():
    """Sets up logging before each test."""
    setup_logging()

def test_log_availability(caplog):
    stats = {
        'example.com': (5, 10),  # 50% availability
        'another-example.com': (9, 9)  # 100% availability
    }
    with caplog.at_level(logging.INFO):
        log_availability(stats)
    assert "example.com has 50% availability percentage" in caplog.text
    assert "another-example.com has 100% availability percentage" in caplog.text

def test_log_endpoint_status(caplog):
    with caplog.at_level(logging.INFO):
        log_endpoint_status("Test Endpoint", "https://example.com", "UP", "120.00 ms")
    assert "Test Endpoint (https://example.com) is UP, latency: 120.00 ms" in caplog.text
