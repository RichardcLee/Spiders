from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
'''
chrome可以静默运行，可以修改请求头
'''

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')     # 静默运行
chrome_options.add_argument('--disable-gpu')
# 修改请求头
chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
browser = webdriver.Chrome(chrome_options=chrome_options)

try:
    browser.get('https://www.taobao.com')
    # input_first = browser.find_element_by_id('q')
    # input_second = browser.find_element_by_css_selector('#q')
    input_third = browser.find_element_by_xpath('//*[@id="q"]')
    input_third.send_keys('iphone')    # 键盘操作
    sleep(1)
    input_third.clear()     # 清空
    input_third.send_keys('iPad')
    # input_third.send_keys(Keys.ENTER)
    button = browser.find_element_by_class_name('btn-search')
    button.click()  # 点击按钮
    # print(input_first, input_second, input_third)
finally:
    browser.close()