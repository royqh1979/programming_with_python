import random
import math

random.seed()
cx,cy=0,0 #圆心的坐标
r=0.5 # 内接圆半径
n=500000 #实验次数
count = 0 #落点在圆内的实验次数
for i in range(n):
    x=random.uniform(-0.5,0.5)
    y=random.uniform(-0.5,0.5)
    if math.hypot(x-cx,y-cy)<=r: # hypot用于计算math.sqrt((x-cx)**2+(y-cy)**2)
        count +=1

area = count / n
pi = area / r / r
print(f"pi = {pi : .4f}")
