import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

s1=np.random.normal(0,1,1000)
s2=np.random.normal(3,1.5,1000)

fig, (ax0,ax1) = plt.subplots(1,2,sharey=True)
ax0.boxplot(s1)
ax1.boxplot(s2)
fig.suptitle("箱型图")
plt.show()