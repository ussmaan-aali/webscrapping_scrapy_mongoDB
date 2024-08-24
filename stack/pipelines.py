# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
# from scrapy.conf import settings
# from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings


# class StackPipeline:
#     def process_item(self, item, spider):
#         return item


class MongoDBPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_URI']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            # log.msg("Question added to MongoDB database!",
            #         level=log.DEBUG, spider=spider)
        return item