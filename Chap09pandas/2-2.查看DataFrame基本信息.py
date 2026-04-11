import numpy as np
import pandas as pd

df = pd.read_csv("学生成绩.csv",encoding="GBK")
print("== 显示整个数据帧 ==")
print(df)

print("== 显示前n行 ==")
print(df.head())

print("== 显示最后n行 ==")
print(df.tail())

print("== 显示整体描述性统计 ==")
print(df.describe())

print("== 字段名 ==")
print(df.columns)

print("== 数据条数 ==")
print(len(df))

print("== 索引 ==")
print(df.index)


