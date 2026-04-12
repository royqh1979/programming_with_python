import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)
print(df.head())

#访问某列
print(df["姓名"])

#修改某列
df["数学"] = np.sqrt(df["数学"])*10

#创建新列
df["总分"]=df["数学"]+df["语文"]+df["英语"]
print(df.head())

#获取指定的几列
df1=df[["姓名","总分"]]
print(df1.head())

#删除列
del df["总分"]
print(df)

