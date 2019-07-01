# 关掉所有警告信息
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

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
    ax=plt.subplot(rows,cols,n)
    sm.qqplot(df[col_name],line='q',ax=ax)
    n+=1

# 去除多余的图形
while n<=rows*cols:
    axes.flat[n-1].set_visible(False)
    n+=1
fig.tight_layout()
plt.show()

