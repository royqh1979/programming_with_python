#  下载北京林业大学教务处“教改动态”新闻

#  使用peewee orm库来进行orm（对象-关系映射）
from peewee import *
#  使用requests_html库来抓取和处理内容
from requests_html import HTMLSession
import re
from lxml import etree

db = SqliteDatabase("demo.db")


# 新闻
class News(Model):
    id = AutoField(primary_key=True)
    title = TextField()
    content = TextField()
    pub_date = TextField()
    click_count = IntegerField(default=0)

    class Meta:
        database = db
        table_name = "news"


# 附件
class Attachment(Model):
    id = AutoField(primary_key=True)
    news_id = IntegerField()
    filename = TextField()
    content = BlobField()
    size = IntegerField()

    class Meta:
        database = db
        table_name = "attachments"


def get_max_page_number(session):
    url = "http://jwc.bjfu.edu.cn/jwkx/index.html"
    response = session.get(url)
    # response.html.render()
    html = response.html
    html.encoding = 'gbk'
    nav = html.find("div#con_fanye", first=True)
    links = nav.find("a")
    last_page = 1
    for link in links:
        # print(link.text)
        text = link.text
        text = text.strip()
        if text == '最后页':
            last_page_link = link.attrs['href']
            nums = re.findall("\d+", last_page_link)
            last_page = int(nums[0])
            break
    return last_page


def innerHTML(elemement, encoding='utf8'):
    elem = etree.fromstring(elemement.html)
    elemName = elem.xpath('name(/*)')
    resultStr = ''
    for e in elem.xpath('/' + elemName + '/node()'):
        if isinstance(e, str):
            resultStr = resultStr + ''
        else:
            resultStr = resultStr + etree.tostring(e, encoding="unicode").strip()
    return resultStr


def download_news(session, link, title, pub_date):
    page = session.get(link)
    # print(page.headers['Content-Type'])
    if  page.headers['Content-Type']!="text/html":
        print("不是html，跳过。。")
        return
    # page.html.render()
    html = page.html
    html.encoding = 'gbk'
    content = innerHTML(html.find("div#con_c", first=True),encoding='gbk')
    news = News()
    news.title = title
    news.content = content
    news.pub_date = pub_date
    news.save()
    id = news.id
    attachments = html.find("div#con_fujian li a")
    session.headers.update({"Referrer":link})
    for a in attachments:
        attach_resp = session.get(list(a.absolute_links)[0],)
        if len(attach_resp.content) > 50000:
            continue
        attach = Attachment()
        attach.news_id = id
        attach.filename = a.text.strip()
        attach.content = attach_resp.content
        attach.size = len(attach.content)
        attach.save()


def download(session, max_page_number, num=100):
    """
    下载所有文章
    :param session:
    :param max_page_number:
    :return:
    """
    count = 0
    for i in range(max_page_number + 1):
        if i == 0:
            page_link = "http://jwc.bjfu.edu.cn/jwkx/index.html"
        else:
            page_link = "http://jwc.bjfu.edu.cn/jwkx/index" + str(i) + ".html"
        session.headers.update({"Referrer": "http://jwc.bjfu.edu.cn/jwkx/index.html"})
        response = session.get(page_link)
        # response.html.render()
        html = response.html
        html.encoding = 'gbk'
        links = html.find("div#con_c li")
        for link in links:
            a = link.find("a", first=True)
            label = link.find("span", first=True)
            print(label.text, a.text)
            # 下载文章内容
            session.headers.update({"Referrer": page_link})
            download_news(session, list(a.absolute_links)[0], a.text, label.text)
            count += 1
            if count >= num:
                return

db.create_tables([News,Attachment])
News.delete().execute()
Attachment.delete().execute()
session = HTMLSession()
session.headers.update({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.9"})
max_page_number = get_max_page_number(session)
download(session, max_page_number)
