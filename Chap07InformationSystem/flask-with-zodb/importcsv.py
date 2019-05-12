"""
从data.csv中导入初始数据到data.fs
"""
from dataclasses import dataclass

import ZODB
import csv
from BTrees.OOBTree import BTree
import transaction

@dataclass()
class Student:
    id: str
    name: str
    class_name: str
    score: float

csv_filename = 'data.csv'
db_filename = 'data/data.fs'

conn = ZODB.connection(db_filename)
students = BTree()
root = conn.root

root.students = students

with open(csv_filename, mode="r", encoding="GBK") as file:
    students.clear()
    reader = csv.reader(file)
    for row in reader:
        id = row[0]
        name = row[1]
        class_name = row[2]
        score = float(row[3])
        if id in students.keys():
            print(f"载入失败：学号{id}已存在！")
        student = Student(id, name, class_name, score)
        students[id] = student
transaction.commit()
conn.close()
