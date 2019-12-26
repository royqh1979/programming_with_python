import numpy as np

# a = np.array([[1,  0],
#                [1,  1],
#                [0,  1]], dtype=bool)
# b = np.array([[1,  1,  0],
#                [0,  1,  1]], dtype=bool)

a = np.array([[True,  False],
               [True,  True],
               [False,  True]], dtype=bool)
b = np.array([[True,  True,  False],
               [False,  True,  True]], dtype=bool)

print(a)

print(b)

print(np.dot(a,b))