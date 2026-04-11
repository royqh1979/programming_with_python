import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK")
print(df.head())

#筛选符合条件的数据
df1 = df[(df["数学"]<60) & (df["性别"]=="女")]
print(df1)

#筛选部分列组成新DataFrame
df2=df[["学号","姓名","数学"]]
print(df2.head())