"""
两阶段单纯形法


算法描述见 《运筹学导论》第8版 Introduction to Operations Research 清华大学出版社 第4.6章

"""
from decimal import Decimal
from fractions import Fraction
from enum import Enum
from typing import Union
import colorama
from colorama import Fore,Style

# init windows ansi color
colorama.init()

class OptimizationType(Enum):
    maximization = 1
    minimization = 2

Rational = Union[int, Fraction]
Rational_Values = Union[int, str, Fraction, Decimal]

class Model:
    """
    两阶段线性规划模型
    """

    def __init__(self, opt_type: OptimizationType = OptimizationType.maximization, enable_log: bool = True, **kwargs):
        """
        构造方法

        :param opt_type: 目标函数类型（最大化/最小化）
        :param enable_log: 是否显示步骤提示信息
        :param kwargs: 目标函数各变量及其系数
        """
        self.variable_names = []  # 所有变量的变量名，包括松弛变量
        self.original_variables = []  # 优化目标中包含的变量(元素为变量在variables_names列表中的下标）
        self.left_side = []  # 存储 扩展后方程组左侧的各变量系数
        self.right_side = []  # 存储 扩展后方程组右侧的常数
        self.ratio = []  # 存储各方程组的离速(ratio)
        self.basic_variables = []  # 基变量列表(元素为变量在variables_names列表中的下标）
        self.slack_variables = []  # 松弛变量列表(元素为变量在variables_names列表中的下标）
        self.artificial_variables = []  # 人工变量列表(元素为变量在variables_names列表中的下标）
        self.surplus_variables = []  # 剩余变量(元素为变量在variables_names列表中的下标）
        self.objective = []  # 扩展后的目标函数中各变量系数
        self.type = opt_type  # 规划类型
        self.enable_log = enable_log

        if opt_type == OptimizationType.maximization:
            equation0 = [1]
            for v in kwargs:
                self.variable_names.append(v)
                self.original_variables.append(len(self.variable_names) - 1)
                equation0.append(-Fraction(kwargs[v]))
        else:
            equation0 = [-1]
            for v in kwargs:
                self.variable_names.append(v)
                self.original_variables.append(len(self.variable_names) - 1)
                equation0.append(Fraction(kwargs[v]))

        self.objective = equation0
        self.left_side.append([])
        self.right_side.append(0)
        self.ratio.append('')
        self.basic_variables.append(None)

    def add_equal_constraint(self, constraint:Rational_Values, **kwargs)->None:
        """
        添加相等约束

        :param constraint: 约束等式右侧的常数
        :param kwargs: 约束等式左侧各变量及其系数
        """

        # 确保右侧常数大于等于0
        constraint = Fraction(constraint)
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_equal_constraint(-constraint, **kwargs)
            return

        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(0)
        eq = [0]
        for var_name in self.variable_names:
            if var_name in kwargs:
                eq.append(Fraction(kwargs[var_name]))
            else:
                eq.append(0)
        eq.append(1)
        self.left_side.append(eq)
        self.variable_names.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)
        self.right_side.append(constraint)
        self.ratio.append('')

    def add_greater_constraint(self, constraint: Rational_Values, **kwargs)->None:
        """
        添加大于等于约束

        :param constraint: 约束等式右侧的常数
        :param kwargs: 约束等式左侧各变量及其系数
        """
        # 确保右侧常数大于等于0
        constraint = Fraction(constraint)
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_less_constraint(-constraint, **kwargs)
            return

        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(0)
            eq.append(0)
        eq = [0]
        for var_name in self.variable_names:
            if var_name in kwargs:
                eq.append(Fraction(kwargs[var_name]))
            else:
                eq.append(0)
        eq.append(-1)
        eq.append(1)
        self.left_side.append(eq)
        self.variable_names.append('_ss' + str(len(self.surplus_variables) + 1))
        self.surplus_variables.append(len(self.variable_names) - 1)
        self.variable_names.append('_a' + str(len(self.artificial_variables) + 1))
        self.artificial_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)
        self.right_side.append(constraint)
        self.ratio.append('')

    def add_less_constraint(self, constraint, **kwargs):
        """
        添加大于等于约束

        :param constraint: 约束等式右侧的常数
        :param kwargs: 约束等式左侧各变量及其系数
        """
        # 确保右侧常数大于等于0
        constraint = Fraction(constraint)
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_greater_constraint(-constraint, **kwargs)
            return

        for i in range(1, len(self.left_side)):
            eq = self.left_side[i]
            eq.append(0)
        eq = [0]
        for var_name in self.variable_names:
            if var_name in kwargs:
                eq.append(Fraction(kwargs[var_name]))
            else:
                eq.append(0)
        eq.append(1)
        self.left_side.append(eq)
        self.variable_names.append('_s' + str(len(self.slack_variables) + 1))
        self.slack_variables.append(len(self.variable_names) - 1)
        self.basic_variables.append(len(self.variable_names) - 1)
        self.right_side.append(constraint)
        self.ratio.append('')

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

    def _prepare_first_phase(self):
        eq0 = [0] * len(self.variable_names)
        for i in self.artificial_variables:
            eq0[i] = 1
        eq0 = [-1] + eq0
        self.right_side[0] = 0
        for i in self.artificial_variables:
            artificial_index = self.basic_variables.index(i)
            basic_eq = self.left_side[artificial_index]
            for j in range(len(basic_eq)):
                eq0[j] -= basic_eq[j]
            self.right_side[0] -= self.right_side[artificial_index]
        self.left_side[0] = eq0

    def _solve(self):
        iteration = 0
        while True:
            iteration += 1
            if self.enable_log:
                print(f'iteration {iteration}:')
                print('---------------------------------')
            # Optimality Test
            # find the variable with the minimum negative coeffecient
            eq0 = self.left_side[0]
            min_v = 0
            min_i = -1
            for i in range(1, len(eq0)):
                if eq0[i] < min_v:
                    min_v = eq0[i]
                    min_i = i
            if min_v == 0:
                if self.enable_log:
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
                        self.ratio[i] = ''
                    else:
                        self.ratio[i] = self.right_side[i] / denominator
                        if min_ratio is None or self.ratio[i] < min_ratio:
                            min_ratio = self.ratio[i]
                            min_i = i
            if min_i == -1:
                if self.enable_log:
                    print("can't find the minimum ratio!")
                return False
            leaving_basic_eq_index = min_i
            leaving_basic = self.basic_variables[min_i]
            if self.enable_log:
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

        if self.enable_log:
            self._display()
        return True

    def _prepare_second_pass(self):
        basic_vars = []
        for i in self.basic_variables:
            if i is None:
                continue
            basic_vars.append(self.variable_names[i])
        # drop artificial variables
        var_names = []
        for i in range(0, len(self.variable_names)):
            if i not in self.artificial_variables:
                var_names.append(self.variable_names[i])
        self.variable_names = var_names
        for i in range(len(self.left_side)):
            old_eq = self.left_side[i]
            new_eq = []
            for j in range(len(old_eq)):
                if (j - 1) not in self.artificial_variables:
                    new_eq.append(old_eq[j])
            self.left_side[i] = new_eq

        self.basic_variables = [None]
        for var_name in basic_vars:
            self.basic_variables.append(self.variable_names.index(var_name))

        for i in range(len(self.objective)):
            self.left_side[0][i] = self.objective[i]

        # Restore proper form for gause elimination
        # eliminate basic variables from equation 0
        eq0 = self.left_side[0]
        for i in range(1, len(self.basic_variables)):
            basic_variable = self.basic_variables[i]
            if eq0[basic_variable + 1] == 0:
                continue
            basic_eq = self.left_side[i]
            coefficient = eq0[basic_variable + 1]
            for j in range(len(basic_eq)):
                eq0[j] -= coefficient * basic_eq[j]
            self.right_side[0] -= coefficient * self.right_side[i]

    def _prepare(self):
        self.left_side[0] = self.objective[:] + [0] * len(self.slack_variables)

    def _no_feasible_solution_test(self):
        for i in self.artificial_variables:
            if i in self.basic_variables:
                return True
        return False

    def solve(self):
        if len(self.artificial_variables) > 0:
            if self.enable_log:
                print("======First Phase=======:")
            self._prepare_first_phase()
            solve_ok = self._solve()  # solve first phase
            if not solve_ok:
                if self.enable_log:
                    print("No feasible solution!")
                return None, None

            if self._no_feasible_solution_test():
                if self.enable_log:
                    print("~~~~~~~~~~~~~~~~~~~~~~")
                    print("Some artificial variable is none zero!")
                    print("No feasible solution!")
                return None, None
            if self.enable_log:
                print("======Second Phase=======:")
            self._prepare_second_pass()
            solve_ok = self._solve()  # solve the second phase
            if not solve_ok:
                if self.enable_log:
                    print("No feasible solution!")
                return None, None
        else:
            self._prepare()
            self._solve()
        if self.enable_log:
            self._display_solution()
        return self.get_result()

    def _display_solution(self):
        print("The optiomal solution:")
        object_value, params = self.get_result()
        for var_name in params:
            print(f'{var_name}: {params[var_name]}')
        print("objective value: ", object_value)

    def get_result(self):
        object_value = self.right_side[0] * self.left_side[0][0]
        params = {}
        for i in self.original_variables:
            found = False
            for j in range(1, len(self.basic_variables)):
                basic_variable = self.basic_variables[j]
                if i == basic_variable:
                    params[self.variable_names[i]] = self.right_side[j]
                    found = True
                    break
            if not found:
                params[self.variable_names[i]] = 0
        return object_value, params

# model = Model(opt_type=OptimizationType.minimization, x1='0.4', x2='0.5')
# model.add_less_constraint('2.7', x1='0.3', x2='0.1')
# model.add_equal_constraint(6, x1='0.5', x2='0.5')
# model.add_greater_constraint(6, x1='0.6', x2='0.4')
# model.solve()

model = Model(opt_type=OptimizationType.minimization, x1=2,x2=3,x3=2)
model.add_greater_constraint(8,x1=1,x2=4,x3=2)
model.add_greater_constraint(6,x1=3,x2=2,x3=0)
model.solve()

# model = Model(x1=3,x2=5)
# model.add_less_constraint(4,x1=1)
# model.add_less_constraint(12,x2=2)
# model.add_less_constraint(18,x1=3,x2=2)
# model.solve()

# No feasible solution
# model = Model(opt_type=OptimizationType.minimization, x1=Fraction(4, 10), x2=Fraction(5, 10))
# model.add_less_constraint(Fraction(18, 10), x1=Fraction(3, 10), x2=Fraction(1, 10))
# model.add_equal_constraint(6, x1=Fraction(5, 10), x2=Fraction(5, 10))
# model.add_greater_constraint(6, x1=Fraction(6, 10), x2=Fraction(4, 10))
# model.solve()

# model = Model(opt_type=OptimizationType.minimization,x1=3,x2=2,x3=4)
# model.add_greater_constraint(8,x1=2,x2=1,x3=3)
# model.add_greater_constraint(6,x1=3,x2=3,x3=5)
# model.solve()