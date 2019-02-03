import math

from easygraphics import *

init_graph(800,600)
#将0,0从屏幕左上角移动到屏幕正中
translate(400,300)
#翻转y轴方向使其朝上
set_flip_y(True)
set_render_mode(RenderMode.RENDER_MANUAL)
set_background_color("black")
set_color("white")
lst_x = []
lst_y = []

center_x,center_y=0,0
radius = 290
n=100
step = math.pi * 2 / n
for i in range(n):
    angle = i * step
    x = center_x+radius * math.cos(angle)
    y = center_y+radius * math.sin(angle)
    lst_x.append(x)
    lst_y.append(y)

for i in range(n):
    j=(i+30) % 100
    x1=lst_x[i]
    y1=lst_y[i]
    x2=lst_x[j]
    y2=lst_y[j]
    line(x1,y1,x2,y2)
    delay(100)

pause()
close_graph()





