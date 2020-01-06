"""
成绩管理系统程序

运行后，使用浏览器打开http://localhost:5050/

需要flask、matplotlib、peewee库
"""
from decimal import Decimal

from peewee import *

import io
from flask import Flask, render_template, request, Response
import csv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure, Axes
import matplotlib as mpl

# matplotlib 使用中文字体显示内容
font_name = "STKaiti"
mpl.rcParams['font.family'] = font_name
mpl.rcParams['axes.unicode_minus'] = False  # in case minus sign is shown as box

# sqlite database file
db  = SqliteDatabase("data.db")

class Student(Model):
    id = IntegerField(unique=True,primary_key=True)
    name= CharField()
    class_name= CharField()
    score= DecimalField()

    class Meta:
        database = db # The student model use "test.db" database

# 数据库相关函数
def init_database():
    with db.connection_context():
        db.create_tables([Student])

def connect_db():
    db.connect()

def close_db():
    db.close()

def get_students():
    students = {}
    for s in Student.select():
        students[s.id]=s
    return students


app = Flask(__name__)

@app.route('/')
def index():
    connect_db()
    students = get_students()
    html = render_template("index.html", num_students=len(students))
    close_db()
    return html


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/do_add", methods=['POST'])
def do_add():
    connect_db()
    id = request.form['id']
    name = request.form['name']
    class_name = request.form['class_name']
    score = Decimal(request.form['score'])
    try:
        Student.create(id=id, name=name, class_name=class_name, score=score)
    except IntegrityError as err:
        return f"添加失败：{err}"
    students = Student.select()
    html=render_template("add_ok.html", students=students)
    close_db()
    return html


@app.route("/show")
def show():
    connect_db()
    students = Student.select()
    html =  render_template("show.html", students=students)
    close_db()
    return html


@app.route("/search", methods=['POST', 'GET'])
def search():
    connect_db()
    if request.method == 'GET':
        results = None
    else:
        keyword = request.form['keyword']
        results = Student.select().where( (Student.name.startswith(keyword)) | ( Student.id.startswith(keyword)))
        if len(results) == 0:
            results = None
    html = render_template("search.html", students=results)
    close_db()
    return html


@app.route("/modify/<id>")
def modify(id):
    connect_db()
    s = Student.get(Student.id==id)
    if s is None:
        return f"修改失败！找不到学号为{id}的学生！"
    html = render_template("modify.html", student=s)
    close_db()
    return html


@app.route("/do_modify/<id>", methods=['POST'])
def do_modify(id):
    connect_db()
    s = Student.get(Student.id==id)
    if s is None:
        return f"修改失败！找不到学号为{id}的学生！"
    s.name = request.form['name']
    s.class_name = request.form['class_name']
    s.score = Decimal(request.form['score'])
    s.save()
    students = Student.select()
    html = render_template("modify_ok.html", students=students)
    close_db()
    return html


@app.route("/delete/<id>")
def delete(id):
    connect_db()
    s = Student.get(Student.id==id)
    if s is None:
        return f"修改失败！找不到学号为{id}的学生！"
    s.delete_instance()
    students = Student.select()
    html = render_template("delete_ok.html", students=students)
    close_db()
    return html


def get_score(student):
    return student.score


@app.route("/sort")
def display_sort():
    connect_db()
    students = Student.select().order_by(Student.score.desc())
    html = render_template("show.html", students=students)
    close_db()
    return html


@app.route("/show_hist")
def display_hist():
    return render_template("show_hist.html")


@app.route("/show_pie")
def display_pie():
    return render_template("show_pie.html")


@app.route("/hist_image")
def hist_image():
    counts = calc_counts()
    fig = Figure()
    axes: Axes = fig.add_subplot(1, 1, 1)
    axes.bar([f"{x * 10}-{(x + 1) * 10 - 1}" for x in range(10)], counts)
    axes.set_title("各分数段人数")
    axes.set_xlabel("分数段")
    axes.set_ylabel("人数")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/pie_image")
def pie_image():
    counts = calc_counts()
    fig = Figure()
    axes: Axes = fig.add_subplot(1, 1, 1)
    axes.pie(counts, labels=[f"{x * 10}-{(x + 1) * 10 - 1}" for x in range(10)])
    axes.set_title("各分数段人数")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def calc_counts():
    connect_db()
    students = Student.select()
    score_list = map(get_score, students)
    counts = [0] * 10
    for score in score_list:
        if round(score) >= 100:
            counts[9] += 1
        else:
            counts[round(score) // 10] += 1
    close_db()
    return counts

init_database()
app.run(None, 5050)

db.close()