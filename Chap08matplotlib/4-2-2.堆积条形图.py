import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#数据准备
colleges=['文学院','生物学院','信息学院','园林学院','水保学院','经管学院','机械学院']
numbers1 =  [35,67,43,92,21,100,77]
numbers2 =  [51,69,32,96,37,87,81]
x=np.arange(len(colleges))

#绘图
rects = plt.bar(x,numbers1,0.35,color='lightgreen',label='男')
plt.bar_label(rects)
rects = plt.bar(x,numbers2,0.35,color='darkgreen',label='女',bottom=numbers1)
plt.bar_label(rects)
plt.xticks(x,colleges)
plt.legend(loc='upper left')
plt.show()