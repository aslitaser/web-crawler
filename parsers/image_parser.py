# parsers/image_parser.py
from bs4 import BeautifulSoup
from parsers.base_parser import BaseParser


class ImageParser(BaseParser):
    def __init__(self, html_content):
        super().__init__(html_content)

    def extract_content(self):
        images = []

        for img in self.soup.find_all("img"):
            src = img.get("src")
            title = img.get("title")

            if src and title:
                images.append({"url": src, "title": title})
                print(f"Found image: {src}, Title: {title}")

        return images
