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

plt.boxplot(df)
plt.xticks(np.arange(4)+1, list(df.columns))
plt.show()