import numpy as np
import pandas as pd

#读取数据
df = pd.read_csv("学生成绩.csv",encoding="GBK")

df.head()
print(df["性别"].unique())
print(df["性别"].describe())
print(df["性别"].value_counts())
