# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem, AMSItem
from functools import reduce


class DoubSpider(scrapy.Spider):
    name = 'doub'
    allowed_domains = ['www.douban.com']
    # 形如 https://movie.douban.com/top250?start=1&filte= 注意，每一次只显示25个电影。。。所以。。
    url_before = 'https://movie.douban.com/top250?start='
    url_after = '&filte='

    def start_requests(self):
        # 获取start参数，start=range[i],
        ranges = [x*25 for x in range(0, 9+1)]
        for i in ranges:
            url = self.url_before + str(i) + self.url_after
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # 页面中的ol.grid_view 包含电影列表
        item = DoubanItem()
        ol = response.css("ol.grid_view li")
        item['order'] = []
        item['title'] = []
        item['link'] = []
        item['img_src'] = []
        item['score'] = []
        item['judge_nums'] = []

        for li in ol:
            item['order'].append(li.css("div.pic em::text").extract_first())
            item['title'].append(reduce(lambda x, y: x.strip()+y.strip(),
                                        li.css("div.info div.hd a span::text").extract()))
            item['link'].append(li.css("div.pic a::attr(href)").extract_first())
            item['img_src'].append(li.css("div.pic a img::attr(src)").extract_first())
            item['score'].append(li.css("div.info div.bd div.star span.rating_num::text").extract_first())
            item['judge_nums'].append(li.css("div.info div.bd div.star span::text").re("(.*?)人评价")[0])
        yield item


# 爬取豆瓣年度电影
class AnnualMovieSpider(scrapy.Spider):
    name = 'AMS'
    url = 'https://movie.douban.com/annual/2017?source=navigation'

    def start_requests(self):
        # 无法获取页数，只能靠异常来终止
        for i in range(1, 1000):
            try:
                yield scrapy.Request(self.url+'#'+str(i), callback=self.parse)
            except Exception as e:
                print(str(e))
                return


    '''
        页面是动态加载，无法爬取！！！
    '''
    def parse(self, response):
        item = AMSItem()
        item['title'] = response.css("div._2pL9Z h1 div::text").extract_first()
        if item['title'] is None:
            return
        item['name'] = []
        item['img_src'] = []
        item['score'] = []
        response.css("div._1sV3Y div._31ZvR a::attr(href)")

