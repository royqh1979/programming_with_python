import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)
print(df)

df2 = pd.read_excel("学生成绩.xlsx",sheet_name="学生成绩",index_col=0)
print(df2)