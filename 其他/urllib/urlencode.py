from urllib.parse import urlencode, parse_qs, parse_qsl

params = {
	'name': 'germy',
	'age': 22
}

base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)
print(parse_qs(urlencode(params)))
print(parse_qsl(urlencode(params)))
