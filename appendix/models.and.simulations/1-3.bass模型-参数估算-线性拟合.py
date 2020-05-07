import math

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import leastsq

real_n = [64,166.8,362.9,685.3,1323,2386, 4330,
          8453,14522,20661,26869,33482,39342.8]

xi = np.array(real_n[:-1])
yi = np.array(real_n[1:])
n=yi-xi


##需要拟合的函数func :指定函数的形状
def func(p,x):
    a,b,c = p
    return a+b*x+c*x*x

##偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
def error(p,x,y):
    return y-func(p,x)

# 初始迭代值
#p0=(450,0.625,-0.0000143)
p0=(0,0,0)
params = leastsq(error,p0,args=(xi,n))

print(params)
a,b,c = params[0]
print(a,b,c)

yy= func((a,b,c),xi)
print(yy)
print(n)

q=(b+math.sqrt(b*b-4*a*c))/2
m=-q/c
p=q-b
print(f"q,m,p={q,m,p}")
print(p*m,-p+q,-q/m)

q=(b-math.sqrt(b*b-4*a*c))/2
m=-q/c
p=q-b
print(f"q,m,p={q,m,p}")
print(p*m,-p+q,-q/m)
