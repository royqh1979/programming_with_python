import pandas as pd
import numpy as np

stock = pd.read_csv("bank_stock.csv",
                 encoding="GBK",
                 index_col=0)
#转化为日期型索引
stock.index = pd.to_datetime(stock.index)

#按照时间索引重新排序
stock = stock.sort_index()

#移位：用收盘价计算对数收益率
stock["收益率"] = np.log(stock["收盘价"] / stock["收盘价"].shift(1))
print(stock["收益率"])
