from easygraphics.turtle import *

def main():
    create_world()

    lt(30)
    for i in range(3):
        fd(100)
        lt(120)
    rt(30)

    pause()
    close_world()

easy_run(main)