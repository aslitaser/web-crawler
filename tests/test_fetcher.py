import pytest
import httpx
from httpx import Response
from unittest.mock import AsyncMock, MagicMock
from fetcher.fetcher import fetch, FetchError, RETRY_ATTEMPTS

@pytest.mark.asyncio
async def test_fetch_successful():
    url = 'http://example.com'
    mock_text = 'Hello, world!'
    mock_status_code = 200

    dummy_request = httpx.Request('GET', url)
    mock_response = Response(status_code=mock_status_code, request=dummy_request)
    mock_response._content = mock_text.encode('utf-8')

    async with httpx.AsyncClient() as mock_client:
        mock_client.get = AsyncMock(return_value=mock_response)
        response = await fetch(url, client=mock_client)

        assert response["url"] == url
        assert response["status_code"] == mock_status_code
        assert response["text"] == mock_text

