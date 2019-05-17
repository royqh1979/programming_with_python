from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    html = "<html><head><title>"
    html +="Hello</title></head><body>"
    html += "<h1>Hello world!</h1>"
    html += "</body></html>"
    return html

app.run(None,5050) # 在本机的5050端口上启动http服务（网页服务）