import requests
import re
import json


# 定义几个全局变量，便于数据存取
offset = [_ for _ in range(0, 100, 10)]
urls = ['http://maoyan.com/board/4?offset=%d' % _ for _ in offset]
films = {}

# 预编译
pattern1 = re.compile('<dd>(.*?)</dd>', re.S)
pattern2 = re.compile('<i class="board-index .*?">(\d+)</i>.*?<p class="name"><a .*?">(.*?)</a>.*?'
                      '<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<p class="score">'
                      '<i class="integer">(.*?)</i></p>', re.S)


# 按参数抓取每一个页面
def get_one_page(url):
    headers = {
        'Host': 'maoyan.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': '__mta=149340041.1536806373329.1536806423677.1536806428172.9; uuid_n_v=v1; uuid=3E7C44C0B6FE11E8B950A94C63CD23135A4292FB62C84820B72D36992B27A0C8; _csrf=2016da4d3ad740e2e337ae5932d1bdf9548f31ce8541f57c5d40efa9e6a84071; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165d0cc4214c8-01ade48dde515c8-1161694a-e1000-165d0cc4215c8; _lxsdk_s=165d0cc4216-afe-0cf-b01%7C%7C20; _lxsdk=3E7C44C0B6FE11E8B950A94C63CD23135A4292FB62C84820B72D36992B27A0C8; __mta=149340041.1536806373329.1536806373329.1536806374923.2',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        parse_page(r.text)
    else:
        print('Error:', r.status_code, r.reason, 'at', url)


# 解析页面，用正则提取数据
def parse_page(text):
    # 先按每部电影分块
    temp = re.findall(pattern1, text)

    # 对单部电影进行数据提取
    for _ in temp:
        _ = _.strip()
        _ = re.sub('</i><i class="fraction">', '', _)
        res = re.findall(pattern2, _)
        # 存入字典
        films[res[0][0]] = {
            'name': res[0][1],
            'star': res[0][2].strip(),
            'release time': res[0][3].replace('上映时间：', ''),
            'score': res[0][4]
        }


# 写入json文件
def write_to_file():
    with open('猫眼电影top100.json', 'w', encoding='utf-8') as f:
        json.dump(films, f)


def main():
    for url in urls:
        try:
            get_one_page(url)
            print(url)
        except Exception as e:
            print(e, 'when parse', url)

    write_to_file()


if __name__ == '__main__':
    main()
    print(films)



