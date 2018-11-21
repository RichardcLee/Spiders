from queue import Queue


class UrlManager(object):
    def __init__(self):
        self.urls = Queue()     # 请求两行的摄影集的api队列，未访问
        self.img_urls = set()   # 每个摄影集中的所有图片的url，未访问，其中元素： (title, url)
        self.old_urls = set()   # 已访问过的api或下载过的图片 集合

    def _get_url(self):
        '''
        :return: 如果有未访问的url，则返回它，否则返回None
        '''
        return self.urls.get() if not self.urls.empty() else None

    def get_urls(self, num):
        '''
        :return: [url1, url2, url3...]
        '''
        return [self._get_url() for _ in range(num)]

    def _add_url(self, url):
        # if url not in self.old_urls:
        #     self.urls.put(url)
        # else:
        #     print('%s already crawl!' % url)
        self.urls.put(url) if url not in self.old_urls else print('%s already crawl!' % url)

    def add_urls(self, urls: list):
        # for url in urls:
        #     self._add_url(url)
        [self._add_url(url) for url in urls]

    def _get_img_url(self):
        '''
        :return: 如果有未访问的url，则返回它，否则返回None
        '''
        return self.img_urls.pop() if len(self.img_urls) != 0 else None

    def get_img_urls(self, num):
        '''
        :return: [url1, url2, url3...]
        '''
        return [self._get_img_url() for _ in range(num)]

    def _add_img_url(self, title_url: tuple):
        # if title_url[1] not in self.old_urls:
        #     self.img_urls.add(title_url)
        # else:
        #     print('%s already crawl!' % title_url[1])
        self.img_urls.add(title_url) if title_url[1] not in self.old_urls else print('%s already crawl!' % title_url[1])

    def add_img_urls(self, title_urls: list):
        # for title_url in title_urls:
        #     self._add_img_url(title_url)
        [self._add_img_url(title_url) for title_url in title_urls]

    def add_to_black_list(self, url):
        self.old_urls.add(url)