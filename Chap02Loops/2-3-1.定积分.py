import math

def integration(f, a, b, step):
    result = 0
    x = a
    while x < b:
        area = step * f(x)
        result += area
        x += step
    return result

result = integration(math.sin, 0, math.pi/2, 0.00001)

print(f"{result : 0.8f}")
