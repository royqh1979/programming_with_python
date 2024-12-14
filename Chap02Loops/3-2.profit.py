import random

#sale/price/rate各用一个随机数发生器，以保证各自相互独立
g1=random.Random()
g2=random.Random()
g3=random.Random()

cost = 200000 # 项目初始成本
sale_mean, sale_dev = 30000,10000
price_mean, price_dev= 6,1
rate_mean, rate_dev = 0.1,0.02

n=500000 # 实验次数
count=0 # 亏损的实验次数
for i in range(n):
    sale = g1.normalvariate(sale_mean,sale_dev)
    price = g2.normalvariate(price_mean,price_dev)
    rate = g3.normalvariate(rate_mean,rate_dev)
    profit = sale * price / (1+rate) - cost #在计算利润时需要进行折现处理
    if profit <= 0:
        count += 1

print(f"亏损的比例为{count/n *100: .2f}%")
