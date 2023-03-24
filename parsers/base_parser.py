from abc import ABC, abstractmethod
from urllib.parse import urljoin

from bs4 import BeautifulSoup


# Define a base class for parsers
class BaseParser(ABC):
    def __init__(self, html_content):
        # Parse the HTML content using BeautifulSoup
        self.soup = BeautifulSoup(html_content, "html5lib")

    # Define an abstract method for extracting content
    @abstractmethod
    def extract_content(self):
        pass

    # Define a method for extracting links from the HTML
    def extract_links(self, base_url):
        links = set()

        # Find all anchor tags and iterate through them
        for link in self.soup.find_all("a"):
            href = link.get("href")
            if href:
                # Create a full URL using the base URL and the href attribute
                full_url = urljoin(base_url, href)
                links.add(full_url)
                print(f"Found link: {full_url}")

        return links
