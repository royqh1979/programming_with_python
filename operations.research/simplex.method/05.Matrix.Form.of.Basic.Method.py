"""
基本的单纯形算法实现

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
变量的取值范围均为非负实数

运筹学导论（Introduction to Operations Research 第9版）第5章
"""
import numpy as np
from numpy.linalg import multi_dot


class Model:
    def __init__(self, **kwargs):
        """
        创建优化模型，并建立（最大化）优化目标函数

        :param kwargs: 目标函数中各变量的系数
        """
        self.variable_names = []  # 所有变量的名称，包括松弛变量
        self.original_variables = []  # 出现在目标函数中的变量
        self.slack_variables = []  # 松弛变量

        equation0_coefficients = []  # 目标函数中各变量的系数
        for v in kwargs:
            self.variable_names.append(v)
            self.original_variables.append(len(self.variable_names) - 1)
            equation0_coefficients.append(kwargs[v])

        self.objective = np.array(equation0_coefficients)  # 目标优化函数的系数向量
        self.constraints_left = []  # 约束的左侧
        self.constraints_right = []  # 约束的右侧

    def add_constraint(self, constaint_value, **kwargs) -> None:
        """
        添加约束（小于等于）

        :param constaint_value: 右侧的约束值，必须大于0
        :param kwargs: 左侧各变量的系数
        :return: 无
        """
        constraint_left = []
        for real_var in self.original_variables:
            real_var_name = self.variable_names[real_var]
            if real_var_name in kwargs:
                constraint_left.append(kwargs[real_var_name])
            else:
                constraint_left.append(0)
        self.constraints_left.append(constraint_left)
        self.constraints_right.append(constaint_value)
        self.variable_names.append('_s' + str(len(self.slack_variables) + 1))
        self.slack_variables.append(len(self.variable_names) - 1)

    def _display(self, iteration, Left, Right,basic_variables):
        print(f"{'Basic':<10} {'Z':<4} ", end="")
        for var_name in self.variable_names:
            print(f"{var_name:<10} ", end="")
        print("Right Side")
        print(f"{'Variables'}")
        for i in range(np.size(Left, 0)):
            if i == 0:
                print(f"{'':<10} {1:<4} ", end="")
            else:
                print(f"{self.variable_names[basic_variables[i-1]]:<10} {0:<4} ", end="")
            for j in range(np.size(Left, 1)):
                print(f"{Left[i, j]:<10f} ", end="")
            print(f"{Right[i][0]:<10f} ")

    def _prepare_iteration_0(self, c, A, I, b):
        zeros_1 = np.zeros((1, len(self.slack_variables)))

        Left = np.block([
            [-c, zeros_1],
            [A, I]
        ])
        Right = np.block(
            [
                [0],
                [b]
            ]
        )
        return Left, Right

    def _optimal_test(self, Left,  non_basic_variables):
        min_index = np.argmin(Left[0][non_basic_variables])
        min_value = Left[0][non_basic_variables[min_index]]
        if min_value >= 0:
            return None
        return min_index

    def _minimum_ratio_test(self,Left,Right,enter_basic):
        min_ratio = None
        min_index = -1
        for i in range(1, np.size(Left, 0)):
            enter_basic_coefficient = Left[i, enter_basic]
            if enter_basic_coefficient <= 0:
                continue
            else:
                ratio = Right[i, 0] / enter_basic_coefficient
                if min_ratio is None or ratio < min_ratio:
                    min_ratio = ratio
                    min_index = i
        if min_index == -1:
            print("can't find the minimum ratio!")
            print("no solution!")
            return -1, None

        return min_index -1, min_ratio

    def solve(self):
        c = np.array(self.objective).reshape((1, len(self.objective)))  # c是行向量
        c_base = np.block([
            c, np.zeros((1, len(self.slack_variables)))
        ])
        A = np.array(self.constraints_left)
        I = np.identity(len(self.slack_variables))
        b = np.array(self.constraints_right).reshape((len(self.constraints_right), 1))  # b是列向量
        AI = np.block([A, I])
        Left, Right = self._prepare_iteration_0(c, A, I, b)

        iteration = 0

        non_basic_variables = self.original_variables[:]
        basic_variables = self.slack_variables

        while True:
            iteration += 1
            print(f'iteration {iteration}:')
            print('---------------------------------')

            # Optimality Test
            enter_basic_index = self._optimal_test(Left, non_basic_variables)
            if enter_basic_index == None:
                print("The solution is optimal")
                break
            enter_basic = non_basic_variables[enter_basic_index]

            # Minimum Ratio Test
            leaving_basic_index,min_ratio = self._minimum_ratio_test(Left,Right,enter_basic)
            if leaving_basic_index == -1:
                self._display(iteration, Left, Right)
                print("can't find the minimum ratio!")
                print("no solution!")
                return None,None
            leaving_basic = basic_variables[leaving_basic_index]
            self._display(iteration, Left, Right,basic_variables)
            print("minimum ratio:", min_ratio)
            print("Entering basic :", self.variable_names[enter_basic])
            print("leaving basic:", self.variable_names[leaving_basic])

            basic_variables[leaving_basic_index] = enter_basic
            non_basic_variables[enter_basic_index] = leaving_basic

            B = AI[:, basic_variables]
            B_inv = np.linalg.inv(B)
            cB = c_base[:, basic_variables]

            Left = np.block([
                [multi_dot([cB, B_inv, A]) - c, multi_dot([cB, B_inv])],
                [multi_dot([B_inv, A]), B_inv]
            ])
            Right = np.block([
                [multi_dot([cB, B_inv, b])],
                [multi_dot([B_inv, b])]
            ])

        self._display(iteration,Left,Right,basic_variables)
        optimal_value, optimal_vars = self._cal_solution(B_inv,b,cB,basic_variables)
        self._display_solution(optimal_value,optimal_vars)
        return optimal_value,optimal_vars

    def _display_solution(self,optimal_value,optimal_vars):
        print("The optimal value: ",optimal_value)
        for var_name in optimal_vars:
            print(f"{var_name} :{optimal_vars[var_name]}")


    def _cal_solution(self,B_inv,b,cB,basic_variables):
        """
        计算最终结果

        :param B_inv:
        :param b:
        :param cB:
        :param basic_variables:
        :return:
        """
        optimal_var_values = np.matmul(B_inv,b)
        optimal_value = np.matmul(cB,optimal_var_values)[0][0]

        optimal_var_values=optimal_var_values.reshape((optimal_var_values.size))

        optimal_var_names = [self.variable_names[i] for i in basic_variables if i in self.original_variables]

        optimal_vars = dict(zip(optimal_var_names,optimal_var_values))
        for i in self.original_variables:
            if not i in basic_variables:
                optimal_vars[self.variable_names[i]]=0
        return optimal_value,optimal_vars


    #
    # def _display_solution(self):
    #     print("The optiomal solution:")
    #     for i in self.real_variables:
    #         found = False
    #         for j in range(1,len(self.basic_variables)):
    #             basic_variable = self.basic_variables[j]
    #             if i==basic_variable:
    #                 print(f'{self.variable_names[i]}: {show_fraction(self.right_side[j])}')
    #                 found = True
    #                 break
    #         if not found:
    #             print(f'{self.variable_names[i]}: 0')
    #     print("objective value: ",self.right_side[0])
    #     print("shadow price:")
    #     eq0 = self.left_side[0]
    #     for i in range(1, len(self.left_side)):
    #         slack_index = len(self.real_variables) - 1 + i
    #         print(f"shadow price for constaint {i}:",eq0[slack_index+1])


model = Model(x1=3, x2=5)
model.add_constraint(4, x1=1)
model.add_constraint(12, x2=2)
model.add_constraint(18, x1=3, x2=2)
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
