import fractions

n=int(input("请输入n:"))
i=1
total=0
while i<=n:
    total=total+fractions.Fraction(1,i)
    i+=1
print(f"结果是{total}")
