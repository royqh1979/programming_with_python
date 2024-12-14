import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: str
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

def count_scores(scores):
    """
    分段计数

    :param scores: scores列表
    :return: 分段计数结果列表
    """
    nums=[0]*10
    params =[
        (0,10,0),
        (10,20,1),
        (20,30,2),
        (30, 40, 3),
        (40, 50, 4),
        (50, 60, 5),
        (60, 70, 6),
        (70, 80, 7),
        (80, 90, 8),
        (90, 100, 9)
    ]
    for s in scores:
        for p in params:
            start,end,index=p
            if start <=s.score < end:
                nums[index]+=1
    return nums

# 读取文件
filename = "4-2-1.score.csv"
scores = read_csv_file(filename)

print(scores)

nums = count_scores(scores)

for i in range(10):
    print(f"分数段{i*10}-{(i+1)*10}人数:{nums[i]}")

# 画柱状图
import matplotlib.pyplot as plt
labels = [f"{i*10}-{(i+1)*10}" for i in range(10)]
plt.bar(labels,nums)
plt.show()





