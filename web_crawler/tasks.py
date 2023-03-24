import logging
import asyncio

from fetcher.fetcher import fetch
from parsers.base_parser import BaseParser
from parsers.default_parser import DefaultParser
from parsers.image_parser import ImageParser
from parsers.product_parser import ProductParser
from storage.storage import Storage
from url_deduplication.url_deduplication import URLDeduplicator
from logger_config import logger
import base64
from celery_config import app


# Define a Celery task for the crawl_worker
@app.task(name="web_crawler.tasks.crawl_worker", bind=True)
def crawl_worker(self, url: str, deduplicator_state: str, db_name: str, connection_string: str):
    # Define an asynchronous function for crawling a single URL
    async def async_crawl_worker(url: str):
        # Check if the URL is already visited, and return early if it is
        if not url_deduplicator.add_url(url):
            return

        # Fetch the content of the URL
        response = await fetch(url)
        if response:
            logging.info(f"Fetched URL: {response['url']}, Status: {response['status_code']}")

            # Choose the appropriate parsers based on the URL or content type
            parser = ImageParser(response['text'])


            # Extract new URLs from the response and add them to the task queue
            new_links_added = 0
            new_links = parser.extract_links(response['url'])
            for new_link in new_links:
                if url_deduplicator.add_url(new_link):
                    deduplicator_state = base64.b64encode(url_deduplicator.get_state()).decode('utf-8')
                    crawl_worker.apply_async(args=(new_link, deduplicator_state, db_name, connection_string),
                                             queue="crawl_worker")
                    logger.debug(f"Added URL: {new_link}")
                    new_links_added += 1
                else:
                    logger.debug(f"Filtered duplicate URL: {new_link}")

            # Process the response data
            content = parser.extract_content()
            logger.debug(f"Extracted content: {content}")
            if content:
                # Save the extracted content to the storage
                if isinstance(content, list):
                    # Save the extracted content to the storage
                    storage.insert_content(url=response['url'], content=content)
                else:
                    logger.error(f"Content data type is not valid: {type(content)}, URL: {url}, Content: {content}")

    # Create an asyncio event loop and set up the crawl_worker
    loop = asyncio.new_event_loop()
    url_deduplicator = URLDeduplicator()
    url_deduplicator.set_state(base64.b64decode(deduplicator_state))
    deduplicator_state = base64.b64encode(url_deduplicator.get_state()).decode('utf-8')
    storage = Storage(db_name=db_name, connection_string=connection_string)

    # Run the asynchronous crawl_worker function for the given URL
    loop.run_until_complete(async_crawl_worker(url))
    loop.close()
