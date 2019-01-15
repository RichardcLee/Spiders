'''
up主空间：
https://space.bilibili.com/ajax/member/getSubmitVideos?mid=192185097&pagesize=30&tid=0&page=1&keyword=&order=pubdate%20HTTP/1.1
其中：
    mid=为某个up主独有
    page=页数

# 某个视频的url
https://www.bilibili.com/video/avssss
    ssss = 该视频的aid
'''
import requests
from tool import sub
import os
import json



class UpVideoListCrawler(object):
    def __init__(self, un, mid, page):
        self.page = page  # 实际爬取的视频个数= min(page*30, up主视频的总个数)
        self.username = un  # up主
        # up主视频列表接口
        self.up_video_list_url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + mid + '&' \
                                 'pagesize=30&tid=0&page={}&keyword=&order=pubdate%20HTTP/1.1'
        self.headers = {
            'Host': 'space.bilibili.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'https://space.bilibili.com/' + mid + '/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.video_list = {}    # 视频列表，结果

    def _get_total_video_num(self):
        "获取up主视频列表，包含self.page*30个视频的url"
        for i in range(self.page):
            self._get_one_page_video_list(i+1)

    def _get_one_page_video_list(self, page):
        "获取某一页视频列表，包含最多30个视频的url"
        self.video_list[page] = {}
        res = requests.get(self.up_video_list_url.format(page), headers=self.headers, verify=False)
        if res.status_code == 200:
            data = res.json().get('data')
            pages = data.get('pages')
            vlist = data.get('vlist')
            # count = data.get('count')
            self.page = min(self.page, pages)  # 调整页数
            self._set_dir(vlist)  # 建立文件目录
            for video in vlist:
                aid = video.get('aid')
                title = video.get('title')
                self.video_list[page][aid] = title
        else:  # 获取失败，对应项目为空{}
            print('Exception: ', self.up_video_list_url.format(page), res.status_code, res.reason)

    def _set_dir(self, vlist):
        "建立文件目录"
        self.root_dir = sub(self.username)
        self._make_dir(self.root_dir)
        for i in range(self.page):
            page_dir = './'+self.root_dir+'/page'+str(i+1)
            self._make_dir(page_dir)
            with open('./'+self.root_dir+'/page'+str(i+1)+'_目录.json', 'w+', encoding='utf-8') as f:
                json.dump(vlist, f)

    def _make_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def main(self):
        "  爬虫入口 "
        self._get_total_video_num()
        return self.root_dir, self.video_list


if __name__ == '__main__':
    un, mid, page = '斑鸠心平气和everyday', '11025317', 4
    root_dir, video_list = UpVideoListCrawler(un, mid, page).main()
    print(root_dir)
    print(video_list)