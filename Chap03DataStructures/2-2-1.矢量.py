class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

v1 = Vector(1,1)
print(v1)
v2 = v1
print(v2)
v1.x *= 2
v1.y *= 2

print(v1,v2)
print(v1 is v2)
