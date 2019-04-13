import numpy as np


A = np.array([[-0.2,0.2,0.2],
              [0.2, -1, 0.2],
              [0, 0.8, -0.4],
              [1,1,1]])


b = np.array([0,0,0,1])

print(b)

print(np.linalg.matrix_rank(A))

X = np.linalg.lstsq(A, b,rcond=None)[0]



print(X)
print(np.dot(A, X))
