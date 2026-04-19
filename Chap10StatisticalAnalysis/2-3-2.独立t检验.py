import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

s1=[4.4,5.1,5.2,6.1,3.9,4.2,4.3,
    4.6,5.2,4.1,4.3,3.5,3.9,4.4,
    5.7,4.3,6.4,4.4,3.0,5.0]
s2=[6.1,5.7,7.4,4.7,5.4,4.5,6.6,
    7.2,5.2,5.5,4.6,5.1,6.5,5.6,
    4.3,5.9,7.2,5.7]
print("单样本t检验")
print(stats.ttest_ind(s1,s2))
print(stats.ttest_ind(s1,s2,equal_var=False))

plt.boxplot([s1,s2])
plt.xticks([1,2],["健康人","冠心病人"])
plt.show()


