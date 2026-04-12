import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)
print(df.head())

#访问前三列
print(df.iloc[:,0:3])

#访问前三行
print(df.iloc[0:3,:])
