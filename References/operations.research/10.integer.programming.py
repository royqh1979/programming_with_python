"""
用分支定界法求解整数规划问题

算法描述见 《运筹学导论》第8版 Introduction to Operations Research 清华大学出版社 第11.6章

其中，使用两阶段法求解松弛整数约束后的线性规划问题

"""
import sys
from fractions import Fraction
from enum import Enum
import heapq
from decimal import Decimal
from typing import Union, List, Optional, Dict

import operator as op
import math
import copy

import colorama
from colorama import Fore,Style

# init windows ansi color
colorama.init()

class OptimizationType(Enum):
    maximization = 1
    minimization = 2


Rational = Union[int, Fraction]
Rational_Values = Union[int, str, Fraction, Decimal]


class LinearModel:
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
                print(kwargs)
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


class ConstraintType(Enum):
    LessEqual = 1
    GreaterEqual = 2
    Equal = 3


class Constraint:
    def __init__(self, left: Dict[str, Rational], constraint_type: ConstraintType, right_value: Rational):
        self.left = left
        self.type = constraint_type
        self.right = right_value


def is_integer(value):
    if isinstance(value, int):
        return True
    if isinstance(value, Fraction) and value.denominator == 1:
        return True
    return False


def get_ceil(value):
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return value
        return value.numerator // value.denominator + 1


def get_floor(value):
    if isinstance(value, int):
        return value
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return value
        return value.numerator // value.denominator


class MaxSearchNode:
    def __init__(self, lower_bounds: Dict[str, Rational], upper_bounds: Dict[str, Rational], optimize_limit: Rational):
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.optimize_limit = optimize_limit
        self.splits = []

    def __lt__(self, other):
        return self.optimize_limit > other.optimize_limit

    def __eq__(self, other):
        return self.optimize_limit == other.optimize_limit

class MinSearchNode:
    def __init__(self, lower_bounds: Dict[str, Rational], upper_bounds: Dict[str, Rational], optimize_limit: Rational):
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.optimize_limit = optimize_limit
        self.splits = []

    def __lt__(self, other):
        return self.optimize_limit < other.optimize_limit

    def __eq__(self, other):
        return self.optimize_limit == other.optimize_limit


class IntegerModel:
    def __init__(self, opt_type: OptimizationType = OptimizationType.maximization, **kwargs):
        self.variable_names = set()  # 优化目标中包含的变量
        self.objective = {}  # 最终的优化目标
        self.type = opt_type  # 优化类型 （最大化/最小化）
        self.constraints = []  # 约束式
        self.lower_bounds = {}
        self.upper_bounds = {}

        self.int_constarints = {}
        for v in kwargs:
            self.variable_names.add(v)
            self.int_constarints[v] = False
            self.objective[v] = Fraction(kwargs[v])
            self.lower_bounds[v] = 0
            self.upper_bounds[v] = sys.maxsize

    def add_integer_constraint(self, var_name: str):
        """
        添加整数约束
        :param var_name: 必须为整数的变量名
        :return:
        """
        if var_name not in self.variable_names:
            raise RuntimeError(f"{var_name} is not in objective function!")
        self.int_constarints[var_name] = True

    def add_constraint(self, constraint: Rational_Values, constraint_type: ConstraintType, **kwargs):
        """
        添加约束

        :param constraint: 约束（不）等式右侧常数
        :param constraint_type: 约束类型（大于等于，小于等于，等于）
        :param kwargs: 不等式左侧各变量系数
        """

        if len(kwargs) == 1:
            var_name = list(kwargs.keys())[0]
            if constraint_type == ConstraintType.GreaterEqual:
                value = kwargs[var_name]
                old_bound = self.lower_bounds[var_name]
                new_bound = max(value, old_bound)
                if new_bound > self.upper_bounds[var_name]:
                    raise RuntimeError("lower bound greater than upper bound!")
                self.lower_bounds[var_name] = new_bound
            elif constraint_type == ConstraintType.LessEqual:
                value = kwargs[var_name]
                old_bound = self.upper_bounds[var_name]
                new_bound = min(value, old_bound)
                if new_bound < self.lower_bounds[var_name]:
                    raise RuntimeError("lower bound greater than upper bound!")
                self.upper_bounds[var_name] = new_bound
            else:
                value = kwargs[var_name]
                if not (self.lower_bounds[var_name] <= value <= self.upper_bounds[var_name]):
                    raise RuntimeError("bound error!")
                self.upper_bounds[var_name] = value
                self.lower_bounds[var_name] = value
        else:
            right = Fraction(constraint)
            left = {}
            for var_name in kwargs:
                left[var_name] = Fraction(kwargs[var_name])
            constraint = Constraint(left, constraint_type, right)
            self.constraints.append(constraint)

    def add_less_constraint(self, constraint, **kwargs):
        """
        添加小于等于约束

        :param constraint: 约束（不）等式右侧常数
        :param kwargs: 不等式左侧各变量系数
        """
        self.add_constraint(constraint, ConstraintType.LessEqual, **kwargs)

    def add_greater_constraint(self, constraint, **kwargs):
        """
        添加大于等于约束

        :param constraint: 约束（不）等式右侧常数
        :param kwargs: 不等式左侧各变量系数
        """
        self.add_constraint(constraint, ConstraintType.GreaterEqual, **kwargs)

    def add_equal_constraint(self, constraint, **kwargs):
        """
        添加等于约束

        :param constraint: 约束（不）等式右侧常数
        :param kwargs: 不等式左侧各变量系数
        """
        self.add_constraint(constraint, ConstraintType.Equal, **kwargs)

    def _integer_constraints_test(self, optimal_values):
        """
        检查最优解是否完全满足整数约束条件

        :param optimal_values:
        :return: 是否满足整数约束条件, 违反约束条件的变量名
        """
        for var_name in optimal_values:
            if self.int_constarints[var_name] and not is_integer(optimal_values[var_name]):
                return False, var_name
        return True, None

    def _calculate_known_vars(self, lower_bounds, upper_bounds):
        """
        根据各变量的上下限，找出存在根据整数约束条件，存在唯一解的变量
        :param lower_bounds: 各变量的上限
        :param upper_bounds: 各变量的下限
        :return: 如果不存在无解变量，则返回 False,字典(关键字为存在到唯一解的变量名，对应的值其对应的解)
            如果存在无解变量，则返回True,无解变量列表
        """
        known_vars = {}
        no_solutions = []
        for var_name in self.variable_names:
            if upper_bounds[var_name] < lower_bounds[var_name]:
                no_solutions.append(var_name)
                continue
            if self.int_constarints[var_name]:
                upper = get_ceil(upper_bounds[var_name])
                lower = get_floor(lower_bounds[var_name])
                if upper == lower:
                    known_vars[var_name] = upper
                elif lower > upper:
                    no_solutions.append(var_name)
        if len(no_solutions) > 0:
            return True, no_solutions
        return False, known_vars

    def solve(self):
        """
        对模型求解
        """
        #
        # initial
        if self.type == OptimizationType.maximization:
            QueueNode = MaxSearchNode
            cmp_op = op.gt
        else:
            QueueNode = MinSearchNode
            cmp_op = op.lt
        queue:List[QueueNode] = [] # 使用堆来存储，关键字为优化值上/下限
        node = QueueNode(lower_bounds=self.lower_bounds,
                         upper_bounds=self.upper_bounds,
                         optimize_limit=sys.maxsize)

        heapq.heappush(queue, node)

        known_optimal_value = -sys.maxsize
        known_optimal_vars = None

        while len(queue) > 0:
            node = heapq.heappop(queue) # 从堆中取出优化值最优的待选项
            if  cmp_op(known_optimal_value,node.optimize_limit):
                # 如果已知的最优值比待选的最优化值还优，不必继续找了
                break
            print('---------------------------------------------------')
            if len(node.splits)>0:
                print("split constraints:")
                for split in node.splits:
                    print("    ",split)
            objective = self.objective.copy()
            lower_bounds = node.lower_bounds.copy()
            upper_bounds = node.upper_bounds.copy()

            # 尝试用各变量的上下限约束夹逼确定该变量的解
            no_solution, known_vars = self._calculate_known_vars(lower_bounds, upper_bounds)
            if no_solution:  # 无满足条件解（某整数变量的上下限之间不存在整数）
                continue

            # 从优化目标函数中删除已得到整数解的变量
            basic_object_value = 0
            for var_name in known_vars:
                var_val = known_vars[var_name]
                if var_name in self.objective:
                    basic_object_value += self.objective[var_name] * var_val
                    del objective[var_name]

            # 从约束式中删除已得到整数解的变量
            constraints = []
            for constraint in self.constraints:
                constraint = copy.copy(constraint)
                left = constraint.left.copy()
                right = constraint.right
                for var_name in known_vars:
                    var_val = known_vars[var_name]
                    if var_name in left:
                        right -= left[var_name] * var_val
                        del left[var_name]
                constraint.left = left
                constraint.right = right
                constraints.append(constraint)

            # 建立对应的线性规划模型
            model = LinearModel(opt_type=self.type, enable_log=False, **objective)

            for constraint in constraints:
                params = constraint.left
                if constraint.type == ConstraintType.LessEqual:
                    model.add_less_constraint(constraint.right, **params)
                elif constraint.type == ConstraintType.GreaterEqual:
                    model.add_greater_constraint(constraint.right, **params)
                else:
                    model.add_equal_constraint(constraint.right, **params)
            # 将各变量的上下限也作为约束式加入线性规划模型
            for var_name in self.variable_names:
                if var_name in known_vars:
                    continue
                lower = lower_bounds[var_name]
                upper = upper_bounds[var_name]
                params = {var_name: 1}
                if lower > 0:
                    model.add_greater_constraint(lower, **params)
                if upper < sys.maxsize:
                    model.add_less_constraint(upper, **params)

            # 对线性规划问题求解
            object_value, var_values = model.solve()
            print("----------------------")
            if object_value is None: # 无解
                print("no solution")
                continue
            # 有解
            object_value += basic_object_value
            var_values.update(known_vars)
            print("object:", object_value)
            for var_name in var_values:
                print(f"{var_name} : {var_values[var_name]}")

            # 如果放松后的线性规划解优于已知最优解，则继续，否则丢弃该搜索方向
            if cmp_op(object_value , known_optimal_value):
                integer_ok, non_int_var_name = self._integer_constraints_test(var_values)
                if integer_ok: # 如果满足所有整数约束，更新最优解
                    known_optimal_value = object_value
                    known_optimal_vars = var_values
                else: # 不满足所有整数约束，产生分支以继续搜索
                    self._split(queue, node, object_value, non_int_var_name, var_values[non_int_var_name])

        print('---------------')
        if known_optimal_value is None:
            print("Don't find solution!")
            return None,None
        else:
            print("The final result object:", known_optimal_value)
            for var_name in known_optimal_vars:
                print(f"{var_name} : {known_optimal_vars[var_name]}")
            return known_optimal_value,known_optimal_vars

    def _split(self, queue, node, optimal_value_limit, split_var_name, split_value):
        """
        在当前搜索节点基础上，分支产生新的搜索节点

        :param queue: 搜索节点队列（实际为堆（heap)）
        :param node: 当前搜索节点
        :param optimal_value_limit: 最优值的上或者下限
        :param split_var_name: 用于产生分支的变量名
        :param split_value: 分支变量对应的值
        """
        if self.type == OptimizationType.maximization:
            SearchNode = MaxSearchNode
        else:
            SearchNode = MinSearchNode

        print(f"split {split_var_name}: {split_value}")
        old_lower = node.lower_bounds[split_var_name]
        old_upper = node.upper_bounds[split_var_name]
        new_node1 = SearchNode(lower_bounds=node.lower_bounds.copy(),
                              upper_bounds=node.upper_bounds.copy(),
                              optimize_limit=optimal_value_limit
                              )
        new_node1.upper_bounds[split_var_name] = min(old_upper, int(math.floor(split_value)))
        new_node1.splits=node.splits.copy()
        new_node1.splits.append(f"{split_var_name}<={new_node1.upper_bounds[split_var_name]}")
        heapq.heappush(queue, new_node1)

        new_node2 = SearchNode(lower_bounds=node.lower_bounds.copy(),
                               upper_bounds=node.upper_bounds.copy(),
                               optimize_limit=optimal_value_limit)
        new_node2.lower_bounds[split_var_name] = max(old_lower, int(math.ceil(split_value)))
        new_node2.splits=node.splits.copy()
        new_node2.splits.append(f"{split_var_name}>={new_node2.lower_bounds[split_var_name]}")
        heapq.heappush(queue, new_node2)


# model = IntegerModel(x1=4, x2=-2, x3=7, x4=-1)
# model.add_less_constraint(10, x1=1, x3=5)
# model.add_less_constraint(1, x1=1, x2=1, x3=-1)
# model.add_less_constraint(0, x1=6, x2=-5)
# model.add_less_constraint(3, x1=-1, x3=2, x4=-2)
# model.add_integer_constraint('x1')
# model.add_integer_constraint('x2')
# model.add_integer_constraint('x3')
# model.solve()

model = IntegerModel(x1=50, x2=30)
model.add_less_constraint(125, x1=4, x2=3)
model.add_less_constraint(50, x1=2, x2=1)
model.add_integer_constraint('x1')
model.add_integer_constraint('x2')
model.solve()
