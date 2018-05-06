# -*- coding: utf8 -*-
from NetEase.items import SongListItem
from scrapy_redis.spiders import RedisSpider
from redis import Redis


class SongListSlaveSpider(RedisSpider):
    name = 'slave_songlist'
    redis_key = "songlist:url"
    pre_url = "http://music.163.com/#"  # pre-link of album page

    def parse(self, response):
        redis = Redis()
        song_list = SongListItem()

        # information from uploader class=user f-cb part
        xpath_songlistName = "//h2[@class='f-ff2 f-brk']/text()"
        xpath_songList_IMG = "//img[@class='j-img']/@src"

        xpath_uploaderName = "//span[@class='name']/a/text()"
        xpath_uploaderLink = "//span[@class='name']/a/@href"
        xpath_uploadTime = "//div[@class='user f-cb']//span[@class='time s-fc4']/text()"

        # basic information of song list
        xpath_types = "//a[@class='u-tag']/i/text()"
        xpath_songcount = "//*[@id='playlist-track-count']/text()"
        xpath_playcount = "//*[@id='play-count']/text()"
        xpath_intro = "//p[@id='album-desc-more']/text()"

        # information of song list from id=content-operation part
        xpath_fav = "//div[@id='content-operation']/a[3]/i/text()"
        xpath_share = "//div[@id='content-operation']/a[4]/i/text()"
        xpath_commentCount = "//span[@id='cnt_comment_count']/text()"

        # songs in the list from table
        xpath_table = "//table[@class='m-table ']/tbody//tr"
        xpath_songLink = xpath_table + "/td[2]//span/a/@href"

        songlistName = response.xpath(xpath_songlistName).extract()[0]
        songlistIMG = response.xpath(xpath_songList_IMG).extract()[0]
        uploaderName = response.xpath(xpath_uploaderName).extract()[0]
        uploaderLink = self.pre_url + response.xpath(xpath_uploaderLink).extract()[0]
        uploadTime = response.xpath(xpath_uploadTime).extract()[0]
        lables = []
        for lable in response.xpath(xpath_types).extract():
            lables.append(lable)
        playCount = response.xpath(xpath_playcount).extract()[0]
        songCount = response.xpath(xpath_songcount).extract()[0]
        albumIntro = response.xpath(xpath_intro).extract()

        favCount = response.xpath(xpath_fav).extract()[0].strip('()')
        shareCount = response.xpath(xpath_share).extract()[0].strip('()')
        commentCount = response.xpath(xpath_commentCount).extract()[0]

        container_songLink = response.xpath(xpath_songLink)
        songsID = []

        idDivider = 9 # extract id from song url
        for i in range(int(songCount)):
            songsID.append(container_songLink.extract()[i][idDivider:])


        song_list['SongList_Link'] = response.url
        song_list['SongList_Name'] = songlistName
        song_list['SongList_IMG'] = songlistIMG
        song_list['SongList_Author'] = uploaderName
        song_list['SongList_Author_Link'] = uploaderLink
        song_list['SongList_CreatTime'] = uploadTime
        song_list['SongList_FavNum'] = favCount
        song_list['SongList_ShareNum'] = shareCount
        song_list['SongList_CommentNum'] = commentCount
        song_list['SongList_PlayNum'] = playCount
        song_list['SongList_Label'] = lables
        song_list['SongList_Intro'] = albumIntro
        song_list['SongList_TotalSongNum'] = songCount
        song_list['SongList_SongRank'] = songsID

        for i in range(int(songCount)):
            element_href = self.pre_url + container_songLink.extract()[i]
            redis.lpush("song:url", element_href)

        # redis.lpush("song:url", "http://music.163.com/#/song?id=223960")
        yield song_list
