import re
import requests
import gzip
import zlib
from io import StringIO


headers = {
	'Host': 'www.zhihu.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Accept-Encoding': 'gzip, deflate, br',
	'Cookie': '__DAYU_PP=6V3NMAZfez3IV2ym2Ur628387c2ca106; q_c1=154071103c684f6899f32612eb833186|1536668999000|1521710431000; _zap=6d35acb1-6c74-43ee-bb1c-9b42eaf8afb7; __utma=51854390.171619122.1524926391.1524926391.1524926391.1; __utmz=51854390.1524926391.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/topic/20056622/organize; z_c0="2|1:0|10:1524210488|4:z_c0|92:Mi4xZ0h1TEJBQUFBQUFBMEM2aE5KTjREU1lBQUFCZ0FsVk5PT25HV3dCN0NEX0xtaWozenBrS2xYVmh6V2xVYW9obVJ3|7ec8cdeda1ecd81cccbd09814ff0924bb82a4d60c990056b919ffe04af7474b7"; __utmv=51854390.100--|2=registration_date=20170328=1^3=entry_date=20170328=1; d_c0="AODgnUJciA2PTu2ixDTeNo9-NhQ9RE7rNWg=|1525269290"; _xsrf=tQ2kOHHJp8Za4FKqutDcNa3k7aTrWAtz; tgw_l7_route=ec452307db92a7f0fdb158e41da8e5d8',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'Cache-Control': 'max-age=0',
	'TE': 'Trailers'
}


res = requests.get('http://www.zhihu.com/explore', headers=headers)
print(res)

print(res.content[:40])

data = zlib.decompress(res.content, 16+zlib.MAX_WBITS).decode("utf-8")


print(data[:20])



