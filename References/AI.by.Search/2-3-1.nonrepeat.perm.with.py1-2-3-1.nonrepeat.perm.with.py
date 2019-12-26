"""
n个数字的无重复排列

使用集合判重

用列表存储方案
"""
n=4
count = 0
used=set()
a = [0]*(n+1)


def perm4():
    global count
    for a[4] in range(1, n + 1):
        if a[4] in used:
            continue
        used.add(a[4])
        count += 1
        print(f"{a[1]},{a[2]},{a[3]},{a[4]}")
        used.remove(a[4])


def perm3():
    for a[3] in range(1, n + 1):
        if a[3] in used:
            continue
        used.add(a[3])
        perm4()
        used.remove(a[3])


def perm2():
    for a[2] in range(1, n + 1):
        if a[2] in used:
            continue
        used.add(a[2])
        perm3()
        used.remove(a[2])

def perm1():
    for a[1] in range(1, n + 1):
        used.add(a[1])
        perm2()
        used.remove(a[1])

perm1()

print(f"共{count}种方案")