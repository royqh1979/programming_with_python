import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

df = pd.read_csv("矽肺治疗数据.csv",encoding="GBK",index_col="患者编号")
print(stats.ttest_rel(df["治疗前"],df["治疗后"], alternative="less"))

df.plot.box()
plt.xticks([1,2],df.columns)

fig2=plt.figure()
df["差值"]=df["治疗后"]-df["治疗前"]
df["差值"].plot.box()
plt.show()



