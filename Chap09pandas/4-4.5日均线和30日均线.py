import pandas as pd
import matplotlib.pyplot as plt

#使用中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif']="Simhei"
mpl.rcParams['axes.unicode_minus']=False

stock = pd.read_csv("bank_stock.csv",
                 encoding="GBK",
                 index_col=0)
#转化为日期型索引
stock.index = pd.to_datetime(stock.index)

stock = stock[stock["收盘价"]>0.1]

#按照时间索引重新排序
stock = stock.sort_index()

mean5 = stock["收盘价"].rolling(window=5).mean()
mean30 = stock["收盘价"].rolling(window=30).mean()

stock["收盘价"].plot(label="day")
mean5.plot(label="5day")
mean30.plot(label="30day")
plt.legend()
plt.show()