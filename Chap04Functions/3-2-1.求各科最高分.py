import csv
from easygraphics import dialog as dlg

class Score:
    def __init__(self,id,name, clazz, math,literacy,english):
        self.id = id
        self.name = name
        self.clazz = clazz
        self.math = math
        self.literacy=literacy
        self.english = english

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

def find_max_math(scores):
    """
    找数学最高分同学
    :return: 最高分同学信息
    """
    max = scores[0]
    for score in scores:
        if score.math > max.math:
            max = score
    return max

def find_max_literacy(scores):
    """
    找语文最高分同学
    :return: 最高分同学信息
    """
    max = scores[0]
    for score in scores:
        if score.literacy > max.literacy:
            max = score
    return max

def find_max_english(scores):
    """
    找英语最高分同学
    :return: 最高分同学信息
    """
    max = scores[0]
    for score in scores:
        if score.english > max.english:
            max = score
    return max

filename = dlg.get_open_file_name("请选择数据文件",dlg.FileFilter.CSVFiles)
if filename == "":
    print("未选择文件")
    exit(-1)
scores = read_csv(filename)
max_math = find_max_math(scores)
max_literacy = find_max_literacy(scores)
max_english = find_max_english(scores)
print(f"数学最高分：id {max_math.id} 姓名 {max_math.name} 班级 {max_math.clazz} 数学 {max_math.math} 语文 {max_math.literacy} 英语 {max_math.english}")
print(f"语文最高分：id {max_literacy.id} 姓名 {max_literacy.name} 班级 {max_literacy.clazz} 数学 {max_literacy.math} 语文 {max_literacy.literacy} 英语 {max_literacy.english}")
print(f"英语最高分：id {max_english.id} 姓名 {max_english.name} 班级 {max_english.clazz} 数学 {max_english.math} 语文 {max_english.literacy} 英语 {max_english.english}")
