# -*- coding: utf8 -*-
from scrapy.http import Request
from NetEase.items import SongListItem
from scrapy_redis.spiders import RedisSpider
from redis import Redis


class SongListSpider(RedisSpider):
    name = 'songList'
    # redis_key = "netease_master:songlist_urls"
    allowed_domain = ['music.163']
    pre_url = "http://music.163.com/#"  # pre-link of album page
    # hot songlist
    base_url = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=1&offset="
    songlist_num = 1   # amount of albums

    def start_requests(self):
        song_list = SongListItem()
        for i in range(0, self.songlist_num):
            url = self.base_url + str(i)
            request = Request(url=url, callback=self.parse, dont_filter=True)
            yield request

    # Hot list page
    def parse(self, response):
        redis = Redis()
        song_list = SongListItem()


        xpath_ul = "//ul[@id='m-pl-container']"
        xpath_title = "//*[@class='msk']/@title"
        xpath_href = "//*[@class='msk']/@href"

        container_ul = response.xpath(xpath_ul)[0]
        element_title = container_ul.xpath(xpath_title)[0].extract()
        element_href = self.pre_url + container_ul.xpath(xpath_href)[0].extract()

        # Set values for SongListItem
        song_list['SongList_Name'] = element_title
        song_list['SongList_Link'] = element_href

        # show off
        print("Title: "+ element_title)
        print("Link URL: "+ element_href)

        redis.lpush("songlist:url", element_href)

