from easygraphics.turtle import *
import math

create_world(600, 400)
n=0
while n<5:
    forward(200)
    left_turn(144)
    n+=1
pause()
close_world()