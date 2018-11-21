# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import HuXiuItem, ArticleItem
from scrapy.exceptions import DropItem
import time


class CoolscrapyPipeline(object):
    def __init__(self):
        self.old = set()

    # 批量加入
    def _add_to_set(self, item, *args):
        for arg in args:
            self.old.add(str(item[arg]))

    def open_spider(self, spider):
        ISO_TIME_FORMAT = '%Y-%m-%d %H-%M-%S'
        filename = '虎嗅' + time.strftime(ISO_TIME_FORMAT, time.localtime(time.time())) + '.html'
        self.file = open(filename, 'w', encoding='utf-8')
        output = '''
                <!doctype html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>虎嗅</title>
                </head>
                    <body>'''
        self.file.write(output)

    def close_spider(self, spider):
        output = '''</body>
                    </html>'''
        self.file.write(output)
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, HuXiuItem):
            if item['link'] in self.old and item['title'] in self.old and item['desc'] in self.old:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                output = '<div>'
                output += '<h2><a href="' + item['link']+'">' + item['title'] + '</a></h2>'
                output += '<p>' + item['desc'] + '</p>'
                output += '</div>'
                self.file.write(output)
                self._add_to_set(item, 'link', 'title', 'desc')

        if isinstance(item, ArticleItem):
            if item['title'] in self.old and item['author'] in self.old \
                    and item['content'] in self.old and item['post_time'] in self.old:
                raise DropItem("Duplicate item found %s" % item)
            else:
                output = '<div>'
                output += '<h2>' + item['title'] + '</h2>'
                output += '<p><span>' + item['author'] + ' </span>' + '<span>' + item['post_time'] + '</span></p>'
                output += '<p>'
                for i in item['content']:
                    output += i
                output += '</p>'
                output += '</div>'
                self.file.write(output)
                self._add_to_set(item, 'title', 'author', 'content', 'post_time')
        return item
