import random
import math
from easygraphics import *

def main():
    init_graph(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    random.seed()
    cx,cy=0,0
    r=0.5
    n=50000
    count = 0

    translate(400,300)
    set_flip_y(True)

    draw_rect(-270,270,270,-270)
    draw_circle(0,0,270)


    for i in range(n):
        x=random.uniform(-0.5,0.5)
        y=random.uniform(-0.5,0.5)
        if math.hypot(x-cx,y-cy)<=r:
            count +=1
        if i<5000:
            set_fill_color("red")
            fill_circle(x*540,y*540,3)
            set_fill_color("white")
            fill_rect(-400,-280,400,-300)
            if i<10:
                draw_text(-400, -280, f"shoot={i+1},count = {count}, press any key to continue...")
                pause()
            elif i<100:
                draw_text(-400, -280, f"shoot={i+1},count = {count}")
                delay_fps(i//10*10)
            set_fill_color("gray")
            fill_circle(x * 540, y * 540, 3)
        set_fill_color("gray")
        fill_circle(x * 540, y * 540, 2)

    area = count / n
    pi = area / r / r
    set_fill_color("white")
    fill_rect(-400, -280, 400, -300)
    draw_text(-400, -280, f"n={n},count = {count},pi = {pi : .4f}")
    pause()
    close_graph()

easy_run(main)