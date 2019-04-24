"""
大M法（带人工变量的单纯形法）

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
或者 变量的线性组合 = 常数 形式
或者 变量的线性组合 >= 常数 形式

"""
from fractions import Fraction
from enum import Enum


class OptimizationType(Enum):
    maximization = 1
    minimization = 2


class Model:
    def __init__(self, type=OptimizationType.maximization, enable_log = True, **kwargs):
        self.variable_names = []  # 所有变量的变量名，包括松弛变量
        self.real_variables = []  # 优化目标中包含的变量
        self.left_side = []  # 存储扩展后方程组左侧的系数
        self.right_side = []  # 存储扩展后方程组右侧的常数
        self.ratio = []  # 存储各方程组的离速
        self.basic_variables = []  # 基变量列表
        self.slack_variables = []  # 松弛变量列表
        self.artificial_variables = []  # 人工变量列表
        self.surplus_variables = []  # 剩余变量
        self.objective=[] # 最终的优化目标
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
        if constraint<0:
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
        if constraint<0:
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
        if constraint<0:
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
        eq0=[0]*len(self.variable_names)
        for i in self.artificial_variables:
            eq0[i]=1
        eq0=[-1]+eq0
        self.right_side[0]=0
        for i in self.artificial_variables:
            artificial_index = self.basic_variables.index(i)
            basic_eq = self.left_side[artificial_index]
            for j in range(len(basic_eq)):
                eq0[j]-=basic_eq[j]
            self.right_side[0]-=self.right_side[artificial_index]
        self.left_side[0]=eq0

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
                raise RuntimeError("can't find the minimum ratio!")
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

    def _prepare_second_pass(self):
        # drop artificial variables
        for i in range(len(self.left_side)):
            old_eq = self.left_side[i]
            new_eq = []
            for j in range(len(old_eq)):
                if (j-1) not in self.artificial_variables:
                    new_eq.append(old_eq[j])
            self.left_side[i] = new_eq
        for i in range(len(self.objective)):
            self.left_side[0][i]=self.objective[i]

        # Restore proper form for gause elimination
        # eliminate basic variables from equation 0
        eq0= self.left_side[0]
        for i in range(1,len(self.basic_variables)):
            basic_variable = self.basic_variables[i]
            if eq0[basic_variable+1] == 0 :
                continue
            basic_eq = self.left_side[i]
            coefficient = eq0[basic_variable+1]
            for j in range(len(basic_eq)):
                eq0[j] -= coefficient*basic_eq[j]
            self.right_side[0] -= coefficient*self.right_side[i]


    def _prepare(self):
        self.left_side[0] = self.objective[:]+[0]*len(self.slack_variables)

    def _no_feasible_solution_test(self):
        for i in self.artificial_variables:
            if i in self.basic_variables:
                return True
        return False

    def solve(self):
        if len(self.artificial_variables)>0:
            if self.enable_log:
                print("======First Phase=======:")
            self._prepare_first_phase()
            self._solve()  # solve first phase
            if self._no_feasible_solution_test():
                if self.enable_log:
                    print("~~~~~~~~~~~~~~~~~~~~~~")
                    print("Some artificial variable is none zero!")
                    print("No feasible solution!")
                return None
            if self.enable_log:
                print("======Second Phase=======:")
            self._prepare_second_pass()
            self._solve() # solve the second phase
        else:
            self._prepare()
            self._solve()
        if self.enable_log:
            self._display_solution()
        return self.get_result()

    def _display_solution(self):
        print("The optiomal solution:")
        object,params = self.get_result()
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
                params[self.variable_names[i]]=0
        return object,params


model = Model(type=OptimizationType.minimization, x1='0.4', x2='0.5')
model.add_less_constraint('2.7', x1='0.3', x2='0.1')
model.add_equal_constraint(6, x1='0.5', x2='0.5')
model.add_greater_constraint(6, x1='0.6', x2='0.4')
model.solve()

# model = Model(x1=3,x2=5)
# model.add_less_constraint(4,x1=1)
# model.add_less_constraint(12,x2=2)
# model.add_less_constraint(18,x1=3,x2=2)
# model.solve()

# No feasible solution
# model = Model(type=OptimizationType.minimization, x1=Fraction(4, 10), x2=Fraction(5, 10))
# model.add_less_constraint(Fraction(18, 10), x1=Fraction(3, 10), x2=Fraction(1, 10))
# model.add_equal_constraint(6, x1=Fraction(5, 10), x2=Fraction(5, 10))
# model.add_greater_constraint(6, x1=Fraction(6, 10), x2=Fraction(4, 10))
# model.solve()