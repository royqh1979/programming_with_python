# 执行下面两行代码，会出错！
x=5
iterator=iter(x)


x=range(5)
iterator = iter(x)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))

