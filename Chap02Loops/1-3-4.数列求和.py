from fractions import Fraction

def calc(n):
    total = 0
    for i in range(1, n + 1):
        item = Fraction((-1) ** (i - 1), i)
        total = total + item
    return total

n=int(input("请输入n:"))
print(f"结果是{calc(n)}")
