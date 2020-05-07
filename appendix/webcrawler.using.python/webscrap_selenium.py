#使用selenium抓取示例网站的新闻标题列表
import time

from selenium import webdriver

#使用with语句，保证driver使用完了之后会自动关闭
with webdriver.Chrome() as driver:
    #打开登录页（请先保证示例网站已打开，且地址正确）
    driver.get("http://127.0.0.1:8080/ajax-auth-list/1")

    #由于验证码处理困难，我们等待用户手工完成登陆
    while True:
        time.sleep(1) #等待1秒
        # 获取全部li元素列表
        li_lst= driver.find_elements_by_css_selector("div#con_c ul.list_c li")

        # 登陆成功则元素列表中不止一个元素
        if len(li_lst)>0:
            break

    # 登陆完成，提取全部li列表中的标题信息
    for li in li_lst:
        a = li.find_element_by_css_selector("a")
        print("标题："+a.text)





