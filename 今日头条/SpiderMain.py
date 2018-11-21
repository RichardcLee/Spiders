import HtmlDownloader, HtmlOutputer, HtmlParser, UrlManager
import threading
import csv
import os


class Spider(object):
    def __init__(self, keyword):
        self._url = 'https://www.toutiao.com/search_content/?offset=%d&format=json&keyword=' + \
                    keyword + '&autoload=true&count=20&cur_tab=2&from=video'    # 2个参数
        self.keyword = keyword  # 参数
        self._htmlDownloader = HtmlDownloader.HtmlDownloader()
        self._htmlParser = HtmlParser.HtmlParser()
        self._urlManger = UrlManager.UrlManager()
        self._htmlOutputer = HtmlOutputer.HtmlOutputer()
        self._prepare()     # 填入url

    def _prepare(self, offset=0):
        start_url = [self._url % offset]
        self._urlManger.add_urls(start_url)

    def _save_data(self, dataTupleList, path):
        with open(path+'/Results.csv', 'a+', encoding='gb2312', errors='ignore') as f:
            writer = csv.writer(f, lineterminator='\n')
            for dataTuple in dataTupleList:
                writer.writerow(dataTuple[:3])

    def _get_one_page(self):
        # 获取每页的数据
        url, *_ = self._urlManger.get_urls(1)
        response = self._htmlDownloader.download(url)
        result = list(self._htmlParser.parse(response, 'json'))
        print('[*]data: ', result)

        path = './%s' % self.keyword
        self._save_data(result, path)

        # 下载相应视频
        self._urlManger.add_img_urls(list(map(lambda x: x[-1], result)))
        # 视频永久真实链接类似
        'http://v11-tt.ixigua.com/eb1fb5e29fe7e69c67fe43f4aa6829ee/5bab992d/video/m/2203400a0395c1e48cd857a6f70e0cd68b71151227a000096389a65dc7f/'
        'http://v11-tt.ixigua.com/4e376b858454503ccdcd5281cca56227/5bab9ce2/video/m/22077952f8cae5d4a13aa9bda317acf12931159512d0000d3b2af2f387c/'

    def _check_sum(self):
        path = './%s' % self.keyword
        if not os.path.exists(path):
            os.mkdir(path)

        with open(path + '/Results.csv', 'a+', encoding='gb2312') as f:
            pass

        with open(path + '/Results.csv', 'r+', encoding='gb2312') as f:
            reader = csv.reader(f)
            # print(list(reader))
            if list(reader) != []:
                return

        with open(path + '/Results.csv', 'a', encoding='gb2312') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(('标题', '作者', '播放量'))

    def main(self, drag=10):
        self._check_sum()   # 为保存数据到文件做准备
        self._get_one_page()    # 默认拉一次
        jump = 20
        for i in range(1, drag+1):  # 拉drag次
            self._prepare(offset=jump*i)
            self._get_one_page()


if __name__ == '__main__':
    keyword = '风景'
    spider = Spider(keyword)
    spider.main()