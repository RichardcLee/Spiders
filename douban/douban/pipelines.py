# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from douban.items import  DoubanItem
import os
import requests
from douban.settings import DEFAULT_REQUEST_HEADERS


class DoubanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, DoubanItem):
            dir = '.\\craw'
            log_file = dir + '\\top250.txt'
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(log_file, 'a', encoding='utf-8') as f:
                for i in range(0, len(item['order'])+1):
                    content = '排名：' + item['order'][i] + '  标题：' + item['title'][i] + '  电影链接：' + \
                              item['link'][i] + '  图片链接：' + item['img_src'][i] + '  评分：' + item['score'][i] \
                              + '  评价人数：' + item['judge_nums'][i] + '\r\n'
                    f.write(content)
                    res = requests.get(item['img_src'][i])
                    with open(dir+'\\'+item['order'][i]+'.jpg', 'wb') as jpg:
                        jpg.write(res.content)
        return item
