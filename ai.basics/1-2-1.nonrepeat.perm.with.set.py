"""
n个数字的无重复排列

使用标志列表判重
"""
n=4
count = 0
used=set()
for i1 in range(1, n + 1):
    used.add(i1)
    for i2 in range(1, n + 1):
        if i2 in used:
            continue
        used.add(i2)
        for i3 in range(1, n + 1):
            if i3 in used:
                continue
            used.add(i3)
            for i4 in range(1, n + 1):
                if i4 in used:
                    continue
                used.add(i4)
                count+=1
                print(f"{i1},{i2},{i3},{i4}")
                used.remove(i4)
            used.remove(i3)
        used.remove(i2)
    used.remove(i1)


print(f"共{count}种方案")