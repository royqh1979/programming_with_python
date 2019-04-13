import csv
import easygraphics.dialog as dlg
from decimal import Decimal

class Score:
    def __init__(self, id, name, score):
        self.id = id
        self.name = name
        self.score = score

def read_csv(filename):
    """
    从csv文件中读入学生成绩信息
    :param filename: csv文件名
    :return: 学生成绩列表
    """
    scores = []
    with open(filename, mode = "r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = int(row[0])
            name = row[1]
            score = Decimal(row[2])
            s=Score(id,name,score)
            scores.append(s)
    return scores

MAX_ID = 1000

def create_index(scores):
    """
    创建index索引列表
    :param scores: 要索引的scores列表
    :return: index索引列表
    """
    index = [-1]*(MAX_ID+1)
    for i in range(len(scores)):
        s=scores[i]
        index[s.id] = i
    return index

def find_using_index(index,id_key):
    """
    使用index索引列表，查找学号等于id_key在scores列表中的下标
    :param index: 索引列表
    :param id_key: 要查找的学号
    :return: 学生在scores列表中的下标。-1表示列表中无此学生。
    """
    return index[id_key]


filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)
index = create_index(scores)
id = int(dlg.get_string("请输入要查找的id"))
i = find_using_index(index,id)
if i==-1:
    dlg.show_message(f"找不到id为{id}的学生")
else:
    s=scores[i]
    dlg.show_message(f"id: {s.id} 姓名: {s.name} 成绩：{s.score}")
