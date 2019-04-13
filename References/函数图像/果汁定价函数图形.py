"""
某商店卖两种品牌的果汁：
A品牌果汁每瓶进价1元，B品牌果汁每瓶进价1.2元。
店主估计，如果A品牌和B品牌果汁每瓶的卖价分别定为x和y，则他们每天的销量分别为70-5x+4y和80+6x-7y。
请问，店主每天应该以什么价格卖两种牌子的果汁，以获取最大收益？
"""
from matplotlib import use
use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def f(x,y):
    return (70-5*x+4*y)*(x-1)+(80+6*x-7*y)*(y-1.2)

fig = plt.figure()
ax = Axes3D(fig)
n = 256
x = np.arange(0,20,0.1)
y = np.arange(0,20,0.1)
X,Y = np.meshgrid(x,y)
Z=f(X,Y)
plt.xlabel('x')
plt.ylabel('y')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
ax.plot_wireframe(X, Y, Z, rcount=10,ccount=10,cmap=cm.coolwarm)
ax.contourf(X, Y, Z, offset = -0.8,cmap = cm.coolwarm)
plt.show()