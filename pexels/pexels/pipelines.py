# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pexels.items import PexelsItem, PexelsPopularItem
import requests
import time
import os
import hashlib
from PIL import Image
import pytesseract

class PexelsPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PexelsItem) or isinstance(item, PexelsPopularItem):
            check_dir_exist("./img/list.txt")
            check_dir_exist('./img/' + item['title'])
            check_dir_exist('./thumbnail/' + item['title'])

            with open("./img/list.txt", 'a', encoding='utf-8') as f:
                f.write("----------------------------------------------start download " + str(item['title'])
                        + '----------------------------------------------' + '\r\n')
            for i, url in enumerate(item["img_url"]):
                # 先查询一下数据库，检查某链接是否被爬过？被爬过就不再爬了
                # 但是上述方法太笨了，我决定还是用MD5给图片内容链接加密，并以加密串为文件命名
                md5 = hashlib.md5()
                md5.update(url.encode('utf-8'))
                url_to_md5str = md5.hexdigest()
                # 若存在相关图片，则不下载
                if os.path.exists('./img/' + item['title'] + '/' + url_to_md5str + '.jpg'):
                    with open("./img/list.txt", 'a', encoding='utf-8') as f:
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                        f.write('<' + str(now) + '> ' + 'skip download ' + url_to_md5str
                                + '.jpg' + ' from ' + url + '\r\n\r\n')

                    # 制作缩略图
                    make_thumbnail('./img/' + item['title'] + '/' + url_to_md5str + '.jpg',
                                   './thumbnail/' + item['title'] + '/' + url_to_md5str + '.jpg')
                    continue

                r = requests.get(url)
                # 新建jpg文件并以MD5摘要命名
                with open('./img/' + item['title'] + '/' + url_to_md5str + '.jpg', 'wb') as f:
                    f.write(r.content)
                # 制作缩略图
                make_thumbnail('./img/' + item['title'] + '/' + url_to_md5str + '.jpg',
                               './thumbnail/' + item['title'] + '/' + url_to_md5str + '.jpg')

                with open("./img/list.txt", 'a', encoding='utf-8') as f:
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    f.write('<'+str(now) + '> ' + 'download ' + url_to_md5str + '.jpg' + ' from ' + url + '\r\n\r\n')

        return item


# 对应文件夹不存在则创建
def check_dir_exist(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


# 制作缩略图
def make_thumbnail(from_path, to_path):
    img = Image.open(from_path)
    scale = img.size[0] / img.size[1]
    newWidth = 150
    newHeight = newWidth * scale
    img.thumbnail((newWidth, newHeight), Image.ANTIALIAS)

    img.save(to_path, "JPEG")


'''
if __name__ == '__main__':
    md5 = hashlib.md5()
    md5.update('1231232'.encode('utf-8'))
    url_to_md5str = md5.hexdigest()
    print(url_to_md5str)
'''