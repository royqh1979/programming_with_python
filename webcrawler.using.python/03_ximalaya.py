#使用requests下载喜马拉雅专辑
import pathlib
import re
import time
import requests
import json
import easygraphics.dialog as dlg

#输入专辑的url地址
link=dlg.get_string("专辑url")

#在HTTP协议的Header信息里将自己伪装成浏览器
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}

# 提取专辑中各音频的列表
#专辑url最后是album的id
albumId = link.split('/')[4]
url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId=1&pageSize=20&pre_page=0'
html = requests.get(url)
print(html.text)
all = json.loads(html.text)
#Thread2 = futures.ThreadPoolExecutor(max_workers=1)
# 音频数量太多时会分页，获取总页数
total_pages = all['data']['maxPageId']
pages_list = range(1,total_pages + 1)
download_list=[]
num=0
for n in pages_list:
    #获取第n页列表中的音频信息
    print("page "+str(n))
    time.sleep(1)
    url = 'http://180.153.255.6/mobile/v1/album/track/ts-1534855383505?albumId=' + albumId + '&device=android&isAsc=true&isQueryInvitationBrand=true&pageId='+ str(n) +'&pageSize=20&pre_page=0'
    html = requests.get(url,headers = headers)
    all = json.loads(html.text)
    data = all['data']['list']
    for x in data:
        title = x['title']
        id = x['trackId']
        url32 = x['playUrl32']
        url64 = x['playUrl64']
        print((title,id,url32,url64))
        download_list.append((title, id, url32, url64))

print("开始下载")
for data in download_list:
    url = data[2]
    if len(url)==0:
        url = data[3]
    # 去除标题中()括起的内容
    title = re.sub(u"\\(.*?\\)", "", data[0])
    title = re.sub(u"（.*?）", "", title)
    file_name = title+".mp3"
    path = pathlib.Path(file_name)
    if path.exists():
        continue
    print(file_name + "开始下载")
    file1 = requests.get(url, headers=headers)
    with open(file_name, 'wb') as code:
        code.write(file1.content)
    print(file_name+"下载完成")
    time.sleep(3)

