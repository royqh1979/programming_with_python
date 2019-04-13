import numpy as np
A=np.array([
    [90,95,85,80],
    [95,100,85,80],
    [85,95,90,80],
    [80,85,90,95]
])
W=np.array([0.3,0.4,0.1,0.2])
T=np.dot(A.T,W)
print(T)
