"""
n个数字的无重复排列

使用标志列表

用列表存储方案
"""
n=4
count = 0
flags=set()
a = [0]*(n+1)
for a[1] in range(1, n + 1):
    flags.add(a[1])
    for a[2] in range(1, n + 1):
        if a[2] in flags:
            continue
        flags.add(a[2])
        for a[3] in range(1, n + 1):
            if a[3] in flags:
                continue
            flags.add(a[3])
            for a[4] in range(1, n + 1):
                if a[4] in flags:
                    continue
                flags.add(a[4])
                count+=1
                print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
                flags.remove(a[4])
            flags.remove(a[3])
        flags.remove(a[2])
    flags.remove(a[1])


print(f"共{count}种方案")