import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

# example data
years=[2000,2001,2002,2003,2004,2005,2006]
numbers =  [21,35,43,67,92,100,77]

plt.step(years,numbers)
plt.show()