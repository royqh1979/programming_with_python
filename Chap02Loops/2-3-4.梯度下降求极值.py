import math
import random

# 用固定的数（比如0）做种子，可以保证每次运行时产生的随机数列完全相同
# random.seed(0)

# random.unifrom(a,b)产生一个[a,b]区间上服从均匀分布的随机浮点数
x0=random.uniform(-10,10)
y0=random.uniform(-10,10)

ep = 0.00000001
xk,yk = x0, y0
zk = xk ** 2 + yk ** 2
t = 0.001
while True:
    grad_x,grad_y = 2*xk,2*yk
    xk1=xk-t*grad_x
    yk1=yk-t*grad_y
    zk1 = xk1 ** 2 + yk1 ** 2
    # print(f"f({xk :.8f},{yk :.8f})={zk :.8f}")
    if math.fabs(zk - zk1) < ep:
        break
    xk, yk = xk1, yk1
    zk = zk1
print(f"f({xk :.8f},{yk :.8f})={zk :.8f}")
