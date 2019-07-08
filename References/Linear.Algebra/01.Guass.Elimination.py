# 使用高斯消元法，将矩阵转化为行简化阶梯型矩阵(Reduced Row Echelon Form)
# 注：使用sympy的rref函数，可以直接求行简化阶梯型矩阵

from sympy import Matrix,Rational
import sympy as sm

def interchange(m:Matrix, i:int, j:int):
    """
    初等行变换：交换第i行和第j行的值
    :param m: 要变换的矩阵
    :param i: 要交换的第一行的行号（行号从0开始）
    :param j: 要交换的第二行的行号（行号从0开始）
    """
    m.row_swap(i , j )


def scale(m:Matrix,i:int, c:Rational):
    """
    初等行变换：将第i行的所有元素乘以同一个非零常量c
    :param m: 要变换的矩阵
    :param i: 要变换的行的行号（行号从0开始）
    :param c: 要乘的常数
    """
    def op_scaling(ele, col):
        return ele*c

    m.row_op(i,op_scaling)

def replace(m:Matrix, i:int,j:int, c:Rational):
    """
    初等行变换: 将第j行各元素乘以非零常量c后，加到第i行
    :param m: 要变换的矩阵
    :param i: 第i行的行号（行号从0开始）
    :param j: 第j行的行号（行号从0开始）
    :param c: 要乘的常数
    """
    def op_scaling(ele,col):
        return ele+m.row(j)[col]*c

    m.row_op(i, op_scaling)


def guass_elimination(m:Matrix,verbose=True):
    """
    高斯消元法求行简化阶梯型矩阵

    :param m: 要简化的矩阵
    :param verbose: 是否显示消元过程
    :return: 行简化阶梯型矩阵
    """
    m=m.copy()
    forward_elemination(m, verbose)
    backward_elemination(m,verbose)
    return m;


def forward_elemination(m:Matrix, verbose:bool):
    """
    前向校园（获得阶梯型矩阵）
    :param m:
    :param verbose:
    :return:
    """
    if verbose:
        print("== 前向消元 ==")
    c = 0
    step = 0
    while c < m.cols and c < m.rows:
        # 判断第c列是否全零，是就跳过该列，继续处理下一列
        first_non_zero_row = -1
        for i in range(m.rows):
            if not sm.Eq(m[i, c], 0):
                first_non_zero_row = i
                break
        if first_non_zero_row == -1:
            c += 1
            continue
        if first_non_zero_row != 0:
            interchange(m, c, first_non_zero_row)
            if verbose:
                step += 1
                print(f"第{step}步：交换第{c + 1}行和第{first_non_zero_row + 1}行")
                print(m)

        if not sm.Eq(m[c, c], 1):
            constant = Rational(1, m[c, c])
            scale(m, c, constant)
            if verbose:
                step += 1
                print(f"第{step}步：第{c + 1}行乘以{constant}")
                print(m)

        for i in range(c + 1, m.rows):
            if not sm.Eq(m[i, c], 0):
                constant = Rational(-m[i, c])
                replace(m, i, c, constant)
                if verbose:
                    step += 1
                    print(f"第{step}步：第{i + 1}行加上{constant}乘以第{c + 1}行")
                    print(m)

        c += 1

def backward_elemination(m:Matrix, verbose:bool):
    """
    后向消元，获得化简的阶梯型矩阵
    :param m:
    :param verbose:
    :return:
    """
    if verbose:
        print("== 后向消元 ==")
    step = 0
    for i in range(m.rows):
        row = m.rows-i-1

        #寻找本行第一个非零元素
        col = 0
        while col < m.cols:
            if not sm.Eq(m[row,col],0):
                break
            col+=1
        if col>=m.cols: #本行全零，继续上一行
            continue

        # pivot的位置为(row,col)
        if not sm.Eq(m[row, col], 1):
            constant = Rational(1, m[row, col])
            scale(m, row, constant)
            if verbose:
                step += 1
                print(f"第{step}步：第{row + 1}行乘以{constant}")
                print(m)

        for j in range(row):
            if not sm.Eq(m[j,col],0):
                constant = Rational(-m[j,col])
                replace(m, j, row, constant)
                if verbose:
                    step += 1
                    print(f"第{step}步：第{j + 1}行加上{constant}乘以第{row + 1}行")
                    print(m)
m1=Matrix([
    [1,-2,1,0],
    [0,2,-8,8],
    [-4,5,9,-9]
])

print(m1)
guass_elimination(m1,True)
# print(m1)
#
# replace(m1,3,1,4)
#
# print(m1)
#
# scale(m1,2,Rational(1,2))
#
# print(m1)
#
# replace(m1,3,2,3)
# print(m1)











