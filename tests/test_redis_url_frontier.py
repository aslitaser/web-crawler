import pytest
from url_frontier.redis_url_frontier import RedisURLFrontier
@pytest.fixture
def redis_url_frontier():
    frontier = RedisURLFrontier()
    frontier.redis_conn.flushdb()
    yield frontier
    frontier.redis_conn.flushdb()

def test_add_get_next_url(redis_url_frontier):
    url = "http://example.com"

    redis_url_frontier.add_url(url)
    assert redis_url_frontier.get_next_url() == url
    assert redis_url_frontier.is_empty() is True

def test_set_get_wait_time(redis_url_frontier):
    domain = "http://example.com"
    wait_time = 60

    redis_url_frontier.set_wait_time(domain, wait_time)
    assert redis_url_frontier.get_wait_time(domain) == wait_time

def test_check_and_add(redis_url_frontier):
    url = "http://example.com"

    assert redis_url_frontier.check_and_add(url) is True
    assert redis_url_frontier.check_and_add(url) is False
