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

unordered_tag_cols = ['svi']
ordered_cols = ['gleason']
tag_cols = unordered_tag_cols + ordered_cols

output_col = 'lpsa'


# 绘制箱型图
fig, axes = plt.subplots(len(tag_cols),1)
n=1
for col_name in tag_cols:
    plt.subplot(len(tag_cols),1,n)
    data = df[[col_name,output_col]]
    sns.boxplot(x=col_name, y=output_col, data=data)
    n+=1
fig.tight_layout()
plt.show()

