# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, Compose


class HuXiuItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


class ArticleItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(str.strip))
    author = scrapy.Field(input_processor=MapCompose(str.strip))
    content = scrapy.Field(input_processor=MapCompose(str.lstrip), output_processor=Join("<br/>"))
    post_time = scrapy.Field(input_processor=MapCompose(str.strip))
