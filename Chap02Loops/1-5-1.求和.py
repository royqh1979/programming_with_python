def calc_total(n):
    total = 0
    for i in range(1,n+1):
        if i % 5 == 0:
            continue
        total += i
    return total


n=int(input("请输入n:"))
total = calc_total(n)
print(f"计算结果为{total}")