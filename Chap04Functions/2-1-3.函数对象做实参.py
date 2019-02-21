def fun1():
    print("this is fun1")

def fun2(f):
    print("this is fun2")
    f()

print("运行fun2:")
fun2(fun1)

