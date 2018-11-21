# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    order = scrapy.Field()  # 排名
    title = scrapy.Field()  # 电影名
    link = scrapy.Field()   # 电影链接
    img_src = scrapy.Field()  # 图片链接
    score = scrapy.Field()  # 评分
    judge_nums = scrapy.Field()  # 评论人数


class AMSItem(scrapy.Item):
    title = scrapy.Field()  # 大标题, str
    name = scrapy.Field()   # 电影名，导演名，或任何名字, list
    img_src = scrapy.Field()  # name对应的图片链接, list
    score = scrapy.Field()  # name对应的评分, list
