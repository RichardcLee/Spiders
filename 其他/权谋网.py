import requests
from pyquery import PyQuery
from queue import Queue
from queue import Empty
from threading import Thread


headers_s = '''Host: www.mou5.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: safedog-flow-item=EBAA3552229E17F3CB3F9B95391878C9; __tins__17255077=%7B%22sid%22%3A%201541231555890%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201541233355890%7D; __51cke__=; __51laig__=1
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache'''


class QMSpider(object):
    def __init__(self, page_num, headers=None, threads_num=1):
        self.start_url = 'http://www.mou5.com/page/%d'  # url，参数 page i
        if headers is not None: # 请求头
            self.headers = self._get_headers(headers)
        self.threads_num = threads_num  # 线程数
        self.page_num = page_num    # page总数
        self.task_queue = Queue(20)     # 消息队列

    def _get_headers(self, headers_str: str):
        '''
        方便请求头从字符串转换到字典
        :param headers_str: 请求头字符串
        :return: headers  请求头字典
        '''
        if headers_str is None:
            return None

        headers_str_list = headers_str.split('\n')
        headers = {}
        for header_str in headers_str_list:
            name, value = header_str.split(": ")
            # print(name, value)
            headers[name] = value
        # print(headers)
        return headers

    def _download_html(self, url):
        '''
        下载网页源码
        :return:
        '''
        res = requests.get(url, headers=self.headers)

        if res.status_code == 200:
            return res.text
        else:
            print('Error When download html! Reason: ', res.status_code, res.reason)

    def _get_pq(self, html):
        '''
        返回doc
        :param html:
        :return:
        '''
        doc = PyQuery(html)
        return doc

    def get_every_page_link_set(self):
        '''
        获取每一页的链接集合
        :return:
        '''
        for i in range(1, self.page_num+1):
            html = self._download_html(self.start_url % i)
            doc = self._get_pq(html)
            linkSet = list(doc('#contentleft h2 a').items())
            print('put %d page\'s link set into queue.' % i)
            self.task_queue.put(linkSet)

    def _dive_into_one_link_set(self):
        '''
        每次获取一个链接集合，然后深入该链接集合中的每一个链接
        :return:
        '''
        linkSet = self.task_queue.get(5)
        print('get a link set of one page.')
        # print(linkSet)
        for link in linkSet:
            link = link.attr('href')
            # print(link)
            yield self._extract_data(link)

    def wrap_for_thread(self):
        '''
        包装一下，以使用多线程
        :return:
        '''
        data_set = self._dive_into_one_link_set()
        # 数据保存
        #
        print(list(data_set))

    def _extract_data(self, url):
        '''
        提取指定url的数据
        :return:
        '''
        html = self._download_html(url)
        doc = self._get_pq(html)
        result = dict()
        result['title'] = doc('#contentleft h2').text()
        result['date'] = doc('#contentleft p.date').text()
        result['content'] = doc('#contentleft p span').text()
        return result

    def run(self):
        '''
        入口
        :return:
        '''
        self.get_every_page_link_set()

        while not self.task_queue.empty():
            pool = []
            for i in range(self.threads_num):
                t = Thread(target=self.wrap_for_thread)
                pool.append(t)

            for t in pool:
                t.start()

            for t in pool:
                t.join()



if __name__ == '__main__':
    qms = QMSpider(page_num=10, headers=headers_s, threads_num=2)
    qms.run()
