#示例：使用NamedTuple定义不可变数据对象
from typing import NamedTuple

#注意本例中Vector类定义和“例2-2-1矢量”的区别
#这里Vector**继承**自NamedTuple类
class Vector(NamedTuple):
    x: float
    y: float

v1 = Vector(1,1)
print(v1)
v2 = v1
print(v2)
#这里会失败，因为用Vector类创建的对象是不可变对象
v1.x *= 2
v1.y *= 2

print(v1,v2)
print(v1 is v2)
