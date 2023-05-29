import math
def sqrt(a,epsilon):
    x1=a # 迭代初始值
    while True:
        x=1/2*(x1+a/x1) # 迭代计算
        if math.fabs(x-x1)<epsilon:
            break
        x1=x # 更新x1以在下次循环中迭代计算
    return x

ep=0.0001
a=float(input("请输入a:"))
root = sqrt(a,ep)
print(f"{a}的平方根是{root}")
