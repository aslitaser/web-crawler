from parsers.base_parser import BaseParser


class DefaultParser(BaseParser):
    def extract_content(self):
        content = []
        paragraphs = self.soup.find_all("h2")
        for p in paragraphs:
            content.append(p.get_text(strip=True))

        return content
