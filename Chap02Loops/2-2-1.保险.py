rate = 0.02
balance = 15350
for age in range(1,26):
    interest = balance * rate
    if 0<=age<=8:
        deposit = 15350
    elif 15<=age<=17:
        deposit = -10000
    elif 18<=age<=21:
        deposit = -20000
    elif age == 25:
        deposit = -50000
    else:
        deposit=0
    balance += deposit + interest
    balance = round(balance,2)
    print(f"{age}岁时 存款{deposit} 账户余额为{balance}")

print(f"{age}岁时，账户余额为{balance}")