from easygraphics.turtle import *

def inner_triangle(size,level):
    """
    绘制内接递归三角形
    :param size: 三角形边长
    :param level:  内接三角形个数
    """
    if level == 0 :
        return
    fd(size/2)  # 绘制线段ad
    rt(60)  # 设定内接三角形起始朝向
    inner_triangle(size/2,level-1) # 绘制内接三角形
    lt(60) # 恢复海龟原有朝向
    fd(size/2)  # 绘制线段db
    rt(120)
    fd(size)  # 绘制线段bc
    rt(120)
    fd(size)  # 绘制线段ca
    rt(120)  # 恢复海龟最初朝向

create_world(800,600)
set_speed(100)
setxy(-200,-200)
inner_triangle(400,10)
pause()
close_world()


