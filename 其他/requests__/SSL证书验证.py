import requests

headers = {
    'Host': 'www.12306.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.12306.cn/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    # 'If-Modified-Since': 'Wed, 29 Aug 2018 06:35:14 GMT',
    'Cache-Control': 'max-age=0'
}


r = requests.get('https://www.12306.cn/mormhweb/', headers=headers, verify=False)
print(r.status_code)
print(r.content.decode('utf-8'))