import numpy as np
#导入pyplot模块
import matplotlib.pyplot as plt

#使用中文字体
import matplotlib as mpl
mpl.rcParams['font.family']=['Microsoft Yahei', 'sans-serif']
mpl.rcParams['axes.unicode_minus']=False

from sklearn import datasets
import pandas as pd

iris_data=datasets.load_iris()
df = pd.DataFrame(data=iris_data.data,
                  columns=iris_data.feature_names)
print(df)

ncol=len(df.columns)
fig,axes = plt.subplots(nrows=ncol,ncols=ncol,layout="constrained",figsize=[7,7])
for i in range(ncol):
    for j in range(ncol):
        iname = df.columns[i]
        jname = df.columns[j]
        #绘制列名
        if i==0:
            axes[i,j].set_title(jname)
        #绘制行名
        if j==0:
            axes[i,j].set_ylabel(iname)
        if (i==j):
            continue
        x=df[iname]
        y=df[jname]
        axes[i,j].plot(x,y,linestyle='',marker='.')
plt.show()