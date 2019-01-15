import time
import re


def timer(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        print('共耗时：', end-start, 's')
    return wrapper


def sub(s):
    "去除文件名中的非法字符"
    patn_1 = re.compile(r'\?')
    patn_2 = re.compile(r'\/')
    patn_3 = re.compile(r'\\')
    patn_4 = re.compile(r'\|')
    patn_5 = re.compile(r'\:')
    patn_6 = re.compile(r'\<')
    patn_7 = re.compile(r'\>')
    patn_8 = re.compile(r'\*')
    patn_9 = re.compile(r'\:')

    s = re.sub(patn_1, "", s)
    s = re.sub(patn_2, "", s)
    s = re.sub(patn_3, "", s)
    s = re.sub(patn_4, "", s)
    s = re.sub(patn_5, "", s)
    s = re.sub(patn_6, "", s)
    s = re.sub(patn_7, "", s)
    s = re.sub(patn_8, "", s)
    s = re.sub(patn_9, "", s)
    return s


def get_headers(self, headers_str: str):
    '''
    方便请求头从字符串转换到字典
    :param headers_str: 请求头字符串
    :return: headers  请求头字典
    '''
    if headers_str is None:
        return None

    headers_str_list = headers_str.split('\n')
    headers = {}
    for header_str in headers_str_list:
        name, value = header_str.split(": ")
        # print(name, value)
        headers[name] = value
    # print(headers)
    return headers