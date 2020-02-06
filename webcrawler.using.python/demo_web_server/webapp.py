from datetime import timedelta
from pathlib import Path

from flask import Flask,render_template,Response
from peewee import *
from werkzeug.urls import url_quote

app= Flask(__name__)
app.config['DEBUG'] = True
# 让Flask自动更新静态文件（每秒1次）
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

db = SqliteDatabase("demo.db")
NEWS_PER_PAGE = 15

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

@app.route('/')
def index():
    return list(1)

@app.route("/newslist/<page>")
def list(page):
    page=int(page)
    lst=News.select().order_by(News.id).paginate(page, NEWS_PER_PAGE)
    total=News.select().count()
    page_info=calc_page(total,page)
    return render_template("index.html",news_list=lst,info=page_info)

@app.route("/news/<id>")
def show_news(id):
    id=int(id)
    news = News.get_by_id(id)
    news.content = str(news.content).replace("<a name=\"_GoBack\" id=\"_GoBack\"/>","")
    attachments = Attachment.select().where(Attachment.news_id == id)
    return render_template("news.html",news=news,attachments=attachments)

@app.route("/attachment/<id>")
def show_attachment(id):
    id=int(id)
    attach = Attachment.get_by_id(id)
    resp=Response(attach.content, mimetype='application/octet-stream')
    resp.content_length = attach.size
    filename = attach.filename
    try:
        filename = filename.encode('latin-1')
    except UnicodeEncodeError:
        filenames = {
            # 'filename': "UTF-8''{}".format(url_quote(filename)),
            'filename': "{}".format(url_quote(filename)),
        }
    else:
        filenames = {'filename': filename}

    resp.headers.set('Content-Disposition', 'attachment', **filenames)
    return resp

def calc_page(total,page):
    info = {}
    total_page = (total - 1) % NEWS_PER_PAGE + 1
    if page<0:
        page=1
    if page>total_page:
        page=total_page
    info['total'] = total
    info['page'] = page
    info['total_page'] = total_page
    return info


if __name__ == "__main__":
    # 在本地的8080端口上启动web服务器
    app.run(None,port=8080)