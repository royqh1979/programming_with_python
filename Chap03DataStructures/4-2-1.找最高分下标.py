import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: int
    name: str
    score: Decimal

def read_csv_file(filename):
    """
    读取指定的csv文件，保存并返回scores列表
    :param filename: 要读取的csv文件名
    :return: scores列表
    """
    scores = []
    with open(filename, mode="r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)  # 跳过csv第一行 (标题行)
        for row in reader:
            id = row[0]
            name = row[1]
            score = Decimal(row[2])
            score = Score(id,name,score)
            scores.append(score)
    return scores

def find_max_score(scores):
    """
    寻找并返回scores列表中成绩最高的学生下标

    :param scores: scores列表
    :return: 最高分同学在scores中的下标
    """
    m = 0
    n = len(scores)
    for i in range(n):
        if scores[i].score > scores[m].score:
            m = i
    return m

# 读取文件
filename = "4-2-1.score.csv"

scores = read_csv_file(filename)

print(scores)

index=find_max_score(scores)
max_score = scores[index]

print(f"获得最高分的同学：{max_score.id} {max_score.name},成绩为{max_score.score}")



