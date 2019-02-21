def fun1():
    def fun2():
        print("this if fun2")
    return fun2

print("运行fun1并将返回值赋给x：")
x=fun1()
print("运行x所指的函数对象：")
x()


