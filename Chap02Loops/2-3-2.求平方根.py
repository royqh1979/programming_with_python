import easygraphics.dialog as gui
import math

def sqrt(a, epsilon):
    k=0
    xk = a
    while True:
        k+=1
        xk1 =xk
        xk = (xk1+a/xk1)/2
        if math.fabs(xk-xk1)<epsilon:
            break
    root=xk
    return xk


ep=0.0001
a=float(gui.get_string("请输入a:"))
root = sqrt(a,ep)
gui.show_message(f"{a}的平方根是{root}")
