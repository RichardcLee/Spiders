import requests


files = {
    'github.jpg': open('github.jpg', 'rb')
}

r = requests.post('http://httpbin.org/post', files=files)
print(r.text)