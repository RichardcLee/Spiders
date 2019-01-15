"""
实际视频链接形如:
http://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/47/43/25894347/25894347-1-32.flv
?e=ig8euxZM2rNcNbh1hwdVhoMzhWdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==
&deadline=1547478697&gen=playurl&nbs=1&oi=1879499521&os=ks3u&platfxorm=pc&trid=725fe7e942d34b39ba6dd4dc9c379c54
&uipk=5&upsig=fed7f8421ba197c20cc44db28a7f96db HTTP/1.1

"""
import requests
import threading
import multiprocessing
import re
from upvideolistcrawler import UpVideoListCrawler
from tool import timer, sub
from time import strftime

class VideoDownLoader(object):
    def __init__(self, un, mid, page, root_dir, video_list):
        self.usename = un  # up主
        self.mid = mid  # up主的mid
        self.page = page  # 爬取第page页的视频
        # self.crawler = UpVideoListCrawler(un, mid, page)    # Up空间视频列表爬虫，为爬取目标视频做前期准备工作
        self.video_page_url = 'https://www.bilibili.com/video/av%d'  # 某个视频页面的url
        self.headers1 = {   # 视频页面请求头
            'Host': 'www.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            #'Cookie': 'buvid3=64866001-0F30-43A4-8EEB-FF91C8CBFA3719354infoc; LIVE_BUVID=AUTO8015213764398557; rpdid=kxmwxpomlpdosiokmxppw; fts=1523250387; sid=an58ym8d; CURRENT_QUALITY=80; stardustvideo=1; CURRENT_FNVAL=16; _uuid=0A5B8C1A-5112-EA89-CE27-C50F73D6D8EC86521infoc; UM_distinctid=1684c683c1cb6-0271ee5bfa04c6-11676f4a-e1000-1684c683c1d395',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.headers2 = {   # 下载视频请求头
            'Host': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
        self.pattern = re.compile('window.__playinfo__={(.*?)}', re.S)  # 正则表达式
        self.pattern2 = re.compile('"url":"(.*?)","backup_url"', re.S)  # 正则表达式，获取视频真实地址
        self.pattern3 = re.compile('http://(.*?)/upgcxcode/')   # 正则表达式，获取主机地址
        self.log_lock = threading.Lock()  # log互斥锁
        self.root_dir = root_dir
        self.video_list = video_list    # 视频列表

    def _get_real_video_url(self):
        '''
        "获取视频真实url，并调用self._download_video下载视频（多线程）"
        :return:
        '''
        # root_dir, video_list = self.crawler.main()  # 调用Up主视频列表爬虫，爬取视频列表并返回创建的目录路径
        # for page, data in video_list.items():
            # print(page, data)
        for aid, title in self.video_list.items():
            # print(aid, title)
            res = requests.get(self.video_page_url % aid, headers=self.headers1)
            if res.status_code == 200:
                data = re.findall(self.pattern, res.text)[0]
                real_video_url = re.findall(self.pattern2, data)[0]
                save_to_path = './' + self.root_dir + '/' + 'page' + str(self.page) + '/' + sub(title) + '.flv' # 保存路径
                # 开多线程！
                thread = threading.Thread(target=self._download_video, args=(real_video_url, save_to_path))
                thread.start()
                thread.join()
                # self._download_video(real_video_url, save_to_path)   # 尽快下载视频！不然链接会失效
            else:
                print('Exception: ', self.video_page_url % aid, res.status_code, res.reason)

    @timer
    def _download_video(self, url, save_to_path):
        '''
        "下载视频"
        :param url: 视频的真实url，只有很短的有效期！
        :param save_to_path: 视频的保存路径以及视频名
        :return:
        '''
        host = re.findall(self.pattern3, url)[0]
        headers = self.headers2.copy()
        headers['Host'] = host
        print('开始下载: ', url)
        try:
            res = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            message = 'Exception: ' + str(e) + '。视频名：' + save_to_path[2:]
        else:
            if res.status_code == 200:
                with open(save_to_path, 'wb') as f:
                    f.write(res.content)
                print('下载成功！')
                message = '下载成功：' + url + '。已保存至：' + save_to_path
            else:
                print('Exception: Download failed!', res.reason, res.status_code)
                message = 'Exception: Download ' + url + ' failed!' + res.reason + str(res.status_code) \
                          + '。视频名：' + save_to_path[2:]
        finally:
            self._log(message)

    def _log(self, message):
        '''
        "记录日志，日志文件为临界资源，需要互斥访问"
        :param message: 记录内容
        :return:
        '''
        self.log_lock.acquire()
        with open('./page' + str(self.page) + '_log_' + strftime('%Y-%m-%d') + '.txt', 'a+', encoding='utf-8', newline='\n') as f:
            f.write(message+'\n')
        self.log_lock.release()

    def main(self):
        self._get_real_video_url()


# def start(un, mid, page, root_dir, a_page_video_list):
#     "为了开多进程，封装一下"
#     VideoDownLoader(un, mid, page, root_dir, a_page_video_list).main()


if __name__ == '__main__':
    un, mid, page = '斑鸠心平气和everyday', '11025317', 2
    root_dir, video_list = UpVideoListCrawler(un, mid, page).main()
    for page, a_page_video_list in video_list.items():
        VideoDownLoader(un, mid, page, root_dir, a_page_video_list).main()

    # 不知为何卡住了，qaq
    # for page, a_page_video_list in video_list.items():
    #     process = multiprocessing.Process(target=start, args=(un, mid, page, root_dir, a_page_video_list))
    #     process.start()
    #     process.join()
