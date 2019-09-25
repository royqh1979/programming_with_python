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

def find_max(scores,cmp_key):
    """
    找数学最高分同学
    :param scores: 成绩列表
    :param cmp_key: 获取成绩信息中要比较的属性值
    :return: 最高分同学信息
    """
    max = scores[0]
    for score in scores:
        if cmp_key(score)>cmp_key(max):
            max = score
    return max

def key_math(score):
    return score.math

def key_literacy(score):
    return score.literacy

def key_english(score):
    return score.english

filename = dlg.get_open_file_name("请选择数据文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)
scores = read_csv(filename)
max_math = find_max(scores, key_math)
max_literacy = find_max(scores, key_literacy)
max_english = find_max(scores, key_english)
print(f"数学最高分：id {max_math.id} 姓名 {max_math.name} 班级 {max_math.clazz} 数学 {max_math.math} 语文 {max_math.literacy} 英语 {max_math.english}")
print(f"语文最高分：id {max_literacy.id} 姓名 {max_literacy.name} 班级 {max_literacy.clazz} 数学 {max_literacy.math} 语文 {max_literacy.literacy} 英语 {max_literacy.english}")
print(f"英语最高分：id {max_english.id} 姓名 {max_english.name} 班级 {max_english.clazz} 数学 {max_english.math} 语文 {max_english.literacy} 英语 {max_english.english}")
