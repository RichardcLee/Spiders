'''
预先获取天气预报目的地的信息，省-市-区，以及对应的url

省：http://xxx.weather.com.cn/
市：http://xxx.weather.com.cn/yyy/index.shtml
区：http://www.weather.com.cn/weather/zzzzzzz.shtml
（xxx为省名小写拼音缩写）(yyy为市小写拼音缩写) (zzzzzzz为代表某个地区的数字)

'''
import pyquery
import requests
import pickle


result = {}


def get_province():
    " 获取省入口 "
    ignore_province = ('台湾', '香港')
    url = 'http://www.weather.com.cn/province/'
    province_entry = []
    res = requests.get(url)
    if res.status_code == 200:
        doc = pyquery.PyQuery(res.content.decode('utf-8'))
        a = doc('div.sheng_rukou ul li a')
        for item in a.items():
            province = item.text()
            if province.endswith("气象局"):
                continue
            if province in ignore_province:  # 忽略，因为没有数据
                continue
            province_entry.append((province, item.attr('href')))
            result[province] = {}
    else:
        print('Exception: ', res.reason, res.status_code)
    return province_entry


def get_city(province_entry: list):
    " 获取市入口 "
    special_province = ('北京', '重庆', '上海', '天津')
    city_entry = []
    for province, url in province_entry:
        res = requests.get(url)
        if res.status_code == 200:
            doc = pyquery.PyQuery(res.content.decode('utf-8'))
            a = doc('div.navbox span a')
            if province in special_province:
                for item in a.items():
                    if item.text().endswith("气象局"):
                        continue
                    city_entry.append((province, url, item.text(), item.attr('href')))
                    result[province][item.text()] = item.attr('href')
            else:
                for item in a.items():
                    if item.text().endswith("气象局"):
                        continue
                    city_entry.append((province, url, item.text(), item.attr('href')))
                    result[province][item.text()] = {}

        else:
            print('Exception: ', res.reason, res.status_code)
    return city_entry


def get_area(city_entry: list):
    special_province = ('北京', '重庆', '上海', '天津')
    area_entry = []
    for province, u, city, url in city_entry:
        if province in special_province:
            # area_entry.append((province, u, city, url))
            continue
        res = requests.get(u+url)
        if res.status_code == 200:
            doc = pyquery.PyQuery(res.content.decode('utf-8'))
            a = doc('div.navbox span a')
            for item in a.items():
                if item.text().endswith("气象局"):
                    continue
                # area_entry.append((province, u, city, url, item.text(), item.attr('href')))
                result[province][city][item.text()] = item.attr('href')
        else:
            print('Exception: ', res.reason, res.status_code)
    return area_entry


def main():
    province_entry = get_province()
    print(province_entry)
    city_entry = get_city(province_entry)
    print(city_entry)
    area_entry = get_area(city_entry)
    # print(area_entry)
    # with open('P_C_A.pkl', 'wb') as f:
    #     pickle.dump(area_entry, f)
    with open('P_C_A.json', 'w+', encoding='utf-8') as f:
        f.write(str(result))


if __name__ == '__main__':
    main()