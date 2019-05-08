"""
数独求解

使用简化的启发式回溯搜索

使用递归实现

每次优先尝试填写可行数字最少的格子

"""
import numpy as np
from easygraphics import *

FONT_WIDTH = 40
BOARD_TOP = 10
BOARD_LEFT = 10
SQUARE_WIDTH = 50

SPEED = 100

# 棋盘，为了方便定义为[10][10]，实际只用[1][1]-[9][9]
board = np.zeros((10, 10))

# 行、列、小九宫已使用数字集合
cols = [set() for i in range(10)]  # 各列数字集合
rows = [set() for i in range(10)]  # 各行数字集合
blks = [set() for i in range(10)]  # 各小九宫格数字集合


# 绘图相关函数
def draw_number_at(i, j, number, color):
    """
    Draw a number at cell(i,j) with the specified color
    :param i: the row
    :param j: the column
    :param number: the number
    :param color: the color
    """
    left = BOARD_LEFT + (j - 1) * SQUARE_WIDTH
    top = BOARD_TOP + (i - 1) * SQUARE_WIDTH
    set_color(color)
    if number != 0:
        draw_rect_text(left + 5, top + 5, FONT_WIDTH, FONT_WIDTH, number)
    else:
        set_color(Color.WHITE)
        fill_rect(left+1, top+1, left + SQUARE_WIDTH-2, top + SQUARE_WIDTH-2)


def draw_board():
    clear_device()
    for i in range(1, 10):
        for j in range(1, 10):
            left = BOARD_LEFT + (j - 1) * SQUARE_WIDTH
            top = BOARD_TOP + (i - 1) * SQUARE_WIDTH
            set_color(Color.LIGHT_GRAY)
            rect(left, top, left + SQUARE_WIDTH, top + SQUARE_WIDTH)
            draw_number_at(i, j, board[i][j], Color.RED)

    # 画小九宫格边框
    set_color(Color.BLACK)
    for i in range(1, 4):
        for j in range(1, 4):
            left = BOARD_LEFT + (j - 1) * 3 * SQUARE_WIDTH
            top = BOARD_TOP + (i - 1) * 3 * SQUARE_WIDTH
            rect(left, top, left + 3 * SQUARE_WIDTH, top + 3 * SQUARE_WIDTH)


def init():
    init_graph(800, 600)
    set_color(Color.BLACK)
    set_background_color(Color.WHITE)
    set_line_width(2)
    set_fill_color(Color.WHITE)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_font_size(FONT_WIDTH)


DATA_FILE = "10soduku.board"


# 候选格子, canPut[n]=1表示该格可以放数字n，否则不行
class CandiateSquare:
    def __init__(self, x=0, y=0):
        self.x = x  # 格子所在的行
        self.y = y  # 格子所在的列
        self.possibles = set()  # 格子中可填的数字集合


def which_block(i, j):
    """
    计算当前方格属于哪一宫

    :param i: 格子所在行
    :param j: 格子所在列
    :return: 格子所在的宫编号
    """
    return ((i - 1) // 3) * 3 + ((j - 1) // 3)


def tag(i, j, number):
    """
    在本列、本行、本宫中标记数字number已被使用

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    rows[i].add(number)
    cols[j].add(number)
    blks[which_block(i, j)].add(number)


def untag(i, j, number):
    """
    在本列、本行、本宫中取消数字val的使用标记

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    rows[i].remove(number)
    cols[j].remove(number)
    blks[which_block(i, j)].remove(number)


def fill(i, j, number):
    """
    将数字val填写到方格(i,j)中

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    board[i][j] = number
    tag(i, j, number)


def unfill(i, j):
    """
    清除方格(i,j)中的数字

    :param i: 格子所在的行
    :param j: 格子所在的列
    """

    number = board[i][j]
    untag(i, j, number)
    board[i][j] = 0


def load_board(boardFile):
    """
    从数据文件中读取数独初始状态

    :param boardFile: 数据文件名
    """
    global board
    try:
        with open(boardFile, mode="r") as file:
            board = [ [0]*10 for i in range(10)]
            for line in file:
                line = line.strip()
                numbers = line.split(',')
                if len(numbers) != 3:
                    continue
                i, j, k = int(numbers[0]), int(numbers[1]), int(numbers[2])
                board[i][j] = k
    except IOError :
        clear_device()
        draw_rect_text(10, 500, 700, 50, f"无法打开文件{boardFile}")


def count_unsolved():
    """
    计算有多少个格子需要填

    :return:
    """
    count = 0
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] == 0:
                count += 1
    return count


def can_fill(i, j, number):
    """
    判断number能否填写在格子(i,j)中

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 要填写的数字
    """
    if number in rows[i]:
        return False
    if number in cols[j]:
        return False
    if number in blks[which_block(i, j)]:
        return False
    return True


def calculatePossible(i, j):
    """
    找出格子（i,j）中所有可填的数字

    :param i: 格子所在的行
    :param j: 格子所在的列
    """
    possibles = set()
    for number in range(1, 10):
        if can_fill(i, j, number):
            possibles.add(number)
    return possibles


def solve(unsolved):
    if unsolved == 0:
        return True

    # 显示用
    delay_fps(SPEED)

    # 找出可填的数字数量最少的格子
    c = CandiateSquare()
    min_possible_count = 10
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] == 0:
                possibles = calculatePossible(i, j)
                if len(possibles) < min_possible_count:
                    min_possible_count = len(possibles)
                    c.x = i
                    c.y = j
                    c.possibles = possibles

    # 尝试填写该格子
    for v in c.possibles:
        fill(c.x, c.y, v)
        draw_number_at(c.x, c.y, v, Color.BLACK)
        if solve(unsolved - 1):
            return True
        unfill(c.x, c.y)
        draw_number_at(c.x, c.y, 0, Color.BLACK)

    return False


init()
load_board(DATA_FILE)
draw_board()
draw_rect_text(10, 550, 700, 50, "按任意键开始...")
pause()
fill_rect(10, 550, 710, 600)
draw_rect_text(10, 550, 700, 50, "正在穷举...")

# 将数独中已有的数字做标记
for i in range(1, 10):
    for j in range(1, 10):
        if board[i][j] != 0:
            tag(i, j, board[i][j])

solve(count_unsolved())
fill_rect(10, 550, 710, 600)
draw_rect_text(10, 550, 700, 50, "找到答案了！按任意键退出...")
pause()
close_graph()
