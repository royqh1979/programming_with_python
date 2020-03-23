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
    i = 4
    for a[i] in range(1, n + 1):
        if a[i] in used:
            continue
        used.add(a[i])
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            # perm5()
            pass
        used.remove(a[i])


def perm3():
    global count
    i = 3
    for a[i] in range(1, n + 1):
        if a[i] in used:
            continue
        used.add(a[i])
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm4()
        used.remove(a[i])


def perm2():
    global count
    i = 2
    for a[i] in range(1, n + 1):
        if a[i] in used:
            continue
        used.add(a[i])
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm3()
        used.remove(a[i])

def perm1():
    global count
    i = 1
    for a[i] in range(1, n + 1):
        if a[i] in used:
            continue
        used.add(a[i])
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm2()
        used.remove(a[i])

perm1()

print(f"共{count}种方案")