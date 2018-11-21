import requests


headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.zhihu.com/signup?next=%2F',
    'Cookie': '__DAYU_PP=6V3NMAZfez3IV2ym2Ur628387c2ca106; q_c1=154071103c684f6899f32612eb833186|1536668999000|1521710431000; _zap=6d35acb1-6c74-43ee-bb1c-9b42eaf8afb7; __utma=51854390.615349536.1536672869.1536672869.1536672869.1; __utmz=51854390.1536672869.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); d_c0="AODgnUJciA2PTu2ixDTeNo9-NhQ9RE7rNWg=|1525269290"; _xsrf=tQ2kOHHJp8Za4FKqutDcNa3k7aTrWAtz; capsion_ticket="2|1:0|10:1536722260|14:capsion_ticket|44:YzM1MTk1NTE0N2EyNDk1YTkzMWM4ZmM3OWNhNmFhNDQ=|4a6c3c96eefe91e129cd9bf9d289e13da6d39ed869bfce38bee8091b01dbb38d"; l_cap_id="MTY1Njk4MTJlN2Y3NGJkYmJmOGYxNGIwOGUzMDQxZTk=|1536672866|b84c52edb063ddfaf94fb14ff13331418b004b36"; r_cap_id="MmIxODQ3ZjE4NzJiNDc5OGJhOWM1MDg0NzIyYzc4MDM=|1536672866|0cc7173bde335b82cc0e23557232b0aec8ca40b9"; cap_id="Y2M3NWE2YjI2MzQ4NGQxYjk1ODY0Y2ZiMzkyMDVkZDY=|1536672866|28a5a0465dacc3c3938b032fd561e41bba2b76a1"; __utmv=51854390.000--|3=entry_date=20180322=1; tgw_l7_route=9553ebf607071b8b9dd310a140c349c5; z_c0="2|1:0|10:1536722265|4:z_c0|92:Mi4xZ0h1TEJBQUFBQUFBNE9DZFFseUlEU1lBQUFCZ0FsVk5XZE9GWEFDS3JNRFBsZ292OVJPTVo3SWRtTGN2NzR4b19B|cdc109d2bda5fcc34570321ca490c713b0e3ef1f518be764119cc985a64047ad"',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers'
}

r = requests.get('https://www.zhihu.com/', headers=headers)
print(r.text)