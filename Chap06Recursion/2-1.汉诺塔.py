from easygraphics import *
from typing import List

def move_disk(from_pole, to_pole):
    print(f"从{from_pole}柱移动到{to_pole}柱")


def hanoi(n, from_pole, to_pole, aux_pole):
    if n==1:
        move_disk(from_pole, to_pole)
    else:
        hanoi(n - 1, from_pole, aux_pole, to_pole)  # 把from的上面n-1个借助to移动到aux
        move_disk(from_pole, to_pole);
        hanoi(n - 1, aux_pole, to_pole, from_pole)  # 把aux上的n-1个借助from移动到to

n=int(input("请输入n:"))
hanoi(n, 'A','C','B') # 设B为辅助，从A移动C

