import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

x=np.linspace(0,3,100)
y=3*x+1+np.random.normal(0,1,100)
colors = np.random.randint(0,50,100)
sizes = np.random.uniform(1,5,100)*30

plt.scatter(x,y, c=colors, s=sizes, cmap='hsv')
plt.show()