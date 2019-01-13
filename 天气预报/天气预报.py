import requests
import pyquery


with open('P_C_A.json', 'r', encoding='utf-8') as f:
    base = f.read()
    base = eval(base)
# print(base)

while True:
    province = input('请输入要查询天气的省份：')
    if province == '退出' or province == 'exit':
        break
    if province not in base:
        print('省份不正确！请重试。')
        continue

    print('请选择要查询的市或区（序号或汉字）：')
    tmp = {}
    for i, city in enumerate(base[province].keys()):
        tmp[i] = city
        print(i, city, sep='.', end='\t')
    city = input()
    try:
        i = int(city)
        if i in tmp:
            city = tmp[i]
        else:
            print('选择错误！返回')
            continue
    except:
        if city not in tmp.values():
            print('选择错误！返回')
            continue

    if province not in ('北京', '重庆', '上海', '天津'):
        print('请选择要查询的区（序号或汉字）：')
        tmp = {}
        for i, area in enumerate(base[province][city]):
            tmp[i] = area
            print(i, area, sep='.', end='\t')
        area = input()
        try:
            i = int(area)
            if i in tmp:
                area = tmp[i]
            else:
                print('选择错误！返回')
                continue
        except:
            if area not in tmp.values():
                print('选择错误！返回')
                continue

    url = base.get(province).get(city)
    if not isinstance(url, str):
        url = base.get(province).get(city).get(area)

    res = requests.get(url)
    html = res.content.decode('utf-8')
    doc = pyquery.PyQuery(html)
    seven_days = doc('li.sky.skyid').items()
    print('-'*30)
    for item in seven_days:
        print(item('h1').text(), item('p').text(), sep='--', end='。\n')
    print('-'*30)
