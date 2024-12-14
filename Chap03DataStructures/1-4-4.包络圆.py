import math
import turtle as t

#计算各原周等分店位置
lst_x = []
lst_y = []

center_x,center_y=0,0
radius = 290
n=100
m=30
step = math.pi * 2 / n
for i in range(n):
    angle = i * step
    x = center_x+radius * math.cos(angle)
    y = center_y+radius * math.sin(angle)
    lst_x.append(x)
    lst_y.append(y)

t.speed(0)
t.hideturtle()
for i in range(n):
    j=(i+m) % n
    x1=lst_x[i]
    y1=lst_y[i]
    x2=lst_x[j]
    y2=lst_y[j]
    t.penup()
    t.goto(x1,y1)
    t.pendown()
    t.goto(x2,y2)

t.mainloop()
