import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: str
    name: str
    score: Decimal

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

filename = "7-1.score.csv"

scores=read_csv(filename)
print(scores)

id=input("请输入要找的学号:")
if id in scores:
    s = scores[id]
    print(f"id: {s.id} 姓名: {s.name} 成绩：{s.score}")
else:
    print(f"找不到id为{id}的学生")