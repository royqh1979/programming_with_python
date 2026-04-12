import pandas as pd

df = pd.read_csv("bank_stock.csv",
                 encoding="GBK")
#转化为日期型
df["日期"] = pd.to_datetime(df["日期"])
print(df["日期"])
#计算年月日
df["年"]=df["日期"].dt.year
df["月"]=df["日期"].dt.month
df["日"]=df["日期"].dt.day
print(df)
#计算相差天数
diff = df["日期"]-pd.to_datetime("2001-01-01")
print(diff.dt.days)

#按月统计
print(df["收盘价"].resample("ME").mean())