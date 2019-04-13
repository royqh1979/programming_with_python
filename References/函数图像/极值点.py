from matplotlib import use
use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def f(x,y):
    return -1*x*y/np.exp(x**2+y**2)

fig = plt.figure()
ax = Axes3D(fig)
n = 256
x = np.linspace(-2,2,n)
y = np.linspace(-2,2,n)
X,Y = np.meshgrid(x,y)
Z=f(X,Y)
plt.xlabel('x')
plt.ylabel('y')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm)
ax.plot_wireframe(X, Y, Z, rcount=10,ccount=10)
ax.contourf(X, Y, Z, offset = -0.2,cmap = cm.coolwarm)
ax.contour(X, Y, Z, offset = -0.2,cmap = cm.gray)
plt.show()