def get_headers(headers_str: str):
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

s = '''Host: 120.221.36.49:6510
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Pragma: no-cache
Cache-Control: no-cache'''
print(get_headers(s))
