# 走迷宫
# 注意，为了和屏幕坐标系一致，maze[x,y]和我们一般的矩阵的行列是反的

from typing import Tuple

from easygraphics import *  # 使用easygraphics绘图
import numpy as np  # 使用numpy的ndarray来保存迷宫信息
import scanf

BRICK_WIDTH = 25 # 迷宫每格宽度
BRICK_HEIGHT = 25 # 迷宫每格高度
WALL_COLOR = Color.DARK_RED
WAY_COLOR = Color.LIGHT_GRAY
WAY_VISITED_COLOR = Color.DARK_GRAY
# 向四个方向走的位置(坐标）变化
step_x=[0,-1,0,1]
step_y=[-1,0,1,0]

class Maze:
    def __init__(self,maze:np.ndarray, entrance: Tuple[int], exit: Tuple[int]):
        self.maze = maze
        # 入口坐标
        self.entrance_x,self.entrance_y = entrance
        # 出口坐标
        self.exit_x,self.exit_y = exit
        # 走迷宫步骤记录
        self.history = []
        n, m = maze.shape  # n和m分别为maze的行数和列数
        self.width = BRICK_WIDTH * m
        self.height = BRICK_HEIGHT * n

def draw_brick(x,y):
    """
    绘制单个方块
    :param x:
    :param y:
    """
    draw_rect(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT)



def draw_maze(maze:Maze):
    """
    绘制迷宫
    :param ma:
    """
    set_background_color(Color.WHITE)
    clear_device()

    n,m = maze.maze.shape #n和m分别为maze的行数和列数
    # 迷宫左上角坐标（不含外墙）
    start_x = (get_width() - maze.width) //2
    start_y = (get_height() - maze.height) // 2
    # 绘制迷宫
    set_color(Color.WHITE)
    for i in range(0,n):
        for j in range(0,m):
            if maze.maze[i,j] == 1: # 是墙
                set_fill_color(WALL_COLOR)
            elif maze.maze[i,j] == 0: #是路
                set_fill_color(WAY_COLOR)
            else:
                set_fill_color(WAY_VISITED_COLOR)
            x = start_x + i*BRICK_WIDTH
            y = start_y + j*BRICK_HEIGHT
            draw_brick(x,y)
    # 绘制历史步骤
    set_fill_color(Color.BLACK)
    for i in range(len(maze.history)):
        x = start_x + maze.history[i][0] * BRICK_WIDTH + BRICK_WIDTH // 2
        y = start_y + maze.history[i][1] * BRICK_HEIGHT + BRICK_HEIGHT // 2
        fill_circle(x, y, 10)

def loadmaze(filepath):
    """
    从数据文件中读入迷宫
    :param filepath: 数据文件路径
    :return: 读入的迷宫
    """
    with open(filepath,mode="r") as file:
        line = file.readline().strip()
        n,m = scanf.scanf("%d,%d",line)
        # 注意，读入的文件中矩阵的行列 和 屏幕坐标（x,y)是反的
        # matrix[i,j]，i是行下标，相当于y； j是列下标，相当于x
        maze = np.zeros((m,n),dtype='int')
        y=0
        while y<n:
            datas = file.readline().strip().split(",")
            if len(datas)!=m:
                raise ValueError(f"第{y+1}行迷宫数据有误，应该有{m}列，但实际有{len(datas)}列")
            for x in range(m):
                maze[x,y] = ord(datas[x])-ord('0')
            y+=1
        line = file.readline().strip()
        entrance = scanf.scanf("%d,%d",line)
        line = file.readline().strip()
        exit = scanf.scanf("%d,%d",line)
        m = Maze(maze,entrance,exit)
        return m

def can_go(maze:Maze, x:int, y:int):
    """
    检测是否可以走到迷宫的x,y位置
    :param maze:
    :param x:
    :param y:
    :return:
    """
    if x<0 or y<0:
        return False
    n,m=maze.maze.shape
    if x>=n or y>=m:
        return False
    if maze.maze[x, y]!=0:
        return False
    return True


history_x=[]
history_y=[]


def try_solve(maze:Maze, x:int, y:int, step:int):
    """
    递归走迷宫
    :param maze:
    :param x:
    :param y:
    :param step:
    :return:
    """
    # 记录当前位置
    maze.history.append((x, y))

    # 设置已经走过
    maze.maze[x][y]=2

    #绘制迷宫当前状态
    draw_maze(maze)
    delay(100)

    # 已经到达终点,结束
    if x==maze.exit_x and y ==maze.exit_y:
        return True

    # 尝试4个方向走法
    for i in range(4):
        next_x = x + step_x[i]
        next_y = y + step_y[i]
        if can_go(maze,next_x,next_y):
            # 可以走，那么就从该点继续递归尝试
            found=try_solve(maze,next_x,next_y,step+1)
            # 已找到迷宫出口，不需要再试了，直接结束
            if found:
                return True

    #从该位置出发已尝试完所有走法，仍未找到出口，回退，从行走历史中删除当前位置
    maze.history.pop()
    return False


def solve(maze:Maze):
    """
    解决迷宫问题
    :param maze:
    :return:
    """
    return try_solve(maze,maze.entrance_x,maze.entrance_y,0)


def main():
    init_graph(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)
    maze=loadmaze("test.maze")
    draw_maze(maze)
    pause()
    solve(maze)
    pause()

easy_run(main)