from parsers.base_parser import BaseParser


class ProductParser(BaseParser):
    def extract_content(self):
        product_data = {}

        # Extract the product title
        title = self.soup.find("h1", class_="product-title")
        if title:
            product_data["title"] = title.text.strip()

        # Extract the product price
        price = self.soup.find("span", class_="product-price")
        if price:
            product_data["price"] = float(price.text.strip().replace("$", ""))

        # Extract the product image URL
        image = self.soup.find("img", class_="product-image")
        if image:
            product_data["image_url"] = image["src"]

        return product_data
