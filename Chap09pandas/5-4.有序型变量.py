import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv", encoding="GBK")
print(df.head())

#生成成绩列
def get_score_cat(row):
    average = (row["数学"]+row["语文"]+row["英语"])/3
    if average<60:
        return "不及格"
    elif average>=90:
        return "优秀"
    elif average>=80:
        return "良好"
    else:
        return "及格"

df["成绩"] = df.apply(get_score_cat, axis=1)
print(df.head())

#转换为分类型
df["成绩"]=df["成绩"].astype("category")
df["成绩"]=df["成绩"].cat.reorder_categories(["不及格","及格","良好","优秀"],ordered=True)
print(df["成绩"].value_counts().sort_index())
