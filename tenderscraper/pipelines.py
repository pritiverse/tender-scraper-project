import pymongo
from scrapy.exceptions import DropItem

class MongoPipeline:
    collection_name = 'tenders'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'tenderdb')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # The item is already a dict, so insert it directly.
        try:
            self.db[self.collection_name].insert_one(dict(item))
            spider.logger.info(f"Tender saved: {item.get('tenderId', '')}")
            return item
        except Exception as e:
            spider.logger.error(f"Error inserting tender: {e}")
            raise DropItem(f"Error inserting tender: {e}")
