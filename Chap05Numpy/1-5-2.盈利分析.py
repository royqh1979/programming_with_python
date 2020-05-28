from numpy import random
import numpy as np

def get_normal(mean,dev,n):
    """
    产生n个非负，服从指定正态分布的随机数

    :param mean: 正态分布的均值
    :param dev: 正态分布的标准差
    :return: 产生的随机数数组
    """
    if mean<=0 or dev<=0 :
        raise  ValueError("Mean and dev must be positive！")
    result = random.normal(mean,dev,n)
    return np.where(result>0,result,0)

random.seed()
cost = 200000
sale_mean, sale_dev = 30000,10000
price_mean, price_dev= 6,1
rate_mean, rate_dev = 0.1,0.02
n=5000000
sale = get_normal(sale_mean,sale_dev,n)
price = get_normal(price_mean,price_dev,n)
rate = get_normal(rate_mean,rate_dev,n)
profit = sale * price / (1+rate) - cost
# count = len(profit[profit<=0])
count = np.count_nonzero(profit<=0)
print(f"亏损的比例为{count/n *100: .2f}%")
