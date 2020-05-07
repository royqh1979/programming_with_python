import math

from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from scipy.optimize import curve_fit

real_n = [64,166.8,362.9,685.3,1323,2386, 4330,
          8453,14522,20661,26869,33482,39342.8]

xi = np.array(real_n[:-1])
yi = np.array(real_n[1:])
n=yi-xi


##需要拟合的函数func :指定函数的形状
def func(x,a,b,c):
    return a+b*x+c*x*x

# 初始迭代值
# guess=(450,0.625,-0.0000143)
guess=(0,0,0)
params,parma_covariance = curve_fit(func,xi,n,guess)

print(params)
a,b,c=tuple(params)
print(a,b,c)

yy= func(xi,a,b,c)
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
