import numpy as np
import pandas as pd

#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif']="Simsun"
mpl.rcParams['axes.unicode_minus']=False

#读取数据
df = pd.read_csv("学生成绩.csv",encoding="GBK")

print(df.groupby("性别").mean(numeric_only=True))
print(df.groupby(["性别","出生年份"]).mean(numeric_only=True))