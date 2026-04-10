import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

labels = ['会员数量','看单价','订单量','销售额','老客占比']
y = [5,3,1.5,4,2.5]
y1=np.append(y,y[0])
x = (np.linspace(0,2*np.pi, len(y1))+np.pi/2) % (2*np.pi)

fig = plt.figure()
ax = fig.add_subplot(projection="polar")
ax.plot(x,y1,marker="o")
ax.set_xticks(x[0:-1], labels)
#隐藏刻度标签
import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.NullFormatter())
plt.show()