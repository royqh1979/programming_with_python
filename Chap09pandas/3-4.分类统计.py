import numpy as np
import pandas as pd

#读取数据
df = pd.read_csv("学生成绩.csv",encoding="GBK",index_col=0)

print(df.groupby("性别").mean(numeric_only=True))
print(df.groupby(["性别","出生年份"]).mean(numeric_only=True))