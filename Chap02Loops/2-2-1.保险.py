rate = 0.02
balance = 15350
for age in range(0,26):
    interest = balance * rate
    balance += interest
    deposit = 0
    if 0<=age<=8:
        deposit += 15350
    if 15<=age<=17:
        deposit -= 10000
    if 18<=age<=21:
        deposit -= 20000
    if age == 25:
        deposit -= 50000
    balance += deposit
    print(f"{age}岁时 存入{deposit}元 账户余额为{balance:.2f}")

print(f"{age}岁时，账户余额为{balance:.2f}")