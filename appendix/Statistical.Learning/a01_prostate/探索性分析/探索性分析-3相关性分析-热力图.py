# 关掉所有警告信息
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# 设置以下属性，保证dataframe各列能全部输出
pd.set_option('display.width',400)
pd.set_option('display.max_column',20)
pd.set_option('display.max_colwidth',100)

# 设置sns样式
sns.set_style('whitegrid')


# 读取数据，数据项之间以"\t"分隔，第一列是索引列
df = pd.read_csv("../prostate.data",sep="\t",index_col=0)

print(df.head(10))

value_cols = ['lcavol','lweight','age','lbph','lcp','pgg45','lpsa']

# 计算协方差矩阵，绘制热力图

corr = df[value_cols].corr() # 计算协方差矩阵

sns.set(font_scale=1.25)
sns.heatmap(corr, annot= True, square=True, cmap=sns.cubehelix_palette(8),
    xticklabels = corr.columns.values,
    yticklabels = corr.columns.values)


plt.show()


