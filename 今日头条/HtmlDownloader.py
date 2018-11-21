import requests
'''
网页下载
'''


class HtmlDownloader(object):
    def __init__(self):
        self.cookie = 'UM_distinctid=1636c1b97ad0-001bb3a22885d5-11636b4a-e1000-1636c1b97af24; CNZZDATA1259612802=610327710-1526522629-%7C1537928545; tt_webid=6605356097333822984; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6605356097333822984; __tasessionId=tkmyt75e11537929314030; csrftoken=64785b2509ae9c679d4c81c9bdc06910; uuid="w:180ddd10a85b4e7693ebb63b31bc50e6"'
        self.headers = {
            'Host': 'www.toutiao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.cookie,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers'
        }

    def download(self, url):
        '''
        :param url: target url
        :return: html or json or xml
        '''
        res = requests.get(url, headers=self.headers)

        try:
            if res.status_code == 200:
                print('[!]down %s successfully!' % url)
                return res
            else:
                print('[?]down %s failed! Reason: %s %s' % (url, res.status_code, res.reason))
        except Exception as e:
            print('[?]', e)