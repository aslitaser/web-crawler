from pymongo import MongoClient

# Define a Storage class for managing data storage
class Storage:
    def __init__(self, db_name="ecommerce_data", connection_string="mongodb://localhost:27017/"):
        # Initialize the MongoDB client and select the database and collection
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.contents_collection = self.db["contents"]

    # Define a method for inserting content into the database
    def insert_content(self, url, content):
        try:
            document = {
                'url': url,
                'content': content,
            }
            self.contents_collection.insert_one(document)
        except Exception as e:
            print(f"Error inserting content: {e}")

    # Define a method for closing the MongoDB client connection
    def close(self):
        self.client.close()
