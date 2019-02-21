def fun1():
    print("----- fun1 --------")
    print(f"x={x} y={y}")
    print("局部变量：", locals())
    print("全局变量:", globals())

def fun2():
    print("----- fun2 --------")
    x="x222"
    y="y222"
    print(f"x={x} y={y}")
    print("局部变量：", locals())
    print("全局变量:", globals())

x="xxx"
y="yyy"
print("程序开始时")
print(f"x={x} y={y}")
print("主程序局部变量:",locals())
print("主程序全局变量:",globals())
fun1()
fun2()
print("程序结束时")
print("主程序局部变量:",locals())
print("主程序全局变量:",globals())


