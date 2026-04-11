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

df.head()
print(df["性别"].describe())
print(df["性别"].value_counts())
df["性别"].value_counts().plot.pie()
plt.show()