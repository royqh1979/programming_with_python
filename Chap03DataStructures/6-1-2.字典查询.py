import csv
from easygraphics import dialog as dlg
from decimal import Decimal

class Score:
    def __init__(self, id, name, score):
        self.id = id
        self.name = name
        self.score = score

def read_csv(filename):
    """
    从csv中读取学生信息，并以学号为关键字存入字典中
    :param filename: csv文件名
    :return: 以学号为关键字的学生信息字典
    """
    scores = {}
    with open(filename,mode="r",encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = row[0]
            name = row[1]
            score = Decimal(row[2])
            s=Score(id,name,score)
            scores[id]=s
    return scores

filename = dlg.get_open_file_name("请选择学生成绩文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未指定文件")
    exit(-1)
scores=read_csv(filename)
dlg.show_objects(list(scores.values()))

id=dlg.get_string("请输入要找的学号")
if id in scores:
    s = scores[id]
    dlg.show_message(f"id: {s.id} 姓名: {s.name} 成绩：{s.score}")
else:
    dlg.show_message(f"找不到id为{id}的学生")