import random
import math
import turtle as t

font=('Arial',12,'normal')

g1=random.Random()
g2=random.Random()

r=1
n=50000
count = 0

#用独立的海龟来绘制文字
textturtle = t.Turtle()
textturtle.penup()
textturtle.hideturtle()

t.speed(0) #关闭动画
#绘制内接圆
t.penup()
t.goto(x=0,y=-270)
t.pendown()
t.circle(270)
#绘制外接正方形
t.forward(270)
for i in range(3):
    t.left(90)
    t.fd(540)
t.left(90)
t.forward(270)
t.penup()
t.hideturtle()

for i in range(n):
    x=g1.uniform(-1,1)
    y=g2.uniform(-1,1)
    if math.sqrt(x*x+y*y)<=r:
        count +=1
    if i<30:
        textturtle.goto(-350, -300)
        textturtle.clear()
        textturtle.write(f"shoot={i + 1},count = {count}",font=font)
        t.goto(x * 270, y * 270)
        t.dot(6,"red")
        if i<10:
            t.delay(5)
        else:
            t.delay(1)
    elif i==50:
        t.tracer(10)
        textturtle.clear()
        textturtle.goto(-350, -300)
        textturtle.write("Calculating...", font=font)
    elif i==1000:
        t.tracer(False)
    if i>0 and i % 10000==0:
        textturtle.goto(-350, -300)
        textturtle.clear()
        textturtle.write(f"Calculating... shoot={i},count = {count}", font=font)
        t.update()
    t.goto(x * 270, y * 270)
    t.dot(6, "gray")
pi = 4*count/n
textturtle.goto(-350, -300)
textturtle.clear()
textturtle.write(f"shoot={n},count = {count},pi = {pi : .4f}",font=font)
t.update()

t.mainloop()
