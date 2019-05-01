"""
n个数字的可重复排列

已知n等于4
"""
n=4
count = 0
for i1 in range(1, n + 1):
    for i2 in range(1, n + 1):
        for i3 in range(1, n + 1):
            for i4 in range(1, n + 1):
                count+=1
                print(f"{i1},{i2},{i3},{i4}")

print(f"共{count}种方案")