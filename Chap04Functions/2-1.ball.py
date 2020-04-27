from easygraphics import *
import random
from dataclasses import dataclass

@dataclass()
class World:
    left: float  # 左上角x坐标
    top: float  # 左上角y坐标
    right: float  # 右下角x坐标
    bottom: float  # 右下角坐标


#注意Ball有自己的方法，不是dataclass
class Ball:
    def __init__(self,world,cx,cy,r,vx,vy):
        self.world = world # 球所在的边框（世界）
        self.cx=cx # 球心x坐标
        self.cy=cy # 球心y坐标
        self.r = r # 球心半径
        self.vx=vx # 速度x分量
        self.vy=vy # 速度y分量

    def move(self):
        """
        球移动一帧
        :return:
        """
        if self.v_collide():
            self.vy = - self.vy
        if self.h_collide():
            self.vx = - self.vx
        self.cx += self.vx
        self.cy += self.vy

    def v_collide(self):
        """
        判断Y方向上是否撞墙
        :return:
        """
        return self.cy < self.world.top + self.r \
               or self.cy > self.world.bottom - self.r

    def h_collide(self):
        """
        判断X方向上是否撞墙
        :return:
        """
        return self.cx < self.world.left + self.r \
               or self.cx > self.world.right - self.r


def main():
    init_graph(400,400)
    set_render_mode(RenderMode.RENDER_MANUAL)
    random.seed()
    world = World(20,20,380,380)
    cx = random.randrange(20,380)
    cy = random.randrange(20,200)
    r=5
    vx = 0
    # 确保随机出来的vx（x方向速度）不会是0
    while vx == 0:
        vx = random.randint(-3,3)

    vy = 0
    while vy == 0:
        vy = random.randint(1,3)
    ball = Ball(world,cx,cy,r,vx,vy)
    while is_run():
        ball.move()
        # Ball.move(ball) # 和上面一行语句等效
        if delay_jfps(100):
            #擦除整个屏幕
            clear()
            #画外框
            set_color("black")
            rect(20,20,380,380)
            #画小球
            set_color("red")
            set_fill_color("red")
            fill_circle(ball.cx,ball.cy,ball.r)
    close_graph()


easy_run(main)









