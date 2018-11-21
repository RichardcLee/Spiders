# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sf.items import SfItem
import pymysql
import os


class SfPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SfItem):
            # 存入数据库，或者格式化信息
            # 或者html形式
            # 或者 csv形式
            # 存入数据库
            # 打开链接
            conn = pymysql.connect(host='localhost', port=3306, user='root',
                                   passwd='819555147', db='spider_site_segmentfaultfull', charset='utf8')
            cursor = conn.cursor()
            for js in item['data']:  # 每一个json对象
                for row in js['data']['rows']:  # 每一行（即一篇文章）
                    tags = ''
                    if row['tags'] is not None:
                        for tag in row['tags']:
                            tags += tag['name'] + " "
                        tags = tags.lstrip()
                    try:
                        cursor.execute('insert into `sf` values("%s","%s","%s","%s","%s","%s");' %
                                       (row['title'],
                                        'https://segmentfault.com' + row['url'],
                                        row['createdDate'],
                                        tags,
                                        row['user']['name'],
                                        'https://segmentfault.com' + row['user']['url'])
                                       )
                    except Exception as e:
                        if not os.path.exists('./log.txt'):
                            with open('./log.txt', 'w') as f:
                                pass    # do nothing
                        with open('./log.txt', 'a', encoding='utf-8') as f:
                            f.write('Error happened when insert into db table' + str(e) + '\r\n\r\n')

            # 不要忘了提交和关闭
            conn.commit()
            conn.close()

        # return item
