# richard lee

import requests
from urllib.parse import quote
import time
import logging
import json
import re
from collections import defaultdict
from threading import Thread
import os

logging.basicConfig(level=logging.NOTSET)  # 设置日志级别


# 注意百度对objURL字段进行了加密！需要解密才能获取最清晰的图片
def decode_url(url: str) -> str:
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d = {'w': 'a',
         'k': 'b',
         'v': 'c',
         '1': 'd',
         'j': 'e',
         'u': 'f',
         '2': 'g',
         'i': 'h',
         't': 'i',
         '3': 'j',
         'h': 'k',
         's': 'l',
         '4': 'm',
         'g': 'n',
         '5': 'o',
         'r': 'p',
         'q': 'q',
         '6': 'r',
         'f': 's',
         'p': 't',
         '7': 'u',
         'e': 'v',
         'o': 'w',
         '8': '1',
         'd': '2',
         'n': '3',
         '9': '4',
         'c': '5',
         'm': '6',
         '0': '7',
         'b': '8',
         'l': '9',
         'a': '0',
         '_z2C$q': ':',
         '_z&e3B': '.',
         'AzdH3F': '/'}
    j = url
    for m in c:
        j = j.replace(m, d[m])
    for char in j:
        if re.match('^[a-w\d]+$', char):
            char = d[char]
        res = res + char

    return res


# 解析响应文本，获取感兴趣字段，并返回
def parse_one(text: str) -> defaultdict:
    res = defaultdict(None)

    jo = json.loads(text)

    gsm = jo.get("gsm")
    if gsm is not None:
        res["gsm"] = gsm

    list_num = jo.get("listNum")
    if list_num is not None:
        res["limits"] = list_num

    data_list = jo.get("data")
    if data_list is not None:

        res["data"] = []

        for data_item in data_list:
            res_item = defaultdict(None)

            obj_url = data_item.get("objURL")
            if obj_url is not None:
                res_item["url"] = decode_url(obj_url)

            title = data_item.get("fromPageTitleEnc")
            if title is not None:
                res_item["title"] = title

            res["data"].append(res_item)

    return res


# 格式化文件名
def fmt_file_name(file_name: str):
    black_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '#', '\n', '\t']
    for c in black_list:
        file_name = file_name.replace(c, "")
    return file_name


# 下载一个url对应的图片
def _download_one(item: defaultdict, save_dir: str):
    img_url = item.get("url")
    if img_url is None:
        logging.error("Lose one image: img_url is None.")
        return

    title = item.get("title")
    if title is None:
        title = str(time.time())
    title = fmt_file_name(title)

    res = requests.get(img_url)
    if res.status_code == 200:
        img_path = os.path.join(save_dir, title + ".jpg")
        logging.info("Save one image to %s" % img_path)
        with open(img_path, "wb") as f:
            f.write(res.content)
    else:
        logging.error("Lose one image. %d, %s." % (res.status_code, res.reason))


# 根据字段进行处理，主要是下载图片
def process(data_list: 'list[defaultdict]', save_dir: str):

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    thread_list = []
    for item in data_list:  # 15个
        thread_list.append(Thread(target=_download_one, args=(item, save_dir)))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()


def main(word_, pn=30, limits=3000):
    """
     word    图片关键字
     pn      类似于tcp序号，是一个图片序号，表示当前页最后一张图片的序号+1（从0开始编号）
     limits  最大爬取张数
    """

    url_template = r"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=%s&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=1&latest=0&copyright=0&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn=%d&rn=30&gsm=%s&%d="

    logid = "11846415876085197636"  # 一个随机串
    word = quote(word_)  # url encode
    gsm = "1e"  # 从1e开始，按某种规律变化的2位字符串，这里不去深究，直接从response里获取

    save_dir = r"./" + fmt_file_name(word_)  # 图片保存路径

    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # "Cookie": "BDqhfp=%E6%8C%96%E6%8E%98%E6%9C%BA%26%26-10-1undefined%26%260%26%261; BIDUPSID=CA2843735B15AE3A628A90AF1B2B9C0E; PSTM=1600996904; BAIDUID=3D50B5D1BACD6C5C7136169A9D48145D:FG=1; __yjs_duid=1_26d598da4f7071f27bf339afc25412581618137630227; MCITY=-%3A; BDSFRCVID_BFESS=4nKOJexroG0YgHnHbu7LJ7xXZcGQd7cTDYLtOwXPsp3LGJLVgadsEG0PtOUBxFP-oxShogKKLgOTHULF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR3aQ5rtKRTffjrnhPF3QjLdXP6-hnjy3bAOKxTt5lQNoqRG0l3AKp4Wbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvX--g3-7PWU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtILMbKvPKITD-tFO5eT22-usJIoi2hcHMPoosIJXbU7_y-D0jPvZtbvvyD7xbR-5KMbUoqRmXnJi0btQDPvxBf7p5K6bQh5TtUJM8U5t2Mjmqt4b0U7yKMniBIv9-pnGBpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjJBea8e3H; BDUSS_BFESS=lRiQjQ0TmJSaks3Mks3LX5ZZU1iM2U3dmU2dDdTZ3B5TjlkTVJLa3h1eThjSHRoRUFBQUFBJCQAAAAAAAAAAAEAAAAIpvWkTV9SaWNoYXJkX0xlZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALzjU2G841NhM; BAIDUID_BFESS=3D50B5D1BACD6C5C7136169A9D48145D:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=null; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; ab_sr=1.0.1_ODFhOTYyZDA5NDk2YjJhYWUwM2E4NTAzMTc2NGNmN2IwZTNlNmNkNmIyY2U5NGM1ZTcyZjFkNGExYWYwYzJlMjdjMTFmYzQyNzkwODBhMmIyNmEzNTc2NmZmMTlmZjYzNzJjNDk3NTQ1M2RiZGRmNTRiYzhlM2QyNjM0OWY2NmI1NjU0YmFhNTQzZmNjMGZkOTBlMTFhMTRlOGFhYTZkYjhmYjBhNzM3ZDY4ZGVlZjIxMWNhNGQzZTgzNDMwOTBi",
        "Host": "image.baidu.com",
        "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1633763283893_R&pv=&ic=&nc=1&z=&hd=0&latest=1&copyright=0&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=%s" % word,
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    while pn <= limits:

        time_stamp = int(time.time() * 1000)
        url = url_template % (logid, word, word, pn, gsm, time_stamp)
        try:
            res = requests.get(url, headers=headers)

            if res.status_code == 200:
                logging.info("Parse one page. Url is %s" % url)

                jo = parse_one(res.text)
                data = jo.get("data")

                if data is None:
                    logging.info("Data is None. %s" % url)
                    break

                process(data[:15], save_dir)
                process(data[15:], save_dir)

                # 更新必要参数
                gsm = jo["gsm"]
                limits = min(jo["limits"], limits)

            else:
                logging.error("Get nothing! %s, %d, at %s" % (res.reason, res.status_code, url))
                break

        except Exception as err:
            logging.error(err)

        finally:
            pn += 30

    logging.info("Crawl end. Total: %d images." % len(os.listdir(save_dir)))


if __name__ == "__main__":
    word = input("输入要爬的图片关键字:")
    main(word, limits=100000)