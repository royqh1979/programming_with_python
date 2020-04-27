import csv
import easygraphics.dialog as dlg
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Student:
    id: int
    name: str
    score: Decimal

@dataclass()
class IndexItem:
    """
    存放index条目
    """
    key: str
    student: Student

def read_csv(filename):
    """
    从csv文件中读入学生成绩信息
    :param filename: csv文件名
    :return: 学生成绩列表
    """
    students = []
    with open(filename, mode = "r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = int(row[0])
            name = row[1]
            score = Decimal(row[2])
            s=Student(id, name, score)
            students.append(s)
    return students

MAX_INDEX_SIZE = 10000

def create_index(students):
    """
    创建index索引列表
    :param students: 要索引的scores列表
    :return: index索引列表
    """
    index = [[] for x in range(MAX_INDEX_SIZE)]
    for s in students:
        i_index = hash(s.name) % MAX_INDEX_SIZE #该姓名的hash值，取余保证其在index的下标范围内
        item = IndexItem(s.name, s)
        index[i_index].append(item)
    return index

def find_using_index(index,name_key):
    """
    使用index索引列表，查找姓名等于name_key在scores列表中的下标
    :param index: 索引列表
    :param name_key: 要查找的姓名
    :return: 姓名为name_key的学生。None表示找不到。
    """
    i_index = hash(name_key) % MAX_INDEX_SIZE
    items=index[i_index]
    for item in items:
        if item.key == name_key:
            return item.student
    return None

#5-2-2.成绩.csv
filename = dlg.get_open_file_name("请选择成绩csv文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)

students = read_csv(filename)
dlg.show_objects(students)
index = create_index(students)
name = dlg.get_string("请输入要查找的姓名")
found = find_using_index(index,name)
if found is None:
    dlg.show_message(f"找不到姓名为{name}的学生")
else:
    dlg.show_message(f"id: {found.id} 姓名: {found.name} 成绩：{found.score}")
