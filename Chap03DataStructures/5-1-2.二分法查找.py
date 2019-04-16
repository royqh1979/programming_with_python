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


def find_by_id(scores, id_key):
    """
    用二分法在scores列表中查找id等于id_key的元素

    :param scores: scores列表
    :param id_key: 要查找的id关键字
    :return: 找到的元素；如果没有找到，返回None
    """
    start,end = 0,len(scores)-1
    while start<=end:
        mid = (start+end)//2
        s=scores[mid]
        if s.id == id_key:
            return s
        elif s.id < id_key: #查找后一半
            start = mid+1
        else: #查找前一半
            end = mid - 1
    return None


filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)
id = int(dlg.get_string("请输入要查找的id"))
found = find_by_id(scores, id)
if found is None:
    dlg.show_message(f"找不到id为{id}的学生")
else:
    dlg.show_message(f"id: {found.id} 姓名: {found.name} 成绩：{found.score}")
