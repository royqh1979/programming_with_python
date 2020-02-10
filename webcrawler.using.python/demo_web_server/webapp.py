from datetime import timedelta
from pathlib import Path
from typing import List

from flask import Flask, render_template, Response, session, request, redirect, url_for
from peewee import *
from playhouse.shortcuts import model_to_dict
from werkzeug.urls import url_quote
from pathlib import Path

app= Flask(__name__)
app.config['DEBUG'] = True
# 让Flask自动更新静态文件（每秒1次）
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.secret_key = b'\x08\xcd|\x01\xf5\x15\xd0{1\x08\xa7/\xd4\xb3\x1eu'

myself = Path(__file__)
parent = myself.parent
db_path=Path(str(parent.absolute())+"/demo.db")
db = SqliteDatabase(db_path.absolute())
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
    return render_template("index.html")

# 普通html网站
@app.route("/html-list/<int:page>")
def list_news_html(page):
    lst = get_news_list(page)
    page_info = calc_page(page)
    return render_template("html-news-list.html", news_list=lst, info=page_info)

@app.route("/html-news/<int:id>")
def show_news_html(id):
    news = get_news(id)
    attachments = get_news_attachments(id)
    return render_template("html-news.html", news=news, attachments=attachments)

# 使用javascript生成内容

@app.route("/js-list/<int:page>")
def list_news_js(page):
    lst = get_news_list(page)
    page_info=calc_page(page)
    return render_template("js-news-list.html", news_list=lst, info=page_info)

@app.route("/js-news/<int:id>")
def show_news_js(id):
    news=get_news(id)
    attachments = get_news_attachments(id)
    return render_template("js-news.html", news=news, attachments=attachments)

# ajax生成

@app.route("/ajax-list/<int:page>")
def list_news_ajax(page):
    return render_template("ajax-news-list.html", page=page)

@app.route("/ajax-news/<int:id>")
def show_news_ajax(id):
    return render_template("ajax-news.html",id=id)

# ajax生成（带登陆)
@app.route("/login",methods=['POST'])
def login():
    error = None
    if request.form['username']=='test' and request.form['password']=='test':
        session['username']='test'
        return redirect(url_for('list_news_ajax_auth',page=1))
    else:
        return render_template("index-noauth.html",error="错误的密码!")

@app.route("/logout")
def logout():
    session.pop("username",None)
    return render_template("index-noauth.html",error="已经退出登陆!")

@app.route("/ajax-auth-list/<int:page>")
def list_news_ajax_auth(page):
    if 'username' not in session:
        return render_template("index-noauth.html")
    return render_template("ajax-auth-news-list.html", page=page)

@app.route("/ajax-auth-news/<int:id>")
def show_news_ajax_auth(id):
    if 'username' not in session:
        return render_template("index-noauth.html")
    return render_template("ajax-auth-news.html",id=id)

# json信息
@app.route("/json-list/<int:page>")
def list_news_json(page):
    news_list = get_news_list(page)
    page_info = calc_page(page)
    lst = []
    for news in news_list:
        news_dict = model_to_dict(news,only=(News.id,News.pub_date,News.title))
        lst.append(news_dict)
    return {
        "news_list":lst,
        "info":page_info
    }

@app.route("/json-news/<int:id>")
def show_news_json(id):
    news = get_news(id)
    result = model_to_dict(news,only=(News.title,News.content))
    attach_list = []
    attachments = get_news_attachments(id)
    for attach in attachments:
        att_dict = model_to_dict(attach,only=(Attachment.id,Attachment.filename))
        attach_list.append(att_dict)
    result['attachments'] = attach_list
    return result

#  共用，附件下载

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

# 通用辅助函数

def get_news_attachments(id):
    """
    获取新闻的所有附件
    :param id: 新闻的id
    :return:
    """
    attachments = Attachment.select().where(Attachment.news_id == id)
    return attachments

def get_news(id):
    """
    获取新闻内容
    :param id: 新闻的id
    :return:
    """
    news = News.get_by_id(id)
    news.content = str(news.content).replace("<a name=\"_GoBack\" id=\"_GoBack\"/>", "")
    return news


def get_news_list(page):
    """
    从数据库中获取第page页的新闻列表
    :param page:
    :return:
    """
    lst = News.select().order_by(News.id).paginate(page, NEWS_PER_PAGE)
    return lst

def calc_page(page):
    """
    计算页面导航信息
    :param page: 页数
    :return: 
    """
    total=News.select().count()
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