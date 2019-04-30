"""
两阶段法的改进单纯形算法实现（The Revised Simplex Method)

变量的取值范围均为非负实数

运筹学导论（Introduction to Operations Research 第9版）第4章和第5章

需要安装numpy和sympy库

结果为浮点数形式
"""
from typing import Dict, List
import sympy as sy

import math
import numpy as np
from enum import Enum

class OptimizationType(Enum):
    maximization = 1
    minimization = 2

class ConstraintType(Enum):
    LessEqual = 1
    GreaterEqual = 2
    Equal = 3

class Constraint:
    def __init__(self, left: Dict[str, float], constraint_type: ConstraintType, right_value: float):
        self.left = left
        self.type = constraint_type
        self.right = right_value

class Model:
    def __init__(self,opt_type: OptimizationType = OptimizationType.maximization, **kwargs):
        """
        创建优化模型，并建立（最大化）优化目标函数

        :param kwargs: 目标函数中各变量的系数
        """
        self.objective = {} # 优化目标

        self.type = opt_type
        if opt_type == OptimizationType.maximization:
            for v in kwargs:
                self.objective[v] = kwargs[v]
        else:
            for v in kwargs:
                self.objective[v] = -kwargs[v]

        self.constraints:List[Constraint] = [] # 约束列表
        self.less_than_constraints = 0 # 小于等于约束数量
        self.equal_constraints = 0 # 等于约束数量
        self.greater_than_constraints = 0 # 大于等于约束数量

        self.variable_names: List[str] = None
        self.running_variable_names: List[str] = None
        self.origin_variables: List[int] = None
        self.surplus_variables: List[int] = None
        self.slack_variables: List[int] = None
        self.artificial_variables: List[int] = None

        self.non_basic_variables: List[int] = None
        self.basic_variables: List[int] = None

        self.t: np.ndarray = None
        self.T: np.ndarray = None
        self.t_star: np.ndarray = None
        self.T_star: np.ndarray = None
        self.B_inv: np.ndarray = None


    def add_constraint(self, constraint: float, constraint_type: ConstraintType, **kwargs):
        """
        添加约束

        :param constraint: 约束（不）等式右侧常数
        :param constraint_type: 约束类型（大于等于，小于等于，等于）
        :param kwargs: 不等式左侧各变量系数
        """
        if constraint<0:
            right = -constraint
            left = {}
            for var_name in kwargs:
                if var_name not in self.objective:
                    raise RuntimeError(f'variables \'{var_name}\' not in objective function!')
                left[var_name] = -kwargs[var_name]
            if constraint_type == ConstraintType.LessEqual:
                constraint_type = ConstraintType.GreaterEqual
            elif constraint_type == ConstraintType.GreaterEqual:
                constraint_type = ConstraintType.LessEqual
        else:
            right = constraint
            left = {}
            for var_name in kwargs:
                if var_name not in self.objective:
                    raise RuntimeError(f'variables \'{var_name}\' not in objective function!')
                left[var_name] = kwargs[var_name]
        constraint = Constraint(left, constraint_type, right)
        if constraint_type==ConstraintType.LessEqual:
            self.less_than_constraints+=1
        elif constraint_type == ConstraintType.GreaterEqual:
            self.greater_than_constraints+=1
        else:
            self.equal_constraints+=1
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


    def _display(self, t_star,T_star):
        print(f"{'Basic':<10} {'Z':<4} ", end="")
        for var_name in self.running_variable_names:
            print(f"{var_name:<10} ", end="")
        print("Right Side")
        print(f"{'Variables'}")

        print(f"{'':<10} {1:<4}",end="")
        for i in range(np.size(t_star,1)):
            print(f"{t_star[0,i]:<10f} ",end="")
        print()
        for i in range(np.size(T_star,0)):
            print(f"{self.variable_names[self.basic_variables[i]]:<10} {0:<4}", end="")
            for j in range(np.size(T_star, 1)):
                print(f"{T_star[i, j]:<10f} ", end="")
            print()

    def _prepare_first_phase(self):
        var_names = []
        original_vars = []
        for var_name in self.objective:
            original_vars.append(len(var_names))
            var_names.append(var_name)


        basic_var_names = []
        surplus_var_names = []
        slack_vars = []
        artificial_vars = []
        surplus_vars = []
        A = []
        b = []
        for constraint in self.constraints:
            b.append(constraint.right)
            row = []
            for var_name in var_names:
                row.append(constraint.left.get(var_name,0))
            surplus_row = [0] * self.greater_than_constraints

            if constraint.type == ConstraintType.LessEqual:
                name = '_s'+str(len(slack_vars))
                slack_vars.append(len(basic_var_names))
                basic_var_names.append(name)
            elif constraint.type == ConstraintType.Equal:
                name = '_a'+str(len(artificial_vars))
                artificial_vars.append(len(basic_var_names))
                basic_var_names.append(name)
            else:
                name = '_a'+str(len(artificial_vars))
                artificial_vars.append(len(basic_var_names))
                basic_var_names.append(name)
                surplus_row[len(surplus_vars)] = -1
                name = '_ss' + str(len(surplus_vars))
                surplus_vars.append(len(surplus_var_names))
                surplus_var_names.append(name)

            A.append(row+surplus_row)

        surplus_vars = [ x+len(var_names) for x in surplus_vars ]
        var_names += surplus_var_names

        slack_vars = [ x+len(var_names) for x in slack_vars ]
        artificial_vars = [ x+len(var_names) for x in artificial_vars ]
        basic_vars = [ x+len(var_names) for x in range(len(slack_vars)+len(artificial_vars)) ]

        non_basic_vars = list(range(len(var_names)))
        var_names+=basic_var_names

        t = np.repeat(0,len(var_names)+1)
        t = t.reshape((1,t.size))# t是行向量
        A = np.array(A)
        I = np.identity(len(basic_vars))
        b = np.array(b).reshape((len(b), 1))  # b是列向量

        T = np.block([A, I, b])
        t[0,artificial_vars]=1
        # for i in artificial_vars:
        #     t[0,i]=1

        for i in artificial_vars:
            index = basic_vars.index(i)
            t = t - T[index, :]

        self.variable_names = var_names
        self.running_variable_names = var_names
        self.origin_variables = original_vars
        self.surplus_variables = surplus_vars
        self.slack_variables = slack_vars
        self.artificial_variables = artificial_vars

        self.non_basic_variables = non_basic_vars
        self.basic_variables = basic_vars

        self.t, self.T = t,T
        self.B_inv = I

    def _optimal_test(self, t_star,  non_basic_variables):
        """
        最优结果测试

        :param t_star: 单纯形表 第0行
        :param non_basic_variables: 非基变量列表
        :return: None 已经最优， 否则返回入基变量在单纯形表第0行中的位置
        """
        min_index = np.argmin(t_star[0,non_basic_variables])
        min_value = t_star[0,non_basic_variables[min_index]]
        if min_value >= 0:
            return None
        return min_index

    def _minimum_ratio_test(self,T_star,enter_basic):
        min_ratio = None
        min_index = -1
        for i in range(np.size(T_star, 0)):
            enter_basic_coefficient = T_star[i, enter_basic]
            if enter_basic_coefficient <= 0:
                continue
            else:
                ratio = T_star[i, -1] / enter_basic_coefficient
                if min_ratio is None or ratio < min_ratio:
                    min_ratio = ratio
                    min_index = i
        if min_index == -1:
            print("can't find the minimum ratio!")
            print("no solution!")
            return -1, None

        return min_index, min_ratio

    def _solve(self, type = OptimizationType.maximization):
        m = len(self.basic_variables)
        t_star = self.t
        T_star = self.T
        iteration = 0

        while True:
            iteration += 1
            print(f'iteration {iteration}:')
            print('---------------------------------')

            # Optimality Test
            enter_basic_index = self._optimal_test(t_star, self.non_basic_variables)
            if enter_basic_index == None:
                print("The solution is optimal")
                break
            enter_basic = self.non_basic_variables[enter_basic_index]

            # Minimum Ratio Test
            leaving_basic_index,min_ratio = self._minimum_ratio_test(T_star,enter_basic)
            if leaving_basic_index == -1:
                self._display( t_star, T_star)
                print("can't find the minimum ratio!")
                print("no solution!")
                return None,None
            leaving_basic = self.basic_variables[leaving_basic_index]

            self._display( t_star, T_star)
            print("minimum ratio:", min_ratio)
            print("Entering basic :", self.variable_names[enter_basic])
            print("leaving basic:", self.variable_names[leaving_basic])

            self.basic_variables[leaving_basic_index] = enter_basic
            self.non_basic_variables[enter_basic_index] = leaving_basic

            E = np.identity(m)
            r = leaving_basic_index
            a_rk = T_star[r,enter_basic]

            eta = - T_star[:,enter_basic].reshape(m) / np.repeat(a_rk,m)
            eta[r] = 1/a_rk
            E[:,r] = eta
            #
            # print(E)

            self.B_inv = E @ self.B_inv
            cB = -self.t[:, self.basic_variables]
            y_star = cB @ self.B_inv
            t_star = self.t + y_star @ self.T
            T_star = self.B_inv @ self.T

        self.t_star,self.T_star = t_star,T_star
        self._display(t_star,T_star)
        optimal_value, optimal_vars = self._cal_solution(t_star,T_star)
        if type == OptimizationType.minimization:
            optimal_value = - optimal_value
        self._display_solution(optimal_value,optimal_vars)
        return optimal_value,optimal_vars

    def _display_solution(self,optimal_value,optimal_vars):
        print("The optimal value: ",optimal_value)
        for var_name in optimal_vars:
            print(f"{var_name} :{optimal_vars[var_name]}")

    def _cal_solution(self,t_star,T_star):
        """
        计算阶段优化结果

        :param B_inv:
        :param b:
        :param cB:
        :param basic_variables:
        :return:
        """
        optimal_var_values = T_star[:,-1]
        optimal_value = t_star[0][-1]

        optimal_var_values=optimal_var_values.reshape((optimal_var_values.size))

        optimal_vars = {}
        for var_name in self.objective:
            i = self.variable_names.index(var_name)
            if not i in self.basic_variables:
                optimal_vars[self.variable_names[i]]=0
            else:
                index = self.basic_variables.index(i)
                optimal_vars[self.variable_names[i]]=optimal_var_values[index]
        return optimal_value,optimal_vars

    def _no_feasible_solution_test(self):
        for i in self.artificial_variables:
            if i in self.basic_variables:
                return True
        return False

    def _preare_second_phase(self):
        self.non_basic_variables = [ i for i in self.non_basic_variables if i not in self.artificial_variables]
        A = self.T_star[:,self.non_basic_variables]
        I = np.identity(len(self.basic_variables))

        b=self.T_star[:, -1]
        b=b.reshape((b.size,1))
        T=np.block([A, I, b])


        var_names = np.array(self.variable_names)
        non_basic_varnames = list(var_names[self.non_basic_variables])
        basic_varnames = list(var_names[self.basic_variables])
        new_varnames = non_basic_varnames + basic_varnames
        t=np.zeros(len(new_varnames)+1)
        t = t.reshape((1,t.size))
        for var_name in self.objective:
            index = new_varnames.index(var_name)
            t[0,index] = - self.objective[var_name]

        for var_name in self.objective:
            index = basic_varnames.index(var_name)
            t = t + self.objective[var_name] * T[index, :]

        # print(t)
        # print(T)
        # print(self.variable_names)
        # print(self.basic_variables)
        # print(self.non_basic_variables)
        self.t = t
        self.T = T
        self.running_variable_names = new_varnames

    def solve(self):
        if self.greater_than_constraints>0 or self.equal_constraints>0:
            print("======First Phase=======:")
            self._prepare_first_phase()
            optimal_value, optimal_vars = self._solve()

            if optimal_value == None:
                print("No feasible solution!")
                return None, None

            if self._no_feasible_solution_test():
                print("~~~~~~~~~~~~~~~~~~~~~~")
                print("Some artificial variable is none zero!")
                print("No feasible solution!")
                return None, None

            print("======Second Phase=======:")
            self._preare_second_phase()
            optimal_value, optimal_vars = self._solve(self.type)

            if optimal_value == None:
                print("No feasible solution!")
                return None, None
            return optimal_value,optimal_vars
        else:
            pass


# model = Model(x1=3, x2=5)
# model.add_constraint(4, x1=1)
# model.add_constraint(12, x2=2)
# model.add_constraint(18, x1=3, x2=2)
# model.solve()

model = Model(opt_type=OptimizationType.minimization, x1=0.4,x2=0.5)
model.add_less_constraint(2.7,x1=0.3,x2=0.1)
model.add_equal_constraint(6,x1=0.5,x2=0.5)
model.add_greater_constraint(6,x1=0.6,x2=0.4)
model.solve()