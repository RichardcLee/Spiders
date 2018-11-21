import requests

r = requests.get('http://www.github.com/favicon.ico')
print(r.text)
print(r.content)

with open('github.jpg', 'wb') as f:
    f.write(r.content)
