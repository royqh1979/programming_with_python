import operator as op
import math
from fractions import Fraction

def double(n):
    return 2*n

# function in operator package
n=op.add(3,5)
print(n)
n=op.add("张三","你好")
print(n)
n=op.sub(3,5)
print(n)
n=op.mul(3,5)
print(n)
n=op.gt(3,5)
print(n)


print('------------- Map --------------')
lst_a = list(range(10))
lst_b = list(map(double,lst_a))

print(lst_a)
print(lst_b)

#数学函数
lst_d = map(math.sin,lst_a)
print(list(lst_d))


lst_c = map(op.add,lst_a,lst_b)
print(lst_c)

# map返回的迭代器对象只能迭代一次
print("iteraction 1:")
for elem in lst_c:
    print(elem, end=" ")
print()
print("iteraction 2:")
for elem in lst_c:
    print(elem, end=" ")
print()

lst_c = map(op.mul,lst_a,lst_b)
print(list(lst_c))

lst_b = [10]*10

# 类的方法，包括构造方法，也可以用于map
lst_c = list(map(Fraction,lst_a,lst_b))
print(lst_c)

f = Fraction(1,2)
lst_d = map(f.__add__,lst_c)
print(list(lst_d))








