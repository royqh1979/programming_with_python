# 关掉所有警告信息
import warnings
warnings.filterwarnings('ignore')

import pandas as pd

# 设置以下属性，保证dataframe各列能全部输出
pd.set_option('display.width',400)
pd.set_option('display.max_column',20)
pd.set_option('display.max_colwidth',100)


# 读取数据，数据项之间以"\t"分隔，第一列是索引列
df = pd.read_csv("../prostate.data",sep="\t",index_col=0)

print(df.head(10))

value_cols = ['lcavol','lweight','age','lbph','lcp','pgg45','lpsa']
unordered_tag_cols = ['svi']
ordered_cols = ['gleason']
tag_cols = unordered_tag_cols + ordered_cols


print("== 各数值属性的整体描述 ==")

desc = df[value_cols].describe().transpose()
desc['median'] = df.median()
desc['skew'] = df.skew()
desc['kurt'] = df.kurt()

print(desc)

print(" == 标签属性的整体描述 ==")


for col_name in tag_cols:
    print(f"-- 属性 {col_name}:")
    print(f"取值内容 {df[col_name].unique()}")
    print(df[col_name].value_counts())



