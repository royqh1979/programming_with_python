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

#去掉含N/A的数据
stock = stock.dropna()
#计算月平均收益率
month_return = stock["收益率"].resample("ME").mean()
print(month_return)
#将索引从时间型转换为期间型
month_return.index = month_return.index.to_period('M')
print(month_return)