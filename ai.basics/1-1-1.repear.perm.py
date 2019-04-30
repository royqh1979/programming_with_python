m=int(input("请输入m："))
count = 0
for i1 in range(1, m + 1):
    for i2 in range(1, m + 1):
        for i3 in range(1, m + 1):
            for i4 in range(1, m + 1):
                count+=1
                print(f"{i1},{i2},{i3},{i4}")

print(f"共{count}种方案")