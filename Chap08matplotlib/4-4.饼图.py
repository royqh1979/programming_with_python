import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

years=[2000,2001,2002,2003,2004,2005,2006]
numbers =  [35,67,43,92,21,100,77]

colors = plt.get_cmap('Spectral')(np.linspace(0.2,0.8,len(years)))
plt.figure(figsize=[5,3])
wedges, texts= plt.pie(numbers, labels = numbers,
        colors=colors, labeldistance=0.7,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        frame=False,
        textprops={"color":"darkgreen"},)
plt.legend(wedges,years,loc="upper right",bbox_to_anchor=(1, 0, 0.5, 1))
plt.show()