# -*- coding: utf-8 -*-
import json
import pymongo
from scrapy.conf import settings
from items import SongListItem, SongItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# # write into json file
# class NeteasePipeline(object):
#     def open_spider(self, spider):
#         self.file = open('items.jl', 'w')
#
#     def close_spider(self, spider):
#         self.file.close()
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item


class NeteasePipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        self.db = client[dbname]




    def process_item(self, item, spider):

        sheetname_songlist = settings["MONGODB_SHEETNAME_SONGLISTS"]
        sheetname_song = settings["MONGODB_SHEETNAME_SONGS"]
        if isinstance(item, SongItem):
            # save to songs
            self.post = self.db[sheetname_song]
        elif isinstance(item, SongListItem):
            # save to songlists
            self.post = self.db[sheetname_songlist]

        data = dict(item)
        self.post.insert(data)
        return item
