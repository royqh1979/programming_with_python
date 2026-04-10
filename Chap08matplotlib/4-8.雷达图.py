import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

labels = ['会员数量','看单价','订单量','销售额','老客占比']
y1 = [5,3,1.5,4,2.5]
y2 = [4.5,2.1,3,4,3]
#尾部增加一个点使图形封闭
y1=np.append(y1,y1[0])
y2=np.append(y2,y2[0])
# 加pi/2使图像逆时针旋转90度
# 对2pi求余，以保证x值能落在0-360度范围内
x = (np.linspace(0,2*np.pi, len(y1))+np.pi/2) % (2*np.pi)

#创建极坐标
fig = plt.figure()
ax = fig.add_subplot(projection="polar")
ax.plot(x,y1,marker="o")
ax.plot(x,y2,marker="o")
ax.set_xticks(x[0:-1], labels, fontsize=13)
plt.show()