#计算1+1/2+1/3+1/4+1/5+...+1/n的和

#从fracation模块中导入Fraction（分数）类
from fractions import Fraction

n=int(input("请输入n:"))
i=1
total=0
while i<=n:
    total=total+Fraction(1,i)
    i+=1
print(f"结果是{total}")
