from easygraphics.turtle import *


def arcl(side, degree):
    for i in range(degree):
        fd(side)
        lt(1)


def arcr(side, degree):
    for i in range(degree):
        fd(side)
        rt(1)

def main():
    create_world(800, 600)

    set_speed(50)

    arcr(2, 90)
    arcl(2, 90)

    pause()
    close_world()

easy_run(main)