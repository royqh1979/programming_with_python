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
    with open(filename, mode = "r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = int(row[0])
            name = row[1]
            score = Decimal(row[2])
            s=Score(id,name,score)
            scores.append(s)
    return scores


def find_by_id(scores, id_key):
    """
    在scores列表中查找id等于id_key的元素

    :param scores: scores列表
    :param id_key: 要查找的id关键字
    :return: 找到的元素在scores列表中的下标。如果没有找到，返回-1
    """
    for i in range(len(scores)):
        s = scores[i]
        if s.id == id_key:
            return i
    return -1

filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)
id = int(dlg.get_string("请输入要查找的id"))
i = find_by_id(scores,id)
if i==-1:
    dlg.show_message(f"找不到id为{id}的学生")
else:
    s=scores[i]
    dlg.show_message(f"id: {s.id} 姓名: {s.name} 成绩：{s.score}")
