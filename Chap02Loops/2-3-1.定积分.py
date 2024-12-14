import math

def integration(f, a, b, step):
    '''
    对函数f(x)在区间[a,b]上关于x的定积分
    :param f: 待积函数
    :param a: 积分区间下限
    :param b: 积分区间上限
    :param step: 近似计算的步长，越小则计算精度越高
    :return: 定积分的值
    '''
    result = 0
    x = a
    while x < b:
        area = step * f(x)
        result += area
        x += step
    return result

result = integration(math.sin, 0, math.pi/2, 0.00001)

print(f"{result : 0.8f}")
