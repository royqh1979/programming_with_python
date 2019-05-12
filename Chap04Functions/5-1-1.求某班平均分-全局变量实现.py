import csv
from easygraphics import dialog as dlg
from dataclasses import dataclass

@dataclass()
class Score:
    id: str
    name: str
    clazz: str
    math: int
    literacy: int
    english: int

def read_csv(filename):
    """
    从csv文件中读取学生成绩信息
    :param filename: 文件名
    :return: 学生信息列表
    """
    scores=[]
    with open(filename,mode="r",encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = row[0]
            name = row[1]
            clazz = row[2]
            math = int(row[3])
            literacy = int(row[4])
            english = int(row[5])
            score = Score(id,name,clazz,math,literacy,english)
            scores.append(score)
    return scores

def score_to_total(score):
    return score.math+score.english+score.literacy

def filter_by_class(score):
    return score.clazz == clazz

filename = dlg.get_open_file_name("请选择数据文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)
scores = read_csv(filename)

clazz = dlg.get_string("请输入班级名称")
lst1=filter(filter_by_class,scores)
lst2=list(map(score_to_total,lst1))
total = sum(lst2)
count = len(lst2)
average = total / count
print(f"{clazz}班{count}名同学三科平均分为{average:.2f}")