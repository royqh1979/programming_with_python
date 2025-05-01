from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    items = list(range(1,10))
    name = "张三"
    return render_template("test.html",
        my_name = name , my_items = items)

app.run(None,5050) # 在本机的5050端口上启动http服务（网页服务）