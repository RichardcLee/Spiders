import requests
import json
import csv
import codecs
import threading
import multiprocessing
import time
import re
'''
手机版页面更容易爬！！！
'''


class WeiBoSpider(object):
    def __init__(self, target_name: 'str', target_uid: 'int', page_range=None, sleep=0):
        # 参数 value=uid, containerid=107603+uid, page
        self.value = target_uid
        self.containerid = '107603'+str(target_uid)

        if page_range is None:
            self.page, self.page_end = 1, None
        else:
            self.page, self.page_end = page_range

        # 保存的文件名
        self.target_name = target_name
        # 睡眠时间
        self.sleep = sleep
        # 微博 api
        self.url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%d&containerid=%s&page=%d'
        # 微博评论 api 参数 id=mid=%s, %s=(&max_id=%s)
        self.comments_url = 'https://m.weibo.cn/comments/hotflow?id=%s&mid=%s%s&max_id_type=0'
        # 用户个人信息 api 参数 uid=%s
        self.user_api = 'https://m.weibo.cn/profile/info?uid=%s'
        # 请求头
        self.headers = {
            'Host': 'm.weibo.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'origin': 'https://m.weibo.cn',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://m.weibo.cn/u/3675868752?uid=3675868752&luicode=10000011&lfid=100103type%3D3%26q%3Dsnh48-%E5%86%AF%E8%96%AA%E6%9C%B5%2'
        }
        # [(ext, source, scheme), ...]
        self.content = []
        # 评论
        self.comment = {}
        # 线程锁
        self.lock = threading.Lock()
        # 男女数量
        self.f, self.m = 0, 0

    # 提取微博内容
    def _extract_weibo(self, json_data_str: 'str'):
        data = json.loads(json_data_str)
        blocks = data.get('data').get('cards')
        for block in blocks:
            scheme = block.get('scheme')    # 微博详细页面
            mblog = block.get('mblog')
            if mblog is not None:
                text = mblog.get('text')    # 微博内容
                source = mblog.get('source')    # 发布工具
                t = (text, source, scheme)
                self.content.append(t)
                print('weibo: ', t)
        time.sleep(self.sleep)    # 睡眠一会

        # 递归获取下一页微博，直到page参数不再变化，说明已经到底 或者 达到规定的范围上限
        page = data.get('data').get('cardlistInfo').get('page')
        if page != self.page and page != self.page_end+1:
            self.page = page
            self.lock.acquire()     # 获得锁
            start = time.time()
            try:
                t = threading.Thread(target=self._get_mblogs, args=(self.url % (self.value, self.containerid, self.page),))
                t.start()
            finally:
                self.lock.release()     # 释放锁
                print('takes', time.time() - start, 'seconds...')

        else:   # 终止
            if self.save_weibo:
                self._save_weibo()

    # 请求微博api
    def _get_mblogs(self, url):
        try:
            res = requests.get(url, self.headers)
            print('get page %d: ' % self.page, url)

            if res.status_code == 200:
                self._extract_weibo(res.text)

            else:
                print('Error %s: ' % url, res.status_code, res.reason)
                return
        except Exception as e:
            print('Error: ', e)

    # 递归获取评论
    def _get_comments(self, mid, max_id, target):
        time.sleep(self.sleep)  # 睡眠
        url = self.comments_url % (mid, mid, max_id)
        try:
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                json_data = json.loads(res.text)
                data = json_data.get('data')
                if data == None:    # 退出递归，如果爬不到数据了，有时微博就是爬不到底？到某个深度就会返回空的json文件
                    print('Get part of comments from %s end! Reason: get data:data is None.' % url)
                    if self.get_user_gender:    # 获取评论区用户的性别
                        t = threading.Thread(target=self._get_user_gender, args=(target,))
                        t.start()
                        # self._get_user_gender(target)
                    if self.save_comments:  # 保存数据
                        self._save_comments(target)
                    return
                data = data.get('data')
                for da in data:
                    created_at = da.get('created_at')       # 评论时间
                    text = da.get('text')                   # 评论内容
                    user = da.get('user').get('profile_url')    # 评论粉丝的个人主页，下一步收集性别
                    self.comment[target].append((created_at, text, user))
                    print('comment: ', (created_at, text, user))
                print('Get part of comments from %s successfully!' % url)

                max_id_new = str(json_data.get('data').get('max_id'))    # 加载更多评论的必要参数
                if max_id_new == '0':   # 这会导致死循环，但这个得到的0并不代表已经爬完所有评论！！！
                    print('Get max_id=0? End or Error? After %s' % url)
                    if self.get_user_gender:    # 获取评论区用户的性别
                        t = threading.Thread(target=self._get_user_gender, args=(target,))
                        t.start()
                        # self._get_user_gender(target)
                    if self.save_comments:  # 保存数据
                        self._save_comments(target)
                    return

                self._get_comments(mid, "&max_id=" + max_id_new, target)

            else:
                print('Get part of comments from %s failed! Reason: %s' % (url, str(res.status_code)+' '+res.reason))
        except Exception as e:
            print('Error: ', e)

    # 爬取所有评论
    def _get_scheme(self):
        for *_, url in self.content:
            mid = re.findall('status/(.*?)\?', url)
            if mid == []:
                print('Get comments from %s failed! Reason: Can\'t get param id and mid' % url)
                continue
            mid = mid[0];max_id = ''
            self.comment[mid] = []      # 用mid唯一表示一个微博
            self._get_comments(mid, max_id, mid)

    # 获取评论区用户性别
    def _get_user_gender(self, target):
        urls = set(list(map(lambda x: x[2], self.comment[target])))
        for url in urls:    # 逐个获取性别，仅统计男女比例！
            time.sleep(1)
            uid = re.findall('u/(.*?)\?uid', url)[0]
            print('uid:', uid)
            url = self.user_api % uid
            try:
                res = requests.get(url, headers=self.headers)
                if res.status_code == 200:
                    data = json.loads(res.text)
                    try:
                        gender = data.get('data').get('user').get('gender')
                        print(gender)
                        if gender == 'f':
                            self.f += 1
                        else:
                            self.m += 1
                    except Exception as e:
                        print('Error:', str(e))

                else:
                    print('Error %s. Reason: ' % url, res.status_code, res.reason)
                    return
            except Exception as e:
                print('Error: ', e)

        with open('user_gender_%s.csv' % target, 'w+', encoding='gb2312') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(('男', '女'))
            writer.writerow((self.m, self.f))
        time.sleep(self.sleep)  # 睡眠一会

    # 保存爬到的微博
    def _save_weibo(self):
        with codecs.open(self.target_name+'.csv', 'w+', encoding='gb2312', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(('微博内容', '客户端', '网址'))
            writer.writerows(self.content)
            print('Save weibo content at %s' % self.target_name+'.csv')

    # 保存评论，注意：评论太多，请及时释放内存！
    def _save_comments(self, filename):
        with open(filename+'.csv', 'w+', encoding='gb2312', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(('评论实际', '评论内容', '用户'))
            writer.writerows(self.comment[filename])
            print('save %s' % filename)
        del self.comment[filename]    # 保存后即删除

    def main(self, get_comments=True, get_user_gender=False, save_weibo=True, save_comments=False):
        self.save_comments = save_comments
        self.get_user_gender = get_user_gender
        self.save_weibo = save_weibo
        start_url = self.url % (self.value, self.containerid, self.page)
        self._get_mblogs(start_url)

        if get_comments:
            self._get_scheme()


# 封装进来，才能开多线程
def start(uid, target, page_range):
    # 设置页数，一是方便测试，而是为了开多进程
    spider = WeiBoSpider(target_name=target, target_uid=uid, page_range=page_range, sleep=5)
    spider.main(get_comments=True, get_user_gender=True, save_weibo=True, save_comments=True)


if __name__ == '__main__':
    # 填写以下两个参数，即可爬取任何目标！第二个其实是保存的文件名
    uid = 3675868752
    target_ = 'snh48-冯薪朵1'
    p1 = multiprocessing.Process(target=start, args=(uid, target_, (1, 10)))
    p1.start()

    target_ = 'snh48-冯薪朵2'
    p2 = multiprocessing.Process(target=start, args=(uid, target_, (11, 20)))
    p2.start()

    target_ = 'snh48-冯薪朵3'
    p3 = multiprocessing.Process(target=start, args=(uid, target_, (21, 30)))
    p3.start()

    target_ = 'snh48-冯薪朵4'
    p4 = multiprocessing.Process(target=start, args=(uid, target_, (31, 40)))
    p4.start()