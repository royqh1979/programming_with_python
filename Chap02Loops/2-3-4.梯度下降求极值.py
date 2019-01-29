import math
import random

random.seed()
# random.unifrom(a,b)产生一个[a,b]区间上服从均匀分布的随机浮点数
x0=random.uniform(-10,10)
y0=random.uniform(-10,10)

ep = 0.00000001
xk,yk = x0, y0
zk = xk ** 2 + yk ** 2
t = 0.001
while True:
    xk1,yk1 = xk,yk
    zk1 = zk
    grad_x,grad_y = 2*xk1,2*yk1
    xk=xk1-t*grad_x
    yk=yk1-t*grad_y
    zk = xk ** 2 + yk ** 2
    # print(f"f({xk :.8f},{yk :.8f})={zk :.8f}")
    if math.fabs(zk - zk1) < ep:
        break
print(f"f({xk :.8f},{yk :.8f})={zk :.8f}")
