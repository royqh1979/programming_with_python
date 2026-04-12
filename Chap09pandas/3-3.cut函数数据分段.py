import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)
print(df.head())

#生成成绩列
average = (df["数学"]+df["语文"]+df["英语"])/3
df["成绩"]=pd.cut(average,[0,60,80,90,100],labels=["不及格","及格","良好","优秀"])
print(df)
print(df["成绩"].value_counts())
