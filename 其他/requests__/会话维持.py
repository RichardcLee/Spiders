import requests
'''
利用会话session可以不用担心cookies
'''

print('-----------不同会话下----------')
r1 = requests.get('http://httpbin.org/cookies/set/number/123456789')
r2 = requests.get('http://httpbin.org/cookies')
print(r1.text)
print(r2.text)


print('-----------同一会话下----------')
s = requests.Session()
r1 = s.get('http://httpbin.org/cookies/set/number/119')
r2 = s.get('http://httpbin.org/cookies')
print(r1.text)
print(r2.text)

