import requests
import re
import pyquery
import json
import csv
'''
huya没有小熊了的微博内容和评论
'''

class WeiBoSpider(object):
    def __init__(self, page_range=(1, 2)):
        '''
        :param page_range: 爬取的页面范围[1,2)
        '''
        # cookies，需要登陆后手动获取
        self.cookies = ''
        # 翻页url 参数 page=%d
        self.page_url = 'https://weibo.com/u/6092178615?pids=Pl_Official_MyProfileFeed__20&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=%d&ajaxpagelet=1&ajaxpagelet_v6=1&__ref=/u/6092178615?refer_flag=1001030101_&is_all=1&_t=FM_153708174520225'
        # 每一页面的请求头
        self.headers_homepage = {
            'Host': 'weibo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'http://s.weibo.com/weibo/%25E6%25B2%25A1%25E6%259C%2589%25E5%25B0%258F%25E7%2586%258A?topnav=1&wvr=6&b=1',
            'Cookie': self.cookies,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        # 下拉加载更多url,参数有三：page=pre_page=%d(页码1,2...) pagebar=%d(0,1)
        self.morebloglist_url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=%d&pagebar=%d&pl_name=Pl_Official_MyProfileFeed__20&id=1005056092178615&script_uri=/u/6092178615&feed_type=0&pre_page=%d&domain_op=100505&__rnd=1537349664162'
        # 加载更多请求头
        # 注意这个referer会变，从第二页开始变化
        # 'Referer': 'https://weibo.com/u/6092178615?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2',
        self.headers_mbloglist = {
            'Host': 'weibo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Referer': '这个头有点东西！！！！',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': self.cookies,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.headers_comment = {
            'Host': 'weibo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': 1,
            'Cookie': self.cookies,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        # 翻页范围
        self.page_range = range(*page_range)
        # 暂存结果
        self.temp_result = {}
        self.weibo = {}     # 微博内容html
        self.weibo_text = {}    # 微博内容文字
        self.comment_urls = {}  # 每条微博下查看评论的url
        self.comments = {}
        self.users = {}

    # 获取下拉显示的更多内容
    def _get_more_blog(self, page_num):
        # 每个页面只“拉”两次
        pagebar = [0, 1]
        res1 = requests.get(self.morebloglist_url % (page_num, pagebar[0], page_num), headers=self.headers_mbloglist)
        res2 = requests.get(self.morebloglist_url % (page_num, pagebar[1], page_num), headers=self.headers_mbloglist)

        if res1.status_code == 200:
            print('get page %d (part two) successfully!' % page_num)
            self.temp_result[page_num].append(eval(res1.text)['data'])
        else:
            print('get page %d (part two) failed! reason:', res1.status_code, res1.reason)

        if res2.status_code == 200:
            print('get page %d (part three) successfully!' % page_num)
            self.temp_result[page_num].append(eval(res2.text)['data'])
        else:
            print('get page %d (part three) failed! reason:', res2.status_code, res2.reason)

        # 处理一下，将\\去掉
        self.temp_result[page_num] = list(map(lambda x: re.sub('\\\\/', '/', x), self.temp_result[page_num]))
        self.temp_result[page_num] = list(map(lambda x: re.sub(r'\\"', '"', x), self.temp_result[page_num]))
        self.temp_result[page_num] = list(map(lambda x: re.sub(r"\\'", '"', x), self.temp_result[page_num]))

        # print(self.temp_result[page_num])

    # 从个人主页逐页
    def _parse_page_one_by_one(self):
        for _ in self.page_range:
            # 先获取初始显示的一部分
            self.temp_result[_] = []
            res = requests.get(self.page_url % _, headers=self.headers_homepage)
            # print(res.text)
            if res.status_code == 200:
                print('get page %d (part one) successfully!' % _)
                temp = re.sub('<script>parent.FM.view\(', '', res.content.decode('utf-8'))
                # print(temp)
                self.temp_result[_].append(eval(re.sub('\)</script>', '', temp))['html'])

            else:
                print('get page %d (part one) failed! reason:', res.status_code, res.reason)

            # 接下来获取下拉显示的部分（下拉两次）
            self._get_more_blog(_)

        # for i, j in self.temp_result.items():
        #     print(i, j)

    # 保存从api下载的json文件，以便观察数据结构，这个对爬虫实际爬取过程没有影响
    def _have_a_look(self):
        for i, list_res in self.temp_result.items():
            for j, data in enumerate(list_res):
                try:
                    with open('%d-%d.json' % (i, j), 'w+', encoding='utf-8') as f:
                        json.dump(data, f)

                except Exception as e:
                    print('Error happened when save file %d-%d. more info:' % (i, j), str(e))

    # 保存爬到的微博内容
    def _save_weibo(self):
        with open('huya没有小熊_text.json', 'w+', encoding='utf-8') as f:
            json.dump(self.weibo_text, f)

        with open('huya没有小熊.json', 'w+', encoding='utf-8') as f:
            json.dump(self.weibo, f)

    # 保存爬到的微博评论
    def _save_comment(self):
            with open('huya没有小熊_评论用户.json', 'w+', encoding='utf-8') as f:
                json.dump(self.users, f)

            with open('huya没有小熊_评论.json', 'w+', encoding='utf-8') as f:
                json.dump(self.comments, f)

    # 提取微博内容
    def _extact_WeiBo(self, watch=False):
        for i, _ in self.temp_result.items():
            self.weibo[i] = {}
            self.weibo_text[i] = {}

            for j, __ in enumerate(_):
                doc = pyquery.PyQuery(__)

                if watch:
                    print(i, j, ':')
                    print(doc('div.WB_detail div.WB_text.W_f14'))
                    print('html: ', [_.html() for _ in doc('div.WB_detail div.WB_text.W_f14').items()], '\n')
                    print('text: ', [_.text() for _ in doc('div.WB_detail div.WB_text.W_f14').items()], '\n')

                # 提取评论id和api以及对应微博的发布时间
                dates = [_.attr('title') for _ in doc('div.WB_from.S_txt2 a.S_txt2[name]').items()]
                urls = ['https://weibo.com'+_.attr('href') for _ in doc('div.WB_from.S_txt2 a.S_txt2[name]').items()]
                comment_id = [_.attr('name') for _ in doc('div.WB_from.S_txt2 a.S_txt2[name]').items()]

                for _ in range(len(dates)):
                    self.comment_urls[dates[_]] = (urls[_], comment_id[_])

                # 提取微博内容
                self.weibo_text[i][j] = [_.text() for _ in doc('div.WB_detail div.WB_text.W_f14').items()]
                self.weibo[i][j] = [_.html() for _ in doc('div.WB_detail div.WB_text.W_f14').items()]

        print('WeiBo content:', self.weibo_text)
        # print(self.weibo)
        # print(self.comment_urls)

    # 获取更多评论
    def _get_more_comment(self, url, datetime):
        res = requests.get(url, headers=self.headers_homepage)
        html = eval(res.content.decode('utf-8'))["data"]["html"]

        # 提取评论的用户名
        users = re.findall('<a target.*?usercard=.*?>(.*?)<', html, re.S)
        users = list(filter(lambda x: True if x != '' and not x.startswith('@') else False, users))
        self.users[datetime] += users

        # 提取评论
        # 首先正则提取包含评论的数据块
        blocks = re.findall('a>：(.*?)div>', html, re.S)
        comments = []
        for block in blocks:
            # 剔除一些不必要的内容
            comment = re.sub('<a.*?评论配图.*?a>', ' ', block[:-3])  # 配图
            comment = re.sub('<a .*?a_topic.*?>', ' ', comment)  # tag
            comment = re.sub('<img .*?W_img_face.*?>', ' ', comment)  # 表情
            comment = re.sub('<a .*?type=atname.*?>', ' ', comment)  # @某某
            comment = re.sub('<a .*?W_ficon ficon_supertopic">', ' ', comment)  # 超话标签
            comment = re.sub('<\\\\/a>', '', comment)  # 去除闭合标签<\/a>
            comment = re.sub('<\\\\/i>', '', comment)  # 去除闭合标签<\/i>
            comment = comment.strip()
            comments.append(comment)
        self.comments[datetime] += comments
        print('users:', users)
        print('comments:', comments)

        # 爬不到内容，说明到底了
        if users == []:
            print('Get nothing about data. Completely!'+url)
            return

        # 继续获取更多评论
        # 首先获取下一个api url的参数，这里有坑
        param = re.findall('comment_loading.*?action-data="(.*?)">', html, re.S)
        print('param:', param)

        # 若获取不到参数，换一种正则表达式尝试
        if param == []:
            param = re.findall('suda-uatrack=.*?action-data="(.*?)"', html, re.S)
            print('param:', param)
            # 这可能获取多个参数，但只有一个正确的参数
            param = list(filter(lambda x: True if x.startswith('id=') else False, param))
            if param == []:
                print('Get nothing about param. Completely! '+url)
                return''

        param = param[0]
        url2 = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&' + param + '&from=singleWeiBo&__rnd=1537350751234'
        self._get_more_comment(url2, datetime)

    # （按时间降序）提取评论
    def _extract_comment(self):
        for datetime, url in self.comment_urls.items():
            print('get comments from: ' + url[0] + '(publish at %s)'%datetime)

            # 首先要在这个页面获取必要参数param1
            res = requests.get(url[0], headers=self.headers_homepage)
            param1 = re.findall('<a.*?"S_txt1 curr.*? action-data=(.*?)>按时间', res.content.decode('utf-8'), re.S)
            if param1 == []:
                print('crawl '+url[0]+' failed! Reason: can\'t get param1!')
                continue
            param1 = param1[0][2: -2]

            # 第一部分评论（按时间降序）
            # 来自网页：https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4245450787136276&filter=all&from=singleWeiBo
            url1 = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&' + param1
            res = requests.get(url1, headers=self.headers_homepage)
            html = eval(res.content.decode('utf-8'))["data"]["html"]

            # 提取评论的用户名
            users = re.findall('<a target.*?usercard=.*?>(.*?)<', html, re.S)
            users = list(filter(lambda x: True if x != '' and not x.startswith('@') else False, users))
            self.users[datetime] = users

            # 提取评论
            # 首先正则提取包含评论的数据块
            comments = []
            blocks = re.findall('a>：(.*?)div>', html, re.S)
            for block in blocks:
                # 剔除一些不必要的内容
                comment = re.sub('<a.*?评论配图.*?a>', ' ', block[:-3])     # 配图
                comment = re.sub('<a .*?a_topic.*?>', ' ', comment)         # tag
                comment = re.sub('<img .*?W_img_face.*?>', ' ', comment)    # 表情
                comment = re.sub('<a .*?type=atname.*?>', ' ', comment)     # @某某
                comment = re.sub('<a .*?W_ficon ficon_supertopic">', ' ', comment)     # 超话标签
                comment = re.sub('<\\\\/a>', '', comment)                   # 去除闭合标签<\/a>
                comment = re.sub('<\\\\/i>', '', comment)                   # 去除闭合标签<\/i>
                comment = comment.strip()
                comments.append(comment)
            self.comments[datetime] = comments
            print('users:', users)
            print('comments:', comments)

            # 继续获取更多评论
            # 首先获取下一个api url的参数
            param = re.findall('comment_loading.*?action-data="(.*?)">', html, re.S)
            # 评论太少（只有一页）
            if param == []:
                continue
            param = param[0]
            url2 = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'+param+'&from=singleWeiBo&__rnd=1537350751234'
            self._get_more_comment(url2, datetime)

    # 爬虫入口
    def main(self, extract_weibo=True, extract_comment=True, save_data=True):
        '''
        :param extrat_weibo: 是否爬微博内容
        :param exratct_comment: 是否爬评论
        :param save_data: 是否保存数据
        :return:
        '''
        self._parse_page_one_by_one()
        # self._have_a_look()
        self._extact_WeiBo()

        if extract_comment:
            self._extract_comment()

        if save_data:
            # self._save_comment()
            if extract_weibo:
                self._save_weibo()
                self._save_comment()


if __name__ == '__main__':
    s = WeiBoSpider(page_range=(1, 2))
    s.main()
    # s.main(True, False, True)


