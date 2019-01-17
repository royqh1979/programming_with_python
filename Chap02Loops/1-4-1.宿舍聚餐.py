count = 0
total = 0
for i in range(1, 7):
    amount = int(input(f"请输入第{i}位同学的饭费："))
    total += amount
    count += 1
    if total >= 300:
        break

average = round(total / count,2)
print(f"共{i}位同学掏钱了，一共{total}元，人均{average}元")
