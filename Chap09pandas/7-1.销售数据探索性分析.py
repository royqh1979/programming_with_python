import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("某公司2025年1月份销售数据.csv",encoding="GBK")
print("="*60)
print("第一步：数据概览（Data Overview）")
print("="*60)
print(f"数据形状: {df.shape}")
print("\n前5行:")
print(df.head())
print("\n数据类型:")
print(df.dtypes)
print("\n基本信息:")
print(df.info())

print("\n" + "="*60)
print("第二步：数据清洗（Data Cleaning）")
print("="*60)

# 检查缺失值
print("缺失值统计:")
print(df.isnull().sum())

# 处理缺失值：用商品类别的中位数填充
df['单价'] = df.groupby('商品类别')['单价'].transform(
    lambda x: x.fillna(x.median())
)

# 检查异常值（数量为负）
print(f"\n异常值检查（数量<0或客户ID为空）: {np.sum((df['数量'] < 0) | df['客户ID'].isnull())}条")
df = df[(df['数量'] > 0) & (~df['客户ID'].isnull())]  # 删除异常值
print(f"清洗后数据形状: {df.shape}")

#将日期类从字符串类型转换为日期类型
df['日期']=pd.to_datetime(df['日期'])
# 创建新特征
df['金额'] = df['单价'] * df['数量']
df['月份'] = df['日期'].dt.month
df['星期'] = df['日期'].dt.day_name()

print("\n" + "="*60)
print("第三步：描述性统计（Descriptive Statistics）")
print("="*60)

# 数值型变量统计
print("数值型变量统计:")
print(df[['单价', '数量', '金额']].describe())

# 类别型变量统计
print("\n商品类别分布:")
print(df['商品类别'].value_counts())

print("\n地区分布:")
print(df['地区'].value_counts(normalize=True).apply(lambda x: f"{x:.1%}"))

# 分组统计：按商品类别
print("\n按商品类别分组统计:")
category_stats = df.groupby('商品类别')['金额'].agg(['count', 'mean', 'sum', 'std'])
print(category_stats.round(2))

print("\n" + "="*60)
print("第四步：数据探索（Data Exploration）")
print("="*60)

# 1. 时间趋势分析
monthly_sales = df.groupby('月份')['金额'].sum()
print("\n月度销售额趋势:")
print(monthly_sales.round(2))

# 2. 地区-类别交叉分析
cross_tab = pd.pivot_table(df, values='金额', index='地区',
                          columns='商品类别', aggfunc='sum', fill_value=0)
print("\n地区×商品类别销售额交叉表:")
print(cross_tab.round(0))

# 3. 客户价值分析（RFM思想）
customer_value = df.groupby('客户ID').agg({
    '日期': 'max',           # 最近购买
    '订单ID': 'count',       # 频次
    '金额': 'sum'            # 金额
}).rename(columns={'订单ID': '购买频次', '金额': '总金额'})

print("\nTOP 10高价值客户:")
print(customer_value.sort_values('总金额', ascending=False).head(10))