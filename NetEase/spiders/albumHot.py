# -*- coding: utf8 -*-
import scrapy
from scrapy.http import Request
from NetEase.items import SongListItem
from NetEase.items import SongItem
import hashlib

class SongListSpider(scrapy.Spider):
    name = 'songList'
    allowed_domain = ['music.163']
    pre_url = "http://music.163.com/#"  # pre-link of album page
    # hot songlist
    base_url = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=1&offset="
    songlist_num = 1   # amount of albums

    def start_requests(self):
        song_list = SongListItem()
        for i in range(0, self.songlist_num):
            song_list['SongList_ID'] = i + 1     # set the ID of songlist
            url = self.base_url + str(i)
            request = Request(url=url, meta={'songList': song_list, 'PhantomJS': True}, callback=self.parse, dont_filter=True)
            yield request

    # Hot list page
    def parse(self, response):
        song_list = response.meta['songList']

        xpath_ul = "//ul[@id='m-pl-container']"
        xpath_title = "//*[@class='msk']/@title"
        xpath_href = "//*[@class='msk']/@href"
        xpath_img = "//img/@src"

        container_ul = response.xpath(xpath_ul)[0]
        element_title = container_ul.xpath(xpath_title)[0].extract()
        element_href = self.pre_url + container_ul.xpath(xpath_href)[0].extract()
        element_img = container_ul.xpath(xpath_img)[0].extract()

        # Set values for SongListItem
        song_list['SongList_Name'] = element_title
        song_list['SongList_Link'] = element_href
        song_list['SongList_IMG'] = element_img

        # show off
        print("Title: "+ element_title)
        print("Link URL: "+ element_href)
        print("Image: "+ element_img)

        # Crawl from song page
        request = Request(url=element_href, meta={'songList': song_list, 'PhantomJS': True}, callback=self.parse_album, dont_filter=True)
        return request

    # Song list page
    def parse_album(self, response):
        song = SongItem()
        song_list = response.meta['songList']

        # information from uploader class=user f-cb part
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
        xpath_songName = xpath_table + "/td[2]//b/@title"
        xpath_songLink = xpath_table + "/td[2]//span/a/@href"
        xpath_songDuration = xpath_table + "/td[3]/span/text()"
        xpath_songSinger = xpath_table + "/td[4]//span/@title"
        xpath_songAlbum = xpath_table + "/td[5]//a/@title"
        xpath_songAlbumLink = xpath_table + "/td[5]//a/@href"

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

        container_songName = response.xpath(xpath_songName)
        container_songLink = response.xpath(xpath_songLink)
        container_songDuration = response.xpath(xpath_songDuration)
        container_songSinger = response.xpath(xpath_songSinger)
        container_songAlbum = response.xpath(xpath_songAlbum)
        container_songAlbumLink = response.xpath(xpath_songAlbumLink)
        songsID = []
        for i in range(int(songCount)):
            songsID.append(hashlib.md5(container_songLink.extract()[i]))   # not include pre_url

        print("uploader name:" + uploaderName)
        print("uploader link:" + uploaderLink)
        print("upload time:" + uploadTime)
        print(lables)
        print("play count:" + playCount)
        print("song count:" + songCount)
        print("fav count:" + favCount)
        print("share count:" + shareCount)
        print("comment count:" + commentCount)
        for sentence in albumIntro:
            print(sentence.strip())

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
        testurl = "http://music.163.com/#/song?id=487379098"
        request = Request(url=testurl, meta={'song': song, 'PhantomJS': True}, callback=self.parse_song,
                          dont_filter=True)
        # songList = []
        # for i in range(int(songCount)):
        #     # tempDict = {'Name':container_songName.extract()[i],
        #     #             'songLink':container_songLink.extract()[i],
        #     #             'duration':container_songDuration.extract()[i],
        #     #             'singer':container_songSinger.extract()[i],
        #     #             'album':container_songAlbum.extract()[i],
        #     #             'albumLink':container_songAlbumLink.extract()[i]
        #     #             }
        #     # songList.append(tempDict)
        #     song['SongID'] = songsID[i]
        #     song['Song_Name'] = container_songName.extract()[i]
        #     song['Song_Link'] = self.pre_url + container_songLink.extract()[i]
        #     song['Song_Duration'] = container_songDuration.extract()[i]
        #     song['Song_Singer'] = container_songSinger.extract()[i]
        #     song['Song_Ablum'] = container_songAlbum.extract()[i]
        #     request = Request(url=song['Song_Link'], meta={'song': song, 'PhantomJS': True}, callback=self.parse_song, dont_filter=True)
        #
        #     yield request
        yield song_list
        yield request
        # testurl = "http://music.163.com/#/song?id=487379098"

    # Song page
    def parse_song(self, response):
        song = response.meta['song']

        xpath_comment_count = "//span[@id='cnt_comment_count']/text()"
        xpath_lyrics = "//div[@id='lyric-content']/text()"
        xpath_lyricsMore = "//div[@id='flag_more']/text()"  # show all
        xpath_albumIMG = "//div[@class='u-cover u-cover-6 f-fl']/img/@src"
        xpath_topCommentsDiv = "//div[count(preceding-sibling::h3[@class='u-hd4'])=1]"
        xpath_topComments = xpath_topCommentsDiv + "//div[@class='cnt f-brk']"
        xpath_topComments_author = xpath_topCommentsDiv + "//div[@class='cnt f-brk']/a/text()"
        xpath_topCommentsTime = xpath_topCommentsDiv + "//div[@class='time s-fc4']/text()"
        xpath_topCommentsCount = "//a[@data-type='like']/text()"

        song_commentCount = response.xpath(xpath_comment_count).extract()[0]
        song_albumIMG = response.xpath(xpath_albumIMG).extract()[0]
        lyrics = ''     # perhaps no lyrics here
        if response.xpath(xpath_lyrics):
            song_lyrics = response.xpath(xpath_lyrics).extract()
            if response.xpath(xpath_lyricsMore).extract():
                song_lyricsMore = response.xpath(xpath_lyricsMore).extract()
                lyrics = song_lyrics + song_lyricsMore
            else:
                lyrics = song_lyrics
        top_comments_temp = {}
        top_comments_list = []

        if response.xpath(xpath_topCommentsDiv):
            for i in range(len(response.xpath(xpath_topComments_author).extract())):
                top_comments_temp['Song_CommentContent'] = response.xpath(xpath_topComments)[i].xpath('string(.)').extract()[0]
                top_comments_temp['Song_CommentAuthor'] = response.xpath(xpath_topComments_author).extract()[i]
                top_comments_temp['Song_CommentTime'] = response.xpath(xpath_topCommentsTime).extract()[i]
                top_comments_temp['Song_CommentThumbsUp'] = response.xpath(xpath_topCommentsCount).extract()[i]
                top_comments_list.append(top_comments_temp)
        song['Song_TopComments'] = top_comments_list
        song['Song_lyrics'] = lyrics
        song['Song_CommentNum'] = song_commentCount
        song['Song_Ablum_IMG'] = song_albumIMG
        return song

        # print("song comment count:" + song_commentCount)
        # for sentence in lyrics:
        #     print(sentence)
