import pandas as pd

df = pd.read_csv("bank_stock.csv",
                 encoding="GBK",
                 index_col=0)
#转化为日期型索引
df.index = pd.to_datetime(df.index)

#计算年月日
df["年"]=df.index.year
df["月"]=df.index.month
df["日"]=df.index.day
print(df)
#计算相差天数
diff = df.index-pd.to_datetime("2001-01-01")
print(diff.days)
#按月统计
print(df["收盘价"].resample("ME").mean())