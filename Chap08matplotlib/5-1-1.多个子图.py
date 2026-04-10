import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#数据准备
x = np.linspace(0, 2*np.pi, 100)
y = np.cos(x)
y2 = np.sin(x)

#绘图
fig, (ax0,ax1) = plt.subplots(2,1,sharex=True);
ax0.plot(x,y,color='green',linestyle='', marker='+', label='余弦曲线')
ax0.legend()
ax1.plot(x,y2,color='red',linestyle='-', marker='.',label='正弦曲线')
ax1.legend()
fig.suptitle("正弦和余弦图像")
plt.show()