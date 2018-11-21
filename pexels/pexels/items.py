# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PexelsItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()


class PexelsPopularItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()
