from selenium import webdriver


'''
对于某些操作，Selenium API并没有提供，比如下拉滚动条，他可以直接模拟运行js。
'''

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
