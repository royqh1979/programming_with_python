import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

# example data
x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)
error = 0.1

plt.errorbar(x,y,error,marker='o',linestyle='-')
plt.show()