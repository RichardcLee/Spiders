# -*- coding: utf-8 -*-
from baomihua.items import VideoItem, ImgItem
import os

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaomihuaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, VideoItem):
            title = item['videoTitle']
            video = item['video']
            channel = item['channel']

            path = './media/%s' % channel
            if not os.path.exists(path):
                os.makedirs(path)

            with open(path+'/%s.mp4' % title, 'wb+') as f:
                f.write(video)

        elif isinstance(item, ImgItem):
            title = item['videoTitle']
            img = item['img']
            channel = item['channel']

            path = './media/%s' % channel
            if not os.path.exists(path):
                os.makedirs(path)

            with open(path+'/%s.jpg' % title, 'wb+') as f:
                f.write(img)

        return item
