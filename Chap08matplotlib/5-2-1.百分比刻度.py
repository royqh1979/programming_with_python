import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

#数据准备
data = [31.6, 39.6, 42.1, 46.6, 45.2]
x = np.arange(len(data))
#绘图
import matplotlib.ticker as mtick
fig, ax = plt.subplots()
ax.plot(x, data , color='orange', marker='o')
#y轴使用百分比刻度，参数100为计算百分比的分母
ax.yaxis.set_major_formatter(mtick.PercentFormatter(100))
plt.show()