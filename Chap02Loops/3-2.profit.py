import random

def get_normal(mean,dev):
    """
    产生一个非负，服从指定正态分布的随机数

    :param mean: 正态分布的均值
    :param dev: 正态分布的标准差
    :return: 产生的随机数
    """
    if mean<=0 or dev<=0 :
        raise  ValueError("Mean and dev must be positive！")
    result = random.normalvariate(mean,dev)
    if result <=0:
        result = 0
    return result
#    return max(0,result)

random.seed()
cost = 200000
sale_mean, sale_dev = 30000,10000
price_mean, price_dev= 6,1
rate_mean, rate_dev = 0.1,0.02
n=500000 # 实验次数
count=0 # 亏损的实验次数
for i in range(n):
    sale = get_normal(sale_mean,sale_dev)
    price = get_normal(price_mean,price_dev)
    rate = get_normal(rate_mean,rate_dev)
    profit = sale * price / (1+rate) - cost
    if profit <= 0:
        count += 1

print(f"亏损的比例为{count/n *100: .2f}%")
