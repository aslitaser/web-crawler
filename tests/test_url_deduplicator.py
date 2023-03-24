import pytest
from url_deduplication.url_deduplication import URLDeduplicator


@pytest.fixture
def url_deduplicator():
    return URLDeduplicator()


def test_add_url(url_deduplicator):
    url = "http://example.com"

    assert url_deduplicator.add_url(url) is True
    assert url_deduplicator.add_url(url) is False


def test_get_set_state(url_deduplicator):
    url1 = "http://example1.com"
    url2 = "http://example2.com"

    url_deduplicator.add_url(url1)
    state = url_deduplicator.get_state()

    new_deduplicator = URLDeduplicator()
    new_deduplicator.set_state(state)

    assert url1 in new_deduplicator.bloom_filter
    assert url2 not in new_deduplicator.bloom_filter
