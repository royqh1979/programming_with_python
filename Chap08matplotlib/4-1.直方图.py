import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#数据准备
rng = np.random.default_rng()
datas = rng.normal(0,1,10000)
bins = np.linspace(-3,3,100)

#绘制图形
plt.hist(datas, bins)
plt.grid()
plt.show()