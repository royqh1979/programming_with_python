import easygraphics.dialog as dlg
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
    寻找并返回scores列表中成绩最高的学生信息

    :param scores: scores列表
    :return: 最高分同学信息
    """
    max_score = scores[0]
    for score in scores:
        if score.score > max_score.score:
            max_score = score
    return max_score

# 读取文件
filename = dlg.get_open_file_name("选择要打开的文件", dlg.FileFilter.CSVFiles)
if filename == '':
    print("未选择文件")
    exit(-1)

scores = read_csv_file(filename)

dlg.show_objects(scores)

max_score=find_max_score(scores)

dlg.show_message(f"获得最高分的同学：{max_score.id} {max_score.name},成绩为{max_score.score}")



