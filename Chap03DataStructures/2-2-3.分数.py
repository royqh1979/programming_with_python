# 不可变对象演示
from fractions import Fraction

# 使用Fraction类来定义对象
# 注意程序开头的import语句
f1=Fraction(1,2)
f2=f1
print(f1,f2)
print(f1 is f2)
print(f1.numerator ,f1.denominator)
#运行到这里会出错，因为用Fraction类创建的对象是不可变对象
f1.numerator = 3
f3=Fraction(1,3)
f1+=f3
print(f1,f2)
print(f1 is f2)