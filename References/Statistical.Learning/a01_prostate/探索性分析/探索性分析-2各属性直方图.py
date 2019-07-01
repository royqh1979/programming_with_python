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

# 绘制各数值属性的直方图
rows = (len(value_cols)-1) // 3 +1
cols = 3
fig,axes = plt.subplots(rows,cols)
#plt.subplots_adjust(wspace =0.3, hspace =0.4)
n=1
for col_name in value_cols:
    plt.subplot(rows,cols,n)
    sns.distplot(df[col_name])
    n+=1

# 去除多余的图形
while n<=rows*cols:
    axes.flat[n-1].set_visible(False)
    n+=1
fig.tight_layout()
plt.show()

