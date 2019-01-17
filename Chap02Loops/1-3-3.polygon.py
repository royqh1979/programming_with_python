from easygraphics.turtle import *
from easygraphics.dialog import *

def polygon(n,size):
    for i in range(n):
        fd(size)
        lt(180-(n-2)*180/n)

create_world(800,600)
results=get_many_strings(labels=['n=','size='])
n=int(results[0])
size=int(results[1])
polygon(n,size)
pause()
close_world()
