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

def find_all_max_score(scores):
    """
    寻找并返回scores列表中所有成绩最高的学生信息对象列表

    :param scores: 元素为学生信息对象的列表
    :return: 最高分同学信息列表
    """
    if len(scores)==0:
        return None
    max_score = scores[0].score
    max_list = []
    for score in scores:
        if score.score > max_score:
            max_score = score.score
            max_list = [score]
        elif score.score == max_score:
            max_list.append(score)
    return max_list

# 读取文件
filename = "4-2-1.score.csv" #4-2-1.score.csv和本程序文件应该在同一个文件夹中
scores = read_csv_file(filename)

#看一下从文件读取的信息是否正确
print(scores)

max_scores=find_all_max_score(scores)

print("获得最高分的同学：")
for s in max_scores:
    print(f"{s.id} {s.name},成绩{s.score}")



