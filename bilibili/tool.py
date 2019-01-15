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
