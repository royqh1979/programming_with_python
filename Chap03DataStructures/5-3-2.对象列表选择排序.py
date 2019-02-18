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

def find_max(scores,start,end):
    """
    找从scores[start]到scores[end-1]中，成绩最高的元素下标
    """
    max = start
    for i in range(start,end):
        if scores[i].score > scores[max].score:
            max = i
    return max

def select_sort(scores):
    """
    选择排序
    :param scores: 待排序列表
    """
    n = len(scores)
    for i in range(n):
        t = find_max(scores,i,n)
        scores[i],scores[t] = scores[t],scores[i]

filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)

select_sort(scores)
dlg.show_objects(scores)