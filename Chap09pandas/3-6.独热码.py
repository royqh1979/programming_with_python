import numpy as np
import pandas as pd

#读取数据
df = pd.read_csv("某公司2025年1月份销售数据.csv",encoding="GBK",index_col=0)
df1 = pd.concat([df, pd.get_dummies(df["商品类别"])],axis=1)
print(df1)
