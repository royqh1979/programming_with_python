"""
基本的单纯形算法实现

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
变量的取值范围均为非负实数

算法说明见《运筹学导论 第8版》（Introduction to Operations Research) 清华大学出版社 第4.4章

因为中文无法和英文、数字对齐，因此表格用英文显示
"""
from fractions import Fraction

#The ANSI escape sequences （用于显示带颜色字符）
class Color:
    Reset = '\033[0m'
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Black_Background = '\033[40m'
    Red_Background = '\033[41m'
    Green_Background = '\033[42m'
    Yellow_Background = '\033[43m'
    Blue_Background = '\033[44m'
    Magenta_Background = '\033[45m'
    Cyan_Background = '\033[46m'
    White_Background = '\033[47m'

def show_fraction(f:Fraction):
    if f is None:
        return ' '
    if not isinstance(f,Fraction):
        return str(f)
    if f.denominator == 1:
        return f.numerator
    else:
        return f'{f.numerator}/{f.denominator}'

class Model:
    def __init__(self, **kwargs):
        """
        创建优化模型，并建立（最大化）优化目标函数

        :param kwargs: 目标函数中各变量的系数
        """
        self.variables = [] # 所有变量，包括松弛变量
        self.real_variables = [] # 优化目标中包含的变量
        self.left_side = [] # 存储扩展后方程组左侧的系数矩阵（用二维列表表示）
        self.right_side = [] # 存储扩展后方程组右侧的常数
        self.ratio = [] # 存储各方程组的离速
        self.basic_variables = [] # 基变量列表

        # equation 0 为方程组中的第一个方程，即目标函数方程
        # 创建该方程
        equation0_left = [Fraction(1)]
        for v in kwargs:
            self.variables.append(v)
            self.real_variables.append(len(self.variables) - 1)
            equation0_left.append(Fraction(-kwargs[v]))
        self.left_side.append(equation0_left)
        self.right_side.append(Fraction(0))
        self.ratio.append('')             # 该方程的离速（无）
        self.basic_variables.append(None) # 该方程对应的基变量（无）



    def add_constraint(self,constaint,**kwargs)->None:
        """
        添加约束（小于等于）

        :param constaint: 右侧的约束值，必须大于0
        :param kwargs: 左侧各变量的系数
        :return: 无
        """
        for equation_left_side in self.left_side:
            equation_left_side.append(Fraction(0))
        equation_left_side=[Fraction(0)]
        for var in self.variables:
            if var in kwargs:
                equation_left_side.append(Fraction(kwargs[var]))
            else:
                equation_left_side.append(Fraction(0))
        equation_left_side.append(Fraction(1))
        self.left_side.append(equation_left_side)
        self.right_side.append(constaint)
        self.ratio.append('')
        self.variables.append('_s' + str(len(self.left_side) - 1))
        self.basic_variables.append(len(self.variables)-1)

    def _display(self, enter_basic=-2,leaving_basic=-2,highlight=True):
        """
        显示迭代表

        :param enter_basic:
        :param leaving_basic:
        :param highlight:
        :return:
        """
        # 扩展表标题 第一行
        print(f'{"Basic":<10} {"Equation":<10} {"Z":<8}',end='')
        for i in range(len(self.variables)):
            var = self.variables[i]
            if i==enter_basic: # 用红色显示入基变量
                print(f' {Color.Red}{var:<8}{Color.Reset}',end='')
            else:
                print(f' {var:<8}',end='')
        if highlight:
            print(f'{"Right":<8} {"Ratio":<10}')
        else:
            print(f'{"Right":<8}')

        # 扩展表标题 第二行
        print(f'{"Variables":<10} {"":<10} {"":<8}',end='')
        print(' '*len(self.variables)*9,end='')
        print(f'{"Side":<8}')

        # 扩展表内容
        for i in range(len(self.basic_variables)):
            if i==0:
                print(f"{'obj.':<10} {'('+str(i)+')':<10}",end='')
            elif i == leaving_basic:  # 用紫色显示出基变量系数
                print(f'{Color.Magenta}{self.variables[self.basic_variables[i]]:<10} {"("+str(i)+")":<10}{Color.Reset}',end='')
            else:
                print(f'{self.variables[self.basic_variables[i]]:<10} {"("+str(i)+")":<10}',end='')

            equation_left=self.left_side[i]
            for j in range(len(equation_left)):
                c=equation_left[j]
                if j == enter_basic+1:  # 用红色显示入基变量系数
                    print(f' {Color.Red}{show_fraction(c):<8}{Color.Reset}', end='')
                elif i == leaving_basic: # 用紫色显示出基变量系数
                    print(f' {Color.Magenta}{show_fraction(c):<8}{Color.Reset}', end='')
                else:
                    print(f' {show_fraction(c):<8}', end='')

            if i == leaving_basic:  # 用紫色显示出基变量系数
                print(Color.Magenta,end='')
            print(f'{show_fraction(self.right_side[i]):<8}', end='')
            if highlight:
                print(f' {show_fraction(self.ratio[i]) :<10}',end='')
            print(Color.Reset)

    def solve(self):
        iteration = 0
        while True:
            iteration += 1
            print()
            print('---------------------------------')
            print(f'iteration {iteration}:')

            # Optimality Test:
            # find the variable with the minimum negative coeffecient
            # 在目标函数约束式中找到系数为负且绝对值最大的变量，作为入基变量
            # 如果没有，则说明目标函数已达到最优
            obj_equation_left = self.left_side[0]
            min_v = 0
            min_i = -1
            for i in range(len(obj_equation_left)):
                if obj_equation_left[i] < min_v:
                    min_v = obj_equation_left[i]
                    min_i = i
            if min_v == 0:
                print("The solution is optimal")
                break
            enter_basic = min_i

            # Minimum Ratio Test
            # find the euqation with the minimal leaving ratio
            # 找出最小比值（约束式右端项和入基变量系数的比值），从而确定出基变量
            min_ratio = None
            min_i = -1
            for i in range(1, len(self.left_side)):
                equation_left = self.left_side[i]
                if equation_left[enter_basic] == 0:
                    self.ratio[i] = ''
                else:
                    denominator = equation_left[enter_basic]
                    if denominator <=0: # 入基变量的系数需大于0，该约束式才有比值（当入基系数为零时，出基变量变为零才能让入基变量变为正）
                        self.ratio[i] == ''
                    else:
                        self.ratio[i] = self.right_side[i]/denominator
                        if min_ratio is None or self.ratio[i] < min_ratio:
                            min_ratio = self.ratio[i]
                            min_i = i
            if min_i == -1:
                print("can't find the minimum ratio!")
                return
            leaving_basic_eq_index = min_i
            leaving_basic = self.basic_variables[min_i]

            self._display(enter_basic-1,leaving_basic_eq_index)
            print("Entering basic :",self.variables[enter_basic-1])
            print("leaving basic:",self.variables[leaving_basic])

            #Gaussian Elimination （高斯消元法，从各约束式中消除入基变量）
            leaving_basic_eq = self.left_side[min_i]
            denominator = leaving_basic_eq[enter_basic]
            for i in range(len(leaving_basic_eq)):
                leaving_basic_eq[i] /= denominator
            self.right_side[min_i] /= denominator
            self.basic_variables[min_i]=enter_basic-1
            for i in range(len(self.left_side)):
                if i==min_i:
                    continue
                equation_left=self.left_side[i]
                multiple = equation_left[enter_basic]
                for j in range(len(equation_left)):
                    equation_left[j] -= multiple * leaving_basic_eq[j]
                self.right_side[i] -= multiple * self.right_side[min_i]

        print()
        print('---------------------------------')
        self._display(highlight=False)
        self._display_solution()

    def _display_solution(self):
        print("The optiomal solution:")
        for i in self.real_variables:
            found = False
            for j in range(1,len(self.basic_variables)):
                basic_variable = self.basic_variables[j]
                if i==basic_variable:
                    print(f'{self.variables[i]}: {show_fraction(self.right_side[j])}')
                    found = True
                    break
            if not found:
                print(f'{self.variables[i]}: 0')
        print("objective value: ",self.right_side[0])
        print("shadow price:")
        eq0 = self.left_side[0]
        for i in range(1, len(self.left_side)):
            slack_index = len(self.real_variables) - 1 + i
            print(f"shadow price for constaint {i}:",eq0[slack_index+1])



# model = Model(x1=3,x2=5)
# model.add_constraint(4,x1=1)
# model.add_constraint(12,x2=2)
# model.add_constraint(18,x1=3,x2=2)
# model.solve()

model = Model(x1=4,x2=-2,x3=7,x4=-1)
model.add_constraint(10,x1=1,x3=5)
model.add_constraint(1, x1=1,x2=1,x3=-1)
model.add_constraint(0,x1=6,x2=-5)
model.add_constraint(3,x1=-1,x3=2,x4=-2)
model.solve()

# model = Model(x1=3,x2=2)
# model.add_constraint(4,x1=1)
# model.add_constraint(12,x2=2)
# model.add_constraint(18,x1=3,x2=2)
# model.solve()

# model = Model(x1=40,x2=30)
# model.add_constraint(120,x1=4,x2=3)
# model.add_constraint(50,x1=2,x2=1)
# model.solve()
