import numpy as np

A = np.array([[36, 51, 13],
              [52, 34, 74],
              [10, 7, 1]])

b = np.array([37, 53, 9])

X = np.linalg.solve(A, b)

print(X)
print(np.dot(A, X))
