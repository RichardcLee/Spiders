# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from qidain.items import QidainItem, FreeArticleItem, FreeArticleListItem
import os


class QidainPipeline(object):
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, QidainItem):
            try:
                db = pymysql.connect('localhost', 'root', '819555147', 'spider')
                cursor = db.cursor()
                for index, title in enumerate(item['name']):
                    if cursor.execute("select Title from `myspider_qidianbooklist` where Title='"+title+"'") != 0:
                        print("already exits!")
                        pass
                    else:
                        cursor.execute("insert into `myspider_qidianbooklist` values('%s','%s','%s','%s')" % \
                                       (title, item['author'][index], 'http:'+item['link'][index],
                                        item['description'][index]))
                        db.commit()
            except Exception as e:
                print("Error happened: " + str(e))
                db.rollback()
            db.close()
        if isinstance(item, FreeArticleListItem):
            pass

        if isinstance(item, FreeArticleItem):
            filename = item["name"][0] + ".html"
            '''with open(filename, "w", encoding='utf8'):
                pass  # do nothing, just for create a new html file if it does not exits
            '''
            if not os.path.exists(filename):
                with open(filename, "w", encoding='utf8') as f:
                    output = '''
                        <!doctype html>
                        <html>
                        <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>起点</title>
                        </head>
                            <body>'''
                    f.write(output)

            file = open(filename, 'a', encoding='utf8')
            output = '<h2>' + str(item['chapter']) + '</h2>'
            for x in item['content']:
                output += '<p>' + x + '</p>'

            output += '''</body>
                                </html>'''
            file.write(output)
            file.close()
        return item  # 在cmd显示item

