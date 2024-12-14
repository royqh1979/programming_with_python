import csv
from decimal import Decimal
from dataclasses import dataclass

@dataclass()
class Score:
    id: int
    name: str
    clazz: str
    sex: str
    birth_year: int
    birth_place: str
    math: Decimal
    literature: Decimal
    english: Decimal

# 姓名查找索引项
@dataclass()
class NameIndex:
    index: int # 在数据列表中的下标
    name: str # 姓名（要索引的属性）

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
            clazz = row[2]
            sex = row[3]
            birth_year = row[4]
            birth_place = row[5]
            math = Decimal(row[6])
            literature = Decimal(row[7])
            english = Decimal(row[8])
            score = Score(id,name,clazz, sex, birth_year, birth_place, math,literature,english)
            scores.append(score)
    return scores

def get_name(index):
    """
    排序用的辅助函数
    :param index:
    :return: index对象的name属性值
    """
    return index.name

def create_indices(scores):
    """
    创建并返回scores列表的姓名索引（可用于对姓名的折半查找）
    :param scores: 要建立索引的Score对象列表
    :return: 姓名索引列表
    """
    name_indices = []
    for i in range(len(scores)):
        # 对scores列表中的每个对象，生成对应的索引项，并放到name_indices索引列表中
        s=scores[i]
        index = NameIndex(i,s.name)
        name_indices.append(index)

    # 对name_indices列表按照姓名从小到大的顺序排序
    return sorted(name_indices, key=get_name)

def find_using_index(name_indices,key_name):
    """
    使用索引和折半查找法对姓名进行查找
    :param scores: Score对象列表
    :param name_indices: 姓名索引
    :param key_name: 要找到的姓名
    :return: 该姓名在Score列表中的下标；找不到返回-1
    """
    start = 0
    end = len(name_indices)-1
    while start<=end:
        mid = (start+end)//2
        index = name_indices[mid]
        if index.name == key_name:
            return index.index
        elif index.name < key_name:
            start = mid+1
        else:
            end = mid - 1
    return None

# 从csv文件中读入学生成绩信息，放到scores列表中
filename = "5-2-1.成绩.csv"

scores = read_csv(filename)
print("--- 原数据 ---")
print(scores)

# 创建姓名的折半查找索引
name_indices = create_indices(scores)
print("--- 索引 ---")
print(name_indices)

# 使用折半查找索引进行查找
key = input("请输入要查找的姓名:")
i = find_using_index(name_indices,key)
if i is None:
    print(f"找不到姓名为{key}的学生")
else:
    print(f"找到了！下标为{i}, {scores[i]}")
