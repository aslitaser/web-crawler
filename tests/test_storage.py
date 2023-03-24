import pytest
from mongomock import MongoClient
from storage.storage import Storage


@pytest.fixture
def mock_storage():
    connection_string = "mongodb://localhost:27017/"
    mock_client = MongoClient(connection_string)
    storage = Storage(db_name="test_db", connection_string=connection_string)
    storage.client = mock_client
    yield storage
    storage.close()


def test_insert_content(mock_storage):
    url = "http://example.com"
    content = "Example content"

    mock_storage.insert_content(url, content)
    document = mock_storage.contents_collection.find_one({"url": url})

    assert document is not None
    assert document["url"] == url
    assert document["content"] == content


def test_close(mock_storage):
    mock_storage.close()
    assert mock_storage.client is not None
    assert mock_storage.client.is_closed
