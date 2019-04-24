"""
大M法（带人工变量的单纯形法）

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
或者 变量的线性组合 = 常数 形式
或者 变量的线性组合 >= 常数 形式

"""
import sys
from decimal import Decimal
from fractions import Fraction
from enum import Enum
import heapq
from typing import Optional, Union

import math


class OptimizationType(Enum):
    maximization = 1
    minimization = 2


class LinearModel:
    def __init__(self, type=OptimizationType.maximization, enable_log=True, **kwargs):
        self.variable_names = []  # 所有变量的变量名，包括松弛变量
        self.real_variables = []  # 优化目标中包含的变量
        self.left_side = []  # 存储扩展后方程组左侧的系数
        self.right_side = []  # 存储扩展后方程组右侧的常数
        self.ratio = []  # 存储各方程组的离速
        self.basic_variables = []  # 基变量列表
        self.slack_variables = []  # 松弛变量列表
        self.artificial_variables = []  # 人工变量列表
        self.surplus_variables = []  # 剩余变量
        self.objective = []  # 最终的优化目标
        self.type = type
        self.enable_log = enable_log

        if type == OptimizationType.maximization:
            equation0 = [1]
            for v in kwargs:
                self.variable_names.append(v)
                self.real_variables.append(len(self.variable_names) - 1)
                equation0.append(-Fraction(kwargs[v]))
        else:
            equation0 = [-1]
            for v in kwargs:
                self.variable_names.append(v)
                self.real_variables.append(len(self.variable_names) - 1)
                equation0.append(Fraction(kwargs[v]))

        self.objective = equation0
        self.left_side.append([])
        self.right_side.append(0)
        self.ratio.append('')
        self.basic_variables.append(None)

    def add_equal_constraint(self, constraint, **kwargs):
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_equal_constraint(-constraint, **kwargs)
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
        self.right_side.append(Fraction(constraint))
        self.ratio.append('')

    def add_greater_constraint(self, constraint, **kwargs):
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_less_constraint(-constraint, **kwargs)
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
        self.right_side.append(Fraction(constraint))
        self.ratio.append('')

    def add_less_constraint(self, constraint, **kwargs):
        if constraint < 0:
            for var_name in kwargs:
                kwargs[var_name] = -kwargs[var_name]
            self.add_greater_constraint(-constraint, **kwargs)
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
        self.right_side.append(Fraction(constraint))
        self.ratio.append('')

    def _display(self):
        print(f'BV.\t\tEq.\t\tZ', end='')
        for var in self.variable_names:
            print(f'\t\t{var}', end='')
        print('\t\tRight\t\tRatio')

        for i in range(len(self.basic_variables)):
            if i == 0:
                print(f"obj\t\t({i})", end='')
            else:
                print(f'{self.variable_names[self.basic_variables[i]]}\t\t({i})', end='')
            eq = self.left_side[i]
            for c in eq:
                print(f'\t\t{c}', end='')
            print(f'\t\t{self.right_side[i]}', end='')
            print(f'\t\t{self.ratio[i]}')

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
        if self.enable_log:
            self._display()
        while True:
            iteration += 1
            if self.enable_log:
                print(f'iteration {iteration}:')
                print('---------------------------------')
                print("Optimality Test:")
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
            if self.enable_log:
                print("Entering basic :", self.variable_names[enter_basic - 1])

            if self.enable_log:
                print("Minumum Ratio Test:")
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
                if self.enable_log:
                    print("can't find the minimum ratio!")
                return False
            leaving_basic = self.basic_variables[min_i]
            if self.enable_log:
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
        for i in range(0,len(self.variable_names)):
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

        self.basic_variables=[None]
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
                return None,None

            if self._no_feasible_solution_test():
                if self.enable_log:
                    print("~~~~~~~~~~~~~~~~~~~~~~")
                    print("Some artificial variable is none zero!")
                    print("No feasible solution!")
                return None,None
            if self.enable_log:
                print("======Second Phase=======:")
            self._prepare_second_pass()
            solve_ok = self._solve()  # solve the second phase
            if not solve_ok:
                if self.enable_log:
                    print("No feasible solution!")
                return None,None
        else:
            self._prepare()
            self._solve()
        if self.enable_log:
            self._display_solution()
        return self.get_result()

    def _display_solution(self):
        print("The optiomal solution:")
        object, params = self.get_result()
        for var_name in params:
            print(f'{var_name}: {params[var_name]}')
        print("objective value: ", object)

    def get_result(self):
        object = self.right_side[0] * self.left_side[0][0]
        params = {}
        for i in self.real_variables:
            found = False
            for j in range(1, len(self.basic_variables)):
                basic_variable = self.basic_variables[j]
                if i == basic_variable:
                    params[self.variable_names[i]] = self.right_side[j]
                    found = True
                    break
            if not found:
                params[self.variable_names[i]] = 0
        return object, params


class ConstraintType(Enum):
    LessEqual = 1
    GreaterEqual = 2
    Equal = 3


class Constraint:
    def __init__(self, left, type, right_value):
        self.left = left
        self.type = type
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


Values = Union[int, str, Fraction, Decimal]

class QueueItem():
    def __init__(self):
        pass

    def __lt__(self, other):
        return self.optimize_limit > other.optimize_limit

    def __eq__(self,other):
        return self.optimize_limit == other.optimize_limit



class IntegerModel:
    def __init__(self, type: OptimizationType = OptimizationType.maximization, **kwargs):
        self.variable_names = set()  # 优化目标中包含的变量
        self.objective = {}  # 最终的优化目标
        self.type = type  # 优化类型 （最大化/最小化）
        self.constraints = []  # 约束式
        self.lower_bounds = {}
        self.upper_bounds = {}

        self.int_constarints = {}
        for v in kwargs:
            self.variable_names.add(v)
            self.int_constarints[v] = False
            self.objective[v]=Fraction(kwargs[v])
            self.lower_bounds[v]=0
            self.upper_bounds[v]=sys.maxsize

    def add_integer_constraint(self, var_name: str):
        """
        添加整数约束
        :param var_name: 必须为整数的变量名
        :return:
        """
        if var_name not in self.variable_names:
            raise RuntimeError(f"{var_name} is not in objective function!")
        self.int_constarints[var_name] = True

    def add_constraint(self, constraint: Values, type: ConstraintType, **kwargs):
        """
        添加约束

        :param constraint: 约束（不）等式右侧常数
        :param type: 约束类型（大于等于，小于等于，等于）
        :param kwargs: 不等式左侧各变量系数
        """

        if len(kwargs) == 1:
            var_name = list(kwargs.keys())[0]
            if type == ConstraintType.GreaterEqual:
                value = kwargs[var_name]
                old_bound = self.lower_bounds[var_name]
                new_bound = max(value, old_bound)
                if new_bound > self.upper_bounds[var_name]:
                    raise RuntimeError("lower bound greater than upper bound!")
                self.lower_bounds[var_name] = new_bound
            elif type == ConstraintType.LessEqual:
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
            right = constraint
            left = kwargs.copy()
            constraint = Constraint(left, type, right)
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
            if upper_bounds[var_name]< lower_bounds[var_name]:
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
        #
        # initial
        queue = []
        item = QueueItem()
        item.lower_bounds = self.lower_bounds
        item.upper_bounds = self.upper_bounds
        item.optimize_limit = sys.maxsize

        heapq.heappush(queue, item)

        max_optimize_value = -sys.maxsize
        max_var_values = None
        while len(queue) > 0:
            item = heapq.heappop(queue)
            if item.optimize_limit < max_optimize_value:
                break
            objective = self.objective.copy()
            constraints = self.constraints[:]
            lower_bounds = item.lower_bounds.copy()
            upper_bounds = item.upper_bounds.copy()
            no_solution, known_vars = self._calculate_known_vars(lower_bounds, upper_bounds)
            if no_solution:  # 无满足条件解（某整数变量的上下限之间不存在整数）
                continue

            basic_object_value = 0
            for var_name in known_vars:
                var_val = known_vars[var_name]
                if var_name in self.objective:
                    basic_object_value+=self.objective[var_name]* var_val
                    del objective[var_name]

            for constraint in constraints:
                left = constraint.left.copy()
                right = constraint.right
                for var_name in known_vars:
                    var_val = known_vars[var_name]
                    if var_name in left:
                        right-= left[var_name] * var_val
                        del left[var_name]
                constraint.left = left
                constraint.right = right

            model = LinearModel(type=self.type, enable_log=False, **objective)
            for constraint in self.constraints:
                params = constraint.left
                if constraint.type == ConstraintType.LessEqual:
                    model.add_less_constraint(constraint.right, **params)
                elif constraint.type == ConstraintType.GreaterEqual:
                    model.add_greater_constraint(constraint.right, **params)
                else:
                    model.add_equal_constraint(constraint.right, **params)

            for var_name in self.variable_names:
                lower = lower_bounds[var_name]
                upper = upper_bounds[var_name]
                params = {}
                params[var_name] = 1
                if lower>0:
                    model.add_greater_constraint(lower,**params)
                if upper < sys.maxsize:
                    model.add_less_constraint(upper,**params)


            object_value, var_values = model.solve()
            print("----------------------")
            if object_value is None:
                print("no solution")
                continue
            object_value += basic_object_value
            var_values.update(known_vars)
            print("object:", object_value)
            for var_name in var_values:
                print(f"{var_name} : {var_values[var_name]}")


            if object_value > max_optimize_value:
                integer_ok, non_int_var_name=self._integer_constraints_test(var_values)
                if integer_ok:
                    max_optimize_value=object_value
                    max_var_values = var_values
                    max_var_values.update(known_vars)
                else:
                    self._split(queue,item,object_value,non_int_var_name,var_values[non_int_var_name])
        if max_optimize_value is None:
            print("Don't find solution!")
        else:
            print("The result object:", max_optimize_value)
            for var_name in max_var_values:
                print(f"{var_name} : {max_var_values[var_name]}")

    def _split(self,queue,item,object_value,split_var_name,split_value):
        print(f"split {split_var_name}: {split_value}")
        old_lower = item.lower_bounds[split_var_name]
        old_upper = item.upper_bounds[split_var_name]
        new_item1 = QueueItem()
        new_item1.lower_bounds = item.lower_bounds.copy()
        new_item1.upper_bounds = item.upper_bounds.copy()
        new_item1.upper_bounds[split_var_name]=min(old_upper, int(math.floor(split_value)))
        new_item1.optimize_limit = object_value
        heapq.heappush(queue,new_item1)
        new_item2 = QueueItem()
        new_item2.lower_bounds = item.lower_bounds.copy()
        new_item2.upper_bounds = item.upper_bounds.copy()
        new_item2.lower_bounds[split_var_name]= max(old_lower, int(math.ceil(split_value)))
        new_item2.optimize_limit = object_value
        heapq.heappush(queue,new_item2)


model = IntegerModel(x1=4, x2=-2, x3=7, x4=-1)
model.add_less_constraint(10, x1=1, x3=5)
model.add_less_constraint(1, x1=1, x2=1, x3=-1)
model.add_less_constraint(0, x1=6, x2=-5)
model.add_less_constraint(3, x1=-1, x3=2, x4=-2)
model.add_integer_constraint('x1')
model.add_integer_constraint('x2')
model.add_integer_constraint('x3')
model.solve()
