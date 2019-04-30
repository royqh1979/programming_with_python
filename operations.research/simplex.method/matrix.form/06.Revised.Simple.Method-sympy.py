"""
基本的改进单纯形算法实现（The Revised Simplex Method)

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
变量的取值范围均为非负实数

运筹学导论（Introduction to Operations Research 第9版）第5.4章

需要sympy

结果为分数形式
"""
import sympy as sy


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
            equation0_coefficients.append(sy.Rational(kwargs[v]))

        self.objective = sy.Matrix([equation0_coefficients])  # 目标优化函数的系数向量
        self.constraints_left = []  # 约束的左侧
        self.constraints_right = []  # 约束的右侧
        self.non_basic_variables = [] # 非基变量集合
        self.basic_variables = []  # 基变量集合(下标为约束式序号-1） basic_variables[0]为约束式（1）对应的基变量，依此类推
        self.B_inv : sy.Matrix = None #
        self.t : sy.Matrix  = None # Row 0 of the initial tableau
        self.T : sy.Matrix  = None # Other rows of the initial tableau

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
                constraint_left.append(sy.Rational(kwargs[real_var_name]))
            else:
                constraint_left.append(0)
        self.constraints_left.append(constraint_left)
        self.constraints_right.append(sy.Rational(constaint_value))
        self.variable_names.append('_s' + str(len(self.slack_variables) + 1))
        self.slack_variables.append(len(self.variable_names) - 1)

    def _display(self, t_star,T_star):
        print(f"{'Basic':<10} {'Z':<4} ", end="")
        for var_name in self.variable_names:
            print(f"{var_name:<10} ", end="")
        print("Right Side")
        print(f"{'Variables'}")

        print(f"{'':<10} {1:<4}",end="")
        for i in range(t_star.shape[1]):
            print(f"{str(t_star[0,i]):<10} ",end="")
        print()
        for i in range(T_star.shape[0]):
            print(f"{self.variable_names[self.basic_variables[i]]:<10} {0:<4}", end="")
            for j in range(T_star.shape[1]):
                print(f"{str(T_star[i, j]):<10} ", end="")
            print()

    def _prepare_iteration_0(self, c:sy.Matrix, A:sy.Matrix, I:sy.Matrix, b:sy.Matrix)->(sy.Matrix,sy.Matrix):
        zeros_1 = sy.zeros(1, len(self.slack_variables)+1)
        t = sy.Matrix(sy.BlockMatrix([[-c, zeros_1]]))
        T = sy.Matrix(sy.BlockMatrix([[A, I, b]]))
        return t, T

    def _optimal_test(self, t_star,  non_basic_variables):
        """
        最优结果测试

        :param t_star: 单纯形表 第0行
        :param non_basic_variables: 非基变量列表
        :return: None 已经最优， 否则返回入基变量在单纯形表第0行中的位置
        """
        min_index = -1
        min_value = 0
        for i in range(len(non_basic_variables)):
            index = non_basic_variables[i]
            value = t_star[0, index]
            if value < min_value:
                min_value = value
                min_index = i
        if min_value >= 0:
            return None
        return min_index

    def _minimum_ratio_test(self,T_star,enter_basic):
        min_ratio = None
        min_index = -1
        for i in range(T_star.shape[0]):
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

    def solve(self):
        c = sy.Matrix([self.objective])  # c是行向量
        A = sy.Matrix(self.constraints_left)
        I = sy.eye(len(self.slack_variables))
        b = sy.Matrix(self.constraints_right) # b是列向量

        self.t, self.T = self._prepare_iteration_0(c, A, I, b)
        self.B_inv = I

        self.non_basic_variables = self.original_variables[:]
        self.basic_variables = self.slack_variables[:]

        m = len(self.slack_variables)
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

            E = sy.eye(len(self.slack_variables))
            r = leaving_basic_index
            a_rk = T_star[r,enter_basic]

            for i in range(m):
                if i == r :
                    E[i,r] = 1/a_rk
                else:
                    E[i,r] = -T_star[i,enter_basic] / a_rk

            self.B_inv = E * self.B_inv
            cB = -self.t[:, self.basic_variables]
            y_star = cB * self.B_inv
            t_star = self.t + y_star * self.T
            T_star = self.B_inv * self.T

        self._display(t_star,T_star)
        optimal_value, optimal_vars = self._cal_solution(t_star,T_star)
        self._display_solution(optimal_value,optimal_vars)
        return optimal_value,optimal_vars

    def _display_solution(self,optimal_value,optimal_vars):
        print("The optimal value: ",optimal_value)
        for var_name in optimal_vars:
            print(f"{var_name} :{optimal_vars[var_name]}")


    def _cal_solution(self,t_star,T_star):
        """
        计算最终结果

        :param B_inv:
        :param b:
        :param cB:
        :param basic_variables:
        :return:
        """

        optimal_var_values = T_star[:,-1]
        optimal_value = t_star[-1]

        optimal_var_values=optimal_var_values.T

        print(optimal_var_values)

        optimal_vars = {}
        for i in self.original_variables:
            if not i in self.basic_variables:
                optimal_vars[self.variable_names[i]]=0
            else:
                index = self.basic_variables.index(i)
                optimal_vars[self.variable_names[i]]=optimal_var_values[index]
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


# model = Model(x1=3, x2=5)
# model.add_constraint(4, x1=1)
# model.add_constraint(12, x2=2)
# model.add_constraint(18, x1=3, x2=2)
# model.solve()

model = Model(x1=4,x2=-2,x3=7,x4=-1)
model.add_constraint(10,x1=1,x3=5)
model.add_constraint(1, x1=1,x2=1,x3=-1)
model.add_constraint(0,x1=6,x2=-5)
model.add_constraint(3,x1=-1,x3=2,x4=-2)
model.solve()
