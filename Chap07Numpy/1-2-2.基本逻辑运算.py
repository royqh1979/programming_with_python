import numpy as np

a = np.array([True,False,True,False])
b = np.array([True,True,False,False])

print(a)
print(b)
print(~ a)
print(a | b)
print(a & b)
print(True & a)
print(a | True)