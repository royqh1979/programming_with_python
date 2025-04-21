"""
从data.csv中导入初始数据到data.fs
"""
from dataclasses import dataclass
import csv
from peewee import *

csv_filename = 'data.csv'
# sqlite database file
db  = SqliteDatabase("data.db")

class Student(Model):
    id = IntegerField(unique=True,primary_key=True)
    name= CharField()
    class_name= CharField()
    score= DecimalField()

    class Meta:
        database = db # The student model use "test.db" database

db.connect()
db.create_tables([Student])
with open(csv_filename, mode="r", encoding="GBK") as file:
    students={}
    reader = csv.reader(file)
    for row in reader:
        id = row[0]
        name = row[1]
        class_name = row[2]
        score = float(row[3])
        if id in students.keys():
            print(f"载入失败：学号{id}已存在！")
        student = Student(id=id,name=name,class_name=class_name,score=score)
        students[id] = student
    Student.bulk_create(students.values())
db.close()