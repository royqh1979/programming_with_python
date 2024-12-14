import math

def sqrt(a,epsilon=0.0001):
    '''
    求a的平方根

    :param a:
    :param epsilon: 计算精度阈值，越小精度越高
    :return: a的平方根
    '''
    x=a # 迭代初始值
    while True:
        x1=1/2*(x+a/x) # 迭代计算
        if math.fabs(x1-x)<epsilon:
            break
        x=x1 # 更新x1以在下次循环中迭代计算
    return x

a=float(input("请输入a:"))
root = sqrt(a)
print(f"{a}的平方根是{root}")
