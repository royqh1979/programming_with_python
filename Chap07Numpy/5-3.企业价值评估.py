import numpy as np

values = np.loadtxt("77家美股上市公司25年4季度数据.csv", delimiter=",", encoding="GBK", skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10))
names = np.loadtxt("77家美股上市公司25年4季度数据.csv", delimiter=",", encoding="GBK", skiprows=1, usecols=(0), dtype=str)

# 提取列方便计算（提高可读性）
revenue = values[:, 0]
net_income = values[:, 1]
market_cap = values[:, 9]

#计算指标
net_margin = net_income / revenue
pe_ratio = np.where(net_income > 0, market_cap / net_income, np.nan)

#筛选
filtered_names = names[net_margin>0.2]
filtered_pe_ratio = pe_ratio[net_margin>0.2]

#排序
order = np.argsort(filtered_pe_ratio)[::-1]

for n,r in zip(filtered_names[order],filtered_pe_ratio[order]):
    print(n,r)