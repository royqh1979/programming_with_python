import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK")
print(df.head())

#创建新列
df["总分"]=df["数学"]+df["语文"]+df["英语"]
print(df.head())

#筛选部分列组成新DataFrame
df1=df[["学号","姓名","总分"]]
print(df1.head())

#删除列
del df1["学号"]
print(df1)

#更新列
df["数学"]=np.sqrt(df["数学"])*10
print(df.head())


