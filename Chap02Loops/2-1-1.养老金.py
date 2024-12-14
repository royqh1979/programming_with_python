rate = 0.025
deposit = 10000
balance = 0
n=40
for i in range(n):
    interest = balance * rate
    balance = balance + interest + deposit
    print(f"第{i}年账户余额为{balance:.2f}")
    #{balance:.2f}中的f表示这是个浮点数，.2表示保留小数点后两位

#n年后
interest = balance * rate
balance = balance + interest

print(f"{n}年后，账户余额为{balance:.2f}")