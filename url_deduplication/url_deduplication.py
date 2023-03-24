from bloom_filter import BloomFilter
import pickle


# Define a URLDeduplicator class for managing URL deduplication
class URLDeduplicator:
    def __init__(self, max_elements: int = 1000000, error_rate: float = 0.1):
        # Initialize a BloomFilter for storing URLs and managing deduplication
        self.bloom_filter = BloomFilter(max_elements=max_elements, error_rate=error_rate)

    # Define a method for adding a URL to the BloomFilter and checking for duplicates
    def add_url(self, url: str) -> bool:
        if url in self.bloom_filter:
            return False
        self.bloom_filter.add(url)
        return True

    # Define a method for getting the current state of the BloomFilter
    def get_state(self):
        return pickle.dumps(self.bloom_filter)

    # Define a method for setting the state of the BloomFilter
    def set_state(self, state):
        self.bloom_filter = pickle.loads(state)
