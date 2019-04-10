import math

def f(x):
    return 2 * x ** 3 - 4 * x ** 2 + 3 * x - 6

def f_derivative(x):
    return 6 * x ** 2 - 8 * x + 3

ep = 0.00000001
xk = 1.5
k=0
while True:
    temp = xk
    k+=1
    xk1 = temp
    xk = xk1 - f(xk1) / f_derivative(xk1)
    print(xk1, xk)
    if math.fabs(xk - xk1) < ep:
        break
print(xk)
