import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)
print(df.head())

#访问某列
print(df.loc[166241101])

print(df.loc[[166241101,166241103,166241107]])