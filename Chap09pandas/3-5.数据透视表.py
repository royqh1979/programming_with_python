import pandas as pd

df = pd.read_csv("某公司2025年1月份销售数据.csv",encoding="GBK",index_col=0)
df["金额"]=df["单价"]*df["数量"]
print(df)

pt=pd.pivot_table(df,values="金额",index="地区",columns="商品类别",aggfunc="sum")
print(pt)

