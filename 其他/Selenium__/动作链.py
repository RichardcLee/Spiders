from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep
'''
鼠标操作、键盘按键等，这些动作用动作链来执行。
'''
browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to_frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')     # 被拉对象
target = browser.find_element_by_css_selector('#droppable')     # 放置目标

actions = ActionChains(browser)
actions.drag_and_drop(source, target)   # 拖拉
actions.perform()
sleep(10)
browser.close()
