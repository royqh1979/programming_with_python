import random
import math

#x和y各用一个随机数发生器，以保证x和y相互独立
g1 = random.Random()
g2 = random.Random()

n=500000 #实验次数
count = 0 #落点在圆内的实验次数
for i in range(n):
    #一次实验
    x=g1.uniform(-1,1)
    y=g2.uniform(-1,1)
    if math.sqrt(x*x+y*y)<=1:
        count +=1

pi = 4 * count / n
print(f"pi = {pi : .4f}")
