import easygraphics.dialog as dlg
import csv
from decimal import Decimal



class Score:
    def __init__(self,id,name,score):
        self.id = id
        self.name = name
        self.score = score

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
    nums = [0]*10
    for s in scores:
        c=int(s.score // 10)
        nums[c]+=1
    return nums

# 读取文件
filename = dlg.get_open_file_name("选择要打开的文件", dlg.FileFilter.CSVFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

scores = read_csv_file(filename)

dlg.show_objects(scores)

nums = count_scores(scores)

for i in range(10):
    print(f"分数段{i*10}-{(i+1)*10}人数:{nums[i]}")

# 画柱状图
import matplotlib.pyplot as plt
labels = [f"{i*10}-{(i+1)*10}" for i in range(10)]
plt.bar(labels,nums)
plt.show()





