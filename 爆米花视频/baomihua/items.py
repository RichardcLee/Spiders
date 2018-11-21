# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    videoTitle = scrapy.Field()
    channel = scrapy.Field()
    video = scrapy.Field()


class ImgItem(scrapy.Item):
    videoTitle = scrapy.Field()
    channel = scrapy.Field()
    img = scrapy.Field()