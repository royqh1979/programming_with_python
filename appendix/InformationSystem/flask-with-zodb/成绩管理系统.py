"""
成绩管理系统程序

运行后，使用浏览器打开http://localhost:5050/

需要flask、matplotlib、zodb库
"""
# zodb
from dataclasses import dataclass

import ZODB
from BTrees.OOBTree import BTree
import transaction

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


@dataclass()
class Student:
    id: str
    name: str
    class_name: str
    score: float


filename = "data/data.fs"

db = ZODB.DB(filename)

# zodb数据库相关函数
def get_conn():
    conn = db.open()
    return conn


def get_students(conn):
    root = conn.root
    if 'students' not in conn.root():
        print("init zodb database...")
        students = BTree()  # btree可以当成一个字典来用
        root.students = students  # 将students交给zodb来管理
    else:
        students = root.students
    return students


def close_conn(conn):
    transaction.commit()
    conn.close()


app = Flask(__name__)


@app.route('/')
def index():
    conn=get_conn()
    students = get_students(conn)
    html = render_template("index.html", num_students=len(students))
    close_conn(conn)
    return html


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/do_add", methods=['POST'])
def do_add():
    conn=get_conn()
    students = get_students(conn)
    id = request.form['id']
    name = request.form['name']
    class_name = request.form['class_name']
    score = float(request.form['score'])
    if id in students.keys():
        return f"添加失败：学号{id}已存在！"
    student = Student(id, name, class_name, score)
    students[id] = student
    html=render_template("add_ok.html", students=students.values())
    close_conn(conn)
    return html


@app.route("/show")
def show():
    conn=get_conn()
    students = get_students(conn)
    html =  render_template("show.html", students=students.values())
    close_conn(conn)
    return html


@app.route("/search", methods=['POST', 'GET'])
def search():
    conn=get_conn()
    students = get_students(conn)
    if request.method == 'GET':
        results = None
    else:
        keyword = request.form['keyword']

        def filter_by_name_or_id(student):
            if student.name.startswith(keyword):
                return True
            if student.id.startswith(keyword):
                return True
            return False

        results = filter(filter_by_name_or_id, students.values())
        results = list(results)
        if len(results) == 0:
            results = None
    html = render_template("search.html", students=results)
    close_conn(conn)
    return html


@app.route("/modify/<id>")
def modify(id):
    conn=get_conn()
    students = get_students(conn)
    if id not in students.keys():
        return f"修改失败！找不到学号为{id}的学生！"
    student = students[id]
    html = render_template("modify.html", student=student)
    close_conn(conn)
    return html


@app.route("/do_modify/<id>", methods=['POST'])
def do_modify(id):
    conn=get_conn()
    students = get_students(conn)
    if id not in students.keys():
        return f"修改失败！找不到学号为{id}的学生！"
    student = students[id]
    student.name = request.form['name']
    student.class_name = request.form['class_name']
    student.score = float(request.form['score'])
    html = render_template("modify_ok.html", students=students.values())
    close_conn(conn)
    return html


@app.route("/delete/<id>")
def delete(id):
    conn=get_conn()
    students = get_students(conn)
    if id not in students.keys():
        return f"删除失败！找不到学号为{id}的学生！"
    del students[id]
    html = render_template("delete_ok.html", students=students.values())
    close_conn(conn)
    return html


def get_score(student):
    return student.score


@app.route("/sort")
def display_sort():
    conn=get_conn()
    students = get_students(conn)
    new_students = reversed(sorted(students.values(), key=get_score))
    html = render_template("show.html", students=new_students)
    close_conn(conn)
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
    conn=get_conn()
    students = get_students(conn)
    score_list = map(get_score, students.values())
    counts = [0] * 10
    for score in score_list:
        if round(score) >= 100:
            counts[9] += 1
        else:
            counts[round(score) // 10] += 1
    close_conn(conn)
    return counts

app.run(None, 5050)

db.close()