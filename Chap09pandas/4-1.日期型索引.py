import pandas as pd
import numpy as np

stock = pd.read_csv("bank_stock.csv",
                 encoding="GBK",
                 index_col=0)
#转化为日期型索引
stock.index = pd.to_datetime(stock.index)

#计算年月日
stock["年"]=stock.index.year
stock["月"]=stock.index.month
stock["日"]=stock.index.day
print(stock)
#计算相差天数
diff = stock.index-pd.to_datetime("2001-01-01")
print(diff.days)

#按月统计
print(stock["收盘价"].resample("ME").mean())