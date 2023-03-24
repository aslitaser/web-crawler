import asyncio

from web_crawler.tasks import crawl_worker
from url_deduplication.url_deduplication import URLDeduplicator
from logger_config import logger
import base64


# Define an asynchronous main function
async def main():
    # Instantiate a URL deduplicator
    url_deduplicator = URLDeduplicator()

    # Define MongoDB database name and connection string
    db_name = "ecommerce_data"
    connection_string = "mongodb://localhost:27017/"

    # Add your seed URL(s) to the task queue
    start_url = "https://www.sahibinden.com/kategori/otomobil"

    # Get the current state of the deduplicator and encode it as a base64 string
    deduplicator_state = base64.b64encode(url_deduplicator.get_state()).decode('utf-8')

    # Add the crawl_worker task to the task queue with the necessary arguments
    crawl_worker.apply_async(args=(start_url, deduplicator_state, db_name, connection_string), queue="crawl_worker")

    # Log the added URL
    logger.debug(f"Added URL: {start_url}")


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
