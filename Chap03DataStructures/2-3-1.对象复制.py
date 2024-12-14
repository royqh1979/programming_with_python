import copy
from dataclasses import dataclass

@dataclass()
class Vector:
    x: float
    y: float

v1 = Vector(1,1)
print(v1)
v2 = copy.copy(v1)
print(v2)
print(v1 is v2)

v1.x *= 2
v1.y *= 2

print(v1,v2)
