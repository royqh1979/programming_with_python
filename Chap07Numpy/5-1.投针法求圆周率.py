import numpy as np
from numpy import random
#用两个随机数发生器来保证x和y的独立性
g1 = random.default_rng()
g2 = random.default_rng()
n=10000000
r=0.5
cx,cy=0,0
x=g1.uniform(-0.5,0.5,n)
y=g2.uniform(-0.5,0.5,n)
in_circle = np.hypot(x-cx,y-cy)<= r

# # 得到是所有在圆内的点的横坐标
# x_in_circle = x[in_circle]
# # 得到是所有在圆内的点的纵坐标
# y_in_circle = y[in_circle]
# # 在圆内的点的个数
# count = len(x_in_circle)

# 在圆内的点的个数 （False 会被当成0， True会被当成1）
count = np.count_nonzero(in_circle)

area = count / n
pi = area / r / r
print(f"pi = {pi : .4f}")
