import requests
import pyquery
import queue
import re
import json
import os
from threading import Thread, Lock


class ZhiHuSpider(object):
    def __init__(self):
        # 请求头
        self.headers = {
            'Host': 'www.zhihu.com', 'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': '__DAYU_PP=6V3NMAZfez3IV2ym2Ur628387c2ca106; q_c1=154071103c684f6899f32612eb833186|1536668999000|1521710431000; _zap=6d35acb1-6c74-43ee-bb1c-9b42eaf8afb7; __utma=51854390.1763056340.1536847291.1536847291.1536847291.1; __utmz=51854390.1536847291.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); d_c0="AODgnUJciA2PTu2ixDTeNo9-NhQ9RE7rNWg=|1525269290"; _xsrf=tQ2kOHHJp8Za4FKqutDcNa3k7aTrWAtz; capsion_ticket="2|1:0|10:1536722260|14:capsion_ticket|44:YzM1MTk1NTE0N2EyNDk1YTkzMWM4ZmM3OWNhNmFhNDQ=|4a6c3c96eefe91e129cd9bf9d289e13da6d39ed869bfce38bee8091b01dbb38d"; l_cap_id="MTY1Njk4MTJlN2Y3NGJkYmJmOGYxNGIwOGUzMDQxZTk=|1536672866|b84c52edb063ddfaf94fb14ff13331418b004b36"; r_cap_id="MmIxODQ3ZjE4NzJiNDc5OGJhOWM1MDg0NzIyYzc4MDM=|1536672866|0cc7173bde335b82cc0e23557232b0aec8ca40b9"; cap_id="Y2M3NWE2YjI2MzQ4NGQxYjk1ODY0Y2ZiMzkyMDVkZDY=|1536672866|28a5a0465dacc3c3938b032fd561e41bba2b76a1"; z_c0="2|1:0|10:1536722265|4:z_c0|92:Mi4xZ0h1TEJBQUFBQUFBNE9DZFFseUlEU1lBQUFCZ0FsVk5XZE9GWEFDS3JNRFBsZ292OVJPTVo3SWRtTGN2NzR4b19B|cdc109d2bda5fcc34570321ca490c713b0e3ef1f518be764119cc985a64047ad"; __utmc=51854390; tgw_l7_route=860ecf76daf7b83f5a2f2dc22dccf049; __utmb=51854390.0.10.1536847291; __utmv=51854390.100--|2=registration_date=20170328=1^3=entry_date=20170328=1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        }
        # 问题列表api（两个参数offset和type）
        self.question_list_api = 'https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset":%d,"type":"%s"}'
        # 问题-回答api（两个参数limit和offset）
        self.question_answer_api_url = 'https://www.zhihu.com/api/v4/questions/%s/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&offset=%d&limit=5&sort_by=default'
        # 个人页面api
        self.person_api_url = 'https://www.zhihu.com/people/%s/activities'
        # 提取question id的正则表达式
        self.pattern = re.compile('.*?question/(.*?)/answer')
        # 问题队列
        self.questions_queue = queue.Queue()
        # 数据保存的路径
        self.save_path = './'
        # 数据保存的文件格式
        self.file_type = '.json'
        # 线程锁
        self.lock = Lock()
        # 代理池，需要从文件或数据库导入
        self.proxy_pool = self._load_proxy_pool()

    # 从文件导入代理池
    def _load_proxy_pool(self):
        pass
        return {}

    # 获取单次api请求的所有问题链接和标题
    def _get_one_url_and_title(self, html):
        # 使用pyquery
        doc = pyquery.PyQuery(html)
        items = doc('a.question_link').items()
        for _ in items:
            mess = (_.text(), 'https://www.zhihu.com' + _.attr('href'))
            print(mess)
            self.questions_queue.put(mess)

    # 获取一定数量的问题及其链接
    def _get_some_url_and_title(self, html):
        # 其实可以直接从offset=0开始，那就不必再使用explore这个url，而直接从api获取即可，但是这样做更不像一个爬虫
        self._get_one_url_and_title(html)

        # 两个必要参数，分别指明获取数据的偏移量和类型
        # offset从5到100，type为今日最热
        offsets = range(5, 105, 5)
        _type = 'day'
        for offset in offsets:
            res = requests.get(self.question_list_api % (offset, _type), headers=self.headers)
            t = Thread(target=self._get_one_url_and_title, args=(res.text, ))
            t.start()

    # 保存到文件
    def _save_to_file(self, filename, result):
        # 可能出现的不规范字符需要去掉！
        filename = re.sub('[\/:*?"<>|]', '-', filename)
        with open(self.save_path+filename+self.file_type, 'w', encoding='utf-8') as f:
            json.dump(result, f)

    # 解析具体的单个问题页面
    def _parse_single_page(self, mess):
        # 首先定义question id，offset 这两个必要的参数
        qs_id = re.search(self.pattern, mess[1]).group(1)
        offset = 0
        title = mess[0]

        # 暂存结果
        result = {}

        # 从api中每次5个，爬取用户的回答
        while True:
            res = requests.get(self.question_answer_api_url % (qs_id, offset), headers=self.headers)
            data = res.json()
            # 说明爬完了，需要退出循环
            if data['data'] == []:
                break
            # print(data['data'] == [], type(data['data']), data['data'])
            for i, _ in enumerate(data['data']):
                result[i+offset] = {}
                result[i+offset]['author'] = _['author']['name']
                result[i+offset]['author_url'] = self.person_api_url % _['author']['url_token']
                result[i+offset]['content'] = _['content']
            offset += 5
            print(title, offset)

        self._save_to_file(title, result)
        print(result)

    # 解析页面
    def _start_parse(self, html):
        self._get_some_url_and_title(html)

        # 只要队列不空，开启一个线程解析数据
        while not self.questions_queue.empty():
            mess = self.questions_queue.get()

            # 已经爬过该问题，则跳过此次循环。这种检查的问题是：如果有新的评论爬不到？？
            # 可能出现的不规范字符需要去掉！
            filename = re.sub('[\/:*?"<>|]', '-', mess[0])
            if filename+self.file_type in os.listdir(self.save_path):
                print(mess[0], 'is already crawled!')
                continue

            p = Thread(target=self._parse_single_page, args=(mess, ))
            p.start()
            # p.join()

    def get_comments(self):
        pass

    # 爬虫入口
    def main(self):
        res = requests.get('http://www.zhihu.com/explore', headers=self.headers)
        # print(res.text)
        self._start_parse(res.text)


if __name__ == '__main__':
    sp = ZhiHuSpider()
    sp.main()