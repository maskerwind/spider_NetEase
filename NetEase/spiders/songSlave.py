# -*- coding: utf8 -*-

from NetEase.items import SongItem
from scrapy_redis.spiders import RedisSpider


class SongSlaveSpider(RedisSpider):
    name = 'slave_song'
    redis_key = "song:url"
    pre_url = "http://music.163.com/#"  # pre-link of album page
    # Song page
    def parse(self, response):
        song = SongItem()

        xpath_name = "//em[@class='f-ff2']/text()"
        xpath_singer = "//p[@class='des s-fc4']//span/@title"
        xpath_album = "//p[@class='des s-fc4'][2]//a/text()"
        xpath_comment_count = "//span[@id='cnt_comment_count']/text()"
        xpath_lyrics = "//div[@id='lyric-content']/text()"
        xpath_lyricsMore = "//div[@id='flag_more']/text()"  # show all
        xpath_albumIMG = "//div[@class='u-cover u-cover-6 f-fl']/img/@src"
        xpath_topCommentsDiv = "//div[count(preceding-sibling::h3[@class='u-hd4'])=1]"
        xpath_topComments = xpath_topCommentsDiv + "//div[@class='cnt f-brk']"
        xpath_topComments_author = xpath_topCommentsDiv + "//div[@class='cnt f-brk']/a/text()"
        xpath_topCommentsTime = xpath_topCommentsDiv + "//div[@class='time s-fc4']/text()"
        xpath_topCommentsCount = "//a[@data-type='like']/text()"

        song_name = response.xpath(xpath_name).extract()[0]
        song_singer = response.xpath(xpath_singer).extract()[0]
        song_album = response.xpath(xpath_album).extract()[0]

        song_commentCount = response.xpath(xpath_comment_count).extract()[0]
        song_albumIMG = response.xpath(xpath_albumIMG).extract()[0]
        lyrics = ''  # perhaps no lyrics here
        if response.xpath(xpath_lyrics):
            song_lyrics = response.xpath(xpath_lyrics).extract()
            if response.xpath(xpath_lyricsMore).extract():
                song_lyricsMore = response.xpath(xpath_lyricsMore).extract()
                lyrics = song_lyrics + song_lyricsMore
            else:
                lyrics = song_lyrics
        top_comments_list = []
        if response.xpath(xpath_topCommentsDiv):
            for i in range(len(response.xpath(xpath_topComments).extract())):
                top_comments_list.append(
                    {'Song_CommentContent': response.xpath(xpath_topComments)[i].xpath('string(.)').extract()[0],
                     'Song_CommentAuthor': response.xpath(xpath_topComments_author).extract()[i],
                     'Song_CommentTime': response.xpath(xpath_topCommentsTime).extract()[i],
                     'Song_CommentThumbsUp': response.xpath(xpath_topCommentsCount).extract()[i].strip('()')})

            for i in range(len(top_comments_list)):
                print(top_comments_list[i])

        song['Song_TopComments'] = top_comments_list
        song['Song_Link'] = response.url
        idDivider = 31 # extract id from song url
        song['SongID'] = response.url[idDivider:]
        song['Song_Name'] = song_name
        song['Song_Singer'] = song_singer
        song['Song_Ablum'] = song_album
        song['Song_lyrics'] = lyrics
        song['Song_CommentNum'] = song_commentCount
        song['Song_Ablum_IMG'] = song_albumIMG
        yield song
