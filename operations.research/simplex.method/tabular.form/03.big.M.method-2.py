"""
大M法（带人工变量的单纯形法）

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
或者 变量的线性组合 = 常数 形式
或者 变量的线性组合 >= 常数 形式

算法描述见 《运筹学导论》第8版 Introduction to Operations Research 清华大学出版社 第4.6章
"""
from bigm import FractionWithM
from fractions import Fraction
from enum import Enum
import colorama
from colorama import Fore,Style

# init windows ansi color
colorama.init()

class OptimizationType(Enum):
    maximization = 1
    minimization = 2


class Model:
    def __init__(self, type=OptimizationType.maximization, **kwargs):
        self.variable_names = []  # 所有变量，包括松弛变量
        self.original_variables = []  # 优化目标中包含的变量
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
                self.variable_names.append(v)
                self.original_variables.append(len(self.variable_names) - 1)
                eq0.append(FractionWithM(-kwargs[v]))
        else:
            eq0 = [FractionWithM(-1)]
            for v in kwargs:
                self.variable_names.append(v)
                self.original_variables.append(len(self.variable_names) - 1)
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
        for var in self.variable_names:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variable_names.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)

    def add_greater_constraint(self, constraint, **kwargs):
        eq0 = self.left_side[0]
        eq0.append(FractionWithM(0))
        eq0.append(FractionWithM(M=1, value=0))
        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(FractionWithM(0))
            eq.append(FractionWithM(0))
        eq = [FractionWithM(0)]
        for var in self.variable_names:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(-1))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variable_names.append('_ss' + str(len(self.surplus_variables) + 1))
        self.surplus_variables.append(len(self.variable_names) - 1)
        self.variable_names.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)

    def add_less_constraint(self, constraint, **kwargs):
        for eq in self.left_side:
            eq.append(FractionWithM(0))
        eq = [FractionWithM(0)]
        for var in self.variable_names:
            if var in kwargs:
                eq.append(FractionWithM(kwargs[var]))
            else:
                eq.append(FractionWithM(0))
        eq.append(FractionWithM(1))
        self.left_side.append(eq)
        self.right_side.append(FractionWithM(constraint))
        self.ratio.append('')
        self.variable_names.append('_s' + str(len(self.slack_variables) + 1))
        self.slack_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)

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
        for i in range(len(self.variable_names)):
            var_name = self.variable_names[i]
            if i==enter_basic: # 用红色显示入基变量
                print(f' {Fore.RED}{var_name:<8}{Style.RESET_ALL}',end='')
            else:
                print(f' {var_name:<8}',end='')
        if highlight:
            print(f'{"Right":<8} {"Ratio":<10}')
        else:
            print(f'{"Right":<8}')

        # 扩展表标题 第二行
        print(f'{"Variables":<10} {"":<10} {"":<8}',end='')
        print(' ' * len(self.variable_names) * 9, end='')
        print(f'{"Side":<8}')

        # 扩展表内容
        for i in range(len(self.basic_variables)):
            if i==0:
                print(f"{'obj.':<10} {'('+str(i)+')':<10}",end='')
            elif i == leaving_basic:  # 用紫色显示出基变量系数
                print(f'{Fore.MAGENTA}{self.variable_names[self.basic_variables[i]]:<10} {"(" + str(i) + ")":<10}{Style.RESET_ALL}', end='')
            else:
                print(f'{self.variable_names[self.basic_variables[i]]:<10} {"(" + str(i) + ")":<10}', end='')

            equation_left=self.left_side[i]
            for j in range(len(equation_left)):
                c=equation_left[j]
                if j == enter_basic+1:  # 用红色显示入基变量系数
                    print(f' {Fore.RED}{str(c):<8}{Style.RESET_ALL}', end='')
                elif i == leaving_basic: # 用紫色显示出基变量系数
                    print(f' {Fore.MAGENTA}{str(c):<8}{Style.RESET_ALL}', end='')
                else:
                    print(f' {str(c):<8}', end='')

            if i == leaving_basic:  # 用紫色显示出基变量系数
                print(Fore.MAGENTA,end='')
            print(f'{str(self.right_side[i]):<8}', end='')
            if highlight:
                print(f' {str(self.ratio[i]) :<10}',end='')
            print(Style.RESET_ALL)

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
            print("Entering basic :", self.variable_names[enter_basic - 1])
            print("leaving basic:", self.variable_names[leaving_basic])

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
        for i in self.original_variables:
            found = False
            for j in range(1, len(self.basic_variables)):
                basic_variable = self.basic_variables[j]
                if i == basic_variable:
                    print(f'{self.variable_names[i]}: {self.right_side[j]}')
                    found = True
                    break
            if not found:
                print(f'{self.variable_names[i]}: 0')
        print("objective value: ", self.right_side[0] * self.left_side[0][0])
        print("shadow price:")
        eq0 = self.left_side[0]
        for i in range(1, len(self.left_side)):
            slack_index = len(self.original_variables) - 1 + i
            print(f"shadow price for constaint {i}:", eq0[slack_index + 1])


# model = Model(type=OptimizationType.minimization, x1=Fraction(4, 10), x2=Fraction(5, 10))
# model.add_less_constraint(Fraction(27, 10), x1=Fraction(3, 10), x2=Fraction(1, 10))
# model.add_equal_constraint(6, x1=Fraction(5, 10), x2=Fraction(5, 10))
# model.add_greater_constraint(6, x1=Fraction(6, 10), x2=Fraction(4, 10))
# model.solve()

model = Model(type=OptimizationType.minimization, x1=2,x2=3,x3=2)
model.add_greater_constraint(8,x1=1,x2=4,x3=2)
model.add_greater_constraint(6,x1=3,x2=2,x3=0)
model.solve()

