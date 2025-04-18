from easygraphics import *
from typing import List
from dataclasses import dataclass

SPEED = 1000        # 绘制时，delay()的参数

XWIDTH = 300        # 每个柱子占据的水平宽度
XHEIGHT = 400       # 所有柱子的高度


#全局场景的矩形
BLEFT = (500-XWIDTH*3/2-20)
BRIGHT = (500+XWIDTH*3/2+20)
BTOP = 50
BBOTTOM =  (BTOP+XHEIGHT+40)

# 每个柱子的中心所在横坐标
POLE_CXA =  (500-XWIDTH)
POLE_CXB =  500
POLE_CXC =  (500+XWIDTH)

POLE_BOTTOM  = (BTOP+XHEIGHT)     # 所有柱子的水平面坐标*/
POLE_TOP =  (BTOP+100)  # 所有柱子的顶部坐标
POLE_THICK =  12  # 柱子厚度

# 绘制圆饼的参数
DISK_THICK = 20  # 圆盘厚度
DISK_MINWIDTH = (POLE_THICK+30)  # 最小的圆盘宽度
DISK_MAXWIDTH = (XWIDTH-20)      # 最大的圆盘宽度
DISK_INCSIZE = 20                # 圆盘宽度增长值
DISK_MAXCOUNT =  8       # 最大圆盘数
DISK_GAP = 1 # 相邻圆盘的垂直距离间隔
DISK_FLYHEIGHT = (POLE_TOP - (DISK_THICK)*3)  # 圆盘的飞行高度

# 颜色定义
COLOR_POLE = Color.BLACK  # Pole颜色
COLOR_POLEBORDER = Color.LIGHT_GRAY # Pole边框颜色
COLOR_BKGND = Color.DARK_GRAY      # 背景颜色
COLOR_DISK = Color.YELLOW # 圆盘的填充色

POLE_A = 0
POLE_B = 1
POLE_C = 2

@dataclass()
class Disk:
    id : int # 圆盘序号
    cx : int # 圆盘中心x坐标
    cy : int  #圆盘中心y坐标
    half_width: int   #圆盘宽度的一半
    at_pole : int = 0 #默认在A柱上

class Pole:
    def __init__(self,id,tag,cx):
        self.id=id
        self.label = tag
        self.cx = cx
        self.disks:List[Disk] = []


poles:List[Pole] = []


def draw_move_disk(from_pole_id, to_pole_id):
    from_pole = poles[from_pole_id]
    to_pole = poles[to_pole_id]
    disk=from_pole.disks.pop()

    set_color("white")
    draw_rect_text(200, 500, 500, 20, f"Moving disk {disk.id} from {from_pole.label} to {to_pole.label}")

    # 移动圆盘到最高处
    while disk.cy > DISK_FLYHEIGHT:
        draw_and_update_disk(disk, disk.cx, disk.cy - 1)
        delay_fps(SPEED)

    # 在最高处位置水平移动圆盘
    if to_pole_id > from_pole_id:
        step = 1
    else:
        step = -1
    while disk.cx != to_pole.cx:
        draw_and_update_disk(disk, disk.cx + step, disk.cy)
        delay_fps(SPEED)

    # 圆盘下落到最低高度
    floor=GetNextDiskTop(len(to_pole.disks))
    while disk.cy < floor:
        draw_and_update_disk(disk, disk.cx, disk.cy + 1)
        delay_fps(SPEED)

    # 更新圆盘数量，索引号信息
    disk.at_pole = to_pole_id
    to_pole.disks.append(disk)

# 复原被DISK移动后的背景，这样会比putimage和getimage提高绘制时的效率！
# 这个方法虽然高效，但是情形过分特殊，即不能通用！
def recover_background(disk):
    set_color(COLOR_BKGND)
    rect(disk.cx - disk.half_width, disk.cy, disk.cx + disk.half_width, disk.cy+DISK_THICK)
    # 看是否需要绘制POLE
    if disk.cy >= POLE_TOP: # 圆盘顶部
        set_color(COLOR_POLE)
        line(disk.cx - POLE_THICK/2+1, disk.cy, disk.cx + POLE_THICK/2-1, disk.cy) # 柱心
        put_pixel(disk.cx - POLE_THICK/2, disk.cy, COLOR_POLEBORDER) # 柱子边框
        put_pixel(disk.cx + POLE_THICK/2, disk.cy, COLOR_POLEBORDER) # 柱子边框
    if disk.cy + DISK_THICK >= POLE_TOP : # 圆盘底部
        set_color(COLOR_POLE)
        line(disk.cx - POLE_THICK/2, disk.cy + DISK_THICK, disk.cx + POLE_THICK/2, disk.cy + DISK_THICK)
        put_pixel(disk.cx - POLE_THICK/2, disk.cy + DISK_THICK, COLOR_POLEBORDER)
        put_pixel(disk.cx + POLE_THICK/2, disk.cy + DISK_THICK, COLOR_POLEBORDER)
    # 是否应该重绘柱顶边框
    if disk.cy == POLE_TOP or disk.cy + DISK_THICK == POLE_TOP:
        set_color(COLOR_POLEBORDER)
        line(disk.cx - POLE_THICK/2, POLE_TOP, disk.cx + POLE_THICK/2, POLE_TOP)

# 绘制圆盘 cx1-中心横坐标，cy1-中心纵坐标
def draw_and_update_disk(disk, cx1, cy1):
    # 复原背景
    recover_background(disk)
    # 更新坐标
    disk.cx=cx1
    disk.cy=cy1

    # 绘制它
    set_fill_color(COLOR_DISK)
    set_color(Color.BLACK)
    fill_rect(disk.cx - disk.half_width + 2, disk.cy + 2, disk.cx + disk.half_width - 2, disk.cy + DISK_THICK - 2)
    draw_rect_text(disk.cx-20,disk.cy,40,16,f"{disk.id}")
    # 连续绘制两个矩形边框，注意向内扩！
    rect(disk.cx - disk.half_width, disk.cy, disk.cx + disk.half_width, disk.cy + DISK_THICK)
    rect(disk.cx - disk.half_width+1, disk.cy+1, disk.cx + disk.half_width-1, disk.cy + DISK_THICK - 1)

# 根据某个柱上已有的圆盘数，计算出下一个放到上面的圆盘的Y坐标
# count表示当前已经有的圆盘数量！
def GetNextDiskTop(count):
    basement = POLE_BOTTOM - DISK_THICK - DISK_GAP            # 从水平面上升一定位置的基点
    return basement - (DISK_THICK + DISK_GAP)*count     # cy

# 输出带有阴影的文本
def textout(x, y, text, color, bordercolor):
    set_color(bordercolor)
    draw_text(x+1,y+1,text)
    set_color(color)
    draw_text(x,y,text)

# 输出带有边框的文本
def textoutwithborder(x, y, text, color,  bordercolor):
    set_color(bordercolor)
    for i in range(-1,2):
        for j in range(-1,2):
            if i!=0 or j!=0:
                draw_text(x+i,y+j,text)
    set_color(color)
    draw_text(x,y,text)


def init(n):
    init_graph(1000,600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_color(Color.LIGHT_GRAY)
    # 绘制背景矩形
    set_fill_color(COLOR_BKGND)
    fill_rect(BLEFT+4, BTOP+4, BRIGHT-4, BBOTTOM-4)
    # 所有元素绘制应该一律向内扩，不要外扩，以免无法确定该元素的边界*/
    rect(BLEFT,BTOP,BRIGHT,BBOTTOM)
    rect(BLEFT+1,BTOP+1,BRIGHT-1,BBOTTOM-1)
    rect(BLEFT+3,BTOP+3,BRIGHT-3,BBOTTOM-3)

    # 柱子边框
    set_color(COLOR_POLEBORDER)
    rect(POLE_CXA-POLE_THICK/2, POLE_TOP, POLE_CXA+POLE_THICK/2, POLE_BOTTOM)
    rect(POLE_CXB-POLE_THICK/2, POLE_TOP, POLE_CXB+POLE_THICK/2, POLE_BOTTOM)
    rect(POLE_CXC-POLE_THICK/2, POLE_TOP, POLE_CXC+POLE_THICK/2, POLE_BOTTOM)
    # 底盘边框
    rect(POLE_CXA-XWIDTH/2, POLE_BOTTOM,  POLE_CXC+XWIDTH/2, POLE_BOTTOM+POLE_THICK)

    # 填充柱子
    set_fill_color(COLOR_POLE)
    fill_rect(POLE_CXA-POLE_THICK/2+1, POLE_TOP+1, POLE_CXA+POLE_THICK/2-1, POLE_BOTTOM)
    fill_rect(POLE_CXB-POLE_THICK/2+1, POLE_TOP+1, POLE_CXB+POLE_THICK/2-1, POLE_BOTTOM)
    fill_rect(POLE_CXC-POLE_THICK/2+1, POLE_TOP+1, POLE_CXC+POLE_THICK/2-1, POLE_BOTTOM)
    # 填充底盘
    fill_rect(POLE_CXA-XWIDTH/2+1, POLE_BOTTOM+1,  POLE_CXC+XWIDTH/2-1, POLE_BOTTOM+POLE_THICK-1)

    # 用自定义的函数绘制柱子的字母名称，A，B，C
    set_font_size(20)
    textout(POLE_CXA-8, POLE_BOTTOM+POLE_THICK+18, "A", Color.RED, Color.BLACK)
    textout(POLE_CXB-8, POLE_BOTTOM+POLE_THICK+18, "B", Color.RED, Color.BLACK)
    textout(POLE_CXC-8, POLE_BOTTOM+POLE_THICK+18, "C", Color.RED, Color.BLACK)

    # 记录每个Pole的中心横坐标
    pole_a = Pole(POLE_A,'A',POLE_CXA)
    poles.append(pole_a)
    pole_b = Pole(POLE_B,'B',POLE_CXB)
    poles.append(pole_b)
    pole_c = Pole(POLE_C,'C',POLE_CXC)
    poles.append(pole_c)

    for i in range(n,0,-1):
        # 从大到小，创建圆盘，最小的圆盘在上面
        disk = Disk(i,
                    pole_a.cx,
                    GetNextDiskTop(n-i),
                    DISK_MINWIDTH + DISK_INCSIZE*i )
        pole_a.disks.append(disk)
        draw_and_update_disk(disk, disk.cx, disk.cy)  # 绘制圆盘

    # 一些额外信息字符串
    set_color(Color.LIGHT_GRAY)


def quit():
    for pole in poles:
        pole.disks.clear()
    poles.clear()

def move_disk(from_pole_id, to_pole_id):
	draw_move_disk(from_pole_id, to_pole_id)


# 三个POLE分别用0，1，2表示, from_id-所在pole, to_id-目标pole, aux_id -辅助pole
def hanoi(n, from_pole_id, to_pole_id, aux_pole_id):
    if n==1:
        move_disk(from_pole_id, to_pole_id)
    else:
        hanoi(n - 1, from_pole_id, aux_pole_id, to_pole_id)  # 把上面n-1个借助to移动到aux
        move_disk(from_pole_id, to_pole_id);
        hanoi(n - 1, aux_pole_id, to_pole_id, from_pole_id)  # 把aux上的n-1个借助from移动到to


# Entry Point
def main():
    n=3
    init(n)
    pause()
    hanoi(n, POLE_A, POLE_C, POLE_B) # 设Pole B为辅助，从A移动C
    pause()
    quit()
    close_graph()

easy_run(main)
