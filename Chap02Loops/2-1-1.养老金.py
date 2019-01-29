rate = 0.025
deposit = 10000
balance = 0
n=40
for i in range(n):
    interest = balance * rate
    balance = balance + interest + deposit
    balance = round(balance,2)
    print(f"第{n}年账户余额为{balance}")

print(f"{n}年后，账户余额为{balance}")