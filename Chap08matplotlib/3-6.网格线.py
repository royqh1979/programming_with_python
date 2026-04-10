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
plt.plot(x,y,color='green', label='余弦曲线')
plt.plot(x,y2,color='red', label='正弦曲线')
plt.title("正弦和余弦图像")
plt.legend()
plt.grid()
plt.show()