"""
成绩管理系统程序

运行后，使用浏览器打开http://localhost:5050/

需要flask、matplotlib库
"""
import io

from flask import Flask,render_template,request,Response
import csv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure,Axes
import matplotlib as mpl
from dataclasses import dataclass

# matplotlib 使用中文字体显示内容
font_name = "STKaiti"
mpl.rcParams['font.family']=font_name
mpl.rcParams['axes.unicode_minus']=False # in case minus sign is shown as box

@dataclass()
class Student:
    id: str
    name: str
    class_name: str
    score: float

students = {}

filename =  "data.csv"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",num_students=len(students))

@app.route("/load")
def load():
    with open(filename, mode="r", encoding="GBK") as file:
        students.clear()
        reader = csv.reader(file)
        for row in reader:
            id = row[0]
            name = row[1]
            class_name = row[2]
            score = float(row[3])
            if id in students.keys():
                return f"载入失败：学号{id}已存在！"
            student = Student(id,name,class_name,score)
            students[id]=student
    return render_template("load.html",students=students.values())

@app.route("/save")
def save():
    with open(filename, mode="w", encoding="GBK") as file:
        for s in students.values():
            file.write(f"{s.id},{s.name},{s.class_name},{s.score}\n")
    return render_template("save.html",students=students.values())

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/do_add", methods = ['POST'])
def do_add():
    id = request.form['id']
    name = request.form['name']
    class_name = request.form['class_name']
    score = float(request.form['score'])
    if id in students.keys():
        return f"添加失败：学号{id}已存在！"
    student = Student(id,name,class_name,score)
    students[id]=student
    return render_template("add_ok.html", students=students.values())

@app.route("/show")
def show():
    return render_template("show.html",students=students.values())


@app.route("/search", methods = ['POST','GET'])
def search():
    if request.method == 'GET':
        results = None
    else:
        keyword=request.form['keyword']

        def filter_by_name_or_id(student):
            if student.name.startswith(keyword):
                return True
            if student.id.startswith(keyword):
                return True
            return False

        results = filter(filter_by_name_or_id,students.values())
        results = list(results)
        if len(results)==0:
            results = None
    return render_template("search.html", students = results)

@app.route("/modify/<id>")
def modify(id):
    if id not in students.keys():
        return f"修改失败！找不到学号为{id}的学生！"
    student = students[id]
    return render_template("modify.html",student=student)

@app.route("/do_modify/<id>",methods=['POST'])
def do_modify(id):
    if id not in students.keys():
        return f"修改失败！找不到学号为{id}的学生！"
    student = students[id]
    student.name = request.form['name']
    student.class_name = request.form['class_name']
    student.score = float(request.form['score'])
    return render_template("modify_ok.html", students=students.values())

@app.route("/delete/<id>")
def delete(id):
    if id not in students.keys():
        return f"删除失败！找不到学号为{id}的学生！"
    del students[id]
    return render_template("delete_ok.html", students=students.values())

def get_score(student):
    return student.score

@app.route("/sort")
def display_sort():
    new_students = reversed(sorted(students.values(),key=get_score))
    return render_template("show.html", students=new_students)

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
    axes:Axes=fig.add_subplot(1,1,1)
    axes.bar([f"{x*10}-{(x+1)*10-1}" for x in range(10)],counts)
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
    axes:Axes=fig.add_subplot(1,1,1)
    axes.pie(counts,labels=[f"{x*10}-{(x+1)*10-1}" for x in range(10)])
    axes.set_title("各分数段人数")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def calc_counts():
    score_list = map(get_score, students.values())
    counts = [0] * 10
    for score in score_list:
        if round(score) >= 100:
            counts[9] += 1
        else:
            counts[round(score) // 10] += 1
    return counts


app.run(None,5050)