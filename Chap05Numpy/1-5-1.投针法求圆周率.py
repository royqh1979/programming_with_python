import numpy as np
from numpy import random

random.seed()
n=10000000
r=0.5
cx,cy=0,0
x=random.uniform(-0.5,0.5,n)
y=random.uniform(-0.5,0.5,n)
in_circle = np.hypot(x-cx,y-cy)<= r
# x_in_circle = x[in_circle]
# count = len(x_in_circle)
count = np.count_nonzero(in_circle)

area = count / n
pi = area / r / r
print(f"pi = {pi : .4f}")
