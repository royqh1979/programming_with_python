import random
import math

random.seed()
cx,cy=0,0
r=0.5
n=500000
count = 0
for i in range(n):
    x=random.uniform(-0.5,0.5)
    y=random.uniform(-0.5,0.5)
    if math.hypot(x-cx,y-cy)<=r:
        count +=1

area = count / n
pi = area / r / r
print(f"pi = {pi : .4f}")
