# -*- coding: utf-8 -*-
import scrapy
from pexels.items import PexelsItem, PexelsPopularItem
import os
import time
import random
import re
'''
    请从项目pexels（外层pexels文件夹下）运行脚本
'''


class PexelsSpiderSpider(scrapy.Spider):
    name = 'pexels_spider'
    allowed_domains = ['www.pexels.com']

    def start_requests(self):
        page_nums = [2 * x for x in range(0, 20)]   # 用来限定爬取页面范围, 如果上限太大超过了页数，自行终止
        content = input("输入要爬的图片：(中文可能失效)\n")
        url = 'https://www.pexels.com/search/'+content+'/?page=%d&seed=%s++0000&format=js&seed=%s+0000'
        for page in page_nums:  # 超出范围怎么办？
            t = time.localtime(time.time() - random.random() * 10
                               * random.random() * 60 * random.random() * 60)
            seed1 = str(time.strftime('%Y-%m-%d+%H:%M:%S', t))
            seed2 = str(time.strftime('%Y-%m-%d %H:%M:%S ', t))
            # print(url % (page, seed)) 看一看
            yield scrapy.Request(url % (page, seed1, seed2), meta={'content': content}, callback=self.parse)

    '''
         1.通过分析XHR请求，得知下滑显示的图片可通过如下链接获取（ajax）
         https://www.pexels.com/search/Food/?page=2&format=js&seed=2018-04-24 03:04:37 +0000
         https://www.pexels.com/search/cat/?page=2&format=js&seed=2018-04-23 17:02:10 +0000
         2.page+=2（从0开始），该网站就是在你下拉页面的时候，发起一个如上xhr请求
         3.经过测试发现，seed=随机的一个时间（格式如上），就用localtime+-一个随机的秒数吧
         4.由于Request下载速度太快，导致以上请求只能获取到js函数，经过分析，可以直接从js代码中用正则表达式提取图片链接
         5.随机user-agent
         6.数据库查重，避免重复下载给网站带来的的压力，但太蠢
    '''
    def parse(self, response):
        item = PexelsItem()
        content = response.meta['content']
        item['title'] = content
        item['img_url'] = []

        # print(response.body.decode('utf-8'))  # 注意返回的是js代码！！！
        # 请用正则匹配！！！或者获取动态加载获得内容
        seed = int(random.random()*100000)
        if not os.path.exists('./img'):
            os.makedirs('./img')
        if not os.path.exists('./img/temp'):
            os.makedirs('./img/temp')

        # <a href=\"巴拉巴拉\" download>
        res_url = re.findall(re.compile(r"<a href=(.*?) download>", re.S), response.body.decode('utf-8'))
        map(lambda x: str(x).strip(), res_url)
        for url in res_url:
            print(url[2:-2])  # 从\"url\"中提取url
            item['img_url'].append(url[2:-2])
        yield item


class PopularSpider(scrapy.Spider):
    # https://www.pexels.com/popular-photos.js?page=%d&seed=%s++0000&format=js&seed=%s+0000
    # https://www.pexels.com/popular-photos/all-time.js?page=%d&seed=%s++0000&format=js&seed=%s+0000
    name = 'Popular'
    allowed_domains = ['www.pexels.com']

    def start_requests(self):
        urls = [
            'https://www.pexels.com/popular-photos.js?page=%d&seed=%s++0000&format=js&seed=%s+0000',
            'https://www.pexels.com/popular-photos/all-time.js?page=%d&seed=%s++0000&format=js&seed=%s+0000'
        ]
        page_nums = [2 * x for x in range(0, 20)]  # 用来限定爬取页面范围, 如果上限太大超过了页数，自行终止
        for url in urls:
            for page in page_nums:  # 超出范围怎么办？
                t = time.localtime(time.time() - random.random() * 10
                                   * random.random() * 60 * random.random() * 60)
                seed1 = str(time.strftime('%Y-%m-%d+%H:%M:%S', t))
                seed2 = str(time.strftime('%Y-%m-%d %H:%M:%S ', t))
                # print(url % (page, seed)) 看一看
                yield scrapy.Request(url % (page, seed1, seed2), callback=self.parse)

    def parse(self, response):
        item = PexelsPopularItem()
        item['title'] = 'Popular'
        item['img_url'] = []

        res_url = re.findall(re.compile(r"<a href=(.*?) download>", re.S), response.body.decode('utf-8'))
        map(lambda x: str(x).strip(), res_url)
        for url in res_url:
            print(url[2:-2])  # 从\"url\"中提取url
            item['img_url'].append(url[2:-2])
        yield item
