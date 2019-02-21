import math

def calc_triangle_area(a,b,c):
    """
    使用海伦公式计算三角形面积
    a、b、c为三角形边长
    :return: 三角形面积
    """
    p=(a+b+c)/2
    return math.sqrt(p*(p-a)*(p-b)*(p-c))


area=calc_triangle_area(3,4,5)
print(f"面积等于{area}")