import operator as op
from fractions import Fraction
from functools import reduce

lst_a = list(range(1,11))
lst_b = ['张三','李四','王五']
print(lst_a)
print(lst_b)

a=reduce(op.add,lst_a,0)
b=reduce(op.add,lst_b,'')

print(a)
print(b)

a=sum(lst_a)
print(a)
# b=sum(lst_b)
# print(b)

lst_a = [1,2,3,4,5]
a=reduce(op.mul,lst_a,1)
print(a)


lst_a=['张三','李四','王五','张三','王五','王五','张三','李四']

def add_to_set(name_set,name):
    name_set.add(name)
    return name_set

name_set=reduce(add_to_set,lst_a,set())
print(name_set)

def count(name_map,name):
    n=name_map.get(name,0)
    name_map[name]=n+1
    return name_map

name_map = reduce(count,lst_a,{})
print(name_map)


