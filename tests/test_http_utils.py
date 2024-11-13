import pytest
import aiohttp
from utils.http_utils import fetch, check_endpoints
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_fetch_success():
    # Mock the response to work with both `async with` and `await`
    with patch("aiohttp.ClientSession.request") as mock_request:
        async def mock_aenter(_):
            mock_response = AsyncMock()
            mock_response.status = 200
            return mock_response
        
        async def mock_aexit(obj, exc_type, exc, tb):
            return

        mock_request.return_value.__aenter__ = mock_aenter
        mock_request.return_value.__aexit__ = mock_aexit

        async with aiohttp.ClientSession() as session:
            result = await fetch(session, {'name': 'test', 'url': 'https://example.com', 'method': 'GET'})
            assert result[2] is True  # is_up should be True
            assert result[3] is not None  # latency should be present

@pytest.mark.asyncio
async def test_fetch_failure():
    with patch("aiohttp.ClientSession.request") as mock_request:
        async def mock_aenter(_):
            mock_response = AsyncMock()
            mock_response.status = 500
            return mock_response
        
        async def mock_aexit(obj, exc_type, exc, tb):
            return

        mock_request.return_value.__aenter__ = mock_aenter
        mock_request.return_value.__aexit__ = mock_aexit

        async with aiohttp.ClientSession() as session:
            result = await fetch(session, {'name': 'test', 'url': 'https://example.com', 'method': 'GET'})
            assert result[2] is False  # is_up should be False
            assert result[3] is not None  # latency should still be present

@pytest.mark.asyncio
async def test_check_endpoints():
    with patch("aiohttp.ClientSession.request") as mock_request:
        async def mock_aenter(_):
            mock_response = AsyncMock()
            mock_response.status = 200
            return mock_response
        
        async def mock_aexit(obj, exc_type, exc, tb):
            return

        mock_request.return_value.__aenter__ = mock_aenter
        mock_request.return_value.__aexit__ = mock_aexit

        endpoints = [
            {'name': 'test1', 'url': 'https://example1.com', 'method': 'GET'},
            {'name': 'test2', 'url': 'https://example2.com', 'method': 'GET'}
        ]

        async with aiohttp.ClientSession() as session:
            results = await check_endpoints(endpoints)
            assert len(results) == 2
            for result in results:
                assert result[2] is True  # All should be UP
