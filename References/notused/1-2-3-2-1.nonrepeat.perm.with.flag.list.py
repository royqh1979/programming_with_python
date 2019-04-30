"""
n个数字的无重复排列

使用标志列表判重

使用函数
"""
n=4
count = 0
flags= [0] * (n + 1)
a = [0] * (n+1)

def perm4():
    global count
    i = 4
    for a[i] in range(1, n + 1):
        if flags[a[i]] == 1:
            continue
        flags[a[i]] = 1
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            #perm5()
            pass
        flags[a[i]] = 0


def perm3():
    global count
    i = 3
    for a[i] in range(1, n + 1):
        if flags[a[i]] == 1:
            continue
        flags[a[i]] = 1
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm4()
        flags[a[i]] = 0


def perm2():
    global count
    i = 2
    for a[i] in range(1, n + 1):
        if flags[a[i]] == 1:
            continue
        flags[a[i]] = 1
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm3()
        flags[a[i]] = 0


def perm1():
    global count
    i = 1
    for a[i] in range(1, n + 1):
        if flags[a[i]] == 1:
            continue
        flags[a[i]] = 1
        if i == 4:
            count += 1
            print(a[1:n + 1])
        else:
            perm2()
        flags[a[i]] = 0


perm1()


print(f"共{count}种方案")