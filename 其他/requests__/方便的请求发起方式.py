import requests

r = requests.get('https://www.baidu.com/')
print(r)
print(r.status_code)
print(r.text)
print(r.content.decode('utf-8'))
print(dict(r.cookies), '\n', list(r.cookies), '\n', r.cookies)

'''
各种请求方法都有对应的函数：
requests.put()
requests.post()
...
'''

