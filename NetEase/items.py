# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SongListItem(scrapy.Item):
    # define the fields for your item here like:
    SongList_ID = scrapy.Field()
    SongList_Name = scrapy.Field()
    SongList_Link = scrapy.Field()
    SongList_Author = scrapy.Field()
    SongList_Author_Link = scrapy.Field()
    SongList_CreatTime = scrapy.Field()
    SongList_FavNum = scrapy.Field()
    SongList_ShareNum = scrapy.Field()
    SongList_CommentNum = scrapy.Field()
    SongList_PlayNum = scrapy.Field()
    SongList_IMG = scrapy.Field()
    SongList_Label = scrapy.Field()     # Tag List which multiple tags included
    SongList_Intro = scrapy.Field()
    SongList_TotalSongNum = scrapy.Field()
    SongList_SongRank = scrapy.Field()      # Song List includes multiple songs

class SongItem(scrapy.Item):
    # define the fields for your item here like:
    SongID = scrapy.Field()
    Song_Name = scrapy.Field()
    Song_Link = scrapy.Field()
    Song_Duration = scrapy.Field()
    Song_Singer = scrapy.Field()
    Song_lyrics = scrapy.Field()
    Song_Ablum = scrapy.Field()
    Song_Ablum_IMG = scrapy.Field()
    Song_CommentNum = scrapy.Field()
    Song_TopComments = scrapy.Field()      # multiple comments included