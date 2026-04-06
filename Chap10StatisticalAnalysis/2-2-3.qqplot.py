import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#产生实验数据，s1服从均匀分布，s2服从正态分布
s1=np.random.uniform(0,100,1000)
s2=np.random.normal(0,1,1000)

fig1=sm.qqplot(s1,line="45")
fig1.suptitle("s1的qq图")
fig2=sm.qqplot(s2,line="45")
fig2.suptitle("s2的qq图")
plt.show()