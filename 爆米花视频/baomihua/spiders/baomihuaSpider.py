# -*- coding: utf-8 -*-
import scrapy
from re import sub, findall, S
from json import loads
from baomihua.items import VideoItem, ImgItem
import requests


class BaomihuaspiderSpider(scrapy.Spider):
    name = 'baomihuaSpider'
    allowed_domains = []

    def start_requests(self):
        url = 'https://interface.video.baomihua.com/index.ashx?jsoncallback=\
        jQuery110208997327577641546_1542191958763&dataType=pc_channel&pageSize=14\
        &pageIndex=%d&from=baidu&channelId=%d&_=1542191958764'  # 两个参数 pageIndex 和 channelId
        # 注意，这里的dataType参数，对于推荐频道，应该用dataType=pc_index!
        url2 = 'https://interface.video.baomihua.com/index.ashx?jsoncallback=\
                jQuery110208997327577641546_1542191958763&dataType=pc_index&pageSize=14\
                &pageIndex=%d&from=baidu&channelId=%d&_=1542191958764'

        channelMap = {'美食': 1, '舞蹈': 2, '搞笑': 3, '时尚': 14, '奇闻': 20, '游戏': 21, '推荐': 100, '娱乐': 101,
                     '影视': 102, '综艺': 104, '美妆': 106, '历史': 107, '生活': 112, '拍客': 115, '秀场': 116,
                     '音乐': 117, '健康': 119, '穿搭': 120, '新时代': 124, '视频购物': 125, }  # 可通过爬虫获取

        page = [1,  1, 1, 1, 1, 1, 1, 1, 1]  # 爬取的页数，每页14个视频
        type_ = ['美食', '舞蹈', '搞笑', '时尚', '奇闻', '游戏', '推荐', '娱乐', '影视']   # 爬取的视频类型
        # page = [1]
        # type_ = ['推荐']

        channelId = [channelMap[_] for _ in type_]
        target = list(zip(page, channelId, type_))

        for one in target:
            if one[-1] == '推荐':
                yield scrapy.Request(url2 % one[:-1], meta={'channel': one[-1]}, callback=self.parse)
            else:
                yield scrapy.Request(url % one[:-1], meta={'channel': one[-1]}, callback=self.parse)

    def parse(self, response):
        # print('headers:', response.headers)
        text = response.text.strip()
        data = sub('jQuery.*?\(', '', text)[:-1]
        # print(data)
        dataSet = loads(data)
        # print(type(dataSet), dataSet)
        url = 'https://play.baomihua.com/getvideourl.aspx?jsoncallback=\
                jQuery1830103891430636318_1542188469470&flvid=%s&devicetype=pc_noflash&dataType=json&_=1542188471281'
        for one in dataSet['Videolist']:
            title = one.get('videoTitle', None)
            id_ = one.get('videoId', None)
            img = one.get('videoImgUrl', None)

            if title is None:
                print('one video is None!')
                continue

            yield scrapy.Request('http:'+img, meta={'title': title, 'channel': response.meta['channel']}, callback=self.download_img)
            yield scrapy.Request(url % id_, meta={'title': title, 'channel': response.meta['channel']}, callback=self.get_real_video_url)

    def get_real_video_url(self, response):
        # print(response.text)

        video = findall('alipalyurl":"(.*?)"}\)', response.text, S)
        # print('video: ', video)
        if video != []:
            yield scrapy.Request('http://'+video[0], meta={'title': response.meta['title'], 'channel': response.meta['channel']}, callback=self.download_media)
        else:
            print('Error: video is None!')

    def download_media(self, response):
        # print(response.body)    # 注意这里要用body！！！由于header里面没有content-type字段
        item = VideoItem()
        item['videoTitle'] = response.meta['title']
        item['channel'] = response.meta['channel']
        item['video'] = response.body
        yield item

    def download_img(self, response):
        item = ImgItem()
        item['videoTitle'] = response.meta['title']
        item['channel'] = response.meta['channel']
        item['img'] = response.body
        yield item