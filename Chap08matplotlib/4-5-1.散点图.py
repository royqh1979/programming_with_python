import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

x=np.linspace(0,3,100)
y=3*x+1+np.random.normal(0,1,100)

plt.plot(x,y, linestyle='', marker='.')
plt.show()