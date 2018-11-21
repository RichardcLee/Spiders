import requests

proxies = {
    'http': 'http://183.129.207.82:18118',
    'https': 'https://120.27.14.125:80'
}

headers = {
    'Host': 'www.taobao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'origin': 'https://www.taobao.com',
    'Cookie': 'cna=Mm2eEmnCXm0CAXAG4w1FuwAZ; isg=BFJSDUmxXXVGFKC_RjKMg0lKoBiYeTuPBz2hghyrf4XwL_IpB_OmDVhNmwsTRM6V; um=0823A424438F76ABE469018CBBE0052FA2AC4A5E17F0ECE9F254F9D4E26C1F34B6236A28B277228FCD43AD3E795C914CBBC5E3E2962401250E91202CB7C7FDBA; thw=cn; miid=7882790962114483785; t=3ea6b1aaf28ff0f02393dbec3d2c24b3; enc=FqsOcMuZ9nuBpdJslSD4ID4qoRG6Fu8wMwIWNjidWytrWlTBLexEZLdCOB3%2FTy0L9OU%2Bhb5ECBeByUxhOssEiw%3D%3D; tracknick=%5Cu4E70%5Cu4E2A%5Cu4E1C%5Cu897F%5Cu90FD%5Cu8FD9%5Cu4E48%5Cu96BE%5Cu554A133; _cc_=WqG3DMC9EA%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; cookie2=3d24506ef6cba97081d74d58953759a0; v=0; _tb_token_=507edd976ba9e',
    'Connection': 'keep-alive',
    # 'If-None-Match': 'W/"2a36-165c95cc45b"',
    'Cache-Control': 'max-age=0'

}

r = requests.get('https://www.taobao.com/', proxies=proxies, headers=headers, timeout=(5, 11))

print(r.status_code)

print(r.text)