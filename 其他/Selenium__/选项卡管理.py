import time
from selenium import webdriver
'''
开多个选项卡
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to.window(browser.window_handles[1])     # 切换卡片
browser.get('https://www.taobao.com')
time.sleep(2)
browser.switch_to.window(browser.window_handles[0])
browser.get('https://python.org')