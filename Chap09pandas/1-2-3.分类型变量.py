import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv", encoding="GBK")
print(df)

print("== 默认类型（字符串） ==")
print(df["籍贯"].dtype)
#转化为分类型
# df["性别"]=df["性别"].astype("category")
# print(df["性别"].dtype)

print("== 基础描述 ==")
print(df["籍贯"].describe())
print("== 分类计数 ==")
print(df["籍贯"].value_counts())
print("=====序数编码=====")
print(pd.factorize(df["籍贯"]))
print("====独热编码====")
print(pd.get_dummies(df["籍贯"]))