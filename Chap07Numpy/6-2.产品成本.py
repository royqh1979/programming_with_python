import numpy as np
C=np.array([
    [0.1,0.3,0.15],
    [0.3,0.4,0.25],
    [0.3,0.2,0.15]
])
P=np.array([
    [4000,4500,4500,4000],
    [2000,2800,2400,2200],
    [5800,6200,6000,6000]
])
T=np.dot(C,P)
print("各季度分类成本:")
print(T)
print("按行计算总和（各分类全年成本总和）:")
print(T.sum(axis = 1))
print("按列计算总和（各季度总成本）:")
print(T.sum(axis = 0))
print("全年总成本:")
print(T.sum())
