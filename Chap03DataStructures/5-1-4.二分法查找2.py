import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: int
    name: str
    score: Decimal

def read_csv(filename):
    """
    从csv文件中读入学生成绩信息
    :param filename: csv文件名
    :return: 学生成绩列表
    """
    scores = []
    with open(filename, mode = "r", encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            id = int(row[0])
            name = row[1]
            score = Decimal(row[2])
            s=Score(id,name,score)
            scores.append(s)
    return scores


def which_by_id(scores, id_key):
    """
    用二分法在scores列表中查找id等于id_key的元素的下标
    scores列表中的各学生对象按照id从小到大顺序排列

    :param scores: scores列表
    :param id_key: 要查找的id关键字
    :return: 找到的元素在scores列表中的下标；如果没有找到，返回None
    """
    start,end = 0,len(scores)-1
    while start<=end:
        mid = (start+end)//2
        s=scores[mid]
        if s.id == id_key:
            return mid
        elif s.id < id_key: #查找后一半
            start = mid+1
        else: #查找前一半
            end = mid - 1
    return None


filename = "5-1.score.csv"

scores = read_csv(filename)
print(scores)
id = int(input("请输入要查找的id:"))
index = which_by_id(scores, id)
if index is None:
    print(f"找不到id为{id}的学生")
else:
    found = scores[index]
    print(f"下标：{index} id: {found.id} 姓名: {found.name} 成绩：{found.score}")
