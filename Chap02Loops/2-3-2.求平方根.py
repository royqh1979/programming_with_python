import easygraphics.dialog as gui
import math

# def sqrt(a, epsilon):
#     xk = a
#     k=0
#     while True:
#         # temp=xk # 保存上一次迭代时的x值(xk值）
#         # k+=1 # 进入一次新的迭代
#         # xk1=temp #
#         xk1 = xk
#         xk = (xk1+a/xk1)/2
#         if math.fabs(xk-xk1)<epsilon:
#             break
#     return xk


def sqrt(a,epsilon):
    xk=a # 在第一次迭代计算之前，xk就是x0，x0初值就是a
    while True:
        xk1=xk #上一次的x k，成了这一次迭代计算的x k-1
        xk=1/2*(xk1+a/xk1) # 用x k-1 去计算得到新的x k
        if math.fabs(xk-xk1)<epsilon:
            break
    return xk

# def sqrt(a,epsilon):
#     xk1=a # 在第一次迭代计算的时候，xk-1就是x0，x0初值就是a
#     while True:
#         xk=1/2*(xk1+a/xk1) # 用x k-1 去计算得到新的x k
#         if math.fabs(xk-xk1)<epsilon:
#             break
#         xk1 = xk  # 上一次的x k，成了这一次迭代计算的x k-1
#     return xk

ep=0.0001
a=float(gui.get_string("请输入a:"))
root = sqrt(a,ep)
gui.show_message(f"{a}的平方根是{root}")
