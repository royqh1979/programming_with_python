from decimal import Decimal
import csv
from datetime import date
from dataclasses import dataclass

"""
股票代码 Symbol
名称	Name
收盘价  Close Price	
最高价	High Price
最低价	Low Price
开盘价	Open Price
前收盘	Last Price 
涨跌额	Change
涨跌幅	Change Rate
换手率	Turnover
成交量	Volume
成交金额	Amount 
总市值	Market Cap(italization)
流通市值 Tradable Market Cap
"""

@dataclass()
class Stock:
    pdate: date
    pclose: Decimal
    high: Decimal
    low: Decimal
    popen: Decimal
    last_price: Decimal
    change: Decimal
    change_percent: Decimal
    turnover_rate: Decimal
    volume: int
    amount: Decimal
    cap: Decimal
    tradable_cap: Decimal

def read_csv(filename):
    """
    从csv文件中读入股票信息

    :param filename: csv文件名
    :return: 股票信息列表
    """
    stocks = []
    with open(filename,mode="r",encoding="GBK") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pdate = date.fromisoformat(row[0])
            pclose = Decimal(row[3])
            high = Decimal(row[4])
            low = Decimal(row[5])
            popen = Decimal(row[6])
            last_price = Decimal(row[7])
            change = Decimal(row[8])
            change_percent = Decimal(row[9])
            turnover_rate = Decimal(row[10])
            volume = int(row[11])
            amount = Decimal(row[12])
            cap = Decimal(row[13])
            tradable_cap = Decimal(row[14])
            stock = Stock(pdate,pclose,high,low,popen,last_price,change,change_percent,turnover_rate,
                          volume,amount,cap,tradable_cap)
            stocks.append(stock)
    return stocks


def filter_by_year(stocks,year):
    """
    筛选出指定年份的股票信息

    :param stocks: 股票信息列表
    :param year: 年份
    :return: 指定年份的股票信息列表
    """
    result = []
    for s in stocks:
        if s.pdate.year == year:
            result.append(s)
    return result


props = 'pdate,pclose,high,low,popen,last_price,change,change_percent,turnover_rate,volume,amount,cap,tradable_cap'.split(',')
prop_names = '日期,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,涨跌幅,换手率,成交量,成交金额,总市值,流通市值'.split(',')

filename = "4-4.浦发银行.csv"

stocks = read_csv(filename)
print(stocks)
filtered = filter_by_year(stocks, 2014)
print("------ 筛选结果 ------")
for s in filtered:
    print(s)
print("--------------------")
