# -*- coding: utf-8 -*-
import scrapy
from sf.items import SfItem
import json
import requests
import os
import hashlib


# 模块名
models = {
    'bc': '区块链', 'ai': '人工智能', 'frontend': '前端',
    'backend': '后端', 'android': '安卓', 'ios': 'ios',
    'toolkit': '工具', 'netsec': '网络安全',
    'programmer': '程序员', 'industry': '行业'
}
# xhr请求模板，需要一个参数 %d，为了方便理解我把每个url单独列出
# 本来其实想一个模板通吃全部url, 就像这样https://segmentfault.com/api/channel/%s/hottest?start=%d&_=%s
url_templates = {
    'bc': 'https://segmentfault.com/api/channel/bc/hottest?start=%d&_=9901cfe62ec4973b10a16b0b198adcf0',
    'ai': 'https://segmentfault.com/api/channel/ai/hottest?start=%d&_=e67606c44b90c32898d889eb3b7e0289',
    'frontend': 'https://segmentfault.com/api/channel/frontend/hottest?start=%d&_=9f2339af77409b57d0e5d68238920fba',
    'backend': 'https://segmentfault.com/api/channel/backend/hottest?start=%d&_=df3fc2457ed1fd8f272fa1c1d3baf995',
    'android': 'https://segmentfault.com/api/channel/android/hottest?start=%d&_=b62b69d0bafc28366e0e7b4770723e7d',
    'ios': 'https://segmentfault.com/api/channel/ios/hottest?start=%d&_=bb24b13b4b6015f2a2979aa51cee8db5',
    'toolkit': 'https://segmentfault.com/api/channel/toolkit/hottest?start=%d&_=38538b56dd767b8e0f9bab09ca9cea85',
    'netsec': 'https://segmentfault.com/api/channel/netsec/hottest?start=%d&_=770296e5829c6e4fd321e80ba52daa93',
    'programmer': 'https://segmentfault.com/api/channel/programmer/hottest?start=%d&_=eb325fdf60c766ecaf189933a5d53151',
    'industry': 'https://segmentfault.com/api/channel/industry/hottest?start=%d&_=81da62882ddfabe93bf9e452d5f92709',
}
headers_pool = {
    'bc': {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
             _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/bc;\
              Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524884853; _gid=GA1.2.1650375487.1524876746; afpCT=1',  # 不同
            'Host': 'segmentfault.com',
            'Referer': 'https://segmentfault.com/bc', # 不同
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'X-Requested-With': 'XMLHttpRequest'
    },
    'ai': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/ai;\
          Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885040; _gid=GA1.2.1650375487.1524876746; afpCT=1; _gat=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/ai',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'frontend': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/frontend;\
          Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885265; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/frontend',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'backend': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/backend;\
          Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885366; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/backend',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'android': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
        _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/android;\
        Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885453; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/android',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'ios': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
        _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/ios;\
        Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885580; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/ios',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    },
    'toolkit': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/toolkit;\
          Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885840; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/toolkit',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'


    },
    'netsec': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
        _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/netsec;\
        Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524883660; _gid=GA1.2.1650375487.1524876746; afpCT=1; _gat=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/netsec',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'

    },
    'programmer': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/programmer;\
          Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524885999; _gid=GA1.2.1650375487.1524876746; afpCT=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/programmer',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'

    },
    'industry': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_e23800c454aa573c0ccb16b52665ac26=1524624545,1524717828,1524719833,1524876745;\
         _ga=GA1.2.636274206.1521637680; PHPSESSID=web1~5df5qhe1jjfhmvrrppeedglr34; last-url=/industry;\
         Hm_lpvt_e23800c454aa573c0ccb16b52665ac26=1524886073; _gid=GA1.2.1650375487.1524876746; afpCT=1; _gat=1',
        'Host': 'segmentfault.com',
        'Referer': 'https://segmentfault.com/industry',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
}
'''
D:\我的文件\各种语言的工作文件\scrapy\sf\sf 下开始
'''


class SfSpider(scrapy.Spider):
    name = 'SF'
    allowed_domains = ['https://segmentfault.com/']

    def start_requests(self):
        urls = [
            'https://segmentfault.com/bc',
            'https://segmentfault.com/ai',
            'https://segmentfault.com/frontend',
            'https://segmentfault.com/backend',
            'https://segmentfault.com/android',
            'https://segmentfault.com/ios',
            'https://segmentfault.com/toolkit',
            'https://segmentfault.com/netsec',
            'https://segmentfault.com/programmer',
            'https://segmentfault.com/industry',
        ]
        for url in urls:
            yield scrapy.Request(url, meta={'model_name': url[25:]}, callback=self.parse)

    def parse(self, response):
        item = SfItem()
        # 模块名
        model_name = response.meta['model_name']
        item['model'] = models.get(model_name, 'Error')
        item['data'] = []
        # 解析下一页面，模拟一个xhr
        # 只需改变next_start参数即可模拟下一页，下一页的start可以通过该xhr请求的响应Json中的 nextStart: xx 获取
        next_start = 1
        while next_start != 0:
            req = requests.get(url_templates[model_name] % next_start, headers=headers_pool[model_name])
            req.encoding = 'utf-8'
            # 下载json文件
            md5 = hashlib.md5()
            md5.update(req.content)
            digest = md5.hexdigest()
            filename = model_name + digest + '.json'
            if not os.path.exists('./temp'):
                os.makedirs('./temp')
            # 注意读写方式，write后直接read，由于数据在内存中，所以读不到，需要先close
            with open('./temp/'+filename, 'w', encoding='utf-8') as f:
                f.write(req.text)
            # load json
            with open('./temp/'+filename, 'r', encoding='utf-8') as f:
                page_data = json.load(f)
            item['data'].append(page_data)
            # 获取下一页的start数字
            next_start = page_data['data']['nextStart']
            # 在此不逐一解析文章，而是交由SfPipeline处理
            '''
                item结构如下：
                item = {
                       'model_name': xxx,
                       'data': [json{ }, json{ }, ...]
                }
                json{ }的结构请参考 栗子.json（浏览器打开，自动美化）
            '''
            yield item
