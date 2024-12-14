import math

def f(x):
    return 2 * x ** 3 - 4 * x ** 2 + 3 * x - 6

def f_derivative(x):
    return 6 * x ** 2 - 8 * x + 3

ep = 0.00000001
x = 1.5 # 迭代初始值
while True:
    x1 = x - f(x) / f_derivative(x) # 迭代计算
    if math.fabs(x1 - x) < ep:
        break
    x = x1 # 更新以进行下次迭代计算
print(x)
