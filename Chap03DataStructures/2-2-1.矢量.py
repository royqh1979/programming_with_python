#示例：使用自定义的Vector类，展示python中变量只是引用的实质
from dataclasses import dataclass

@dataclass()
class Vector:
    x: float
    y: float

v1 = Vector(1,1)
print(v1)
#注意：这里是赋值给一个变量
v2 = v1
print(v2)
#这里是赋值给变量所指的对象的属性（赋值后变量依然指向原来的对象）
v1.x *= 2
v1.y *= 2

print(v1,v2)
print(v1 is v2)
