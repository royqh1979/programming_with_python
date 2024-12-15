#展示在python中如何复制对象
from copy import copy
from dataclasses import dataclass

@dataclass()
class Vector:
    x: float
    y: float

v1 = Vector(1,1)
print(v1)
#使用copy模块中的copy方法来复制对象
#注意程序开头的import语句
v2 = copy(v1)
print(v2)
print(v1 is v2)

v1.x *= 2
v1.y *= 2

print(v1,v2)
