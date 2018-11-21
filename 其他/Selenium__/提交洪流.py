from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from threading import Thread


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")

    browser = webdriver.Chrome(chrome_options=chrome_options)
    try:
        browser.get('http://acm.wh.sdu.edu.cn:8000/problem/HDU/1000')
        login = browser.find_element_by_css_selector('div.form-inline span a')
        login.click()
        sleep(2)    # 等一会
        username = browser.find_element_by_css_selector('input[name="username"]')
        username.send_keys('提交洪流')
        password = browser.find_element_by_css_selector('input[name="password"]')
        password.send_keys('123')
        button = browser.find_element_by_css_selector('button.btn.btn-primary')
        button.click()
        sleep(2)
        textarea = browser.find_element_by_css_selector('textarea#code')
        textarea.send_keys('''# inlcude<iostream>
                                using namespace std;
                                int main(){
                                    cout<<''不会C++";
                                }''')
        submit = browser.find_element_by_css_selector('#submit')
        submit.click()
        sleep(2)

    finally:
        browser.close()

i = 0
while i < 20:
    main()
    i += 1

