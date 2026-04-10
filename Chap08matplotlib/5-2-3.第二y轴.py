import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
import pandas as pd

mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

df = pd.DataFrame(data={
    'date' : ['2022年6月','2022年12月','2023年6月','2023年12月','2024年6月'],
    'users' : [33250,42272,45363,50901,49721],
    'usage' : [0.316, 0.396, 0.421, 0.466, 0.452],
})
print(df)

import matplotlib.ticker as mtick

fig, ax = plt.subplots()
rects = ax.bar(df.index, df['users'], width=0.5, label="用户规模（万人）")
ax.bar_label(rects)
ax.set_yticks(np.linspace(0,60000,4))
ax.set_xticks(df.index, df["date"])

#建立第二y轴
ax1 = ax.twinx()
ax1.plot(df.index, df['usage'], color='orange', marker='o',label="使用率")
ax1.set_yticks(np.linspace(0,0.5,6))
#第二y轴使用%刻度
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1))
#绘制各数据点的数值标签
for i in df.index:
    ax1.annotate(f"{df['usage'][i]*100:.1f}%",xy=(i, df['usage'][i]))

fig.suptitle("在线旅行用户规模及使用率")
fig.legend()
plt.show()