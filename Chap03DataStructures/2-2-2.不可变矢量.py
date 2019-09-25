#使用NamedTuple定义不可变数据对象
from typing import NamedTuple

class Vector(NamedTuple):
    x: float
    y: float

v1 = Vector(1,1)
print(v1)
v2 = v1
print(v2)
v1.x *= 2
v1.y *= 2

print(v1,v2)
print(v1 is v2)
