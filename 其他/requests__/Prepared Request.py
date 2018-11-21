from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
    'name': 'Tom'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0'
}
s = Session()
req = Request('POST', url, data=data, headers=headers)
prereq = s.prepare_request(req)
r = s.send(prereq)
print(r.status_code)
print(r.text)