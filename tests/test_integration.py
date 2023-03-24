import pytest
import httpx
from fetcher.fetcher import fetch
from storage.storage import Storage
from url_deduplication.url_deduplication import URLDeduplicator
from url_frontier.redis_url_frontier import RedisURLFrontier
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
from time import sleep

# Set up a simple HTTP server for testing
class TestHTTPServer(HTTPServer):
    allow_reuse_address = True

class TestServer:
    def __init__(self, port):
        self.port = port
        self.handler = SimpleHTTPRequestHandler
        self.httpd = TestHTTPServer(("", port), self.handler)

    def start(self):
        self.thread = Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.thread.join()

# Run a test server for the duration of the tests
@pytest.fixture(scope="module")
def test_server():
    server = TestServer(8080)
    server.start()
    yield server
    server.stop()

# Create a Storage instance for the duration of the tests
@pytest.fixture(scope="module")
def storage():
    storage = Storage()
    yield storage
    storage.close()

# Create a URLDeduplicator instance for the duration of the tests
@pytest.fixture(scope="module")
def url_deduplicator():
    deduplicator = URLDeduplicator()
    yield deduplicator

# Create a RedisURLFrontier instance for the duration of the tests
@pytest.fixture(scope="module")
def redis_url_frontier():
    frontier = RedisURLFrontier()
    frontier.redis_conn.flushdb()
    yield frontier
    frontier.redis_conn.flushdb()

@pytest.mark.asyncio
async def test_integration(test_server, storage, url_deduplicator, redis_url_frontier):
    url = "http://localhost:8080/test.html"
    redis_url_frontier.add_url(url)
    next_url = redis_url_frontier.get_next_url()

    assert next_url == url
    url_deduplicator.add_url(url)  # Add the URL to the deduplicator
    assert url_deduplicator.add_url(url) is False

    async with httpx.AsyncClient() as client:
        response = await fetch(next_url, client)
        assert response["status_code"] == 200
        assert response["url"] == url

        storage.insert_content(response["url"], response["text"])
        assert storage.contents_collection.count_documents({'url': response["url"]}) == 1
