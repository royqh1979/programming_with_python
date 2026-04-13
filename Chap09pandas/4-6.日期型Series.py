import pandas as pd

df = pd.read_csv("tmall_order.csv",
                 encoding="GBK",index_col=0)

print(df.columns)
df["订单创建时间"] = pd.to_datetime(df["订单创建时间"])
df["订单付款时间"] = pd.to_datetime(df["订单付款时间"])
# 计算年月日
df["年"] = df["订单创建时间"].dt.year
# 计算时间差
df["付款时长"] = df["订单付款时间"]-df["订单创建时间"]
print(df["付款时长"].dt.seconds)
