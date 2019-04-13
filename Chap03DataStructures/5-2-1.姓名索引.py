import csv
import easygraphics.dialog as dlg
from decimal import Decimal

class Score:
    def __init__(self, id, name, score):
        self.id = id
        self.name = name
        self.score = score


class IndexItem:
    """
    存放index条目
    """
    def __init__(self,key,index):
        self.key = key
        self.index = index

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

MAX_INDEX_SIZE = 10000

def create_index(scores):
    """
    创建index索引列表
    :param scores: 要索引的scores列表
    :return: index索引列表
    """
    index = [[] for x in range(MAX_INDEX_SIZE)]
    for i in range(len(scores)):
        s=scores[i]
        i_index = hash(s.name) % MAX_INDEX_SIZE #该姓名的hash值，取余保证其在index的下标范围内
        item = IndexItem(s.name, i)
        index[i_index].append(item)
    return index

def find_using_index(index,name_key):
    """
    使用index索引列表，查找姓名等于name_key在scores列表中的下标
    :param index: 索引列表
    :param name_key: 要查找的姓名
    :return: 学生在scores列表中的下标。-1表示列表中无此学生。
    """
    i_index = hash(name_key) % MAX_INDEX_SIZE
    items=index[i_index]
    for item in items:
        if item.key == name_key:
            return item.index
    return -1


filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

scores = read_csv(filename)
dlg.show_objects(scores)
index = create_index(scores)
name = dlg.get_string("请输入要查找的姓名")
i = find_using_index(index,name)
if i==-1:
    dlg.show_message(f"找不到姓名为{name}的学生")
else:
    s=scores[i]
    dlg.show_message(f"id: {s.id} 姓名: {s.name} 成绩：{s.score}")
