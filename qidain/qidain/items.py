# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidainItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()


class FreeArticleListItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()


class FreeArticleItem(scrapy.Item):
    name = scrapy.Field()
    chapter = scrapy.Field()
    content = scrapy.Field()
