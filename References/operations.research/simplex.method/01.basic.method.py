"""
基本的单纯形算法实现

要优化的目标为 最大化目标函数值
约束条件均为 变量的线性组合<=常数 形式
变量的取值范围均为非负实数


"""
from fractions import Fraction


def show_fraction(f:Fraction):
    if f is None:
        return ' '
    if f.denominator == 1:
        return f.numerator
    else:
        return f'{f.numerator}/{f.denominator}'

class Model:
    def __init__(self, **kwargs):
        self.variables = [] # 所有变量，包括松弛变量
        self.objective = [] # 优化目标中包含的变量
        self.coefficients = [] # 存储扩展后方程组左侧的系数
        self.right_side = [] # 存储扩展后方程组右侧的常数
        self.ratio = [] # 存储各方程组的离速
        self.basic_variables = [] # 基变量列表

        eq0 = [Fraction(1)]
        for v in kwargs:
            self.variables.append(v)
            self.objective.append(len(self.variables)-1)
            eq0.append(Fraction(-kwargs[v]))

        self.coefficients.append(eq0)
        self.right_side.append(Fraction(0))
        self.ratio.append('')
        self.basic_variables.append(None)



    def add_constraint(self,constaint,**kwargs):
        for eq in self.coefficients:
            eq.append(Fraction(0))
        eq=[Fraction(0)]
        for var in self.variables:
            if var in kwargs:
                eq.append(Fraction(kwargs[var]))
            else:
                eq.append(Fraction(0))
        eq.append(Fraction(1))
        self.coefficients.append(eq)
        self.right_side.append(constaint)
        self.ratio.append('')
        self.variables.append('_s'+str(len(self.coefficients)-1))
        self.basic_variables.append(len(self.variables)-1)

    def display(self):
        print(f'BV.\t\tEq.\t\tZ',end='')
        for var in self.variables:
            print(f'\t\t{var}',end='')
        print('\t\tRight\t\tRatio')

        for i in range(len(self.basic_variables)):
            if i==0:
                print(f"obj\t\t({i})",end='')
            else:
                print(f'{self.variables[self.basic_variables[i]]}\t\t({i})',end='')
            eq=self.coefficients[i]
            for c in eq:
                print(f'\t\t{show_fraction(c)}',end='')
            print(f'\t\t{show_fraction(self.right_side[i])}',end='')
            print(f'\t\t{self.ratio[i]}')

    def done(self):
        self.display()
        iteration = 0
        while True:
            iteration += 1
            print(f'iteration {iteration}:')
            print('---------------------------------')
            print("Optimality Test:")
            # find the variable with the minimum negative coeffecient
            eq0 = self.coefficients[0]
            min_v = 0
            min_i = -1
            for i in range(len(eq0)):
                if eq0[i] < min_v:
                    min_v = eq0[i]
                    min_i = i
            if min_v == 0:
                print("The solution is optimal")
                break
            enter_basic = min_i
            print("Entering basic :",self.variables[enter_basic-1])

            print("Minumum Ratio Test:")
            min_ratio = None
            min_i = -1
            for i in range(1,len(self.coefficients)):
                eq = self.coefficients[i]
                if eq[enter_basic] == 0:
                    self.ratio[i] = ''
                else:
                    denominator = eq[enter_basic]
                    if denominator == 0:
                        self.ratio[i] == ''
                    else:
                        self.ratio[i] = self.right_side[i]/denominator
                        if self.ratio[i]<=0:
                            continue
                        if min_ratio is None or self.ratio[i] < min_ratio:
                            min_ratio = self.ratio[i]
                            min_i = i
            if min_i == -1:
                raise RuntimeError("can't find the minimum ratio!")
            leaving_basic = self.basic_variables[min_i]
            print("leaving basic:",self.variables[leaving_basic])

            #Gaussian Elimination
            leaving_basic_eq = self.coefficients[min_i]
            denominator = leaving_basic_eq[enter_basic]
            for i in range(len(leaving_basic_eq)):
                leaving_basic_eq[i] /= denominator
            self.right_side[min_i] /= denominator
            self.basic_variables[min_i]=enter_basic-1
            for i in range(len(self.coefficients)):
                if i==min_i:
                    continue
                eq=self.coefficients[i]
                multiple = eq[enter_basic]
                for j in range(len(eq)):
                    eq[j] -= multiple * leaving_basic_eq[j]
                self.right_side[i] -= multiple * self.right_side[min_i]
            self.display()
        self.display_solution()

    def display_solution(self):
        print("The optiomal solution:")
        for i in self.objective:
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
        eq0 = self.coefficients[0]
        for i in range(1,len(self.coefficients)):
            slack_index = len(self.objective)-1+i
            print(f"shadow price for constaint {i}:",eq0[slack_index+1])



model = Model(x1=3,x2=5)
model.add_constraint(4,x1=1)
model.add_constraint(12,x2=2)
model.add_constraint(18,x1=3,x2=2)
model.done()

# model = Model(x1=3,x2=2)
# model.add_constraint(4,x1=1)
# model.add_constraint(12,x2=2)
# model.add_constraint(18,x1=3,x2=2)
# model.done()

# model = Model(x1=40,x2=30)
# model.add_constraint(120,x1=4,x2=3)
# model.add_constraint(50,x1=2,x2=1)
# model.done()
