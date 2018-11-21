# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from qidain.items import QidainItem, FreeArticleItem, FreeArticleListItem
from qidain.sql import Sql

'''
https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1
https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=2
https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=3
'''


class QidianSpider(scrapy.Spider):
    name = 'qidian-spider'
    allowed_domains = ['www.qidian.com']
    start_urls = ['https://www.qidian.com/all']

    def parse(self, response):
        base_url = 'https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page='
        for i in range(1, 6000):
            follow_url = base_url + str(i)

            yield scrapy.Request(follow_url, self.get_things_i_want)

    def get_things_i_want(self, response):
        loader = ItemLoader(item=QidainItem(), response=response)
        loader.add_css("name", "h4 a::text")
        loader.add_css("link", "h4 a::attr(href)")
        loader.add_css("author", "p.author a.name::text")
        loader.add_css("description", "p.intro::text")
        return loader.load_item()


class Qidian_GetFree_Spider(scrapy.Spider):
    name = 'get-free-spider'
    start_urls = ['https://www.qidian.com/free']

    def parse(self, response):
        loader = ItemLoader(item=FreeArticleListItem(), response=response)
        loader.add_css("name", ".book-mid-info h4 a::text")
        loader.add_css("link", ".book-mid-info h4 a::attr(href)")
        loader.add_css("author", ".book-mid-info p.author a[class='name']::text")
        item = loader.load_item()
        yield item
        name = item["name"]
        follow_urls = response.css("p.btn a.red-btn::attr(href)").extract()
        for index, url in enumerate(follow_urls):
            yield scrapy.Request("http:"+url, meta={'name': name[index]}, callback=self.getin)

    def getin(self, response):
        url = response.css("a#readBtn::attr(href)").extract_first()
        name = response.meta["name"]
        yield scrapy.Request("http:"+url, meta={'name': name}, callback=self.get_things)

    def get_things(self, response):
        loader = ItemLoader(item=FreeArticleItem(), response=response)
        loader.add_value("name", response.meta["name"])
        loader.add_css("chapter", "h3.j_chapterName::text")
        loader.add_css("content", "div.read-content.j_readContent p::text")
        yield loader.load_item()
        next_page_url = response.css("a#j_chapterNext::attr(href)").extract_first()
        yield scrapy.Request("http:"+next_page_url, meta={"name": response.meta["name"]}, callback=self.get_things)
