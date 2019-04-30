"""
n个数字的无重复排列

使用标志列表
"""
n=4
count = 0
flags=set()
for i1 in range(1, n + 1):
    flags.add(i1)
    for i2 in range(1, n + 1):
        if i2 in flags:
            continue
        flags.add(i2)
        for i3 in range(1, n + 1):
            if i3 in flags:
                continue
            flags.add(i3)
            for i4 in range(1, n + 1):
                if i4 in flags:
                    continue
                flags.add(i4)
                count+=1
                print(f"{i1},{i2},{i3},{i4}")
                flags.remove(i4)
            flags.remove(i3)
        flags.remove(i2)
    flags.remove(i1)


print(f"共{count}种方案")