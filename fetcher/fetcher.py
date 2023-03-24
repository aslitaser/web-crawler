import httpx
import tenacity
from aiolimiter import AsyncLimiter
from tenacity import retry, wait_random_exponential, stop_after_attempt
from urllib.parse import urlparse
import asyncio
from collections import defaultdict

from logger_config import logger

TIMEOUT = 10
RETRY_ATTEMPTS = 3

# Replace with your own proxy list
PROXIES = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
]

# Setup the rate limiter
global_limiter = AsyncLimiter(5, 1)  # 5 requests per second
domain_limiters = defaultdict(lambda: AsyncLimiter(1, 1))  # 1 request per second per domain


class FetchError(Exception):
    def __init__(self, message, original_exception):
        super().__init__(message)
        self.original_exception = original_exception


async def fetch(url, client=None):
    async def _fetch_with_retries(url, client):
        response = await client.get(url)

        if response.status_code != 200:
            raise httpx.HTTPStatusError(
                f"Status code: {response.status_code}",
                request=response.request,
                response=response
            )

        return {
            'url': str(response.url),
            'status_code': response.status_code,
            'text': response.text
        }

    async def fetch_retry(url, client, attempt=None):
        async with global_limiter:
            domain = urlparse(url).netloc
            async with domain_limiters[domain]:
                logger.debug(f"Fetching URL: {url}")

                if client is None:
                    client = httpx.AsyncClient(timeout=TIMEOUT)
                    client_created = True
                else:
                    client_created = False

                retryer = tenacity.AsyncRetrying(
                    retry=tenacity.retry_if_exception_type(httpx.RequestError),
                    wait=tenacity.wait_random_exponential(multiplier=1, max=60),
                    stop=tenacity.stop_after_attempt(RETRY_ATTEMPTS),
                    reraise=True
                )

                try:
                    response = await retryer.__call__(_fetch_with_retries, url, client)
                    return response

                except httpx.RequestError as e:
                    logger.error(f"Request error occurred while fetching {url}: {e}")
                    if attempt == RETRY_ATTEMPTS - 1:
                        raise FetchError(f"Request error occurred while fetching {url}: {e}", e)
                finally:
                    if client_created:
                        await client.aclose()

    return await fetch_retry(url, client)