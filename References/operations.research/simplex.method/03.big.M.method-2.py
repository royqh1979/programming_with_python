"""
大M法（带人工变量的单纯形法）

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
或者 变量的线性组合 = 常数 形式
或者 变量的线性组合 >= 常数 形式

算法描述见 《运筹学导论》第8版 Introduction to Operations Research 清华大学出版社 第4.6章
"""
from fractions import Fraction
from enum import Enum
from decimal import Decimal

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

class FractionWithM:
    """
    class for
    """

    def __init__(self, value, M=0):
        super().__setattr__('M', Fraction(M))
        super().__setattr__('fraction', Fraction(value))

    def __add__(self, y):
        if isinstance(y, FractionWithM):
            return FractionWithM(self.fraction + y.fraction, self.M + y.M)
        else:
            return FractionWithM(self.fraction + y, self.M)

    def __sub__(self, y):
        if isinstance(y, FractionWithM):
            return FractionWithM(self.fraction - y.fraction, self.M - y.M)
        else:
            return FractionWithM(self.fraction - y, self.M)

    def __mul__(self, y):
        if y.M != 0 and self.M != 0:
            return NotImplemented("Cant multiply 2 FractionWithM objects!")
        if y.M != 0:
            return FractionWithM(self.fraction * y.fraction, self.fracation * y.M)
        else:
            return FractionWithM(self.fraction * y.fraction, self.M * y.fraction)

    def __truediv__(self, y):
        if y.M != 0:
            return NotImplemented("Cant divide 2 FractionWithM objects!")
        return FractionWithM(self.fraction / y.fraction, self.M / y.fraction)

    def __gt__(self, y):
        if not isinstance(y, FractionWithM):
            if self.M > 0:
                return True
            elif self.M < 0:
                return False
            else:
                return self.fraction > y
        if self.M > y.M:
            return True
        elif self.M < y.M:
            return False
        return self.fraction > y.fraction

    def __eq__(self, y):
        if not isinstance(y, FractionWithM):
            if self.M != 0:
                return False
            else:
                return self.fraction == y

        return self.M == y.M and self.fraction == y.fraction

    def __lt__(self, y):
        if not isinstance(y, FractionWithM):
            if self.M < 0:
                return True
            elif self.M > 0:
                return False
            else:
                return self.fraction < y
        if self.M < y.M:
            return True
        elif self.M > y.M:
            return False
        return self.fraction < y.fraction

    def __ge__(self, y):
        if not isinstance(y, FractionWithM):
            if self.M > 0:
                return True
            elif self.M < 0:
                return False
            else:
                return self.fraction >= y
        if self.M > y.M:
            return True
        elif self.M < y.M:
            return False
        return self.fraction >= y.fraction

    def __le__(self, y):
        if not isinstance(y, FractionWithM):
            if self.M < 0:
                return True
            elif self.M > 0:
                return False
            else:
                return self.fraction <= y
        if self.M < y.M:
            return True
        elif self.M > y.M:
            return False
        return self.fraction <= y.fraction

    def __setattr__(self, key, value):
        raise AttributeError(f"Can't set a FractionWithM object's {key} attribute!")

    def __str__(self):
        str = ''
        if self.M != 0:
            if self.M.denominator == 1:
                str += f'{self.M.numerator}*M'
            else:
                str += f'{self.M.numerator}/{self.M.denominator}*M'
            if self.fraction > 0:
                str += '+'
        if self.fraction != 0:
            if self.fraction.denominator == 1:
                str += f'{self.fraction.numerator}'
            else:
                str += f'{self.fraction.numerator}/{self.fraction.denominator}'
        else:
            if self.M == 0:
                str = '0'
        return str

    def __format__(self, format_spec):
        return format(str(self), format_spec)

class OptimizationType(Enum):
    maximization = 1
    minimization = 2


class Model:
    def __init__(self, type=OptimizationType.maximization, **kwargs):
        self.variables = []  # 所有变量，包括松弛变量
        self.real_variables = []  # 优化目标中包含的变量
        self.left_side = []  # 存储扩展后方程组左侧的系数
        self.right_side = []  # 存储扩展后方程组右侧的常数
        self.ratio = []  # 存储各方程组的离速
        self.basic_variables = []  # 基变量列表
        self.slack_variables = []  # 松弛变量列表
        self.artificial_variables = []  # 人工变量列表
        self.surplus_variables = []  # 剩余变量

        if type == OptimizationType.maximization:
            eq0 = [FractionWithM(1)]
            for v in kwargs:
                self.variables.append(v)
                self.real_variables.append(len(self.variables) - 1)
                eq0.append(FractionWithM(-kwargs[v]))
        else:
            eq0 = [FractionWithM(-1)]
            for v in kwargs:
                self.variables.append(v)
                self.real_variables.append(len(self.variables) - 1)
                eq0.append(FractionWithM(kwargs[v]))

        self.left_side.append(eq0)
        self.right_side.append(FractionWithM(0))
        self.ratio.append('')
        self.basic_variables.append(None)

    def add_equal_constraint(self, constraint, **kwargs):
        eq0 = self.left_side[0]
        eq0.append(FractionWithM(M=1, value=0))
        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(FractionWithM(0))
        eq = [FractionWithM(0)]
        for var in self.variables:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variables.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variables) - 1)
        self.basic_variables.append(len(self.variables) - 1)

    def add_greater_constraint(self, constraint, **kwargs):
        eq0 = self.left_side[0]
        eq0.append(FractionWithM(0))
        eq0.append(FractionWithM(M=1, value=0))
        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(FractionWithM(0))
            eq.append(FractionWithM(0))
        eq = [FractionWithM(0)]
        for var in self.variables:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(-1))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variables.append('_ss' + str(len(self.surplus_variables) + 1))
        self.surplus_variables.append(len(self.variables) - 1)
        self.variables.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variables) - 1)
        self.basic_variables.append(len(self.variables) - 1)

    def add_less_constraint(self, constraint, **kwargs):
        for eq in self.left_side:
            eq.append(FractionWithM(0))
        eq = [FractionWithM(0)]
        for var in self.variables:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variables.append('_s' + str(len(self.slack_variables) + 1))
        self.slack_variables.append(len(self.variables) - 1)
        self.basic_variables.append(len(self.variables) - 1)

    def _display(self, enter_basic=-2, leaving_basic=-2, highlight=True):
        """
        显示迭代表

        :param enter_basic:
        :param leaving_basic:
        :param highlight:
        :return:
        """
        # 扩展表标题 第一行
        print(f'{"Basic":<10} {"Equation":<10} {"Z":<8}', end='')
        for i in range(len(self.variables)):
            var = self.variables[i]
            if i == enter_basic:  # 用红色显示入基变量
                print(f' {Color.Red}{var:<8}{Color.Reset}', end='')
            else:
                print(f' {var:<8}', end='')
        if highlight:
            print(f'{"Right":<8} {"Ratio":<10}')
        else:
            print(f'{"Right":<8}')

        # 扩展表标题 第二行
        print(f'{"Variables":<10} {"":<10} {"":<8}', end='')
        print(' ' * len(self.variables) * 9, end='')
        print(f'{"Side":<8}')

        # 扩展表内容
        for i in range(len(self.basic_variables)):
            if i == 0:
                print(f"{'obj.':<10} {'(' + str(i) + ')':<10}", end='')
            elif i == leaving_basic:  # 用紫色显示出基变量系数
                print(f'{Color.Magenta}{self.variables[self.basic_variables[i]]:<10} {"(" + str(i) + ")":<10}{Color.Reset}', end='')
            else:
                print(f'{self.variables[self.basic_variables[i]]:<10} {"(" + str(i) + ")":<10}', end='')

            equation_left = self.left_side[i]
            for j in range(len(equation_left)):
                c = equation_left[j]
                if j == enter_basic + 1:  # 用红色显示入基变量系数
                    print(f' {Color.Red}{c:<8}{Color.Reset}', end='')
                elif i == leaving_basic:  # 用紫色显示出基变量系数
                    print(f' {Color.Magenta}{c:<8}{Color.Reset}', end='')
                else:
                    print(f' {c:<8}', end='')

            if i == leaving_basic:  # 用紫色显示出基变量系数
                print(Color.Magenta, end='')
            print(f'{self.right_side[i]:<8}', end='')
            if highlight:
                print(f' {self.ratio[i] :<10}', end='')
            print(Color.Reset)

    def _eliminate_artificials(self):
        artificials = self.artificial_variables[:]
        eq0 = self.left_side[0]
        for i in artificials:
            index = self.basic_variables.index(i)
            eq = self.left_side[index]
            co_of_artificial = eq0[i + 1]
            for j in range(len(eq)):
                eq0[j] -= co_of_artificial * eq[j]
            self.right_side[0] -= co_of_artificial * self.right_side[index]

    def solve(self):
        print("Intial form:")
        print('---------------------------------')
        self._display(highlight=False)
        print()
        print("Converting Equaiton(0) to proper form:")
        print('---------------------------------')
        self._eliminate_artificials()
        self._display(highlight=False)
        iteration = 0
        while True:
            iteration += 1
            print(f'iteration {iteration}:')
            print('---------------------------------')
            # Optimality Test
            # find the variable with the minimum negative coeffecient
            eq0 = self.left_side[0]
            min_v = FractionWithM(0)
            min_i = -1
            for i in range(1, len(eq0)):
                if eq0[i] < min_v:
                    min_v = eq0[i]
                    min_i = i
            if min_v == 0:
                print("The solution is optimal")
                break
            enter_basic = min_i

            # Minumum Ratio Test
            min_ratio = None
            min_i = -1
            for i in range(1, len(self.left_side)):
                eq = self.left_side[i]
                if eq[enter_basic] == 0:
                    self.ratio[i] = ''
                else:
                    denominator = eq[enter_basic]
                    if denominator <= 0:
                        self.ratio[i] == ''
                    else:
                        self.ratio[i] = self.right_side[i] / denominator
                        if min_ratio is None or self.ratio[i] < min_ratio:
                            min_ratio = self.ratio[i]
                            min_i = i
            if min_i == -1:
                print("can't find the minimum ratio!")
                return
            leaving_basic_eq_index = min_i
            leaving_basic = self.basic_variables[min_i]

            self._display(enter_basic-1,leaving_basic_eq_index)
            print("Entering basic :", self.variables[enter_basic - 1])
            print("leaving basic:", self.variables[leaving_basic])

            # Gaussian Elimination
            leaving_basic_eq = self.left_side[min_i]
            denominator = leaving_basic_eq[enter_basic]
            for i in range(len(leaving_basic_eq)):
                leaving_basic_eq[i] /= denominator
            self.right_side[min_i] /= denominator
            self.basic_variables[min_i] = enter_basic - 1
            for i in range(len(self.left_side)):
                if i == min_i:
                    continue
                eq = self.left_side[i]
                multiple = eq[enter_basic]
                for j in range(len(eq)):
                    eq[j] -= multiple * leaving_basic_eq[j]
                self.right_side[i] -= multiple * self.right_side[min_i]

        self._display(highlight = False)
        self._display_solution()

    def _display_solution(self):
        print("The optiomal solution:")
        for i in self.real_variables:
            found = False
            for j in range(1, len(self.basic_variables)):
                basic_variable = self.basic_variables[j]
                if i == basic_variable:
                    print(f'{self.variables[i]}: {self.right_side[j]}')
                    found = True
                    break
            if not found:
                print(f'{self.variables[i]}: 0')
        print("objective value: ", self.right_side[0] * self.left_side[0][0])
        print("shadow price:")
        eq0 = self.left_side[0]
        for i in range(1, len(self.left_side)):
            slack_index = len(self.real_variables) - 1 + i
            print(f"shadow price for constaint {i}:", eq0[slack_index + 1])


model = Model(type=OptimizationType.minimization, x1=Fraction(4, 10), x2=Fraction(5, 10))
model.add_less_constraint(Fraction(27, 10), x1=Fraction(3, 10), x2=Fraction(1, 10))
model.add_equal_constraint(6, x1=Fraction(5, 10), x2=Fraction(5, 10))
model.add_greater_constraint(6, x1=Fraction(6, 10), x2=Fraction(4, 10))
model.solve()

