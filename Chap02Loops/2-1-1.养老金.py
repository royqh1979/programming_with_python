rate = 0.025
deposit = 10000
balance = 10000
n=40
for i in range(1,n+1):
    interest = balance * rate
    balance = balance + interest + deposit
    print(f"第{i}年账户余额为{balance}")

print(f"{n}年后，账户余额为{balance}")