from selenium import webdriver
import time

with webdriver.Chrome() as driver:
    #打开登录页（请先保证示例网站已打开，且地址正确）
    driver.get("http://www.bjfu.edu.cn")
    print(driver.current_url)
    time.sleep(5)
    print(driver.page_source)