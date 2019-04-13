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
props = ['id','name','clazz','math','literacy','english']
prop_names=['学号','姓名','班级','数学','语文','英语']
scores = read_csv(filename)
scores = sorted(scores,key=key_math,reverse=True)
dlg.show_objects(scores, fields=props,field_names=prop_names)
scores = sorted(scores,key=key_literacy,reverse=True)
dlg.show_objects(scores, fields=props,field_names=prop_names)
scores = sorted(scores,key=key_english,reverse=True)
dlg.show_objects(scores, fields=props,field_names=prop_names)

