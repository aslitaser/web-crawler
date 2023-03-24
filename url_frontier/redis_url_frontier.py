import redis
from urllib.parse import urlparse

# Define a RedisURLFrontier class for managing URL frontier using Redis
class RedisURLFrontier:
    def __init__(self, host='localhost', port=6379, db=0):
        # Initialize a Redis connection
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db)
        self._url_queue_key = 'url_queue'
        self._url_set_key = 'url_set'
        self._domain_wait_times_key = 'domain_wait_times'

    # Define a method for adding a URL to the frontier
    def add_url(self, url, priority=0):
        if not self.redis_conn.sismember(self._url_set_key, url):
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            self.redis_conn.zadd(self._url_queue_key, {url: priority})
            self.redis_conn.sadd(self._url_set_key, url)

    # Define a method for getting the next URL from the frontier
    def get_next_url(self):
        url = self.redis_conn.zpopmin(self._url_queue_key)
        if url:
            url = url[0][0].decode()
            self.redis_conn.srem(self._url_set_key, url)
            return url
        return None

    # Define a method for checking if the frontier is empty
    def is_empty(self):
        return self.redis_conn.zcard(self._url_queue_key) == 0

    # Define methods for setting and getting wait times for domains
    def set_wait_time(self, domain, wait_time):
        self.redis_conn.hset(self._domain_wait_times_key, domain, wait_time)

    def get_wait_time(self, domain):
        return int(self.redis_conn.hget(self._domain_wait_times_key, domain) or 0)

    # Define a method for checking if a URL is already in the frontier and adding it if not
    def check_and_add(self, url):
        if self.redis_conn.sismember(self._url_set_key, url):
            return False
        else:
            self.add_url(url)
            return True

