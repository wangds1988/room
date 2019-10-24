# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymysql import connect


class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.client.room.ziroom.insert(item)
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    def open_spider(self, spider):
        self.client = connect(host="localhost", prot=3306, user="root", password="123456", db="room", charset="utf8")
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        args=[]
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
