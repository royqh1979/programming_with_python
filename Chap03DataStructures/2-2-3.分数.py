from fractions import Fraction

f1=Fraction(1,2)
f2=f1
print(f1,f2)
print(f1 is f2)
print(f1.numerator ,f1.denominator)
f1.numerator = 3
f3=Fraction(1,3)
f1+=f3
print(f1,f2)
print(f1 is f2)