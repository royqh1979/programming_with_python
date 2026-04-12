import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#使用中文字体
from pylab import mpl
mpl.rcParams['font.sans-serif']="Simsun"
mpl.rcParams['axes.unicode_minus']=False

from pathlib import Path

corps = [
    # 科技（20）
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AVGO', 'ORCL', 'ADBE',
    'CRM', 'NFLX', 'AMD', 'INTC', 'CSCO', 'QCOM', 'TXN', 'IBM', 'UBER', 'ABNB',

    # 金融（20）
    'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'BLK', 'AXP', 'PNC', 'USB',
    'COF', 'TFC', 'SPGI', 'ICE', 'CME', 'MCO', 'BK', 'STT', 'SCHW', 'ALL',

    # 消费（20）
    'WMT', 'COST', 'HD', 'LOW', 'PG', 'KO', 'PEP', 'MCD', 'NKE', 'SBUX',
    'TGT', 'TJX', 'DG', 'EL', 'CL', 'KMB', 'GIS', 'K', 'CPB', 'HSY',

    # 医药（20）
    'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'LLY', 'TMO', 'ABT', 'DHR', 'BMY',
    'AMGN', 'GILD', 'VRTX', 'REGN', 'BIIB', 'ZTS', 'CVS', 'CI', 'HUM', 'ELV',

    # 工业能源（20）
    'XOM', 'CVX', 'COP', 'CAT', 'GE', 'BA', 'HON', 'UPS', 'RTX', 'LMT',
    'MMM', 'UNP', 'FDX', 'CSX', 'NSC', 'DE', 'ITW', 'EMR', 'ETN', 'SLB'
]

balance = pd.DataFrame()
income = pd.DataFrame()

for c in corps:
    balance_sheet_file_name = f"美股2025季度财报\\{c} balance sheet 2005-12.csv"
    balance_sheet_file = Path(balance_sheet_file_name)
    if not balance_sheet_file.is_file():
        print(f"‘{balance_sheet_file_name}’ not exists.")
        continue
    df = pd.read_csv(balance_sheet_file_name,index_col=0)
    balance[c]= df.iloc[:, 0]

balance=balance.T

for c in corps:
    income_file_name = f"美股2025季度财报\\{c} income 2005-12.csv"
    income_file = Path(income_file_name)
    if not income_file.is_file():
        print(f"‘{income_file_name}’ not exists.")
        continue
    df = pd.read_csv(income_file_name,index_col=0)
    income[c]=df.iloc[:,0]
income = income.T
print(balance)
print(income)

info = pd.read_csv("美股2025季度财报/info 2025-12.csv",index_col=0)
print(info)
financials = pd.DataFrame()
financials["ROE"] = income['Net Income'] / balance['Stockholders Equity']
financials["ROA"] = income['Net Income'] / balance['Total Assets']
financials["净利润率"] = income['Net Income'] / income['Total Revenue']
financials["流动比率"] = balance['Current Assets'] / balance['Current Liabilities']
financials["资产负债率"] = balance['Total Liabilities Net Minority Interest'] / balance['Total Assets']
financials["资产周转率"] = income['Total Revenue'] / balance['Total Liabilities Net Minority Interest']
financials["市盈率"] = info["marketCap"] / income['Net Income']

print(financials)
print(financials.describe())
print(financials["市盈率"].mean())
print(financials[financials["市盈率"] > np.mean(financials["市盈率"])])
